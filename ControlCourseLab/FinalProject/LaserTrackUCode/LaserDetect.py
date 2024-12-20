# for camera
import cv2
print(cv2.__version__)
import numpy as np
import time



IsDebug = False


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
def DeterLaserArea(img, areaThreshold, x1_bound, y1_bound, x2_bound, y2_bound): 

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
    LaserCenter=[0,0]
    #【找到輪廓(外框)後的應用】印出來/得各輪廓所包面積/邊長/多邊形近似輪廓(回傳近似後多邊形的頂點)
    for cnt in contours: #(用for迴圈跑出所有輪廓點)***(此變數cnt將會一一索引跑過contour這個陣列的點)
        #print(cnt) #>>印出contour內的輪廓點(是文字方式去印)
        #<各種印用>
        cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 4) #1st:輪廓要畫在的圖imgContour上/2nd:要畫的點/3rd:要畫第幾個輪廓(因為可能會有很多輪廓)(1:都畫)/4th:顏色/5th:粗度(4像素)
        area = cv2.contourArea(cnt)  #取得輪廓(cnt)的面積
        sumArea += area
        
        if(area > maxArea and area <40) : #夠小才有可能是雷射筆
            maxArea=area
            M = cv2.moments(cnt)
            if M and M["m00"] != 0:  # Ensure M exists and is valid
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                if(x1_bound<cx and cx<x2_bound and y1_bound<cy and cy<y2_bound):
                    LaserCenter[0] = int(M["m10"] / M["m00"])
                    LaserCenter[1] = int(M["m01"] / M["m00"])
                
                
            # x1_bound, y1_bound, x2_bound, y2_bound

        # peri = cv2.arcLength(cnt, True) #取得每個輪廓(cnt)的邊長，1st: 要畫的輪廓點，2nd: 輪廓是開放(False)or閉合(True)
        # vertices = cv2.approxPolyDP(cnt, peri * 0.02, True) #用多邊形去近似輪廓(會回傳多邊形的頂點"vertices")，1st:要近似的輪廓/2nd:近似值(up->多邊形的邊越多)/3rd:輪廓是否閉合
        # corners = len(vertices) #頂點座標陣列vertices的陣列長度即為"頂點數量"
        
    # if M and M["m00"] != 0:  # Ensure M exists and is valid
    #         LaserCenter[0] = int(M["m10"] / M["m00"])
    #         LaserCenter[1] = int(M["m01"] / M["m00"])
            # print(f"Centroid: ({cX}, {cY})") 
    # else:
        # cX, cY = 0, 0
    cv2.putText(imgCanny, f"sumArea: {int(sumArea)}", (int(imgCanny.shape[1]/2), int(imgCanny.shape[0]/2)), cv2.FONT_HERSHEY_SIMPLEX,  0.5, (255, 255, 255), 2) # 在輪廓的中心位置添加文字，顯示該輪廓的面積
    cv2.putText(imgContour, f"sumArea: {int(sumArea)}", (int(imgCanny.shape[1]/2), int(imgCanny.shape[0]/2)), cv2.FONT_HERSHEY_SIMPLEX,  0.5, (255, 255, 255), 2) # 在輪廓的中心位置添加文字，顯示該輪廓的面積
    
    if maxArea>areaThreshold: #用area去過濾噪點雜訊(面積>500才去做下面"判斷形狀"這件事)
        
        return LaserCenter, imgContour, imgCanny #表示看到紅色大面積了
    else: 
        return LaserCenter, imgContour, imgCanny
    
def DeterBlueBoundingArea(img, areaThreshold): 

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
    LaserCenter=[0,0]
    filtered_contours = []  # To store contours within the area range

    #【找到輪廓(外框)後的應用】印出來/得各輪廓所包面積/邊長/多邊形近似輪廓(回傳近似後多邊形的頂點)
    for cnt in contours: #(用for迴圈跑出所有輪廓點)***(此變數cnt將會一一索引跑過contour這個陣列的點)
        #print(cnt) #>>印出contour內的輪廓點(是文字方式去印)
        #<各種印用>
        cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 4) #1st:輪廓要畫在的圖imgContour上/2nd:要畫的點/3rd:要畫第幾個輪廓(因為可能會有很多輪廓)(1:都畫)/4th:顏色/5th:粗度(4像素)
        area = cv2.contourArea(cnt)  #取得輪廓(cnt)的面積
        sumArea += area
        if(IsDebug):
            cv2.imshow("imgContourBlue", imgContour)
        cv2.waitKey(1)
        
        if(area >areaThreshold) : #夠小才有可能是雷射筆
            # maxArea=area
            M = cv2.moments(cnt)
            filtered_contours.append(cnt) 

    if filtered_contours:
        all_points = np.vstack(filtered_contours)
        # Get minimum bounding box for filtered contours
        x, y, w, h = cv2.boundingRect(all_points)  # Axis-aligned bounding box
        # Draw bounding boxes on the image
        cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Draw axis-aligned box
        # peri = cv2.arcLength(cnt, True) #取得每個輪廓(cnt)的邊長，1st: 要畫的輪廓點，2nd: 輪廓是開放(False)or閉合(True)
        # vertices = cv2.approxPolyDP(cnt, peri * 0.02, True) #用多邊形去近似輪廓(會回傳多邊形的頂點"vertices")，1st:要近似的輪廓/2nd:近似值(up->多邊形的邊越多)/3rd:輪廓是否閉合
        # corners = len(vertices) #頂點座標陣列vertices的陣列長度即為"頂點數量"
        return  x, y, x + w, y + h #左上點右下點
    else: 
        return  0, 0, img.shape[1], img.shape[0]
    # if M and M["m00"] != 0:  # Ensure M exists and is valid
    #         LaserCenter[0] = int(M["m10"] / M["m00"])
    #         LaserCenter[1] = int(M["m01"] / M["m00"])
    #         # print(f"Centroid: ({cX}, {cY})") 
    # # else:
    #     # cX, cY = 0, 0
    # cv2.putText(imgCanny, f"sumArea: {int(sumArea)}", (int(imgCanny.shape[1]/2), int(imgCanny.shape[0]/2)), cv2.FONT_HERSHEY_SIMPLEX,  0.5, (255, 255, 255), 2) # 在輪廓的中心位置添加文字，顯示該輪廓的面積
    # cv2.putText(imgContour, f"sumArea: {int(sumArea)}", (int(imgCanny.shape[1]/2), int(imgCanny.shape[0]/2)), cv2.FONT_HERSHEY_SIMPLEX,  0.5, (255, 255, 255), 2) # 在輪廓的中心位置添加文字，顯示該輪廓的面積
    
    # if maxArea>areaThreshold: #用area去過濾噪點雜訊(面積>500才去做下面"判斷形狀"這件事)
        
    #     return LaserCenter, imgContour, imgCanny #表示看到紅色大面積了
    # else: 
    #     return LaserCenter, imgContour, imgCanny




#============================ the public function ===================================
def getLaserCoordinate(img2): 
    
    #[Parameters]
    #The already refined parameters will be setted here, if want to justify a new one, run main
    h_min, h_max, s_min, s_max, v_min, v_max = 63, 99, 35, 124, 159, 255   # for filter 只留下綠色雷射筆色
    h_min_b, h_max_b, s_min_b, s_max_b, v_min_b, v_max_b = 27, 163, 69, 255, 0, 255   # 89, 140, 90, 255, 0, 255) #89, 140, 99, 255, 50, 255   #60, 168, 0, 255, 0, 210)###########################################################################



    # img2 = cv2.resize(img2, (0, 0), fx=0.5, fy=0.5)
    img2HSV = cv2.cvtColor(img2,cv2.COLOR_BGR2HSV)
    img2_filter = filterColor(img2, img2HSV, h_min, h_max, s_min, s_max, v_min, v_max)
    result_image = img2.copy()
    if(IsDebug): 
        cv2.imshow('LaserFilterImg', img2_filter)

    # Filter Blue Color To get the Blue Bounding Box
    img2_filter_blue = filterColor(img2, img2HSV, h_min_b, h_max_b, s_min_b, s_max_b, v_min_b, v_max_b)
    x1_bound, y1_bound, x2_bound, y2_bound = DeterBlueBoundingArea(img2_filter_blue, 10)
    result_image = cv2.rectangle(result_image, (x1_bound, y1_bound), (x2_bound, y2_bound), (0, 255, 0), 2)
    if(IsDebug):
        bound_image = cv2.rectangle(img2, (x1_bound, y1_bound), (x2_bound, y2_bound), (0, 255, 0), 2)  # Draw axis-aligned box
        bound_image2 = cv2.rectangle(img2_filter_blue, (x1_bound, y1_bound), (x2_bound, y2_bound), (0, 255, 0), 2)  # Draw axis-aligned box
    
    
        cv2.imshow('Blue bound_image ', bound_image)
        cv2.imshow('Blue bound_image2 ', bound_image2)

    # DetectRed, img2Contour, img2Canny = DeterArea(img2_filter, 2000) #areaThreshold

    LaserCenter, img2Contour, img2Canny = DeterLaserArea(img2_filter, 0, x1_bound, y1_bound, x2_bound, y2_bound) #2000#areaThreshold不太好
    # LaserCenter, img2Contour, img2Canny = DeterLaserArea(img2_filter, 0, 0, 0, img2_filter.shape[1], img2_filter.shape[0]) 
    # Draw the center point
    if(IsDebug):
        cv2.imshow('img2Contour', img2Contour)
        cv2.imshow('img2Canny', img2Canny)
    
    result_image = cv2.circle(result_image, LaserCenter, 5, (0, 255, 255), -1)  # Yellow dot at the center
    result_image = cv2.putText(result_image, f"({LaserCenter[0]}, {LaserCenter[1]})", (LaserCenter[0]-50, LaserCenter[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0,255,255), 1, cv2.LINE_AA)
            
    # cv2.putText(imgContour, f"{int(maxArea)}", (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,  0.5, (255, 255, 255), 2) # 在輪廓的中心位置添加文字，顯示該輪廓的面積
    
    # cv2.imshow('OriginalImg', result_image)
    return LaserCenter, result_image


#==================== using the   function above (main example) ====================
if __name__ == '__main__':
    print("Laser Detect Starts")
    #======================= setup camera ======================
    cap=cv2.VideoCapture(1) #1
    try:
        while True:
            # ================= Camera ===============================
            ret2, img = cap.read()
            img2 = img.copy()
            img2 = cv2.resize(img2, (0, 0), fx=0.5, fy=0.5)
            if not ret2:
                print("Error: Could not read frame from camera")
                break  # Exit the loop if camera is not functioning correctly

            LaserCenter, result_image = getLaserCoordinate(img2) #2000#areaThreshold不太好
            # Draw the center point
            img2 = cv2.circle(img2, LaserCenter, 5, (0, 255, 255), -1)  # Yellow dot at the center
            img2 = cv2.putText(img2, f"({LaserCenter[0]}, {LaserCenter[1]})", (LaserCenter[0]-50, LaserCenter[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0,255,255), 1, cv2.LINE_AA)
            
            # cv2.putText(imgContour, f"{int(maxArea)}", (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,  0.5, (255, 255, 255), 2) # 在輪廓的中心位置添加文字，顯示該輪廓的面積
    
            cv2.imshow('The original image draw with laser center', img2)
            cv2.imshow('The result image generated by the function', result_image)

#=========================================================


            # Check for 'q' key press to exit the loop
            if cv2.waitKey(10) & 0xFF == ord('q'):
                # GPIO.cleanup()
                break

    except KeyboardInterrupt:
        # RPI 8. Clean up
        #GPIO.cleanup()
        print("Code end")
  





#===================================【完整測試所有選色, 選色的code 不可刪!!】=============================================
# if __name__ == '__main__':
#     print("Laser Detect Starts")
#     #======================= setup camera ======================
#     theCap=0
#     # for i in range(5):  # Try indices 0-4
#     #     try:
#     #         cap = cv2.VideoCapture(i+1)
#     #         print(f"Camera finding at index {i+1}")
#     #         cv2.waitKey(20)
#     #         if cap.isOpened():
#     #             print(f"Camera found at index {i+1}")
#     #             theCap=i+1
#     #             break
#     #     except: 
#     #         continue
#     # cap.release()
#     # cap=cv2.VideoCapture(theCap)
#     cap=cv2.VideoCapture(1) #1
#     setColorFlag=True
#     # DetectRed=False

#     ret,img = cap.read()
#     if ret: #如果ret是TRUE
#         #cv2.imshow('The Original Image',img) #顯示出這張frame照片
#         print("get first image")
#     else:
#         print("there are some problem for camera, stop code")
        
#     img = cv2.resize(img,(0,0),fx=0.5,fy=0.5)
#     imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

#     h_min, h_max, s_min, s_max, v_min, v_max = 63, 99, 35, 124, 159, 255  # 0, 179, 0, 74, 233, 255#Green1(較不strict): 0, 179, 0, 179, 220, 255#Red Laser: 136, 179, 14, 255, 255, 255



#     if(setColorFlag==True): 
#         #【2.找到正確的顏色HSV限制值-在視窗'TrackBer'建立一個控制條】
#         #創視窗
#         cv2.namedWindow('TrackBar') #創建一個視窗1st[視窗名稱]
#         cv2.resizeWindow('TrackBar',640,320) #調整視窗大小

#         #在視窗'TrackBar'建立一個控制條
#         #                   [控制條名稱][視窗名稱][bar最小值][最大值][更動完要呼叫的函式]
#         cv2.createTrackbar('Hue Min','TrackBar', h_min, 179, empty)
#         cv2.createTrackbar('Hue Max','TrackBar', h_max, 179, empty)
#         cv2.createTrackbar('Saturation Min','TrackBar', s_min, 255, empty)
#         cv2.createTrackbar('Saturation Max','TrackBar', s_max, 255, empty)
#         cv2.createTrackbar('Value Min','TrackBar', v_min, 255, empty)
#         cv2.createTrackbar('Value Max','TrackBar', v_max, 255, empty)

#         while(True): 
#             imgColorFilt, h_min, h_max, s_min, s_max, v_min, v_max=setColor(img, imgHSV)
#             cv2.imshow('TrackBar',imgColorFilt)
#             #要加if,要有break!!不然電腦判斷自己卡在迴圈裡就當機了
#             if cv2.waitKey(10) & 0xFF == ord('d'):
#                 cv2.destroyWindow('TrackBar')
#                 break
#             cv2.waitKey(1)

#     print(h_min, h_max, s_min, s_max, v_min, v_max)



#     vacuum_off_time = None  # <Debug> 要初始化在迴圈外面，不然一直重新設成None了，而且因為跨越迴圈之後還要記得資料Initialize a variable to store the time when vacuum is turned off
#     try:
#         while True:
#             # ================= Camera ===============================
#             ret2, img2 = cap.read()
#             if not ret2:
#                 print("Error: Could not read frame from camera")
#                 break  # Exit the loop if camera is not functioning correctly

#             # Resize img2 if necessary
#             img2 = cv2.resize(img2, (0, 0), fx=0.5, fy=0.5)
#             img2HSV = cv2.cvtColor(img2,cv2.COLOR_BGR2HSV)
#             img2_filter = filterColor(img2, img2HSV, h_min, h_max, s_min, s_max, v_min, v_max)
#             # Display the image in a window
#             # cv2.imshow('OriginalImg', img2)
#             cv2.imshow('FilterImg', img2_filter)

#             # Filter Blue Color To get the Blue Bounding Box
#             img2_filter_blue = filterColor(img2, img2HSV, 27, 163, 69, 255, 0, 255)#89, 140, 90, 255, 0, 255) #89, 140, 99, 255, 50, 255   #60, 168, 0, 255, 0, 210)###########################################################################
#             x1_bound, y1_bound, x2_bound, y2_bound = DeterBlueBoundingArea(img2_filter_blue, 10)
#             bound_image = cv2.rectangle(img2, (x1_bound, y1_bound), (x2_bound, y2_bound), (0, 255, 0), 2)  # Draw axis-aligned box
#             bound_image2 = cv2.rectangle(img2_filter_blue, (x1_bound, y1_bound), (x2_bound, y2_bound), (0, 255, 0), 2)  # Draw axis-aligned box
            
#             cv2.imshow('bound_image ', bound_image)
#             cv2.imshow('bound_image2 ', bound_image2)

#             # DetectRed, img2Contour, img2Canny = DeterArea(img2_filter, 2000) #areaThreshold
#             LaserCenter, img2Contour, img2Canny = DeterLaserArea(img2_filter, 0, x1_bound, y1_bound, x2_bound, y2_bound) #2000#areaThreshold不太好
#             # LaserCenter, img2Contour, img2Canny = DeterLaserArea(img2_filter, 0, 0, 0, img2_filter.shape[1], img2_filter.shape[0]) 
#             # Draw the center point
#             cv2.circle(img2, LaserCenter, 5, (0, 255, 255), -1)  # Yellow dot at the center

            
#             cv2.imshow('img2Contour', img2Contour)
#             cv2.imshow('img2Canny', img2Canny)
            
#             # if DetectRed == False: 
#             #     if vacuum_off_time and (time.time() - vacuum_off_time) < 5:
#             #         pass
#             #     else: 
#             #         post_data_Red = 'VacuumOn'
#             #         # print("Vacuum Status: " + post_data_Red)
#             #         NowCommant_Red = post_data_Red.encode()
#             #         vacuum_off_time = None  # Reset the off time

#             # else: 
#             #     # If red is detected, turn off the vacuum and record the time
#             #     vacuum_off_time = time.time()  # Record the current time
#             #     post_data_Red = 'VacuumOff'
#             #     # print("Vacuum Status: " + post_data_Red)
#             #     NowCommant_Red = post_data_Red.encode()
#             #     # ser.write(b"%s\n" %(NowCommant_Red))
#             # # print("Vacuum Status: " + post_data_Red)
#             # # Draw the `post_data_Red` on the original image
#             # font = cv2.FONT_HERSHEY_SIMPLEX
#             # font_scale = 0.5
#             # color = (0, 0, 255)  # Red color for the text
#             # thickness = 2
#             # position = (50, 50)  # Position of the text (x, y)

#             # Overlay the text on the original image
#             #LaserP: 
#             cv2.putText(img2, f"({LaserCenter[0]}, {LaserCenter[1]})", (LaserCenter[0]-50, LaserCenter[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0,255,255), 1, cv2.LINE_AA)
            
#             # cv2.putText(imgContour, f"{int(maxArea)}", (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,  0.5, (255, 255, 255), 2) # 在輪廓的中心位置添加文字，顯示該輪廓的面積
    
#             cv2.imshow('OriginalImg', img2)

# #=========================================================


#             # Check for 'q' key press to exit the loop
#             if cv2.waitKey(10) & 0xFF == ord('q'):
#                 # GPIO.cleanup()
#                 break




#             #Set camera 如果偵測到紅色圓圓就把vacuum停掉
#             # ret2,img2 = cap.read()
#             # if ret: #如果ret是TRUE
#             #     cv2.imshow('The_original_image',img) #顯示出這張frame照片
#             # else:
#             #     print("there are some problem for camera, stop code")
#             #     break  #如果ret不是true，就跳出這個while迴圈(影片結束or出問題了)
#             # cv2.imshow('The_original_image',img2)
#             # img2 = cv2.resize(img2,(0,0),fx=0.5,fy=0.5)
#             # imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

#             # imgColorFilt = filterColor(imgHSV)
#             # cv2.imshow('TrackBar1',img2)



#             # time.sleep(1)
#     except KeyboardInterrupt:
#         # RPI 8. Clean up
#         #GPIO.cleanup()
#         print("Code end")
