import cv2

import stage_1
from tello import Tello
from detection import detect_moving_objects

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

    now_mode_flag = 1 # 0: 跑square mode 1: 跑circle mode
    if(now_mode_flag==0):
        targets = stage_1.square_pathing(frame, visualize = False)
    else: 
        targets = stage_1.circle_pathing(frame, visualize = False)
    
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
        


