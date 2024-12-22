import cv2
import numpy as np
from skimage.morphology import skeletonize, remove_small_objects
from collections import deque

IsDebug = False

def little_trace(img = None, imagePath = "ControlCourseLab\FinalProject\LaserTrackUCode\stage_2\Stage2_ref.png", visualize = False):
    """
    input: 
            img (optional)
            imagePath (default to Stage2_ref.png)
            visualize: boolean, (default to false)
    output: checkpoints, 2D array of pixel coord (y,x)

    if no image is given, use default as example
    """

    if type(img) == type(None):
        # Load the image
        img = cv2.imread(imagePath)

    # Extract red, green, and blue channels
    R = img[:,:,2]  # Red channel
    G = img[:,:,1]  # Green channel
    B = img[:,:,0]  # Blue channel

    # Create the red mask that isolate the path
    
    redMask = (R > 100) & (G < 100) & (B < 100) & (R - G > 60) & (R - B > 60)
    redMask = (redMask * 255).astype(np.uint8)
    if(IsDebug):
        cv2.imshow('Before Blur', redMask)
    redMask = cv2.blur(redMask, (25,25))
    if(IsDebug):
        cv2.imshow('After Blur', redMask)
        cv2.waitKey(10)

    # Remove small noise
    minSize = 30
    num_labels, labels = cv2.connectedComponents(redMask)
    sizes = [np.sum(labels == i) for i in range(num_labels)]
    for i in range(num_labels):
        if sizes[i] < minSize:
            redMask[labels == i] = 0

    # Find path of the redMask with skimage skeletonize
    redMaskSkeleton = skeletonize(redMask)

    # branch pruning
    cleanedSkeleton = remove_small_objects(redMaskSkeleton, min_size = 0.5) #2

    def trace_skeleton_with_branches(skeleton):
        # Get coordinates of the skeleton points
        skeleton_coords = np.argwhere(skeleton)

        # Initialize the list of ordered coordinates and a set for visited pixels
        ordered_coords = []
        visited = set()

        # Find the starting point (an endpoint or any point with fewer than 2 neighbors)
        max_point = (0, 0)
        for (y, x) in skeleton_coords:
            # print(f"current coord: y = {y}, x = {x}")
            if y >= max_point[0] and x >= max_point[1]:
                max_point = (y, x)
        start_point = max_point


        def bfs(y, x):
            # Initialize the queue with the starting point
            queue = deque([(y, x)])
            visited.add((y, x))
            ordered_coords.append((y, x))

            while queue:
                current = queue.popleft()
                cy, cx = current
                
                # Get neighbors
                neighbors = [
                    (cy-1, cx-1), (cy-1, cx), (cy-1, cx+1),
                    (cy, cx-1),               (cy, cx+1),
                    (cy+1, cx-1), (cy+1, cx), (cy+1, cx+1)
                ]
                neighbors = [
                    p for p in neighbors 
                    if 0 <= p[0] < skeleton.shape[0] and 0 <= p[1] < skeleton.shape[1]
                ]
                connected_neighbors = [
                    p for p in neighbors 
                    if skeleton[p[0], p[1]] == 1 and p not in visited
                ]

                # Add unvisited connected neighbors to the queue
                for neighbor in connected_neighbors:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        ordered_coords.append(neighbor)
                        queue.append(neighbor)

        # Call BFS from starting point
        bfs(start_point[0], start_point[1])

        return np.array(ordered_coords)

    ordered_skeleton = trace_skeleton_with_branches(cleanedSkeleton)

    # print(ordered_skeleton, len(ordered_skeleton))

    # def compute_cumulative_distances(coords):
    #     distances = np.sqrt(np.diff(coords[:, 0])**2 + np.diff(coords[:, 1])**2)
    #     cumulative_distances = np.concatenate(([0], np.cumsum(distances)))
    #     return cumulative_distances

    # # use cumulative distances to prevvent clumping points
    # cumulative_distances = compute_cumulative_distances(ordered_skeleton)

    # the number of checkpoints for drone
    num_points = 20

    # equally_spaced_distances = np.linspace(0, cumulative_distances[-1], num_points)

    # # interpolate to find the points corresponding to these equally spaced distances
    # equally_spaced_points = []
    # for dist in equally_spaced_distances:
    #     idx = np.searchsorted(cumulative_distances, dist)
    #     if idx < len(ordered_skeleton):
    #         equally_spaced_points.append(ordered_skeleton[idx])

    equally_spaced_points = [ordered_skeleton[int(point)][:] for point in np.linspace(0, len(ordered_skeleton)-1, num_points, dtype=int)]
    equally_spaced_points = equally_spaced_points[1:]########################################################
    equally_spaced_points = np.array(equally_spaced_points)

    # # Generate indices spaced evenly within valid range
    # indices = np.linspace(0, len(ordered_skeleton) - 1, num_points, dtype=int)

    # # Collect the points from ordered_skeleton using the indices
    # equally_spaced_points = [ordered_skeleton[idx] for idx in indices]

    # # Convert to a NumPy array
    # equally_spaced_points = np.array(equally_spaced_points)


    for points in equally_spaced_points:
        cv2.circle(img, (points[1],points[0]), 1, (255,0,0), -1)
    if(IsDebug):
        cv2.imshow('img', img)
        cv2.waitKey(10)

    if visualize == True:   
        # make a copy
        skeleton_with_points = (redMaskSkeleton * 255).astype(np.uint8)

        # draw checkpoints
        index = 3
        for (y, x) in equally_spaced_points:
            cv2.circle(skeleton_with_points, (x, y), index, (255, 0, 0), 3)
            index += 1

        # visualize
        cv2.imshow("Original", (redMaskSkeleton * 255).astype(np.uint8))
        cv2.imshow('Skeleton with checkpoints', skeleton_with_points)

    return equally_spaced_points

if __name__ == "__main__":
    little_trace(visualize=True)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
