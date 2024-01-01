import networkx as nx
import matplotlib.pyplot as plt
import random

def create_graph(nodes, edges):
    G = nx.complete_graph(nodes)
    edges_to_remove = G.number_of_edges() - edges
    random_edges = list(G.edges())
    random.shuffle(random_edges)

    for edge in random_edges[:edges_to_remove]:
        G.remove_edge(*edge)

    while not nx.is_connected(G):
        disconnected_nodes = list(nx.isolates(G))
        new_edge = random.choice(random_edges)
        G.add_edge(*new_edge)
        random_edges.remove(new_edge)

    return G

def coarsen(G, k):
    # Coarsening algorithm (example: using a matching-based approach)
    while len(G) > 2 * k:  # Coarsen until desired graph size is reached
        matching = nx.maximal_matching(G)  # Find a maximal matching
        for u, v in matching:
            G = nx.contracted_nodes(G, u, v, self_loops=False)  # Contract edges in the matching
    return G

def partition_coarsest_graph(G, k):
    return recursive_bisection(G, k)

def refine(G, partition):
    # Refinement algorithm
    for node in G.nodes():
        # Consider moving node to a different partition
        for part in range(k):
            if part != partition[node]:
                new_partition = partition.copy()
                new_partition[node] = part
                if evaluate_partition(G, new_partition) < evaluate_partition(G, partition):
                    partition = new_partition
    return partition

def evaluate_partition(G, partition):
    # Function to evaluate the quality of a partition
    return sum(1 for u, v in G.edges() if partition[u] != partition[v])

def draw_graph(G, partition=None):
    pos = nx.spring_layout(G)

    if partition is not None:
        for i in range(len(partition)):
            node_color = ['lightblue', 'lightgreen', 'lightyellow'][i % 3]
            nx.draw_networkx_nodes(G, pos, nodelist=[node for node, part in partition.items() if part == i],
                                   node_color=node_color)
    else:
        nx.draw(G, pos, with_labels=True, font_weight='bold', node_color='lightblue', edge_color='gray')

    plt.show()

def main():
    nodes = int(input("Enter the number of nodes: "))
    edges = int(input("Enter the number of edges: "))
    k = int(input("Enter the number of partitions: "))

    G = create_graph(nodes, edges)
    draw_graph(G)

    G_coarsened = coarsen(G.copy())
    draw_graph(G_coarsened, title="Coarsened Graph")

    partition = partition_coarsest_graph(G_coarsened, k)
    partition = refine(G, partition)

    draw_graph(G, partition, title="Partitioned Graph")

if __name__ == "__main__":
    main()
