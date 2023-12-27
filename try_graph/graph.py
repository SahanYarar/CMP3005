from collections import defaultdict
import matplotlib.pyplot as plt
import networkx as nx

def createGraph(edges_dict):
    G = nx.Graph() 
    print(edges_dict.items())
    for node,edges in edges_dict.items():
        G.add_node(node)
        for edge in edges:
            G.add_edge(node ,edge)
    initialPartition(edges_dict=edges_dict,sub_set_number=4)
    pos = drawGraph(G)
    return G, pos


def drawGraph(G):
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, font_weight='bold', node_color='lightblue', edge_color='gray')
    plt.pause(110)
    return pos

## TODO: Sub setlere bölme halloldu ama edgeleri takmadan bölüyor onun için logic düşünmemiz gerekli
def initialPartition(edges_dict, sub_set_number):
    node_list = []
    for node,_ in edges_dict.items():
        node_list.append(node)
    büyük_sub_list = []
    for i in range(sub_set_number):
        kücük_sub_list = []
        # Starting from i, incrementing by k, and stopping before reaching or exceeding len(vertices)
        for j in range(i, len(node_list), sub_set_number):
            kücük_sub_list.append(node_list[j])
            print("Kucuk partition",kücük_sub_list)
            print("J and i:",j, i)
            print("*******")
        büyük_sub_list.append(kücük_sub_list)
        print("Kucuk partition bitmis hali",kücük_sub_list)
        print("***************************")
        print("Büyük partition bitmis hali",büyük_sub_list)
    return büyük_sub_list

def buildGraph():
    edges = [
        ["A", "B"], ["A", "E"],
        ["A", "C"], ["B", "D"],
        ["B", "E"], ["C", "F"],
        ["C", "G"], ["D", "E"],
    ]
    dict_graph = defaultdict(list)

    for edge in edges:
        a, b = edge[0], edge[1]
        dict_graph[a].append(b)
        dict_graph[b].append(a)
    print(dict_graph)
    return dict_graph

def visualizeGraph(graph):
    plt.figure(figsize=(8, 6))
    position = {}
    y = 0
    for node, neighbors in graph.items():
        position[node] = (len(neighbors), y)
        print(position)
        y += 2

    for node, neighbors in graph.items():
        plt.plot(position[node][0], position[node][1], 'bo')  # Plot nodes without connecting lines
        plt.text(position[node][0], position[node][1], node, fontsize=12,)

        for neighbor in neighbors:
            plt.plot([position[node][0], position[neighbor][0]], [position[node][1], position[neighbor][1]], 'bo-')

    plt.title('Graph Visualization')
    plt.xlabel('Nodes')
    plt.yticks([])
    plt.show()
graph = buildGraph()
#graph = build_graph()
#visualize_graph(graph)
createGraph(graph)
