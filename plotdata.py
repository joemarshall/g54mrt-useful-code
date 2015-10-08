# run this in the emulator to plot data from the emulated  grovepi
# or run it standalone to get data from a remote grovepi

import wx
import collections
import threading


class DrawPanel(wx.Frame):
    
    def __init__(self,width=600,height=512):
        wx.Frame.__init__(self, None,title="Draw on Panel")
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.bufferSnd=collections.deque(maxlen=500)
        self.bufferLight=collections.deque(maxlen=500)
        self.xPos=0
        self.addPoint(0,0)
        self.timer=wx.Timer(self,1)
        self.timer.Start(10)

    def addPoint(self,snd,light):
        self.bufferSnd.append((self.xPos,int(snd/4)))
        self.bufferLight.append((self.xPos,int(light/4)))
        self.xPos+=1
        curWidth=self.GetClientSizeTuple()[0]
        if self.bufferSnd.maxlen!=curWidth:
            self.bufferSnd=collections.deque(self.bufferSnd,maxlen=curWidth)
            self.bufferLight=collections.deque(self.bufferLight,maxlen=curWidth)
        self.Refresh(False)
        
    def OnTimer(self, event=None):
        if REMOTE_ADDRESS==None:
            # reading from a (emulated) grovepi
            snd=grovepi.analogRead(0)
            light=grovepi.analogRead(1)
            self.addPoint(snd,light)
        else:
            # running standalone, read from http server
            resp=urllib2.urlopen(REMOTE_ADDRESS,timeout=1)
            header=resp.readline().split(",")
            srcvals=resp.readline().split(",")
            values={}
            for key,val in zip(header,srcvals):
                try:
                    values[key]=int(val)
                except ValueError:
                    values[key]=float(val)
            self.addPoint(values["sound"],values["light"])
            
    def OnPaint(self, event=None):
        dc = wx.PaintDC(self)
        dc.Clear()        
        dc.SetPen(wx.Pen(wx.BLACK, 1))
        dc.DrawLines(self.bufferSnd,xoffset=-self.bufferSnd[0][0],yoffset=0)
        dc.DrawLines(self.bufferLight,xoffset=-self.bufferLight[0][0],yoffset=270)
        dc.DrawText("Sound",0,0)
        dc.DrawText("Light",0,270)

def initPanel():        
    frame = DrawPanel()
    frame.Show()
        
if threading.current_thread().name == 'MainThread':      
    import urllib2
    REMOTE_ADDRESS = "http://www.cs.nott.ac.uk/~pszjm2/sensordata/?id=1"

    app = wx.App(False)
    initPanel()
    app.MainLoop()
else:
    REMOTE_ADDRESS=None
    import grovepi
    wx.CallAfter(initPanel)