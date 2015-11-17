# if you run this on a PI, it will output analogread 0 and analogread 1 in a webserver that can be accessed by the emulator at http://pi-ip-address:23456/ 
# can use this to put PI data straight into code running in an emulator, or to make your own sensor box just like the sensor boxes that we have in A32

import BaseHTTPServer
import time
import grovepi

PORT = 23456

class GetSensorHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Update-Rate","25")
        self.end_headers()
        self.wfile.write("timestamp,sound,light,temperature\n%d,%d,%d,%d\n"%(time.time(),grovepi.analogRead(0),grovepi.analogRead(2),grovepi.analogRead(1)))
        
    def log_request(self,code=None,size=None):
        None

Handler = GetSensorHandler

httpd = BaseHTTPServer.HTTPServer(("", PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()
