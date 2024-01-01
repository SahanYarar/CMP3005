import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

def create_degree_matrix(graph):
    nodes = graph.number_of_nodes()
    degree_matrix = np.zeros((nodes, nodes))

    for i in range(nodes):
        degree_matrix[i, i] = sum(1 for _ in graph.neighbors(i))

    return degree_matrix

def create_adjacency_matrix(graph):
    nodes = graph.number_of_nodes()
    adjacency_matrix = np.zeros((nodes, nodes))

    for edge in graph.edges:
        adjacency_matrix[edge[0], edge[1]] = 1
        adjacency_matrix[edge[1], edge[0]] = 1

    return adjacency_matrix

def create_laplacian_matrix(graph):
    degree_matrix = create_degree_matrix(graph)
    adjacency_matrix = create_adjacency_matrix(graph)
    laplacian_matrix = degree_matrix - adjacency_matrix

    return laplacian_matrix

def spectral_partition(graph, num_clusters, num_iterations=1000):
    laplacian_matrix = create_laplacian_matrix(graph)

    eigenvalues, eigenvectors = np.linalg.eigh(laplacian_matrix)
    sorted_indices = np.argsort(eigenvalues)
    sorted_eigenvectors = eigenvectors[:, sorted_indices]
    cluster_matrix = sorted_eigenvectors[:, :num_clusters]

    for i in range(cluster_matrix.shape[1]):
        norm = np.linalg.norm(cluster_matrix[:, i])
        cluster_matrix[:, i] = cluster_matrix[:, i] / norm if norm != 0 else cluster_matrix[:, i]

    kmeans = KMeans(n_clusters=num_clusters, init='k-means++', random_state=100)
    labels = kmeans.fit_predict(cluster_matrix)

    partition = {node: label for node, label in zip(graph.nodes(), labels)}

    return partition

# Example usage:
G = nx.Graph()
G.add_edges_from([
    (0, 1), (0, 2), (0, 3),
    (1, 3), (1, 4),
    (2, 4), (2, 5),
    (3, 5), (3, 6),
    (4, 6), (4, 7),
    (5, 7), (5, 8),
    (6, 8),
    (0, 9), (0, 10),
    (1, 10), (1, 11),
    (2, 11), (2, 12),
    (3, 12), (3, 13),
    (4, 13), (4, 14),
    (5, 14), (5, 15),
    (6, 15), (6, 16),
    (7, 16), (7, 17),
    (8, 17), (8, 18),
    (9, 10), (10, 11),
    (9, 19), (9, 20),
    (10, 20), (10, 21),
    (11, 21), (11, 22),
    (12, 22), (12, 23),
    (13, 23), (13, 24),
    (14, 24), (14, 25),
    (15, 25), (15, 26),
    (16, 26), (16, 27),
    (17, 27), (17, 28),
    (18, 28), (18, 29),
    (19, 20), (20, 21),
    (21, 22), (22, 23),
    (23, 24), (24, 25),
    (25, 26), (26, 27),
    (27, 28), (28, 29),
    (19, 30), (19, 31),
    (20, 31), (20, 32),
    (21, 32), (21, 33),
    (22, 33), (22, 34),
    (23, 34), (23, 35),
    (24, 35), (24, 36),
    (25, 36), (25, 37),
    (26, 37), (26, 38),
    (27, 38), (27, 39),
    (28, 39), (28, 40),
    (29, 40), (29, 41),
    (30, 31), (31, 32),
    (32, 33), (33, 34),
    (34, 35), (35, 36),
    (36, 37), (37, 38),
    (38, 39), (39, 40),
    (40, 41),
    # Additional edges for a larger graph
    (30, 42), (31, 42),
    (32, 43), (33, 43),
    (34, 44), (35, 44),
    (36, 45), (37, 45),
    (38, 46), (39, 46),
    (40, 47), (41, 47),
    (42, 43), (43, 44),
    (44, 45), (45, 46),
    (46, 47)
])
degree_matrix = create_degree_matrix(G)
adjacency_matrix = create_adjacency_matrix(G)
laplacian_matrix = create_laplacian_matrix(G)

print("Degree Matrix:")
print(degree_matrix)
print("\nAdjacency Matrix:")
print(adjacency_matrix)
print("\nLaplacian Matrix:")
print(laplacian_matrix)

num_clusters = 3
partition = spectral_partition(G, num_clusters=num_clusters)
print("\nSpectral Partition:")
print(partition)

pos = nx.spring_layout(G)

colors = [partition[node] for node in G.nodes()]

for i in range(num_clusters):
    nodes_in_cluster = [node for node, label in partition.items() if label == i]
    nx.draw_networkx_nodes(G, pos, nodelist=nodes_in_cluster, node_color=[plt.cm.jet(i / float(num_clusters))], node_shape='o')

nx.draw_networkx_edges(G, pos, alpha=0.5)
node_labels = {node: str(node) for node in G.nodes()}
nx.draw_networkx_labels(G, pos, labels=node_labels)

plt.show()