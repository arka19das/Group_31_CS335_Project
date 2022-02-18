import regex as re
import pydot
import sys

def main(input_path, output_path):
    original_stdout = sys.stdout
    file = open(input_path, "r")
    text = file.read()
    split_text = re.split(r"\nstate (\d+)\n", text)
# there are 0-360  361 total states

    shift_dict = {}
    reduce_dict = {}

    for i in range(2, 723, 2):
        matching_text = re.findall(
            "(\w+)(\s+) shift and go to state (\d+)\n", split_text[i]
        )
        for items in matching_text:
            shift_dict[int(split_text[i - 1]), int(items[2])] = items[0]
        matching_text1 = re.findall("(\w+)(\s+) reduce using rule (\d+)", split_text[i])

    graph = pydot.Dot("Grammar_graph", graph_type="digraph", bgcolor="white")

    for i in range(0, 361):
        my_node = pydot.Node(str(i), label=f"I{i}", shape="circle",style="filled",fillcolor="yellow")
        graph.add_node(my_node)

    for key, value in shift_dict.items():
        graph.add_edge(pydot.Edge(str(key[0]), str(key[1]), label=value, color="black"))

    graph.write_raw(output_path)

    file.close()


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
