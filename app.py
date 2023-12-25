import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import random

##Ya gain hesaplamam yanlıs yada cut_size

def createGraph(nodes,edges):
    G = nx.Graph() 
    G.add_nodes_from(nodes)

    if edges < len(nodes)-1:
        raise ValueError("The number of random edges must be greater than the number of nodes.")
    
    for _ in range(edges):
        node1 = random.choice(nodes)    
        node2 = random.choice(nodes)

        while G.has_edge(node1, node2) or node1 == node2:
            node1 = random.choice(nodes)
            node2 = random.choice(nodes)
        G.add_edge(node1, node2)
    return G


def drawGraph(G):
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, font_weight='bold', node_color='lightblue', edge_color='gray') 
    plt.show()
    return


def initialPartition(graph, k):
    vertices = list(graph.nodes)
    np.random.shuffle(vertices)
    partitions = []
    for i in range(k):
        partition = []
        # Starting from i, incrementing by k, and stopping before reaching or exceeding len(vertices)
        for j in range(i, len(vertices), k):
            partition.append(vertices[j])
        partitions.append(partition)
        print("Partition",partition)
    
    return partitions


def computeCutSize(graph, partition):
    cut_size = 0
    for i in range(len(partition)):
        for j in range(i + 1, len(partition)):
            vertices_i = partition[i]
            vertices_j = partition[j]
            for vertex_i in vertices_i:
                for vertex_j in vertices_j:
                    if graph.has_edge(vertex_i, vertex_j):
                        cut_size += 1
    return cut_size


def kernighan_lin(graph, sub_set, max_iterations=3):
    best_partition = initialPartition(graph, sub_set)
    best_cut_size = computeCutSize(graph, best_partition)
    print("Initial Cut Size:", best_cut_size)
    for iteration in range(max_iterations):
        improvement = False
        for i in range(sub_set):
            for j in range(i + 1, sub_set):
                if i < len(best_partition) and j < len(best_partition):
                    gain = calculate_gain(graph, best_partition, i, j)

                    print(f"Iteration {iteration + 1}: Gain for swap i: {i} and j: {j}: gain:{gain}")
                    if gain > 0:
                        print(f"Iteration {iteration + 1}: Swap Performed with subsets {best_partition[i]} and {best_partition[j]}")
                        # Swap elements within the subsets
                        best_partition[i], best_partition[j] = swap_elements(best_partition[i], best_partition[j])
                        improvement = True
                        print("Updated Partition:", best_partition)
                        print("*********************************************")

        if not improvement:
            break
        best_cut_size = computeCutSize(graph, best_partition)
        print(f"Iteration {iteration + 1}: Current Cut Size: {best_cut_size}")
    return best_partition, best_cut_size ,graph


def swap_elements(subset1, subset2):
    element1 = random.choice(subset1)
    element2 = random.choice(subset2)
    
    subset1[subset1.index(element1)] = element2
    subset2[subset2.index(element2)] = element1
    
    return subset1, subset2


def calculate_gain(graph, partition, i, j):
    gain = 2 * (
        computeCutSize(graph, partition[:i] + [partition[j]]) +
        computeCutSize(graph, partition[:j] + [partition[i]])
    ) - (
        computeCutSize(graph, partition[:i] + [partition[j]]) +
        computeCutSize(graph, partition[:j] + [partition[i]])
    )
    return gain


def run ():
    try:
        nodes = [1, 2, 3, 4,5]
        edges = 8
        G = createGraph(nodes, edges)
        sub_set = 2
        result_partition, result_cut_size , graph1 = kernighan_lin(G, sub_set)
        print("Best Partition:", result_partition)
        print("Cut Size:", result_cut_size)
        drawGraph(G)
    except ValueError as ve:
        print({'message': f"Given edges can't be smaller than nodes :{ve}"}, 400)
        return {'message': f"Given edges can't be smaller than nodes :{ve}"}, 400

run()