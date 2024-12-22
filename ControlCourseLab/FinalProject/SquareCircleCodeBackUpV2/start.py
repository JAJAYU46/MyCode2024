import cv2

import stage_1
from tello import Tello
from detection import detect_moving_objects
import time

def follow(tello: Tello, currentX: int, currentY: int, targetX: int, targetY: int):
    """
    sending rc command to tello based on how far current and target coord
    x is pixels right from upperleft
    y is pixels down from upperleft
    """
    proportion = 0.40           # 35 power per 100 pixels difference
    proportion_ver = 2   
    roll = proportion * (targetX - currentX)                    # pos: right
    throttle = proportion_ver * (currentY - targetY)            # pos: up



    if abs(roll) <= 40 and abs(throttle) <= 10:
        roll *= -2.5
    
    roll = min(roll, 80)
    roll = max(-80, roll)

    throttle = min(throttle, 50)
    throttle = max(-50, throttle)

    #if abs(roll)>40 & abs(throttle)<=10:
    #    throttle=-throttle

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
    time.sleep(2)
    
    preCenter = [0,0]
    center = [0,0]
    mode = 'pathing'
    proximity = 10  # 20 pixels is close enough
    index = 0

    flag = True  #True: for square
    if flag == True:
        targets = stage_1.square_pathing(frame, visualize = True)
    else:
        targets = stage_1.circle_pathing(frame, visualize = True)
    
    while True:
        ret, frame = cap.read()
        if not ret:  # If no frame is read, exit the loop (end of video)
            break

        # Call the function to detect moving objects
        preCenter = center
        frame, center = detect_moving_objects(preCenter, frame, fgbg, visualize = True)

        # Break the loop if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            tello.send_command("land")
            break

        if cv2.waitKey(1) & 0xFF == ord('p'):   #按下p後開始跟隨循跡
            mode = 'pathing'

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

            target = targets[index % len(targets)]
            cv2.circle(frame, (target[0], target[1]), proximity, (255, 0, 0), 5)
            follow(tello, center[0], center[1], target[0], target[1])

            if (center[0] - target[0])**2 + (center[1] - target[1])**2 <= proximity**2:
                # this is close enough to this point, going to the next point
                print("GOAL")
                index += 1

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
        


