import regex as re
import sys

original_stdout = sys.stdout
file1 = open("parser.out", "r")
text = file1.read()
split_text = re.split(r"\nstate (\d+)\n", text)
# there are 0-360  361 total states

shift_dict = {}
reduce_dict = {}
# print(split_text[0])

for i in range(2, 723, 2):
    matching_text = re.findall(
        "(\w+)(\s+) shift and go to state (\d+)\n", split_text[i]
    )
    for items in matching_text:
        shift_dict[int(split_text[i - 1]), int(items[2])] = items[0]
    matching_text1 = re.findall("(\w+)(\s+) reduce using rule (\d+)", split_text[i])

    for items in matching_text1:
        reduce_dict[int(split_text[i - 1]), int(items[2])] = items[0]


with open("shift_dict.txt", "w") as f:
    sys.stdout = f  # Change the standard output to the file we created.
    print(shift_dict)
    sys.stdout = original_stdout


with open("reduce_dict.txt", "w") as f:
    sys.stdout = f  # Change the standard output to the file we created.
    print(reduce_dict)
    sys.stdout = original_stdout


file1.close()
