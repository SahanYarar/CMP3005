import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import random
from collections import defaultdict
import copy

##iki bug var graph cizmede bazen tekli kalıyor node ++ best partition ilk partitionsa kod hata veriyor onun için if lazım

def createGraph(nodes, edges):
    G = nx.complete_graph(nodes)

    if edges > G.number_of_edges():
        raise ValueError("The number of random edges must be less than or equal to the maximum possible edges.")

    edges_to_remove = G.number_of_edges() - edges
    random_edges = list(G.edges())
    random.shuffle(random_edges)

    for edge in random_edges[:edges_to_remove]:
        G.remove_edge(*edge)

    return G

def drawGraph(G):
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, font_weight='bold', node_color='lightblue', edge_color='gray') 
    plt.show()

def has_edges_for_all_nodes(G):
    return {node: G.degree(node) > 0 for node in G.nodes()}


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
    print("Choosen first partition",partitions)
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
 
def kernighan_lin(graph, sub_set,max_iterations):
    main_partition = initialPartition(graph, sub_set)
    main_cut_size = computeCutSize(graph, main_partition)
    dict_partitions = defaultdict(list)
    dict_partitions[main_cut_size].append(copy.deepcopy(main_partition))

    for iteration in range(max_iterations):
        for i in range(sub_set):
            for j in range(i + 1, sub_set):
                if i < len(main_partition) and j < len(main_partition):
                    main_partition[i], main_partition[j] = swap_elements(main_partition[i], main_partition[j])
                    gain = calculate_gain(graph, main_partition,main_cut_size, i, j)
                    if (gain > 0) :
                         new_cut_size = computeCutSize(graph, main_partition)
                         dict_partitions[new_cut_size].append(copy.deepcopy(main_partition))
   
    best_cut_size, best_partitions = min(dict_partitions.items())
    return best_partitions, best_cut_size, graph



def swap_elements(subset1, subset2):
    random_value1 = random.choice(subset1)
    random_value2 = random.choice(subset2)
    
    subset1[subset1.index(random_value1)] = random_value2
    subset2[subset2.index(random_value2)] = random_value1
    
    return subset1, subset2

## Sub set elemanlarına bak sonra diğer subset elemanlarıyla arasında edege varmı ona bak varsa bir arttır
def calculate_gain(graph, partition,current_cut_size, i, j):
    subset_i = partition[i]
    subset_j = partition[j]
    cut_edge = 0
    for vertex_i in subset_i:
        for vertex_j in subset_j:
            if graph.has_edge(vertex_i, vertex_j):
                cut_edge += 1
    gain = current_cut_size - cut_edge
    return gain


def run ():
    try:
        nodes = [1, 2, 3, 4,5,6,7]
        edges = 8
        G = createGraph(nodes, edges)
        edges_info = has_edges_for_all_nodes(G)
        for node, has_edge in edges_info.items():
            if not has_edge:
                print(f"Node {node} does not have edges. Regenerating the graph.")
                G = createGraph(nodes, edges)
                break

        sub_set = 2
        iterationNumber =2 ** len(nodes)
        result_partition, result_cut_size , graph1 = kernighan_lin(G, sub_set, iterationNumber)
        print("Best Partitions:", result_partition)
        print("Best Cut Size:", result_cut_size)
        drawGraph(G)
    except ValueError as ve:
        print({'message': f"Given edges can't be smaller than nodes :{ve}"}, 400)
        return {'message': f"Given edges can't be smaller than nodes :{ve}"}, 400

run()