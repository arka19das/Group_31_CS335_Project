# str1 = " unsigned long* * *"
# print(str1.strip(" *") + "1")
import re
file1 = open('sorted_code_gen.txt', 'r')
Lines = file1.readlines()
type_of_instruction=[]
for line in Lines:
    last_index=line.index(',')
    line1=line[17:last_index]
    
    type_of_instruction.append(line1[::-1])
unique_types=set(type_of_instruction)

for i in sorted(unique_types):
    print(i[::-1])
# instr_dict={}
# instr_dict["int="]=""
# instr_dict["load="]=""
# instr_dict["label"]="label"
# instr_dict["goto"]=
# instr_dict[]=
# instr_dict[]=
# instr_dict[]=
# instr_dict[]=
# instr_dict[]=
