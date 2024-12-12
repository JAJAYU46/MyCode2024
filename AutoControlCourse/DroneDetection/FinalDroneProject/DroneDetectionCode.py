import cv2
import numpy as np
# from imutils.video import VideoStream
import time
import pickle
import scipy.io

mat = scipy.io.loadmat('Detector.mat')

detector = mat['mat']
# # Load the pre-trained ACF detector
# with open('Detector.pkl', 'rb') as f:
#     detector = pickle.load(f)  # Assuming the detector is serialized in pickle format

# Streaming Flag
StreamingFlag = 1  # 0: for webcam, 1: for video

# Initialize webcam or video
if StreamingFlag == 0:
    mycam = cv2.VideoCapture(0)  # Initialize webcam
else:
    vidReader = cv2.VideoCapture('DroneVideo1.mp4')  # VideoReader for the video file

# Start Object Detection
ret, I = mycam.read() if StreamingFlag == 0 else vidReader.read()  # Capture first frame

previous_bboxes = []
previous_scores = []
imageHeight, imageWidth, _ = I.shape
centreX = imageWidth // 2
centreY = imageHeight // 2
dobra = False

def get_drone_center(I, previous_bboxes, previous_scores, detector):
    bboxes, scores = detector.detect(I)  # Assuming detector has a method .detect() similar to MATLAB's 'detect'
    NowDroneCenter = [0, 0]

    if len(scores) > 0 and len(bboxes) > 0:
        # Select strongest detection
        idx = np.argmax(scores)
        # Calculate and print the center of the bounding box
        centerX = bboxes[idx][0] + bboxes[idx][2] // 2
        centerY = bboxes[idx][1] + bboxes[idx][3] // 2

        NowDroneCenter = [centerX, centerY]
        # Draw rectangle and center point on the image
        cv2.rectangle(I, (bboxes[idx][0], bboxes[idx][1]), 
                      (bboxes[idx][0] + bboxes[idx][2], bboxes[idx][1] + bboxes[idx][3]), 
                      (0, 255, 0), 2)
        cv2.circle(I, (int(centerX), int(centerY)), 5, (0, 0, 255), -1)
        
        previous_scores = scores
        previous_bboxes = bboxes

    elif len(previous_scores) > 0:
        # Use previous data if the current frame doesn't have detections
        idx = np.argmax(previous_scores)
        centerX = previous_bboxes[0][0] + previous_bboxes[0][2] // 2
        centerY = previous_bboxes[0][1] + previous_bboxes[0][3] // 2
        NowDroneCenter = [centerX, centerY]
        # Draw previous rectangle and center point
        cv2.rectangle(I, (previous_bboxes[0][0], previous_bboxes[0][1]), 
                      (previous_bboxes[0][0] + previous_bboxes[0][2], previous_bboxes[0][1] + previous_bboxes[0][3]), 
                      (0, 255, 0), 2)
        cv2.circle(I, (int(centerX), int(centerY)), 5, (0, 0, 255), -1)

    return I, previous_bboxes, previous_scores, NowDroneCenter

# Main loop
try:
    while not dobra:
        ret, I = mycam.read() if StreamingFlag == 0 else vidReader.read()  # Capture frame

        # Detect Drone center
        I, previous_bboxes, previous_scores, NowDroneCenter = get_drone_center(I, previous_bboxes, previous_scores, detector)

        # Show the image with annotations
        cv2.imshow('Drone Detection', I)

        # Check for exit condition
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except Exception as e:
    print(f"Error occurred: {str(e)}")

finally:
    # Cleanup resources
    print('Cleaning up...')
    if StreamingFlag == 0:
        mycam.release()
    else:
        vidReader.release()
    cv2.destroyAllWindows()
    print('Cleanup complete.')
