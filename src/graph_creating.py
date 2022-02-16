import pydot
import ast

graph = pydot.Dot("graph_for_my_grammar", graph_type="graph", bgcolor="white")

# Add nodes
file = open("shift_dict.txt", "r")

contents = file.read()
shift_dict = ast.literal_eval(contents)

file.close()

# file = open("reduce_dict.txt", "r")

# contents = file.read()
# reduce_dict = ast.literal_eval(contents)

# file.close()


for i in range(0, 361):
    my_node = pydot.Node(str(i), label="Foo", shape="circle", color="blue")
    graph.add_node(my_node)


# Add edges

for key, value in shift_dict.items():
    print(key)
    graph.add_edge(pydot.Edge(str(key[0]), str(key[1]), label=value, color="blue"))

graph.write_raw("output_raw.dot")
# output_graphviz_dot = graph.create_dot()
# print(output_graphviz_dot)
# graph.write_png("output.png")
