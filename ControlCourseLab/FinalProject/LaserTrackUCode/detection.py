
import cv2
from LaserDetect import getLaserCoordinate, filterColor_getMask

def detect_moving_objects(preCenter, frame, fgbg: cv2.BackgroundSubtractorMOG2, min_contour_area=500, visualize = False):
    """
    Detect moving objects in a video frame using background subtraction and contour detection.

    Parameters:
    - frame: The current frame from the video feed.
    - fgbg: The background subtractor object (e.g., cv2.createBackgroundSubtractorMOG2()).
    - min_contour_area: The minimum area of a contour to be considered as a moving object (default is 500).

    Returns:
    - frame: The frame with rectangles and circles drawn around detected moving objects.
    """


    # Apply background subtraction to detect moving objects
    fg_mask = fgbg.apply(frame)

    #拿到綠色的遮罩 把他在今過綠色的mask讓綠色過不去, 雷射就不會被當成drone了
    frameHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    filteredFrame_green, filtered_Mask_green= filterColor_getMask(frame, frameHSV, 43,93,0, 255, 135,255)#59, 99, 9, 124, 155, 255) #此為更寬限的綠色，因為之後要反向，才會成更嚴格的反向maskh_min, h_max, s_min, s_max, v_min, v_max = 
    #用綠色的反向mask 再做一次，留下非綠色的部分
    # Invert the mask
    inverted_Mask_green = cv2.bitwise_not(filtered_Mask_green)
    fg_mask2 = cv2.bitwise_and(fg_mask, fg_mask, mask=inverted_Mask_green)



    # Optional: Perform some image processing (e.g., thresholding) to improve detection
    _, thresh = cv2.threshold(fg_mask2, 200, 255, cv2.THRESH_BINARY)
    _, thresh_noGreenMask = cv2.threshold(fg_mask, 200, 255, cv2.THRESH_BINARY)
    # Find contours in the thresholded mask
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    largest_contour = None
    max_area = 0

    # Iterate through all contours to find the largest one
    for contour in contours:
        # x, y, w, h = cv2.boundingRect(contour)
        # cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)

        # if cv2.contourArea(contour) > min_contour_area:  # Filter small contours (noise)
        contour_area = cv2.contourArea(contour)
        if contour_area > max_area:
            max_area = contour_area
            largest_contour = contour

    center = preCenter
    # If a largest contour is found, draw its bounding box and center
    if largest_contour is not None:
        # Get bounding box for the largest contour
        x, y, w, h = cv2.boundingRect(largest_contour)
        center[0]= x + w // 2
        center[1]= y + h // 2
        # preCenter = center
        
        # Draw a rectangle around the largest moving object
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
        label = "MY Drone"
        cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255) , 2)

    cv2.circle(frame, (center[0], center[1]), 2, (0, 0, 255), 2)
        
    
    if visualize == True:
        cv2.imshow("motion detection", thresh)
        cv2.imshow("motion detection_noGreenMask", thresh_noGreenMask)
        
    


    return frame, center