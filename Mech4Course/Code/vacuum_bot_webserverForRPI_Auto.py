
#!/usr/bin/env python3
#建立一個web server去接收按鈕的東東
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

# RPI 1. for RPI to Arduino communication
import serial
import time
import RPi.GPIO as GPIO

#host(server) 就是你的這台電腦，Define server address(讓之後client(browser可以知道server的IP位置))
host_name = '192.168.100.11'  # IP Address of Raspberry Pi (就是你電腦的IP) 要選Wi-Fi的IPv4 !!
host_name = '10.20.28.237'
host_port = 8000 #自己給的Port

#當在web browser打http://10.120.161.20:8000，會送一個request 給IP=10.120.161.20 on port 8000 的那個位置，而那位置就是server，server 會接收到client browser來的request
class MyServer(BaseHTTPRequestHandler):

    def do_HEAD(self): #Handle client 傳來的"HEAD request". server 回傳sends the HTTP headers 給client，告訴client 我這個server存在的，健在
        self.send_response(200) #HTTP 200 (OK) status 表示request was successful
        self.send_header('Content-type', 'text/html') #告訴client我現在是用HTML的格式response
        self.end_headers() #close header, 說之後的data，就是body of the response 了 (就是那個HTML網頁)

    def _redirect(self, path): #自動重新刷新更新畫面用
        self.send_response(303)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', path)
        self.end_headers()

    def do_GET(self): #(輸入網址，執行的就是這個函式)Handle client 傳來的"GET request" 當有人visit 這個browser(輸入網址)，serber會用這個回應(就會給HTTP的資料)
        # 那個HTML網頁格式(把網頁的長相傳給client)
        # html = '''
        #    <html>
        #    <body 
        #     style="width:960px; margin: 20px auto;">
        #    <h1>Welcome to my Raspberry Pi</h1>
        #    <p>Current GPU temperature is {}</p>
        #    <p>Current GPU temperature is {}</p>
        #    <form action="/" method="POST"> 
        #         Turn LED : 
        #         <input type="submit" name="submit" value="On"> 
        #         <input type="submit" name="submit" value="Off">

               
        #    </form>
        #    </body>
        #    </html>
        # '''
        if self.path == '/':
            html = '''
            <html>
            <head>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <link rel="stylesheet" href="styles.css">
                <title>Vacuum Control WebApp </title>        
            </head>
            <body 
                style="width:960px; margin: 20px auto;">
            <h1>Welcome to the Vacuum Controlling web browser !</h1>
            <p>Current GPU temperature is {}</p>
            
            <form id="movementForm" action="/" method="POST" onsubmit="return false;"> 
                    Control Panel : 
                    <button type="button" id="moveLButton" onmousedown="holdButton('Left')" onmouseup="releaseButton('Stop')">Left</button>
                    <button type="button" id="moveRButton" onmousedown="holdButton('Right')" onmouseup="releaseButton('Stop')">Right</button>
                    <button type="button" id="moveFButton" onmousedown="holdButton('Front')" onmouseup="releaseButton('Stop')">Front</button>
                    <button type="button" id="moveBButton" onmousedown="holdButton('Back')" onmouseup="releaseButton('Stop')">Back</button>    
            </form>
            <button type="button" id="vacuumOnButton" onmousedown="holdButton('VacuumOn')" onmouseup="releaseButton_noSerial()">VacuumOn</button>
            <button type="button" id="vacuumOffButton" onmousedown="holdButton('VacuumOff')" onmouseup="releaseButton_noSerial()">VacuumOff</button> 

            


                <script>
                    let interval; // Variable to hold the interval ID

                    function holdButton(state) {{
                        // Send the request immediately
                        sendRequest(state);

                        // Set an interval to keep sending the request while the button is held down
                        interval = setInterval(() => {{
                            sendRequest(state);
                        }}, 500); // Adjust the interval time as needed (500 ms here)
                    }}

                    function releaseButton(state) {{
                        // Clear the interval when the button is released
                        clearInterval(interval);
                        sendRequest(state);
                    }}
                    
                    function releaseButton_noSerial() {{
                        // Clear the interval when the button is released
                        clearInterval(interval);
                    }}

                    function sendRequest(state) {{
                        // Create an XMLHttpRequest to send the POST request
                        const xhr = new XMLHttpRequest();
                        xhr.open("POST", "/"); // Set the URL to your server
                        xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
                        xhr.send("submit=" + state); // Send the data as key=value
                    }}
                </script>


            </body>
            </html>
            '''
            temp = "50.0"#getTemperature()
            temp2 = "60.0"#getTemperature()
            self.do_HEAD() #to check if a resource is available without downloading the entire body (HTML content).
            # self.wfile.write(html.format(temp[5:]).encode("utf-8"))
            self.wfile.write(html.format(temp).encode("utf-8")) #.format(temp,temp2): 把兩個place holder 依序放入變數temp,temp2
            #<注意> format(temp)，這會把整個HTML的{ }當成place holder，所以script 中的{ }要記得double它成{{}}(每個都要!!內層的也要!!)，不然就是不要用place holder!
            # self.wfile.write(html.format(temp, temp2).encode("utf-8")) #.format(temp,temp2): 把兩個place holder 依序放入變數temp,temp2
            # self.wfile.write(html.encode("utf-8")) #若沒有place holder，也要有這個，這把content send 給browser as part of the HTTP response.
        elif self.path == '/styles.css': #handle css 
            # Serve CSS file
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            with open("styles.css", "rb") as file:
                self.wfile.write(file.read())
        else:
            # 404 Not Found for other paths
            self.send_response(404)
            self.end_headers()
    def do_POST(self):

        content_length = int(self.headers['Content-Length']) #self.headers['Content-Length']: 回傳從client的POST request送來的包含的data 的長度(string) --> int
        post_data = self.rfile.read(content_length).decode("utf-8") #reads the specified number of bytes from the request body (the data sent by the client).
        # .decode("utf-8") method converts the byte data into a string using UTF-8 encoding, allowing you to work with the data as a normal string in Python.
        post_data = post_data.split("=")[1] #把那POST request送來的字串data用=切開，取index 1的那個元素丟進post data的這個變數

        # setupGPIO()

#         if post_data == 'On':
#             # GPIO.output(18, GPIO.HIGH)
#             print("Botton On is clicked")
#             #ser.write(b"red\n")
#         else:
#             # GPIO.output(18, GPIO.LOW)
#             print("Botton Off is clicked")

        print("Turn {}".format(post_data))
#         #ser.write(b"%s\n" %(post_data).encode())
#         if post_data == 'Left':
#             print("LEFT is clicked")
#             #ser.write(b"Left\n")
#         elif post_data == 'Right':
#             print("RIGHT is clicked")
#             #ser.write(b"Right\n")
#         elif post_data == 'Front':
#             print("Front is clicked")
#             #ser.write(b"Front\n")
#         elif post_data == 'Back':
#             print("Back is clicked")
#             #ser.write(b"Back\n")
#         elif post_data == 'Stop':
#             print("Stop is clicked")
#             #ser.write(b"Stop\n")
        try:
            NowCommant = post_data.encode()
            #ser.write(b"%s\n" %(NowCommant))
        except:
            pass
        
#         try:
#             #ser.write(b"%s\n" %(post_data))
#         except:
#             pass
        self._redirect('/')  # 就是會自動刷新這個root URL page，所以新的資料會被自動更新上去 Redirect back to the root url 
        # After handling the form submission (turning the LED on or off), this line effectively refreshes the page 
        # or shows the updated status, preventing the browser from resubmitting the form if the user refreshes the page.

# # # # # Main # # # # #
if __name__ == '__main__':
    http_server = HTTPServer((host_name, host_port), MyServer)
    print("Server Starts - %s:%s" % (host_name, host_port))
    #RPI 2. 
    # ttyACM=0
    # try:
    #     ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    #     ttyACM=0
    # except:
    #     ser = serial.Serial('/dev/ttyACM1', 9600, timeout=1)
    #     ttyACM=1
        
    # print("Arduino plugged in '/dev/ttyACM%d'" % (ttyACM))

    #RPI 3. ser.


#         if post_data == 'On':
#             # GPIO.output(18, GPIO.HIGH)
#             print("Botton On is clicked")
#             #ser.write(b"red\n")
#         else:
#             # GPIO.output(18, GPIO.LOW)
#             print("Botton Off is clicked")

    
    print("Serial Starts")
    #ser.flush() #flush out every thing in the buffer

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()


    
    #RPI 4. GPIO.setup
    #pip install RPi.GPIO

    UltraPinR_Trig=11
    UltraPinR_Echo=12 #目前靠右走, 只有這個
    #UltraPin2=13
    #UltraPin3=15

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(UltraPinR_Trig, GPIO.OUT)
    GPIO.setup(UltraPinR_Echo, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Input加下拉電阻所以浮動的時候是0
    #GPIO.setup(UltraPin3, GPIO.IN)  
    # GPIO.setup(UltraPin1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
    duration=0
    distanceL=0 #(cm)
    distanceF=0
    distanceR=0
    timeout = 0.0012  # 最遠測到20cm
    # 20 milliseconds = maximum range of ~6.86 meters

    print("OK1")

    # 【For right sensor】 
    # Trigger the sensor
    GPIO.output(UltraPinR_Trig, GPIO.LOW)
    time.sleep(0.000005)
    GPIO.output(UltraPinR_Trig, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(UltraPinR_Trig, GPIO.LOW)

    # Wait for the echo to go HIGH (start)
    start_time = time.time()
    while GPIO.input(UltraPinR_Echo) == 0:
        pulse_startR = time.time()
        if pulse_startR - start_time > timeout:
            print("Timeout: No echo received (start)")
            pulse_startR = None
            break

    # Wait for the echo to go LOW (end)
    start_time = time.time()
    while GPIO.input(UltraPinR_Echo) == 1:
        pulse_endR = time.time()
        if pulse_endR - start_time > timeout:
            print("Timeout: No echo received (end)")
            pulse_endR = None
            break
    
    # Calculate distance if valid echo was received
    if pulse_startR and pulse_endR:
        pulse_durationR = pulse_endR - pulse_startR
        distanceR = (pulse_durationR * 34300) / 2
        print(f"Distance: {distanceR:.2f} cm")
    else:
        print("No valid measurement in Right Sensor")
        distanceR=1000 #1000cm 10 meter
    


    # # Wait for echo
    # while GPIO.input(UltraPinR_Echo) == 0:
    #     pulse_startR = time.time()
    # while GPIO.input(UltraPinR_Echo) == 1:
    #     pulse_endR = time.time()

    # Calculate distance
    # pulse_duration = pulse_endR - pulse_startR
    # distance = (pulse_duration * 34300) / 2  # Speed of sound = 343 m/s  # Speed of sound: 34300 cm/s divided by 2
    # print(f"Distance: {distance:.2f} cm")
    # GPIO.output(UltraPinR_Trig, GPIO.HIGH)

    if distance<=5
    #setup camera


    while(True): #loop下令區域 就靠右走吧
        




        # setupGPIO()

