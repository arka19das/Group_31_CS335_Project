from utils import *


def type_util(op1: Node, op2: Node, op: str):
    rule_name = "type_util"
    temp = Node(
        name=op + "Operation",
        val=op1.val + op + op2.val,
        lno=op1.lno,
        type="int",
        children=[],
    )

    # print(temp)
    if op1.type == "" or op2.type == "":
        temp.type = "int"  # default
        return temp
    top1 = str(op1.type)
    top2 = str(op2.type)
    tp1 = op1.base_type
    tp2 = op2.base_type

    if top1.endswith("*") and top2.endswith("*"):
        if op == "==" or op == "!=":
            temp.type = "int"
        else:
            ST.error(
                Error(
                    -1,
                    rule_name,
                    "compilation error",
                    "Cannot cast pointer to pointer or invalid operation with pointer",
                )
            )
            temp.type = op1.type
        # temp.level = op1.level
    elif top1.endswith("*") or top2.endswith("*"):
        # MODIFIED
        if top1.endswith("*") and tp2 in TYPE_FLOAT:
            ST.error(
                Error(
                    -1,
                    rule_name,
                    "compilation error",
                    f"Incompatible data type {op} operator",
                )
            )
            temp.type = op1.type
            temp.level = op1.level
        elif top1.endswith("*"):
            temp.type = op1.type
            temp.level = op1.level
        elif top2.endswith("*") and tp1 in TYPE_FLOAT:
            ST.error(
                Error(
                    -1,
                    rule_name,
                    "compilation error",
                    f"Incompatible data type {op} operator",
                )
            )
            temp.type = op2.type
            temp.level = op2.level
        elif top2.endswith("*"):
            temp.type = op2.type
            temp.level = op2.level

    else:
        if tp1 not in ops_type[op] or tp2 not in ops_type[op]:
            ST.error(
                Error(
                    -1,
                    rule_name,
                    "compilation error",
                    f"Incompatible data type {op} operator",
                )
            )

        size1 = SIZE_OF_TYPE[tp1]
        size2 = SIZE_OF_TYPE[tp2]
        if size1 > size2:
            ST.error(
                Error(
                    -1,
                    rule_name,
                    "warning",
                    f"Implicit type casting of {op2.val}",
                )
            )
            temp.type = op1.type
        elif size2 > size1:
            ST.error(
                Error(
                    -1,
                    rule_name,
                    "warning",
                    f"Implicit type casting of {op1.val}",
                )
            )
            temp.type = op2.type
        else:
            if tp1 == "FLOAT" or tp2 == "FLOAT":
                temp.type = "float"
            elif tp1 == "DOUBLE" or tp2 == "DOUBLE":
                temp.type = "float"
            elif top1.startswith("unsigned"):
                temp.type = op1.type
            else:
                temp.type = op2.type

    if temp.type == "char":
        temp.type = "int"
    if temp.type == "unsigned char":
        temp.type == "unsigned int"
    # if op in ["*", "-", "%"]:
    #     temp.val = op1.val

    tmp_var = ST.get_tmp_var(temp.type)
    temp.place = tmp_var

    check_identifier(op1)
    check_identifier(op2)
    return temp
