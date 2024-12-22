import cv2

# import stage_1
from tello import Tello
from detection import detect_moving_objects
from LaserDetect import getLaserCoordinate

def follow(tello: Tello, currentX: int, currentY: int, targetX: int, targetY: int):
    """
    sending rc command to tello based on how far current and target coord
    x is pixels right from upperleft
    y is pixels down from upperleft
    """
    proportion = 0.17    # 17 power per 100 pixels difference
    roll = proportion * (targetX - currentX)                # pos: right
    throttle = proportion * (currentY - targetY) + 11       # pos: up       with vertical offset

    roll = min(roll, 100)
    roll = max(-100, roll)

    throttle = min(throttle, 100)
    throttle = max(-100, throttle)

    tello.send_command2(f"rc {int(roll)} -4 {int(throttle)} 0")
    return None

# Example usage in a video processing loop
if __name__ == "__main__":
    # Initialize video capture (replace with your video file or camera)
    cap = cv2.VideoCapture(1)
    fgbg = cv2.createBackgroundSubtractorMOG2()
    ret, frame = cap.read()

    tello = Tello()
    # lotcziny(tello)
    tello.send_command("command")
    tello.send_command("takeoff")
    
    preCenter = [0,0]
    center = [0,0]
    mode = 'manual'
    proximity = 20  # 20 pixels is close enough




    # Target 現在追蹤到的雷射筆點
    # targets = stage_1.square_pathing(frame, visualize = False)
    previousTarget = [0,0] #用來存之前的資料
    
    
    while True:
        ret, frame = cap.read()
        if not ret:  # If no frame is read, exit the loop (end of video)
            break

        # Call the function to detect moving objects
        preCenter = center
        frame, center = detect_moving_objects(preCenter, frame, fgbg, visualize = True)

        # 如果是按l 就是用雷射筆控制模式
        if cv2.waitKey(1) & 0xFF == ord('l'):   #按下p後開始跟隨循跡
            mode = 'laser'

        # Break the loop if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            tello.send_command("land")
            break

        if cv2.waitKey(1) & 0xFF == ord('p'):   #按下p後開始跟隨循跡
            mode = 'pathing'


        # laser筆模式
        if mode == "laser":
            #就要追蹤laser 當作target (傳進去一個frame，要能拿到這個frame過濾出的雷射筆座標)
                        # LaserCenter, result_image = getLaserCoordinate(img2) #2000#areaThreshold不太好
            # # Draw the center point
            # img2 = cv2.circle(img2, LaserCenter, 5, (0, 255, 255), -1)  # Yellow dot at the center
            # img2 = cv2.putText(img2, f"({LaserCenter[0]}, {LaserCenter[1]})", (LaserCenter[0]-50, LaserCenter[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0,255,255), 1, cv2.LINE_AA)
            
            # cv2.putText(imgContour, f"{int(maxArea)}", (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,  0.5, (255, 255, 255), 2) # 在輪廓的中心位置添加文字，顯示該輪廓的面積
    
            # cv2.imshow('The original image draw with laser center', img2)
            # cv2.imshow('The result image generated by the function', result_image)
     

            
            target, laser_detect_result_image = getLaserCoordinate(frame) #target is LaserCenter #一直即時看到laser在哪裡
            #if laser_center = [0,0] 表示沒有laser, 這樣你就沿用之前的laser #[0,0] 是在你前面的function code弄出的
            if(target[0]==0 and target[1]==0): 
                target=previousTarget
            else: #所以如果上上次也是沒有雷射，就是繼續沿用之前的laser資料
                previousTarget = target 

            # frame = cv2.circle(frame, (target[0], target[1]), proximity, (0, 255, 255), 5) #黃色是你目標座標(laser)
            # frame = cv2.circle(frame, (center[0], center[1]), proximity, (255, 0, 0), 5) #紅色是你現在無人機座標
            cv2.imshow('The result image generated by the function', laser_detect_result_image)

            frame = cv2.circle(frame, (target[0], target[1]), 5, (0, 255, 255), -1) #黃色是你目標座標(laser)
            frame = cv2.circle(frame, (center[0], center[1]), 5, (255, 0, 0), -1) #紅色是你現在無人機座標

            follow(tello, center[0], center[1], target[0], target[1]) 

            # if (center[0] - target[0])**2 + (center[1] - target[1])**2 <= proximity**2:
            #     # this is close enough to this point, going to the next point
            #     print("GOAL")
            #     targets = targets[1:]

        if mode == "manual":
        # Controll the drone by hand (for testing purpose only)
            strength = 20
            if cv2.waitKey(1) & 0xFF == ord('w'):
                print("\nthrottle UP")
                tello.send_command2(f"rc 0 0 {strength} 0")

            if cv2.waitKey(1) & 0xFF == ord('a'):
                print("\nroll LEFT")
                tello.send_command2(f"rc -{strength} 0 0 0")

            if cv2.waitKey(1) & 0xFF == ord('s'):
                print("\nthrottle DOWN")
                tello.send_command2(f"rc 0 0 -{strength} 0")

            if cv2.waitKey(1) & 0xFF == ord('d'):
                print("\nroll RIGHT")
                tello.send_command2(f"rc {strength} 0 0 0")

        elif mode == "pathing":
            # visualize

            target = targets[0]
            cv2.circle(frame, (target[0], target[1]), proximity, (255, 0, 0), 5)
            follow(tello, center[0], center[1], target[0], target[1])

            if (center[0] - target[0])**2 + (center[1] - target[1])**2 <= proximity**2:
                # this is close enough to this point, going to the next point
                print("GOAL")
                targets = targets[1:]

            if len(targets) == 0:
                # done traversal, ending
                mode = 'end'

        elif mode == "end":
            tello.send_command("land")
            break

        # Display the frame with detected objects
        cv2.imshow('Camera Feed', frame)

    # Release resources
    cap.release()
    cv2.destroyAllWindows()
    tello.send_command("land")      # preventing accidental break from main loop
        


