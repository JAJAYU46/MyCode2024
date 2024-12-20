# Python Program of graph coloring using greedy algorithm
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

# Example usage:
if __name__ == "__main__":
    # Create a graph with 5 vertices
    graph = Graph(5)
    graph.add_edge(0, 1)
    graph.add_edge(0, 2)
    graph.add_edge(1, 2)
    graph.add_edge(1, 3)
    graph.add_edge(2, 3)
    graph.add_edge(3, 4)

    print("Coloring of vertices:")
    graph.greedy_coloring()