
#!/usr/bin/env python3
#建立一個web server去接收按鈕的東東
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

#host(server) 就是你的這台電腦，Define server address(讓之後client(browser可以知道server的IP位置))
host_name = '192.168.106.119'  # IP Address of Raspberry Pi (就是你電腦的IP)
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
        html = '''
           <html>
           <body 
            style="width:960px; margin: 20px auto;">
           <h1>Welcome to the Vacume Controling web browser !</h1>
           <p>Current GPU temperature is {}</p>
           
           <form id="movementForm" action="/" method="POST" onsubmit="return false;"> 
                Control Panel : 
                <button type="button" id="moveLButton" onmousedown="holdButton('Right')" onmouseup="releaseButton()">Right</button>
                <button type="button" id="moveRButton" onmousedown="holdButton('Left')" onmouseup="releaseButton()">Left</button>   
                <button type="button" id="moveFButton" onmousedown="holdButton('Front')" onmouseup="releaseButton()">Front</button>
                <button type="button" id="moveBButton" onmousedown="holdButton('Back')" onmouseup="releaseButton()">Back</button>    
           </form>

           


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

                function releaseButton() {{
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
    
    def do_POST(self):

        content_length = int(self.headers['Content-Length']) #self.headers['Content-Length']: 回傳從client的POST request送來的包含的data 的長度(string) --> int
        post_data = self.rfile.read(content_length).decode("utf-8") #reads the specified number of bytes from the request body (the data sent by the client).
        # .decode("utf-8") method converts the byte data into a string using UTF-8 encoding, allowing you to work with the data as a normal string in Python.
        post_data = post_data.split("=")[1] #把那POST request送來的字串data用=切開，取index 1的那個元素丟進post data的這個變數

        # setupGPIO()

        if post_data == 'On':
            # GPIO.output(18, GPIO.HIGH)
            print("Botton On is clicked")
        else:
            # GPIO.output(18, GPIO.LOW)
            print("Botton Off is clicked")

        print("Turn {}".format(post_data))
        self._redirect('/')  # 就是會自動刷新這個root URL page，所以新的資料會被自動更新上去 Redirect back to the root url 
        # After handling the form submission (turning the LED on or off), this line effectively refreshes the page 
        # or shows the updated status, preventing the browser from resubmitting the form if the user refreshes the page.

# # # # # Main # # # # #
if __name__ == '__main__':
    http_server = HTTPServer((host_name, host_port), MyServer)
    print("Server Starts - %s:%s" % (host_name, host_port))

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()