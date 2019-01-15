# run this in the emulator to plot data from the emulated grovepi
# or run it standalone to get data from a remote grovepi

import wx
import collections
import threading
import sys


class DrawPanel(wx.Frame):
    
    def __init__(self):
        wx.Frame.__init__(self, None,title="Sensor Graphs",size=(600,540+270))
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.bufferSnd=collections.deque(maxlen=500)
        self.bufferLight=collections.deque(maxlen=500)
        self.bufferTemperature=collections.deque(maxlen=500)
        self.xPos=0
        self.addPoint(0,0,0)
        self.timer=wx.Timer(self,1)
        self.timer.Start(10)

    def addPoint(self,snd,light,temperature):
        self.bufferSnd.append((self.xPos,256-int(snd/4)))
        self.bufferLight.append((self.xPos,256-int(light/4)))
        self.bufferTemperature.append((self.xPos,256-int(temperature/4)))
        self.lastSnd=snd
        self.lastLight=light
        self.lastTemp=temperature
        self.xPos+=1
        curWidth=self.GetClientSizeTuple()[0]
        if self.bufferSnd.maxlen!=curWidth:
            self.bufferSnd=collections.deque(self.bufferSnd,maxlen=curWidth)
            self.bufferLight=collections.deque(self.bufferLight,maxlen=curWidth)
            self.bufferTemperature=collections.deque(self.bufferTemperature,maxlen=curWidth)
        self.Refresh(False)
        
    def OnTimer(self, event=None):
        if REMOTE_ADDRESS==None:
            # reading from an emulated grovepi
            snd=grovepi.analogRead(0)
            temperature=grovepi.analogRead(1)
            light=grovepi.analogRead(2)
            self.addPoint(snd,light,temperature)
        else:
            # running standalone, read from http server
            resp=urllib.request.urlopen(REMOTE_ADDRESS,timeout=1)
            header=resp.readline().rstrip("\n").split(",")
            srcvals=resp.readline().rstrip("\n").split(",")
            values={}
            for key,val in zip(header,srcvals):
                try:
                    values[key]=int(val)
                except ValueError:
                    values[key]=float(val)
            self.addPoint(values["sound"],values["light"],values["temperature"])
            
    def OnPaint(self, event=None):
        dc = wx.PaintDC(self)
        dc.Clear()        
        dc.SetPen(wx.Pen(wx.BLACK, 1))
        dc.DrawLines(self.bufferSnd,xoffset=-self.bufferSnd[0][0],yoffset=0)
        dc.DrawLines(self.bufferLight,xoffset=-self.bufferLight[0][0],yoffset=270)
        dc.DrawLines(self.bufferTemperature,xoffset=-self.bufferLight[0][0],yoffset=540)
        dc.DrawText("Sound:%d"%self.lastSnd,0,0)
        dc.DrawText("Light:%d"%self.lastLight,0,270)
        dc.DrawText("Temperature:%d"%self.lastTemp,0,540)

def initPanel():        
    frame = DrawPanel()
    frame.Show()
        
if threading.current_thread().name == 'MainThread':      
    # we're not in the emulator
    import urllib.request, urllib.error, urllib.parse
    if len(sys.argv)>1:
        REMOTE_ADDRESS=sys.argv[1]
    else:
        REMOTE_ADDRESS = "http://www.cs.nott.ac.uk/~pszjm2/sensordata/?id=1"

    app = wx.App(False)
    initPanel()
    app.MainLoop()
else:
    # we're in the emulator
    REMOTE_ADDRESS=None
    import grovepi
    wx.CallAfter(initPanel)