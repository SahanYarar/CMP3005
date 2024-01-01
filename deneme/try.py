import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import random

def create_and_draw_graph(nodes, num_random_edges):
    G = create_graph(nodes, num_random_edges)
    pos = draw_graph(G)
    return G, pos

def create_graph(nodes, num_random_edges):
    G = nx.Graph()
    G.add_nodes_from(nodes)

    for node in nodes:
        connect_nodes_randomly(G, nodes, node)

    add_random_edges(G, nodes, num_random_edges)
    return G

def draw_graph(G):
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, font_weight='bold', node_color='lightblue', edge_color='gray')
    plt.pause(0.1)
    return pos

def connect_nodes_randomly(G, nodes, node):
    other_node = random.choice(nodes)
    while other_node == node or G.has_edge(node, other_node):
        other_node = random.choice(nodes)
    G.add_edge(node, other_node, capacity=1)

def add_random_edges(G, nodes, num_random_edges):
    while G.number_of_edges() < num_random_edges:
        node1, node2 = random.sample(nodes, 2)
        while G.has_edge(node1, node2):
            node1, node2 = random.sample(nodes, 2)
        G.add_edge(node1, node2, capacity=1)

def calculate_cut_size(G, partition):
    cut_size = sum(G[node][neighbor]['capacity'] for node in partition for neighbor in G.neighbors(node) if partition[neighbor] != partition[node])
    return cut_size

def find_maximum_cut(G, source, target):
    _, partition_maximum = nx.maximum_flow(G, source, target)
    result_partition_maximum = [list(set(partition_maximum)), list(set(G.nodes) - set(partition_maximum))]
    result_cut_size_maximum = calculate_cut_size(G, partition_maximum)
    return result_partition_maximum, result_cut_size_maximum

def find_minimum_cut(G, source, target):
    cut_value_minimum, partition_minimum = nx.minimum_cut(G, source, target)
    result_partition_minimum = [list(partition_minimum[0]), list(partition_minimum[1])]
    result_cut_size_minimum = cut_value_minimum
    return result_partition_minimum, result_cut_size_minimum

def run():
    try:
        nodes = [1, 2, 3, 4, 5,6]
        num_random_edges = 7
        source, target = 1, 2

        plt.ion()

        G, pos = create_and_draw_graph(nodes, num_random_edges)

        result_partition_maximum, result_cut_size_maximum = find_maximum_cut(G, source, target)
        result_partition_minimum, result_cut_size_minimum = find_minimum_cut(G, source, target)

        print("Best Partition maximum:", result_partition_maximum)
        print("Cut Size maximum: ", result_cut_size_maximum)
        print("Best Partition minimum:", result_partition_minimum)
        print("Cut Size minimum: ", result_cut_size_minimum)

        plt.ioff()

        plt.show()

    except ValueError as ve:
        print({'message': f"Given edges can't be smaller than nodes :{ve}"}, 400)
        return {'message': f"Given edges can't be smaller than nodes :{ve}"}, 400

run()
