import cv2
import numpy as np
from skimage.morphology import skeletonize, remove_small_objects

from collections import deque

# Load the image
imagePath = "ControlCourseLab\FinalProject\LaserTrackUCode\stage_2\Stage2_ref.png"

img = cv2.imread(imagePath)

# Extract red, green, and blue channels
R = img[:,:,2]  # Red channel (in OpenCV, channels are BGR)
G = img[:,:,1]  # Green channel
B = img[:,:,0]  # Blue channel

# Create the red mask based on conditions similar to MATLAB's
redMask = (R > 100) & (G < 80) & (B < 80) & (R - G > 60) & (R - B > 60)

# Create a blue mask (if needed in your analysis)
blueMask = (B > 100) & (B - R > 50) & (R < 130)

# Remove small noise (equivalent to bwareaopen in MATLAB)
minSize = 30
num_labels, labels = cv2.connectedComponents(redMask.astype(np.uint8))
sizes = [np.sum(labels == i) for i in range(num_labels)]
for i in range(num_labels):
    if sizes[i] < minSize:
        redMask[labels == i] = 0

# Skeletonize the redMask using skimage's skeletonize function
# Note: skeletonize works on boolean images (True/False), so we need to convert the mask.
redMaskSkeleton = skeletonize(redMask)

cleanedSkeleton = remove_small_objects(redMaskSkeleton, min_size=1)


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

    # Start DFS from the starting point
    def dfs(y, x):
        # Add the current point to the ordered list and mark it as visited
        if (y, x) not in visited:
            # print(f"visit ({y}, {x})")
            ordered_coords.append((y, x))
            visited.add((y, x))

            # Get neighbors and explore unvisited neighbors
            neighbors = [(y-1, x-1), (y-1, x), (y-1, x+1), (y, x-1), (y, x+1), (y+1, x-1), (y+1, x), (y+1, x+1)]
            neighbors = [p for p in neighbors if 0 <= p[0] < skeleton.shape[0] and 0 <= p[1] < skeleton.shape[1]]
            connected_neighbors = [p for p in neighbors if skeleton[p[0], p[1]] == 1]

            for neighbor in connected_neighbors:
                if neighbor not in visited:
                    dfs(neighbor[0], neighbor[1])
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

        # Call BFS starting from the chosen endpoint
    bfs(start_point[0], start_point[1])

    
    # Call DFS starting from the chosen endpoint
    #dfs(start_point[0], start_point[1])

    return np.array(ordered_coords)


ordered_skeleton = trace_skeleton_with_branches(cleanedSkeleton)

print(ordered_skeleton, len(ordered_skeleton))



def compute_cumulative_distances(coords):
    distances = np.sqrt(np.diff(coords[:, 0])**2 + np.diff(coords[:, 1])**2)
    cumulative_distances = np.concatenate(([0], np.cumsum(distances)))
    return cumulative_distances

# Compute cumulative distances
cumulative_distances = compute_cumulative_distances(ordered_skeleton)


# Define the number of equally spaced points you want
num_points = 20

# Generate equally spaced distances along the path
equally_spaced_distances = np.linspace(0, cumulative_distances[-1], num_points)

# Interpolate to find the points corresponding to these equally spaced distances
equally_spaced_points = []
for dist in equally_spaced_distances:
    idx = np.searchsorted(cumulative_distances, dist)
    if idx < len(ordered_skeleton):
        equally_spaced_points.append(ordered_skeleton[idx])

equally_spaced_points = np.array(equally_spaced_points)


# Visualize the result
skeleton_with_points = (cleanedSkeleton.copy() * 255).astype(np.uint8)

# Draw points from ordered_skeleton
index = 3
for (y, x) in equally_spaced_points:
    cv2.circle(skeleton_with_points, (x, y), index, (255, 0, 0), 3)
    index += 1

# Display using OpenCV
cv2.imshow("Original", (cleanedSkeleton * 255).astype(np.uint8))
cv2.imshow('Skeleton with Branches Traced', skeleton_with_points)
cv2.waitKey(0)
cv2.destroyAllWindows()


# # Display the original red mask and the skeletonized image
# plt.figure(figsize=(10, 5))
# plt.subplot(1, 2, 1)
# plt.imshow(redMask, cmap='gray')
# plt.title('Original Red Mask')
# plt.subplot(1, 2, 2)
# plt.imshow(cleanedSkeleton, cmap='gray')
# plt.title('Skeletonized Red Mask')
# plt.show()
