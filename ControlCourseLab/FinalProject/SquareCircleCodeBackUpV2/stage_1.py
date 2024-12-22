import cv2
import numpy as np
# import drone_detectionFunc


def circle_pathing(photo = None, imagePath="Stage1_circle_ref.png", visualize=False):
    """
    Function to find the 12 points on a circle from an image
    
    Parameters:
        photo (MatLike): the image to detect circles from, if none is given then uses imagePath instead
        imagePath (str): Path to the image. Default is "Stage1_ref.png"
    
    Returns:
        checkpoints (numpy.ndarray): An array containing the 12 intermediate points for circles
    """
    if type(photo) == type(None):
        # Read the image instead
        img = cv2.imread(imagePath)
    else:
        img = photo
    
    # Get the width of the image
    height, width, _ = img.shape
    
    # Split the image into color channels
    B, G, R = cv2.split(img)
    
    # Find red region mask as boolean, then saturate as grayscale image for later
    redImg = (((R > 100) & (G < 80) & (B < 80)) * 255).astype(np.uint8)
    
    # Remove noise by applying a morphological open operation
    # minSize = 30
    # redImg = cv2.morphologyEx(redImg, cv2.MORPH_OPEN, np.ones((minSize, minSize), np.uint8))
    
    # Find contours for the red mask (for circles)
    contours, _ = cv2.findContours(redImg, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    # Sort contours by area and select the second largest circle
    contours_sorted_by_area = sorted(contours, key=cv2.contourArea, reverse=True)
    circleBoundary = contours_sorted_by_area[0]
    
    # Create checkpoints for circles by interpolating along the boundary
    checkpointCount = 13
    intermediate = np.round(np.linspace(0, len(circleBoundary) - 1, checkpointCount)).astype(int)
    cir_checkpoints = circleBoundary[intermediate[1:]][:,0,:]

    cir_checkpoints = np.roll(cir_checkpoints,-3,axis=0)
    cir_checkpoints = cir_checkpoints[::-1]
    
    if visualize == True:
        for index, point in enumerate(cir_checkpoints):
            # Draw each point as a small circle (5 pixels radius)
            cv2.circle(img, (point[0], point[1]), (index+3), (255, 0, 0), -1)  # Red color for the points

        # Display the image with the points
        cv2.imshow("Image with Points", img)
    
    return cir_checkpoints

def square_pathing(photo = None, imagePath="Stage1_square_ref.png", visualize = False):
    """
    Function to find the corners of a square in a given image
    
    Parameters:
        imagePath (str): Path to the image. Default is "Stage1_ref.png"
    
    Returns:
        checkpoints (numpy.ndarray): An array containing the intermediate checkpoints for squares
    """

    if type(photo) == type(None):
        # Read the image instead
        img = cv2.imread(imagePath)
    else:
        img = photo
    
    # Get the width of the image
    height, width, _ = img.shape
    
    # Split the image into color channels
    B, G, R = cv2.split(img)
    
    # Create a red mask: Red region with R > 100, G < 70, B < 70
    redImg = (((R > 100) & (G < 80) & (B < 80)) * 255).astype(np.uint8)
    
    # Find contours for the left half of the image (for squares)
    # left_half = redImg[:, :width // 2]
    contours, _ = cv2.findContours(redImg, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    # return 0

    # Sort contours by size and select the second largest (square)
    contours_sorted_by_size = sorted(contours, key=cv2.contourArea, reverse=True)
    squareBoundary = contours_sorted_by_size[0]

    # Create checkpoints for squares by interpolating along the boundary
    squ_checkpoints = np.array(cv2.approxPolyDP(squareBoundary, epsilon=3, closed=True))
    squ_checkpoints = squ_checkpoints[:, 0]  # Flatten the contour points

    if visualize == True:
        for index, point in enumerate(squ_checkpoints):
            # Draw each point as a small circle (5 pixels radius)
            cv2.circle(redImg, (point[0], point[1]), 3*(index+2), (0, 0, 255), -1)  # Red color for the points

        # Display the image with the points
        cv2.imshow("Image with Points", redImg)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
    
    return squ_checkpoints

def croix_pathing(imagePath="Stage1_square_ref.png", visualize = False):
    """
    Function to find the black cross
    
    Parameters:
        imagePath (str): Path to the image. Default is "Stage1_square_ref.png"
    
    Returns:
        sqr_croix (list): the center point of the biggest black thing (should be the cross)
    """
    # Read the image
    img = cv2.imread(imagePath)
    
    # Split the image into color channels
    B, G, R = cv2.split(img)
    
    # Create a BLACK mask: Red region with R < 30, G < 30, B < 30
    redImg = (((R < 30) & (G < 30) & (B < 30)) * 255).astype(np.uint8)
    
    # Find contours for the left half of the image (for squares)
    # left_half = redImg[:, :width // 2]
    contours, _ = cv2.findContours(redImg, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    # Sort contours by size and select the second largest (square)
    contours_sorted_by_size = sorted(contours, key=cv2.contourArea, reverse=True)
    croix = contours_sorted_by_size[0]
    
    # Create checkpoints for squares by interpolating along the boundary
    squ_croix=[]
        # Get bounding box for the largest contour
    x, y, w, h = cv2.boundingRect(croix)
    squ_croix[0]= x + w // 2
    squ_croix[1]= y + h // 2
    # preCenter = center


    
    return squ_croix



if __name__ == "__main__":
    # Example usage:
    # checkpoints = stage1_circle_pathing("Stage1_circle_ref.png", visualize=True)
    camera = cv2.VideoCapture(1)
    while True:
        ret, frame = camera.read()
        cv2.imshow("camera", frame)
        square_pathing(frame, visualize=True)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # print(checkpoints)
    ###以下是我在1214做的事
    #多寫了追蹤中心十字
    #試著寫了以下這段



