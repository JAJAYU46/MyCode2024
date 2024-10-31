#!/usr/bin/env python3

# import RPi.GPIO as GPIO
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

host_name = '10.120.161.20'  # IP Address of Raspberry Pi
host_port = 8000


# def setupGPIO():
#     GPIO.setmode(GPIO.BCM)
#     GPIO.setwarnings(False)

#     GPIO.setup(18, GPIO.OUT)


# def getTemperature():
#     temp = os.popen("/opt/vc/bin/vcgencmd measure_temp").read()
#     return temp


class MyServer(BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _redirect(self, path):
        self.send_response(303)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', path)
        self.end_headers()

    def do_GET(self):
        html = '''
           <html>
           <head>
            <link rel="stylesheet" href="styles.css">
            <title>Vacuum Control WebApp </title>        
           </head>
           <body 
            style="width:960px; margin: 20px auto;">
           <h1>Welcome to my Raspberry Pi</h1>
           <p>Current GPU temperature is {}</p>
           <form action="/" method="POST">
               Turn LED :
               <input type="submit" name="submit" value="On">
               <input type="submit" name="submit" value="Off">
           </form>
           </body>
           </html>
        '''
        temp = "50.0"#getTemperature()
        self.do_HEAD()
        # self.wfile.write(html.format(temp[5:]).encode("utf-8"))
        self.wfile.write(html.format(temp).encode("utf-8"))
    def do_POST(self):

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode("utf-8")
        post_data = post_data.split("=")[1]

        # setupGPIO()

        if post_data == 'On':
            # GPIO.output(18, GPIO.HIGH)
            print("Botton On is clicked")
        else:
            # GPIO.output(18, GPIO.LOW)
            print("Botton Off is clicked")

        print("LED is {}".format(post_data))
        self._redirect('/')  # Redirect back to the root url


# # # # # Main # # # # #

if __name__ == '__main__':
    http_server = HTTPServer((host_name, host_port), MyServer)
    print("Server Starts - %s:%s" % (host_name, host_port))

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()
