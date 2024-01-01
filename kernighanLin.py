import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import random
from collections import defaultdict
import copy


def createGraph(nodes, edges):
    G = nx.complete_graph(nodes)
    print("Maximum possible edges", G.number_of_edges())
    print("Given edge number", edges)
    # Check if the desired number of edges is greater than the maximum possible edges
    if edges > G.number_of_edges():
        print("The number of random edges must be less than or equal to the maximum possible edges.")
        return ValueError
    # Calculate the number of edges to remove to achieve the desired number
    edges_to_remove = G.number_of_edges() - edges

    random_edges = list(G.edges())
    random.shuffle(random_edges)

    # Remove edges from the graph until the desired number is reached
    for edge in random_edges[:edges_to_remove]:
        G.remove_edge(*edge)
    while not nx.is_connected(G):
        # Get a list of isolated (disconnected) nodes
        disconnected_nodes = list(nx.isolates(G))
        # Choose a random edge from the shuffled list
        new_edge = random.choice(random_edges)
        # Add the chosen edge to the graph
        G.add_edge(*new_edge)
        # Remove the chosen edge from the list of available edges
        random_edges.remove(new_edge)
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
 
def kernighan_lin(graph, sub_set, max_iterations):
    main_partition = initialPartition(graph, sub_set)
    main_cut_size = computeCutSize(graph, main_partition)
    print("First cut size:", main_cut_size)
    dict_partitions = defaultdict(list)
    dict_partitions[main_cut_size].append((copy.deepcopy(main_partition)))
    for iteration in range(max_iterations):
        for i in range(sub_set):
            for j in range(i + 1, sub_set):
                if i < len(main_partition) and j < len(main_partition):
                    main_partition[i], main_partition[j] = swap_elements(main_partition[i], main_partition[j])
                    gain = calculate_gain(graph, main_partition, main_cut_size, i, j)
                    if gain > 0:
                        new_cut_size = computeCutSize(graph, main_partition)
                        dict_partitions[new_cut_size].append((copy.deepcopy(main_partition)))
    best_cut_size = min(dict_partitions.keys())
    best_partitions = dict_partitions[best_cut_size]
    return best_partitions, best_cut_size, graph

def swap_elements(subset1, subset2):
    random_value1 = random.choice(subset1)
    random_value2 = random.choice(subset2)
    
    subset1[subset1.index(random_value1)] = random_value2
    subset2[subset2.index(random_value2)] = random_value1
    
    return subset1, subset2

## Sub set elemanlarına bak sonra diğer subset elemanlarıyla arasında edge varmı ona bak varsa bir arttır
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

def delete_duplicated_values(partition_list):
    unique_list = []
    seen_set = set()
    #Orjinal listin içindeki listi al sortla ve tuple olarak don
    for inner_list in partition_list:
        sorted_inner = sorted(inner_list, key=lambda x: x)
        tuple_inner = tuple(map(tuple, sorted_inner))
        #Eğer bos setin içinde bu tuple yoksa set içine at ve uniqe_liste ata
        if tuple_inner not in seen_set:
            seen_set.add(tuple_inner)
            unique_list.append(inner_list)
    return unique_list

def make_sorted_list(partition_list):
    result_list = []
    for sub_list in partition_list:
        new_sub_list = []
        for partition in sub_list:
            sorted_partition_list = sorted(partition)
            new_sub_list.append(sorted_partition_list)
        result_list.append(new_sub_list)
    return result_list
                    
def run ():
    try:
        nodes = [1, 2, 3, 4,5]
        edges = 7
        G = createGraph(nodes, edges)
        edges_info = has_edges_for_all_nodes(G)
        for node, has_edge in edges_info.items():
            if not has_edge:
                print(f"Node {node} does not have edges. Regenerating the graph.")
                G = createGraph(nodes, edges)
                break
        sub_set = 2
        iterationNumber = 100
        result_partition, result_cut_size , graph1 = kernighan_lin(G, sub_set, iterationNumber)
        sorted_list = make_sorted_list(result_partition)
        last_list = delete_duplicated_values(sorted_list)
        print("Best Partitions  ",last_list)  
        print("Best Cut Size:", result_cut_size)
        drawGraph(G)
    except ValueError as ve:
        return {'message': f"Given edges can't be smaller than nodes :{ve}"}, 400
run()