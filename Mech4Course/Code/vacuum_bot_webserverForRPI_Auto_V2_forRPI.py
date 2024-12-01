
#!/usr/bin/env python3
#建立一個web server去接收按鈕的東東
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

# RPI 1. for RPI to Arduino communication
import serial
import time
import RPi.GPIO as GPIO

# for camera
import cv2
print(cv2.__version__)
import numpy as np


#host(server) 就是你的這台電腦，Define server address(讓之後client(browser可以知道server的IP位置))
host_name = '192.168.100.11'  # IP Address of Raspberry Pi (就是你電腦的IP) 要選Wi-Fi的IPv4 !!
host_name = '10.20.28.237'
host_port = 8000 #自己給的Port

class UltrasonicSensor:
    def __init__(self, trig_pin, echo_pin, timeout):
        self.trig = trig_pin
        self.echo = echo_pin
        
        # RPI 6. 設定Ultra
        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)
        self.timeout = timeout

    def measure_distance(self):
        # distance=4
        # RPI 7. 計算Distance
        GPIO.output(self.trig, False)
        time.sleep(0.000005)
        GPIO.output(self.trig, True)
        time.sleep(0.00001)
        GPIO.output(self.trig, False)
        # Rest of the measurement code
        start_time = time.time()
        while GPIO.input(self.echo) == 0:
            pulse_start = time.time()
            if pulse_start - start_time > self.timeout:
                print("Timeout: No echo received (start)")
                pulse_start = None
                break

        # Wait for the echo to go LOW (end)
        start_time = time.time()
        while GPIO.input(self.echo) == 1:
            pulse_end = time.time()
            if pulse_end - start_time > self.timeout:
                print("Timeout: No echo received (end)")
                pulse_end = None
                break
        
        # Calculate distance if valid echo was received
        if pulse_start and pulse_end:
            pulse_duration = pulse_end - pulse_start
            distance = (pulse_duration * 34300) / 2
            print(f"Distance: {distance:.2f} cm")
        else:
            print("No valid measurement in Right Sensor")
            distance=1000 #1000cm 10 meter
        
        
        return distance



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
#             ser.write(b"red\n")
#         else:
#             # GPIO.output(18, GPIO.LOW)
#             print("Botton Off is clicked")

        print("Turn {}".format(post_data))
#         ser.write(b"%s\n" %(post_data).encode())
#         if post_data == 'Left':
#             print("LEFT is clicked")
#             ser.write(b"Left\n")
#         elif post_data == 'Right':
#             print("RIGHT is clicked")
#             ser.write(b"Right\n")
#         elif post_data == 'Front':
#             print("Front is clicked")
#             ser.write(b"Front\n")
#         elif post_data == 'Back':
#             print("Back is clicked")
#             ser.write(b"Back\n")
#         elif post_data == 'Stop':
#             print("Stop is clicked")
#             ser.write(b"Stop\n")
        try:
            NowCommant = post_data.encode()
            ser.write(b"%s\n" %(NowCommant))
        except:
            pass
        
#         try:
#             ser.write(b"%s\n" %(post_data))
#         except:
#             pass
        self._redirect('/')  # 就是會自動刷新這個root URL page，所以新的資料會被自動更新上去 Redirect back to the root url 
        # After handling the form submission (turning the LED on or off), this line effectively refreshes the page 
        # or shows the updated status, preventing the browser from resubmitting the form if the user refreshes the page.



#【創建函式】
def empty(v):
      pass
def setColor(img, imgHSV): 
    #【取得現在控制條上的位置值】
    h_min = cv2.getTrackbarPos('Hue Min','TrackBar')
    h_max = cv2.getTrackbarPos('Hue Max','TrackBar')
    s_min = cv2.getTrackbarPos('Saturation Min','TrackBar')
    s_max = cv2.getTrackbarPos('Saturation Max','TrackBar')
    v_min = cv2.getTrackbarPos('Value Min','TrackBar')
    v_max = cv2.getTrackbarPos('Value Max','TrackBar')
    # print(h_min, h_max, s_min, s_max, v_min, v_max) #印出來
    
    #【4.過濾顏色】
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    
    #找到留下之區(imgMask是一個遮罩)
    imgMask = cv2.inRange(imgHSV,lower,upper) #過濾顏色 1st:要過濾的圖片名稱/2nd: 最小值/3rd: 最大值 (2nd,3rd皆用array表示)
    #過濾顏色: 黑: 被過濾掉的顏色，白: 留下來沒被過濾掉顏色的地方區域(留下之區,白)
    
    #把留下之區套回原圖裁減保留，得到過濾顏色的效果
    imgColorFilt = cv2.bitwise_and(img, img, mask=imgMask)
    #取img和img的交集(1 1 true...)，再套上遮罩，這個遮罩的區域就是imgMask
    return imgColorFilt, h_min, h_max, s_min, s_max, v_min, v_max
def filterColor(img, imgHSV, h_min, h_max, s_min, s_max, v_min, v_max): 
    #【4.過濾顏色】
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    
    #找到留下之區(imgMask是一個遮罩)
    imgMask = cv2.inRange(imgHSV,lower,upper) #過濾顏色 1st:要過濾的圖片名稱/2nd: 最小值/3rd: 最大值 (2nd,3rd皆用array表示)
    #過濾顏色: 黑: 被過濾掉的顏色，白: 留下來沒被過濾掉顏色的地方區域(留下之區,白)
    
    #把留下之區套回原圖裁減保留，得到過濾顏色的效果
    imgColorFilt = cv2.bitwise_and(img, img, mask=imgMask)
    #取img和img的交集(1 1 true...)，再套上遮罩，這個遮罩的區域就是imgMask
    return imgColorFilt
def DeterArea(img, areaThreshold): 
    #【另外複製一張圖片.copy】
    imgContour = img.copy()   #複製img這張圖放到imgContour中
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #先弄成灰色比較好找邊

    #【找輪廓(即找出很多輪廓點)】
    #<先找邊緣>
    imgCanny = cv2.Canny(img, 150, 200)  #先找邊緣canny
    #<再找輪廓>:輪廓點儲存在contours變數
    #回傳輪廓點陣列/階層       #找輪廓                  偵測外輪廓        近似方法:no(即保留所有輪廓點)
    contours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) #3rd:近似方法(壓縮水平or垂直輪廓點) 

    sumArea=0
    maxArea=0

    M=None
    area=0
    sumArea=0
    maxArea=0
    #【找到輪廓(外框)後的應用】印出來/得各輪廓所包面積/邊長/多邊形近似輪廓(回傳近似後多邊形的頂點)
    for cnt in contours: #(用for迴圈跑出所有輪廓點)***(此變數cnt將會一一索引跑過contour這個陣列的點)
        #print(cnt) #>>印出contour內的輪廓點(是文字方式去印)
        #<各種印用>
        cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 4) #1st:輪廓要畫在的圖imgContour上/2nd:要畫的點/3rd:要畫第幾個輪廓(因為可能會有很多輪廓)(1:都畫)/4th:顏色/5th:粗度(4像素)
        area = cv2.contourArea(cnt)  #取得輪廓(cnt)的面積
        sumArea += area
        
        if(area > maxArea):
            maxArea=area
            M = cv2.moments(cnt)

        # peri = cv2.arcLength(cnt, True) #取得每個輪廓(cnt)的邊長，1st: 要畫的輪廓點，2nd: 輪廓是開放(False)or閉合(True)
        # vertices = cv2.approxPolyDP(cnt, peri * 0.02, True) #用多邊形去近似輪廓(會回傳多邊形的頂點"vertices")，1st:要近似的輪廓/2nd:近似值(up->多邊形的邊越多)/3rd:輪廓是否閉合
        # corners = len(vertices) #頂點座標陣列vertices的陣列長度即為"頂點數量"
        
    if M and M["m00"] != 0:  # Ensure M exists and is valid
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            # print(f"Centroid: ({cX}, {cY})") 
    else:
        cX, cY = 0, 0
    cv2.putText(imgCanny, f"sumArea: {int(sumArea)}", (int(imgCanny.shape[1]/2), int(imgCanny.shape[0]/2)), cv2.FONT_HERSHEY_SIMPLEX,  0.5, (255, 255, 255), 2) # 在輪廓的中心位置添加文字，顯示該輪廓的面積
    cv2.putText(imgContour, f"sumArea: {int(sumArea)}", (int(imgCanny.shape[1]/2), int(imgCanny.shape[0]/2)), cv2.FONT_HERSHEY_SIMPLEX,  0.5, (255, 255, 255), 2) # 在輪廓的中心位置添加文字，顯示該輪廓的面積
    
    if maxArea>areaThreshold: #用area去過濾噪點雜訊(面積>500才去做下面"判斷形狀"這件事)
        
        return True, imgContour, imgCanny #表示看到紅色大面積了
    else: 
        return False, imgContour, imgCanny
            # x, y, w, h = cv2.boundingRect(vertices) #用方形把一陣列所有點全框住(回傳x:方形左上角x座標,y,w:方形寬,h:方形高)
            # cv2.rectangle(imgContour, (x, y), (x+w, y+h), (0, 255, 0), 4)#畫出此方形(2nd3rd: 方形左上角&右下角x,y座標)
            
            # #<用近似多邊形的角數判斷原圖是甚麼形狀>(by近似多邊形角數3->三角形/角數>6->圓形)
            # if corners == 3:
            #     cv2.putText(imgContour, 'triangle', (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            # elif corners == 4:
            #     cv2.putText(imgContour, 'rectangle', (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            # elif corners == 5:
            #     cv2.putText(imgContour, 'pentagon', (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            # elif corners >= 6:
            #     cv2.putText(imgContour, 'circle', (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    # return False, imgContour, imgCanny


# # # # # Main # # # # #
if __name__ == '__main__':
    # http_server = HTTPServer((host_name, host_port), MyServer)
    # print("Server Starts - %s:%s" % (host_name, host_port))
    #RPI 2. 
    ttyACM=0
    try:
        ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        ttyACM=0
    except:
        ser = serial.Serial('/dev/ttyUSB1', 9600, timeout=1)
        ttyACM=1
        
    print("Arduino plugged in '/dev/ttyUSB%d'" % (ttyACM))

    #RPI 3. ser.
    print("Serial Starts")
    ser.flush() #flush out every thing in the buffer


    #不行這個了, 城市會卡在這裡
    # try:
    #     http_server.serve_forever()
    # except KeyboardInterrupt:
    #     http_server.server_close()
    #
    print("ok0")

    
    
    UltraPinR_Trig=11
    UltraPinR_Echo=12 #目前靠右走, 只有這個
    UltraPinF_Trig=15
    UltraPinF_Echo=16
    timeoutR = 0.0012  # 最遠測到20cm
    timeoutF = 0.0012  # 最遠測到20cm
    
    #RPI 5. 設定Ultra
    GPIO.setmode(GPIO.BCM)
    sensorR = UltrasonicSensor(UltraPinR_Trig, UltraPinR_Echo, timeoutR)
    sensorF = UltrasonicSensor(UltraPinF_Trig, UltraPinF_Echo, timeoutF)

    post_data_Ultra='Front' #最開始就直走
    NowCommant_Ultra = post_data_Ultra.encode()
    ser.write(b"%s\n" %(NowCommant_Ultra))


    #======================= setup camera ======================
    cap=cv2.VideoCapture(0)
    setColorFlag=False
    DetectRed=False

    ret,img = cap.read()
    if ret: #如果ret是TRUE
        #cv2.imshow('The Original Image',img) #顯示出這張frame照片
        print("get first image")
    else:
        print("there are some problem for camera, stop code")
        
    # img = cv2.resize(img,(0,0),fx=0.5,fy=0.5)
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    h_min, h_max, s_min, s_max, v_min, v_max=0,82,147,255,149,255



    if(setColorFlag==True): 
        #【2.找到正確的顏色HSV限制值-在視窗'TrackBer'建立一個控制條】
        #創視窗
        cv2.namedWindow('TrackBar') #創建一個視窗1st[視窗名稱]
        cv2.resizeWindow('TrackBar',640,320) #調整視窗大小

        #在視窗'TrackBar'建立一個控制條
        #                   [控制條名稱][視窗名稱][bar最小值][最大值][更動完要呼叫的函式]
        cv2.createTrackbar('Hue Min','TrackBar', h_min, 179, empty)
        cv2.createTrackbar('Hue Max','TrackBar', h_max, 179, empty)
        cv2.createTrackbar('Saturation Min','TrackBar', s_min, 255, empty)
        cv2.createTrackbar('Saturation Max','TrackBar', s_max, 255, empty)
        cv2.createTrackbar('Value Min','TrackBar', v_min, 255, empty)
        cv2.createTrackbar('Value Max','TrackBar', v_max, 255, empty)

        while(True): 
            imgColorFilt, h_min, h_max, s_min, s_max, v_min, v_max=setColor(img, imgHSV)
            cv2.imshow('TrackBar',imgColorFilt)
            #要加if,要有break!!不然電腦判斷自己卡在迴圈裡就當機了
            if cv2.waitKey(10) & 0xFF == ord('d'):
                cv2.destroyWindow('TrackBar')
                break
            cv2.waitKey(1)

    print(h_min, h_max, s_min, s_max, v_min, v_max)



    vacuum_off_time = None  # <Debug> 要初始化在迴圈外面，不然一直重新設成None了，而且因為跨越迴圈之後還要記得資料Initialize a variable to store the time when vacuum is turned off
    try:
        while True:
            # cap2=cv2.VideoCapture(0)
            # print("ok2")
            
            #RPI 4. GPIO.setup
            #pip install RPi.GPIO
            distanceR = sensorR.measure_distance()
            print(f"DistanceR: {distanceR:.2f} cm")
            distanceF = sensorR.measure_distance()
            print(f"DistanceF: {distanceF:.2f} cm")

            if(distanceF<15): #前面太近就左轉
                post_data_Ultra='Left'
            elif(distanceR>10 and distanceF>15): #右邊太遠而且前面沒有東西, 還沒要轉彎
                post_data_Ultra='Right'
            elif(distanceR<5 and distanceF>15): #右邊太近而且還沒要轉彎
                post_data_Ultra='Left'
            else: 
                post_data_Ultra='Front'



            print("turn: "+post_data_Ultra)
            NowCommant_Ultra = post_data_Ultra.encode()
            ser.write(b"%s\n" %(NowCommant_Ultra))
            #================= Camera ===============================
            # ================= Camera ===============================
            ret2, img2 = cap.read()
            if not ret2:
                print("Error: Could not read frame from camera")
                break  # Exit the loop if camera is not functioning correctly

            # Resize img2 if necessary
            img2 = cv2.resize(img2, (0, 0), fx=0.5, fy=0.5)
            img2HSV = cv2.cvtColor(img2,cv2.COLOR_BGR2HSV)
            img2_filter = filterColor(img2, img2HSV, h_min, h_max, s_min, s_max, v_min, v_max)
            # Display the image in a window
            # cv2.imshow('OriginalImg', img2)
            cv2.imshow('FilterImg', img2_filter)

            DetectRed, img2Contour, img2Canny = DeterArea(img2_filter, 2000) #areaThreshold
            cv2.imshow('img2Contour', img2Contour)
            cv2.imshow('img2Canny', img2Canny)
            # if(DetectRed==False): 
            #     post_data_Red='VacuumOn'
            #     print("Vocuum Status: "+post_data_Red)
            #     NowCommant_Red = post_data_Red.encode()
            #     ser.write(b"%s\n" %(NowCommant_Red))
            # else: 
            #     post_data_Red='VacuumOff'
            #     print("Vocuum Status: "+post_data_Red)
            #     NowCommant_Red = post_data_Red.encode()
                
            #     ser.write(b"%s\n" %(NowCommant_Red))
            
            if DetectRed == False: 
                # If no red is detected and the vacuum is off due to a prior detection, ensure it's only turned on after 5 seconds
                # print("vacuum_off_time: " + str(vacuum_off_time))
                # print("time.time(): " + str(time.time()))
                # print("time.time() - vacuum_off_time: " + str(time.time() - vacuum_off_time))
                if vacuum_off_time and (time.time() - vacuum_off_time) < 5:
                    # print("Vacuum remains off for 5 seconds")
                    # post_data_Red = 'VacuumOff'
                    # print("Vacuum Status: " + post_data_Red)
                    # NowCommant_Red = post_data_Red.encode()
                    pass
                else: 
                    post_data_Red = 'VacuumOn'
                    # print("Vacuum Status: " + post_data_Red)
                    NowCommant_Red = post_data_Red.encode()
                    vacuum_off_time = None  # Reset the off time
                    # ser.write(b"%s\n" %(NowCommant_Red))

            else: 
                # If red is detected, turn off the vacuum and record the time
                vacuum_off_time = time.time()  # Record the current time
                post_data_Red = 'VacuumOff'
                # print("Vacuum Status: " + post_data_Red)
                NowCommant_Red = post_data_Red.encode()
                # ser.write(b"%s\n" %(NowCommant_Red))
            # print("Vacuum Status: " + post_data_Red)
            # Draw the `post_data_Red` on the original image
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.5
            color = (0, 0, 255)  # Red color for the text
            thickness = 2
            position = (50, 50)  # Position of the text (x, y)

            # Overlay the text on the original image
            cv2.putText(img2, f"Vacuum Status: {post_data_Red}", position, font, font_scale, color, thickness, cv2.LINE_AA)
            # cv2.putText(imgContour, f"{int(maxArea)}", (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,  0.5, (255, 255, 255), 2) # 在輪廓的中心位置添加文字，顯示該輪廓的面積
    
            cv2.imshow('OriginalImg', img2)

#=========================================================



            # Check for 'q' key press to exit the loop
            if cv2.waitKey(10) & 0xFF == ord('q'):
                # GPIO.cleanup()
                break




            #Set camera 如果偵測到紅色圓圓就把vacuum停掉
            # ret2,img2 = cap.read()
            # if ret: #如果ret是TRUE
            #     cv2.imshow('The_original_image',img) #顯示出這張frame照片
            # else:
            #     print("there are some problem for camera, stop code")
            #     break  #如果ret不是true，就跳出這個while迴圈(影片結束or出問題了)
            # cv2.imshow('The_original_image',img2)
            # img2 = cv2.resize(img2,(0,0),fx=0.5,fy=0.5)
            # imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

            # imgColorFilt = filterColor(imgHSV)
            # cv2.imshow('TrackBar1',img2)



            # time.sleep(1)
    except KeyboardInterrupt:
        # RPI 8. Clean up
        GPIO.cleanup()
        print("Code end")
    # while(True): #loop下令區域 就靠右走吧
    #     o=0




        # setupGPIO()

