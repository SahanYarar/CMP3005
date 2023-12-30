import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import random
from collections import defaultdict
import copy

##iki bug var graph cizmede bazen tekli kalıyor node ++ best partition ilk partitionsa kod hata veriyor onun için if lazım

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
    print("İlk setler",partitions)    
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

    print("İlk Cut Size:", main_cut_size)
    print("*********************************************")
    for iteration in range(max_iterations):
        for i in range(sub_set):
            for j in range(i + 1, sub_set):
                if i < len(main_partition) and j < len(main_partition):
                    print(f"Iteration {iteration + 1}: Main subset swap olacak {main_partition[i]} and {main_partition[j]} = {main_partition} " )
                    main_partition[i], main_partition[j] = swap_elements(main_partition[i], main_partition[j])
                    gain = calculate_gain(graph, main_partition,main_cut_size, i, j)
                    print("Swaped Partition:", main_partition)
                    print(f"Iteration {iteration + 1}: gain:{gain}")
                    print("*********************************************")
                    if (gain > 0) :
                         print(f"Iteration {iteration + 1}: Cut size updated because gain > 0 so graph improve eski best cut:{main_cut_size}")
                         new_cut_size = computeCutSize(graph, main_partition)
                         dict_partitions[new_cut_size].append(copy.deepcopy(main_partition))
                         print("Updated dict \n",dict_partitions)
                         print(f"best_cut:{new_cut_size}")
                         print(main_partition)
                         print("#####################################")
    for cut_dict, partitions_dict in dict_partitions.items():
            print(min(dict_partitions.keys()))
            print(dict_partitions.values())
            print(f'Cut size Dict: {cut_dict}, Partitions dict: {partitions_dict}')
    print("Son dict \n",dict_partitions)
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
        nodes = [1, 2, 3, 4,5]
        edges = 5
        G = createGraph(nodes, edges)
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