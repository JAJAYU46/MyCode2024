import cv2
import numpy as np
import random

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[] for _ in range(vertices)]

    def add_edge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)

    def greedy_coloring(self):
        result = [-1] * self.V
        result[0] = 0
        available = [False] * self.V

        for u in range(1, self.V):
            for v in self.graph[u]:
                if result[v] != -1:
                    available[result[v]] = True

            for color in range(self.V):
                if not available[color]:
                    break

            result[u] = color

            for v in self.graph[u]:
                if result[v] != -1:
                    available[result[v]] = False

        return result

    def visualize_coloring(self, colors, image_path):
        # Load the Taiwan map image
        original_image = cv2.imread(image_path)
        if original_image is None:
            print("Image not found!")
            return

        # Resize the image
        img_size = 600
        image = cv2.resize(original_image, (img_size, img_size))

        # Apply Canny edge detection
        edges = cv2.Canny(image, 100, 200)

        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Calculate centers of each block (region)
        centers = []
        for contour in contours:
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                centers.append((cx, cy))

        # Build the graph: connect centers that are close
        max_distance = 100  # Define a threshold for connection
        for i, center1 in enumerate(centers):
            for j, center2 in enumerate(centers):
                if i != j:
                    distance = np.linalg.norm(np.array(center1) - np.array(center2))
                    if distance < max_distance:
                        self.add_edge(i, j)

        # Define colors for the nodes
        color_map = [
            (255, 0, 0),  # Red
            (0, 255, 0),  # Green
            (0, 0, 255),  # Blue
            (255, 255, 0),  # Cyan
            (255, 0, 255),  # Magenta
            (0, 255, 255),  # Yellow
            (128, 0, 128),  # Purple
            (0, 128, 255),  # Orange
        ]

        # Draw edges
        for u in range(self.V):
            for v in self.graph[u]:
                if u < v:
                    cv2.line(image, centers[u], centers[v], (0, 255, 255), 2)

        # Draw nodes
        for i, center in enumerate(centers):
            color = color_map[colors[i] % len(color_map)]
            cv2.circle(image, center, 20, color, -1)

        # Show the final image
        cv2.imshow("Taiwan Graph Coloring", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

# Example usage
if __name__ == "__main__":
    # Load the Taiwan map
    taiwan_image_path = "taiwan_map.jpg"  # Replace with the path to your Taiwan map image

    # Create the graph
    graph = Graph(16)

    # Visualize graph coloring
    graph.visualize_coloring([], taiwan_image_path)
