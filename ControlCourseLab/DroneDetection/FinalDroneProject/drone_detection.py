import cv2
import numpy as np

# Open the video file
video_capture = cv2.VideoCapture('DroneVideo1.mp4')  # Replace with your video file path

# Check if video was successfully opened
if not video_capture.isOpened():
    print("Error: Couldn't open video.")
    exit()

# Background subtractor (used for motion detection)
fgbg = cv2.createBackgroundSubtractorMOG2()

while True:
    # Read a frame from the video
    ret, frame = video_capture.read()

    if not ret:
        break  # If no frame is read, exit the loop (end of video)

    # Apply background subtraction to detect moving objects
    fg_mask = fgbg.apply(frame)

    # Optional: Perform some image processing (e.g., thresholding) to improve detection
    _, thresh = cv2.threshold(fg_mask, 200, 255, cv2.THRESH_BINARY)

    # Find contours in the thresholded mask
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw contours (representing moving objects)
    for contour in contours:
        if cv2.contourArea(contour) > 500:  # Filter small contours (noise)
            # Get bounding box for each contour
            x, y, w, h = cv2.boundingRect(contour)
            # Draw a rectangle around the moving object
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.circle(frame,(x + w//2, y + h//2),2,(0,0,255),2)

    # Display the original frame with detected moving objects
    cv2.imshow('Moving Objects Detection', frame)

    # Wait for key press to close the video (press 'q' to quit)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all OpenCV windows
video_capture.release()




cv2.destroyAllWindows()
