import networkx as nx
import matplotlib.pyplot as plt
import random

vertices = []
edges = []
clusters = []
cluster_size = 2
initial_edges = []

def create_graph():
    global vertices, edges, initial_edges
    vertices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    edges = [[1, 3], [2, 4], [3, 5], [5, 6], [6, 7], [8, 9], [1, 2], [2, 3], [3, 4], [4, 5], [7, 10], [8, 10]]
    initial_edges = [[1, 3], [2, 4], [3, 5], [5, 6], [6, 7], [8, 9], [1, 2], [2, 3], [3, 4], [4, 5], [7, 10], [8, 10]]
    return vertices, edges, initial_edges

def create_clusters():
    global vertices, clusters
    for vertex in vertices:
        clusters.append([vertex])

def merge_two_clusters():
    global clusters, edges
    edge = get_random_edge_from_edge_list()
    vertex1, vertex2 = edge[0], edge[1]

    # Find the indices of vertices in clusters
    index1, index2 = -1, -1
    for i, cluster in enumerate(clusters):
        if vertex1 in cluster:
            index1 = i
        if vertex2 in cluster:
            index2 = i

    # Merge vertices and remove the unused one
    if index1 != -1 and index2 != -1 and index1 != index2:
        merged_list = clusters[index1] + clusters[index2]
        clusters[index1] = merged_list
        del clusters[index2]
        edges.remove(edge)

def get_random_edge_from_edge_list():
    global edges
    if edges:
        return random.choice(edges)
    else:
        return None

# Create the graph
create_graph()

# Create the list of vertices
create_clusters()

# Print the initial state
print("Initial Clusters:", clusters)
print("Initial Edges:", edges)

while len(clusters) > cluster_size:
    merge_two_clusters()
    print("Clusters After Merging:", clusters)
    print("Edges After Merging:", edges)
    print("Cluster Size:", len(clusters))

for edge in edges:
    edge1 = edge[0]
    edge2 = edge[1]

    # Check if edge1 and edge2 are in the same cluster
    same_cluster = False
    for cluster in clusters:
        if edge1 in cluster and edge2 in cluster:
            same_cluster = True
            break

    # If they are in the same cluster, remove the edge
    if same_cluster:
        edges.remove(edge)


final_cut_size = len(edges)
final_cutted_edges = [edge for edge in initial_edges if edge not in edges]

print("\nFinal Cut Size:", final_cut_size)
print("Final Cutted Edges:", final_cutted_edges)

# Draw the final graph
G = nx.Graph()
G.add_nodes_from(vertices)
G.add_edges_from(final_cutted_edges)
print(len(initial_edges)-len(final_cutted_edges))
# Visualization
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue', font_size=10, edge_color='gray', linewidths=1, arrowsize=10)
plt.title("Graph Visualization")
plt.show()
