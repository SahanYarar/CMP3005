from collections import defaultdict
import matplotlib.pyplot as plt
import networkx as nx

def createGraph(edges_dict):
    G = nx.Graph() 
    node_list, edge_list = getNodesAndEdgesFromDict(edges_dict=edges_dict)
    print(edges_dict.items())
    for node,edges in edges_dict.items():
        G.add_node(node)
        print(edges)
        for edge in edges:
            print(edge)
            G.add_edge(node ,edge)
    initialPartition(edges_dict=edges_dict,sub_set_number=2)
    pos = drawGraph(G)
    return G, pos


def drawGraph(G):
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, font_weight='bold', node_color='lightblue', edge_color='gray')
    plt.pause(110)
    return pos

def getNodesAndEdgesFromDict(edges_dict):
    node_list = []
    edge_list = []
    for node,edge in edges_dict.items():
        node_list.append(node)
        edge_list.append(edge)
    return node_list, edge_list


## TODO: Sub setlere bölme halloldu ama edgeleri takmadan bölüyor onun için logic düşünmemiz gerekli
def initialPartition(edges_dict, sub_set_number):
    node_list,_ = getNodesAndEdgesFromDict(edges_dict=edges_dict)
    büyük_sub_list = []
    for i in range(sub_set_number):
        kücük_sub_list = []
        # Starting from i, incrementing by k, and stopping before reaching or exceeding len(vertices)
        for j in range(i, len(node_list), sub_set_number):
            kücük_sub_list.append(node_list[j])
        büyük_sub_list.append(kücük_sub_list)
    print("***************************") 
    print("Büyük partition bitmis hali",büyük_sub_list)
    print("***************************") 
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
    print("Dict of graph:",dict_graph)
    return dict_graph


graph = buildGraph()
createGraph(graph)
