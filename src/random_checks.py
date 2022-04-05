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
    if op1.type == "" or op2.type == "":
        temp.type = "int"  # default
        return temp

    top1 = str(op1.type)
    top2 = str(op2.type)
    tp1 = op1.base_type
    tp2 = op2.base_type

    if top1.count("*") > 0 and top2.count("*") > 0:
        if op == "==" or op == "-":
            if op1.level != op2.level:
                ST.error(
                    Error(
                        -1,
                        rule_name,
                        "compilation error",
                        f"Invalid operation {op} on pointers of different levels",
                    )
                )

            if op1.base_type != op2.base_type:
                ST.error(
                    Error(
                        -1,
                        rule_name,
                        "compilation error",
                        f"Invalid operation {op} on pointers of different types",
                    )
                )
        else:
            ST.error(
                Error(
                    -1,
                    rule_name,
                    "compilation error",
                    f"Invalid operation {op} on pointers",
                )
            )
        temp.type = op1.type
        temp.level = op1.level

    elif top1.count("*") > 0 or top2.count("*") > 0:
        if top1.count("*") > 0 and tp2 in TYPE_FLOAT:
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
        elif top1.count("*") > 0:
            if op not in ["+", "-"]:
                ST.error(
                    Error(
                        -1,
                        rule_name,
                        "compilation error",
                        f"Invalid operation {op} on pointers",
                    )
                )
            temp.type = op1.type
            temp.level = op1.level
        elif top2.count("*") > 0 and tp1 in TYPE_FLOAT:
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
        elif top2.count("*") > 0:
            if op not in ["+", "-"]:
                ST.error(
                    Error(
                        -1,
                        rule_name,
                        "compilation error",
                        f"Invalid operation {op} on pointers",
                    )
                )

            temp.type = op2.type
            temp.level = op2.level

    elif top1.startswith("struct") or top2.startswith("struct"):
        ST.error(
            Error(
                -1,
                rule_name,
                "compilation error",
                f"Incompatible data type {op} operator",
            )
        )
        typ = op1.type if top1.startswith("struct") else op2.type
        temp.type = typ
        return temp

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

    # if op in ["*", "-", "%"]:
    #     temp.val = op1.val
    # check_identifier(op1)
    # check_identifier(op2)

    p_node = ST.find(op1.val)
    if (p_node is not None) and (op1.is_func == 1):
        ST.error(
            Error(
                p.lno,
                "Check Identifier",
                "compilation error",
                f"Invalid operation on {op1.val}",
            )
        )

    p_node = ST.find(op2.val)
    if (p_node is not None) and (op2.is_func == 1):
        ST.error(
            Error(
                p.lno,
                "Check Identifier",
                "compilation error",
                f"Invalid operation on {op2.val}",
            )
        )

    return temp
