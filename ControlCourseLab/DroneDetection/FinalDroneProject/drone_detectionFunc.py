import cv2

def detect_moving_objects(frame, fgbg, min_contour_area=500):
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

    # Optional: Perform some image processing (e.g., thresholding) to improve detection
    _, thresh = cv2.threshold(fg_mask, 200, 255, cv2.THRESH_BINARY)
    # Find contours in the thresholded mask
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    largest_contour = None
    max_area = 0

    # Iterate through all contours to find the largest one
    for contour in contours:
        if cv2.contourArea(contour) > min_contour_area:  # Filter small contours (noise)
            contour_area = cv2.contourArea(contour)
            if contour_area > max_area:
                max_area = contour_area
                largest_contour = contour
    center = [0,0]
    # If a largest contour is found, draw its bounding box and center
    if largest_contour is not None:
        # Get bounding box for the largest contour
        x, y, w, h = cv2.boundingRect(largest_contour)
        center[0]= x + w // 2
        center[1]= y + h // 2

        # Draw a rectangle around the largest moving object
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
        # Draw a circle at the center of the largest moving object
        cv2.circle(frame, (center[0], center[1]), 2, (0, 0, 255), 2)
        label = "MY Drone"
        cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255) , 2)



    return frame, center

# Example usage in a video processing loop
if __name__ == "__main__":
    # Initialize video capture (replace with your video file or camera)
    cap = cv2.VideoCapture('DroneVideo1.mp4')
    fgbg = cv2.createBackgroundSubtractorMOG2()

    while True:
        ret, frame = cap.read()
        if not ret:  # If no frame is read, exit the loop (end of video)
            break

        # Call the function to detect moving objects
        frame, center = detect_moving_objects(frame, fgbg)

        # Display the frame with detected objects
        cv2.imshow('Detected Objects', frame)

        # Break the loop if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()
