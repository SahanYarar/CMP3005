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
    while len(G) > 2 * k:
        matching = nx.maximal_matching(G)
        for u, v in matching:
            G = nx.contracted_nodes(G, u, v, self_loops=False)
    return G

def draw_graph(G, partition=None, title=None):
    pos = nx.spring_layout(G)

    if partition is not None:
        for i in range(len(partition)):
            node_color = ['lightblue', 'lightgreen', 'lightyellow'][i % 3]
            nx.draw_networkx_nodes(G, pos, nodelist=[node for node, part in partition.items() if part == i],
                                   node_color=node_color)
    else:
        nx.draw(G, pos, with_labels=True, font_weight='bold', node_color='lightblue', edge_color='gray')

    if title is not None:  
        plt.title(title)  

    plt.show()

def partition_coarsest_graph(G, k):
    if k == 1:
        return {node: 0 for node in G.nodes()}
    else:
        A, B = nx.algorithms.community.kernighan_lin_bisection(G)
        partition_A = partition_coarsest_graph(G.subgraph(A), k // 2)
        partition_B = partition_coarsest_graph(G.subgraph(B), k - k // 2)
        return {**partition_A, **partition_B}

def refine_level(G, partition, k):
    for node in G.nodes():
        for part in range(k):
            if part != partition[node]:
                new_partition = partition.copy()
                new_partition[node] = part
                if evaluate_partition(G, new_partition) < evaluate_partition(G, partition):
                    partition = new_partition
    return partition

def refine(G, partition, k, num_levels=2):
    for _ in range(num_levels):
        partition = refine_level(G, partition, k)
        G = nx.coarsen(G, partition)
    return partition

def evaluate_partition(G, partition):
    cut_size = sum(1 for u, v in G.edges() if partition[u] != partition[v])
    modularity = nx.algorithms.community.modularity(partition, G)
    balance = max(partition.values()) - min(partition.values())
    return cut_size, modularity, balance

def main():
    while True:
        try:
            nodes = int(input("Enter the number of nodes: "))
            edges = int(input("Enter the number of edges: "))
            k = int(input("Enter the number of partitions: "))

            if nodes <= 0 or edges <= 0 or k <= 0:
                raise ValueError("Invalid input: nodes, edges, and k must be positive integers.")

            break
        except ValueError as e:
            print(e)

    G = create_graph(nodes, edges)
    draw_graph(G, title="Original Graph")

    G_coarsened = coarsen(G.copy(), k)
    draw_graph(G_coarsened, title="Coarsened Graph")

    partition = partition_coarsest_graph(G_coarsened, k)
    partition = refine(G, partition, k)

    cut_size, modularity, balance = evaluate_partition(G, partition)
    print("Cut size:", cut_size)
    print("Modularity:", modularity)
    print("Balance:", balance)

    draw_graph(G, partition, title="Partitioned Graph")

if __name__ == "__main__":
    main()
