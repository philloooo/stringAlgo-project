import pydot
import dot_parser
graph = pydot.Dot(graph_type = 'digraph')
node_a = pydot.Node("Node A", style="filled", fillcolor="red")
node_b = pydot.Node("Node B", style="filled", fillcolor="green")
graph.add_node(node_a)
graph.add_node(node_b)
graph.add_edge(pydot.Edge(node_a, node_b))
graph.write_png('example2_graph.png')
