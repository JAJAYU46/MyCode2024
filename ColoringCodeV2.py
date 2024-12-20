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
        # Initialize all vertices as unassigned
        result = [-1] * self.V  
        
        # Assign the first color to the first vertex
        result[0] = 0

        # A temporary array to store the colors of the adjacent vertices
        available = [False] * self.V

        # Assign colors to remaining V-1 vertices
        for u in range(1, self.V):
            # Mark colors of adjacent vertices as unavailable
            for v in self.graph[u]:
                if result[v] != -1:
                    available[result[v]] = True

            # Find the first available color
            for color in range(self.V):
                if not available[color]:
                    break

            result[u] = color

            # Reset the values back to false for the next iteration
            for v in self.graph[u]:
                if result[v] != -1:
                    available[result[v]] = False

        # Print the result
        for u in range(self.V):
            print(f"Vertex {u} --> Color {result[u]}")

        return result

    def visualize_coloring(self, colors):
        # img = cv2.imread(image_path)
        # if img is None:
        #     print("Error: Image not found!")
        #     return
        # # Create a blank canvas
        
        img_size = 800
        # img = cv2.resize(img, (int(img.shape[1]*0.5), int(img.shape[0]*0.5)))
        # img = cv2.resize(img, (400, 600))
        
        # canvas = np.ones((img_size, img_size, 3), dtype=np.uint8) * 255
        
        img = np.ones((img_size, img_size, 3), dtype=np.uint8) * 255
        
        # # Generate random positions for each node
        # positions = {i: (random.randint(100, img_size - 100), random.randint(100, img_size - 100)) for i in range(self.V)}
        # Pre-defined positions for counties (x, y coordinates on the resized map)
        # These values should be calculated based on the resized image.
        county_positions = {
            0: (530, 85),   # Taipei
            1: (495, 100),  # New Taipei
            2: (360, 250),  # Taichung
            3: (440, 570),  # Kaohsiung
            4: (400, 520),  # Tainan
            5: (460, 130),  # Hsinchu
            6: (550, 65),   # Keelung
            7: (470, 170),  # Taoyuan
            8: (550, 210),  # Yilan
            9: (540, 350),  # Hualien
            10: (510, 480), # Taitung
            11: (430, 610), # Pingtung
            12: (390, 420), # Chiayi
            13: (420, 200), # Miaoli
            14: (410, 310), # Nantou
            15: (360, 400), # Changhua
        }

        # Use these positions instead of random ones
        positions = {i: county_positions[i] for i in range(self.V)}

        # Define colors for the nodes
        color_map = [
            (150, 100, 0),  # Red
            (0, 255, 0),  # Green
            (0, 0, 255),  # Blue
            (255, 255, 0),  # Cyan
            (255, 0, 255),  # Magenta
            (0, 255, 255),  # Yellow
            (128, 0, 128),  # Purple
            (0, 128, 255),  # Orange
        ]
        county_names = [
            "Taipei", "New Taipei", "Taichung", "Kaohsiung", "Tainan", 
            "Hsinchu", "Keelung", "Taoyuan", "Yilan", "Hualien", 
            "Taitung", "Pingtung", "Chiayi", "Miaoli", "Nantou", "Chianhua"
        ]

        # Draw edges
        
        for u in range(self.V):
            for v in self.graph[u]:
                if u < v:  # Avoid drawing the same edge twice
                    cv2.line(img, positions[u], positions[v], (0, 0, 0), 2)

        # Draw nodes
        for node in range(self.V):
            county_name = county_names[node]
            pos = positions[node]
            color = color_map[colors[node]]
            cv2.circle(img, pos, 20, color, -1)
            cv2.putText(img, str(county_name), (pos[0] - 10, pos[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        # Show the image
        cv2.imshow("Graph Coloring", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

# Example usage:
if __name__ == "__main__":
    # Create a graph with 5 vertices
    graph = Graph(16)
    graph.add_edge(0, 1)
    graph.add_edge(1, 6)
    graph.add_edge(1, 7)
    graph.add_edge(7, 5)
    graph.add_edge(7, 8)
    graph.add_edge(5, 8)
    graph.add_edge(5, 13)
    graph.add_edge(5, 10)
    graph.add_edge(13, 10)
    graph.add_edge(10, 14)
    graph.add_edge(10, 15)
    graph.add_edge(15, 9)
    graph.add_edge(15, 14)
    graph.add_edge(15, 12)
    graph.add_edge(14, 12)
    graph.add_edge(4, 12)
    graph.add_edge(4, 3)
    graph.add_edge(3, 12)
    graph.add_edge(3, 11)
    graph.add_edge(10, 11)
    graph.add_edge(10, 3)
    graph.add_edge(10, 9)
    graph.add_edge(9, 14)
    graph.add_edge(9, 8)
    graph.add_edge(9, 2)
    graph.add_edge(8, 2)
    graph.add_edge(2, 14)
    # #         county_positions = {
    #         0: (300, 50),   # Taipei
    #         1: (280, 80),   # New Taipei
    #         2: (200, 300),  # Taichung
    #         3: (400, 500),  # Kaohsiung
    #         4: (350, 450),  # Tainan
    #         5: (250, 100),  # Hsinchu
    #         6: (320, 70),   # Keelung
    #         7: (290, 150),  # Taoyuan
    #         8: (340, 250),  # Yilan
    #         9: (350, 350),  # Hualien
    #         10: (400, 400), # Taitung
    #         11: (450, 500), # Pingtung
    #         12: (300, 400), # Chiayi
    #         13: (200, 150), # Miaoli
    #         14: (250, 250), # Nantou
    #         15: (200, 400), # chianhua
    #     }

    print("Coloring of vertices:")
    colors = graph.greedy_coloring()
    graph.visualize_coloring(colors)
