# TODO: check invalid operation on function and backpatching
# TODO: small error,, in repeated cases unable to display line number
# Yacc example
import copy
import re
import signal

import ply.yacc as yacc
from graphviz import Digraph

from scanner import *
from utils import *
from mips import mips_generation

# Get the token map from the lexer.  This is required.
lexer = Lexer()
lexer.build()
tokens = lexer.tokens


cur_num = 0

# in_whose_scope = ""
offsets[0] = 0
activation_record = []
valid_goto_labels = []


def is_const(p):
    if p[0] >= "0" and p[0] <= "9":
        return True
    elif p[0] == "-" and p[1] >= "0" and p[1] <= "9":
        return True
    return False


def cal_offset(p):
    # if (isinstance(p, Node) and p.place.startswith("__tmp")) or (isinstance(p, str)):
    #     return ""
    if isinstance(p, str):
        return p
    if is_const(p.place):
        return p.place
    if p.in_whose_scope == "#global":
        offset = p.offset
        if offset:
            offset_string = f"{-offset}($static)"
        else:
            offset_string = "0($static)"
        return offset_string

    count_ = p.in_whose_scope.count("_")
    offset = 0
    for c_ in range(count_):  # CHECK ARKA BC
        offset += offsets[1 + c_]

    offset += p.offset
    if offset:
        offset_string = f"{-offset}($fp)"
    else:
        offset_string = "0($fp)"

    return offset_string


def build_AST(p, rule_name):
    global cur_num
    length = len(p)
    if length == 2:
        if type(p[1]) is Node:
            return p[1].ast
        else:
            return p[1]
    else:
        cur_num += 1
        p_count = cur_num
        graph.node(str(p_count), str(rule_name))  # make new vertex in dot file
        for child in range(1, length, 1):
            if type(p[child]) is Node and p[child].ast is None:
                continue
            if type(p[child]) is not Node:
                if type(p[child]) is tuple:
                    if ignore_char(p[child][0]) is False:
                        graph.edge(str(p_count), str(p[child][1]))
                else:
                    if ignore_char(p[child]) is False:
                        cur_num += 1
                        p[child] = (p[child], cur_num)
                        graph.node(str(cur_num), str(p[child][0]))
                        graph.edge(str(p_count), str(p[child][1]))
            else:
                if type(p[child].ast) is tuple:
                    if ignore_char(p[child].ast[0]) is False:
                        graph.edge(str(p_count), str(p[child].ast[1]))
                else:
                    if ignore_char(p[child].ast) is False:
                        cur_num += 1
                        p[child].ast = (p[child].ast, cur_num)
                        graph.node(str(cur_num), str(p[child].ast[0]))
                        graph.edge(str(p_count), str(p[child].ast[1]))

        return (rule_name, p_count)


# def build_AST_2(p, p_list, rule_name):


def build_AST_2(p, p_list, rule_name):
    global cur_num
    cur_num += 1
    p_count = cur_num
    graph.node(str(p_count), str(rule_name))  # make new vertex in dot file
    for child in p_list:
        if type(p[child]) is Node and p[child].ast is None:
            continue
        if type(p[child]) is not Node:
            if type(p[child]) is tuple:
                if ignore_char(p[child][0]) is False:
                    graph.edge(str(p_count), str(p[child][1]))
            else:
                if ignore_char(p[child]) is False:
                    cur_num += 1
                    p[child] = (p[child], cur_num)
                    graph.node(str(cur_num), str(p[child][0]))
                    graph.edge(str(p_count), str(p[child][1]))
        else:
            if type(p[child].ast) is tuple:
                if ignore_char(p[child].ast[0]) is False:
                    graph.edge(str(p_count), str(p[child].ast[1]))
            else:
                if ignore_char(p[child].ast) is False:
                    cur_num += 1
                    p[child].ast = (p[child].ast, cur_num)
                    graph.node(str(cur_num), str(p[child].ast[0]))
                    graph.edge(str(p_count), str(p[child].ast[1]))

    return (rule_name, p_count)


# in scope name, 0 denotes #global, 1 denotes loop and 2 denotes if/switch, 3 denotes function
# add more later
ts_unit = Node("START", val="", type="", children=[])


def p_primary_expression(p):
    """primary_expression : identifier
    | float_constant
    | hex_constant
    | oct_constant
    | int_constant
    | char_constant
    | string_literal
    | LEFT_BRACKET expression RIGHT_BRACKET"""

    if len(p) == 2:
        p[0] = p[1]
    else:
        # print(p[2])
        p[0] = p[2]
        # p[0].lhs = 1


def p_float_constant(p):
    """float_constant : FLOAT_CONSTANT"""
    p[0] = Node(
        name="Constant",
        val=p[1],
        lno=p.lineno(1),
        type="float",
        children=[],
        place=p[1],
        lhs=1,
    )
    rule_name = "float_constant"
    p[0].ast = build_AST(p, rule_name)
    if "l" in p[1] or "L" in p[1]:
        p[0].type = "double"
        p[0].val = p[1][:-2]


def p_hex_constant(p):
    """hex_constant : HEX_CONSTANT"""
    p[0] = Node(
        name="Constant",
        val=p[1],
        lno=p.lineno(1),
        type="int",
        children=[],
        place=p[1],
        code="",
        lhs=1,
    )
    rule_name = "hex_constant"
    p[0].ast = build_AST(p, rule_name)
    temp = re.findall("[0-9a-fA-F]+", p[1][2:])
    p[0].val = int(temp[0], 16)
    p[0].place = int(temp[0], 16)
    if "l" in p[1] or "L" in p[1]:
        p[0].type = "long"

    if "u" in p[1] or "U" in p[1]:
        p[0].type = "unsigned " + p[0].type


def p_oct_constant(p):
    """oct_constant : OCT_CONSTANT"""
    p[0] = Node(
        name="Constant",
        val=p[1],
        lno=p.lineno(1),
        type="int",
        children=[],
        place=p[1],
        code="",
        lhs=1,
    )
    temp = re.findall("[0-7]+", p[1][1:])
    p[0].val = int(temp[0], 8)
    p[0].place = int(temp[0], 8)
    if "l" in p[1] or "L" in p[1]:
        p[0].type = "long"

    if "u" in p[1] or "U" in p[1]:
        p[0].type = "unsigned " + p[0].type
    rule_name = "oct_constant"
    p[0].ast = build_AST(p, rule_name)


def p_int_constant(p):
    """int_constant : INT_CONSTANT"""
    p[0] = Node(
        name="Constant",
        val=p[1],
        lno=p.lineno(1),
        type="int",
        children=[],
        place=p[1],
        code="",
        lhs=1,
    )
    temp = re.findall("[0-9]+", p[1])
    p[0].val = temp[0]
    if "l" in p[1] or "L" in p[1]:
        p[0].type = "long"

    if "u" in p[1] or "U" in p[1]:
        p[0].type = "unsigned " + p[0].type
    rule_name = "int_constant"
    p[0].ast = build_AST(p, rule_name)


def p_char_constant(p):
    """char_constant : CHAR_CONSTANT"""
    a = p[1][1:-1]
    b = None
    if len(a) == 2:
        if a == "\a":
            b = 7
        elif a == "\b":
            b = 8
        elif a == "\f":
            b = 12
        elif a == "\n":
            b = 10
        elif a == "\r":
            b = 13
        elif a == "\t":
            b = 9
        elif a == "\v":
            b = 11
        elif a == "'":
            b = 39
        elif a == '"':
            b = 34
        elif a == "\\":
            b = 92
        elif a == "?":
            b = 63
        elif a == "\0":
            b = 0
        elif a == "\?":
            b = 63
        else:
            ST.error(
                Error(
                    p.lineno(1),
                    "rule_name",
                    "Lexical Error",
                    "Invalid character constant",
                )
            )

    elif len(a) == 1:
        if a == "\\":
            ST.error(
                Error(
                    p.lineno(1),
                    "rule_name",
                    "Lexical Error",
                    "Invalid character constant",
                )
            )
        b = ord(a)
    else:
        ST.error(
            Error(
                p.lineno(1), "rule_name", "Lexical Error", "Invalid character constant"
            )
        )

    p[0] = Node(
        name="Constant",
        val=str(b),
        lno=p.lineno(1),
        type="int",
        children=[],
        place=str(b),
        code="",
        lhs=1,
    )
    rule_name = "char_constant"
    p[0].ast = build_AST(p, rule_name)

    p[0] = Node(
        name="Constant",
        val=str(b),
        lno=p.lineno(1),
        type="int",
        children=[],
        place=str(b),
        code="",
        lhs=1,
    )
    rule_name = "char_constant"
    p[0].ast = build_AST(p, rule_name)


def p_string_literal(p):
    """string_literal : STRING_LITERAL"""
    p[0] = Node(
        name="Constant",
        val=p[1],
        lno=p.lineno(1),
        type="string",
        level=1,
        children=[],
        place=p[1],
        code="",
        lhs=1,
    )
    rule_name = "string_literal"
    p[0].ast = build_AST(p, rule_name)


def p_identifier(p):
    """identifier : IDENTIFIER"""
    p[0] = Node(
        name="PrimaryExpression",
        val=p[1],
        lno=p.lineno(1),
        type="",
        children=[],
        place=p[1],
        code="",
    )
    rule_name = "identifier"
    p1_node = ST.find(p[1])
    if p1_node is not None:
        p[0].type = p1_node.type
        temp_count = str(p[0].type).count("*")
        if temp_count != 0:
            p[0].level = temp_count
        p[0].array = p1_node.array
        p[0].level += len(p1_node.array)
        p[0].is_func = p1_node.is_func
        p[0].ast = build_AST(p, rule_name)
        p[0].offset = p1_node.offset
        p[0].in_whose_scope = p1_node.in_whose_scope
        if temp_count != p[0].level:
            p[0].type += (" *") * (p[0].level - temp_count)

    else:
        ST.error(
            Error(
                p.lineno(1),
                rule_name,
                "compilation error",
                f"Identifier {p[1]} not declared",
            )
        )


def p_postfix_expression_3(p):
    """postfix_expression : primary_expression
    | postfix_expression LEFT_BRACKET argument_expression_list RIGHT_BRACKET
    | postfix_expression LEFT_BRACKET RIGHT_BRACKET
    | postfix_expression LEFT_THIRD_BRACKET expression RIGHT_THIRD_BRACKET
    | postfix_expression DOT IDENTIFIER
    | postfix_expression PTR_OP IDENTIFIER
    | postfix_expression INC_OP
          | postfix_expression DEC_OP
    """
    rule_name = "postfix_expression"
    if len(p) == 2:
        p[0] = p[1]
        # p[0].ast = build_AST(p, rule_name)

    elif len(p) == 3:
        if len(p[1].array) > 0 and isinstance(p[1].array[0], int):
            ST.error(
                Error(
                    p[1].lno,
                    rule_name,
                    "compilation error",
                    f"Array {p[1].val} pointer increment",
                )
            )

        tmp_var, tmp_offset_string = ST.get_tmp_var(p[1].type)
        p[0] = Node(
            name="IncrementOrDecrementExpression",
            val=p[1].val,
            lno=p[1].lno,
            type=p[1].type,
            children=[],
            place=tmp_var,
            level=p[1].level,
            offset=p[1].offset,
            lhs=1,
        )
        p[0].ast = build_AST_2(p, [1], p[2])
        check_identifier(p[1], p.lineno(1))
        offset_string = cal_offset(p[1])
        if p[1].type.endswith("*"):
            code_gen.append(["8=", p[1].place, tmp_var])
            activation_record.append(["8=", offset_string, tmp_offset_string])

        else:
            code_gen.append(
                [str(get_data_type_size(p[1].type)) + "=", p[1].place, tmp_var,]
            )
            activation_record.append(
                [
                    str(get_data_type_size(p[1].type)) + "=",
                    offset_string,
                    tmp_offset_string,
                ]
            )

        # code_gen.append(f"f{tmp_var} := {p[1].place}")
        # DONE: FLOAT not supported yet and neither are pointers dhang se
        if p[2] == "++":
            if p[1].type.endswith("*"):
                code_gen.append(
                    [
                        "long-",
                        p[1].place,
                        p[1].place,
                        str(get_data_type_size(p[1].type[:-2])),
                    ]
                )
                activation_record.append(
                    [
                        "long-",
                        offset_string,
                        offset_string,
                        str(get_data_type_size(p[1].type[:-2])),
                    ]
                )
            else:
                code_gen.append([p[1].type + "+", p[1].place, p[1].place, "1"])
                activation_record.append(
                    [p[1].type + "+", offset_string, offset_string, "1",]
                )

            # code_gen.append(f"{p[1].place} := {p[1].place} + 1")
        elif p[2] == "--":
            if p[1].type.endswith("*"):
                code_gen.append(
                    [
                        "long-",
                        p[1].place,
                        p[1].place,
                        f"-{get_data_type_size(p[1].type[:-2])}",
                    ]
                )
                activation_record.append(
                    [
                        "long-",
                        offset_string,
                        offset_string,
                        f"-{get_data_type_size(p[1].type[:-2])}",
                    ]
                )
            else:
                code_gen.append([p[1].type + "+", p[1].place, p[1].place, "-1"])
                activation_record.append(
                    [p[1].type + "+", offset_string, offset_string, "-1",]
                )

            # code_gen.append(f"{p[1].place} := {p[1].place} - 1")
        # code_gen.append()
        # p[0].ast = build_AST(p, rule_name)

    elif len(p) == 4:
        if p[2] == "(":
            p[0] = Node(
                name="FunctionCall1",
                val=p[1].val,
                lno=p[1].lno,
                type=p[1].type,
                children=[p[1]],
                is_func=0,
                place=p[1].place,
                lhs=1,
            )
            p[0].ast = build_AST_2(p, [1], "()")
            # p[0].ast = build_AST(p, rule_name)
            p1v_node = ST.find(p[1].val)
            if p1v_node is None or not p1v_node.is_func:
                ST.error(
                    Error(
                        p[1].lno,
                        rule_name,
                        "compilation error",
                        f"No function declared with name {p[1].val}",
                    )
                )
                return
            elif len(p1v_node.argument_list) != 0:
                ST.error(
                    Error(
                        p[1].lno,
                        rule_name,
                        "semantic error",
                        f"Function {p[1].val} called with incorrect number of arguments",
                    )
                )
                return
            func_size = 0
            for scope_table in ST.scope_tables:
                if scope_table.name == p[1].val:
                    for node in scope_table.nodes:
                        func_size += node.size

            code_gen.append([f"call_{func_size}", p[1].val, "", ""])
            activation_record.append(
                [f"call_{func_size}", p[1].val, "", f"__{p[1].val}"]
            )

        else:
            if not p[1].name.startswith("Dot"):
                p1v_node = ST.find(p[1].val)
                if p1v_node is None:
                    ST.error(
                        Error(
                            p[1].lno,
                            rule_name,
                            "compilation error",
                            f"{p[1].val} not declared",
                        )
                    )

            p[0] = Node(
                name="DotOrPTRExpression",
                val=p[3],
                lno=p[1].lno,
                type=p[1].type,
                children=[],
                place=p[1].place,
                offset=p[1].offset,
            )
            p[0].ast = build_AST_2(p, [1, 3], p[2])

            struct_name = p[1].type
            if not struct_name.startswith("struct"):
                ST.error(
                    Error(
                        p[1].lno,
                        rule_name,
                        "compilation error",
                        f"{p[1].val} is not a struct",
                    )
                )
                return

            if (struct_name.endswith("*") and p[2] == ".") or (
                not struct_name.endswith("*") and p[2] == "->"
            ):
                ST.error(
                    Error(
                        p[1].lno,
                        rule_name,
                        "compilation error",
                        f"Invalid operator on {struct_name}",
                    )
                )
                return
            # Akshay added this ..now -> shouldnt work ..check it
            if (p[1].level > 0 and p[2] == ".") or (p[1].level > 1 and p[2] == "->"):
                ST.error(
                    Error(
                        p[1].lno,
                        rule_name,
                        "compilation error",
                        f" Invalid dimensions on struct {p[1].val}",
                    )
                )

            struct_node = ST.find(struct_name)
            flag = 0
            for curr_list in struct_node.field_list:
                if curr_list[1] == p[3][0]:
                    # TODO:INCOMPLETE
                    flag = 1
                    offset_string = cal_offset(p[1])
                    tmp, tmp_offset_string = ST.get_tmp_var("long")

                    type1 = curr_list[0]
                    tmp2, tmp_offset_string2 = ST.get_tmp_var(curr_list[0])
                    p[0] = ST.find(tmp2)

                    p[0].addr = tmp
                    p[0].name = "DotOrPTRExpression"
                    p[0].val = p[3]
                    if len(curr_list) == 5:
                        p[0].name = tmp2
                        p[0].array = curr_list[4]
                        # p[0].size = 8
                    p[0].type = curr_list[0]

                    p[0].parentStruct = struct_name
                    p[0].level = curr_list[0].count("*")
                    if len(curr_list) == 5:
                        p[0].level += len(curr_list[4])
                    if p[0].level <= -1:
                        ST.error(
                            Error(
                                p[1].lno,
                                rule_name,
                                "compilation error",
                                f"Incorrect number of dimensions for {p[1].val}",
                            )
                        )
                        return  ## IS RETURN ACTUALLY REQUIRED --ADDED BY ARKA

                    # offset_string = cal_offset(p[1])
                    # tmp, tmp_offset_string = ST.get_tmp_var("long")
                    # p[0].addr = tmp
                    # type1 = curr_list[0]
                    # tmp2, tmp_offset_string = ST.get_tmp_var(curr_list[0])
                    # if len(curr_list) > 4:
                    #     tmp2.array = copy.deepcopy(curr_list[4])
                    code_gen.append(["addr", tmp, p[1].place, ""])
                    activation_record.append(
                        ["addr", tmp_offset_string, offset_string[0:-5], "",]
                    )

                    # if curr_list[3] > 0:
                    code_gen.append(["long-", tmp, curr_list[3], tmp])
                    activation_record.append(
                        ["long-", tmp_offset_string, curr_list[3], tmp_offset_string,]
                    )
                    # print(type1)
                    # if len(p[0].array) > 0:
                    #     print(1)
                    #     code_gen.append([f"long=", tmp2, tmp, ""])
                    #     activation_record.append([f"long=", tmp2, tmp, ""])
                    if type1.upper() in PRIMITIVE_TYPES:
                        code_gen.append(
                            [f"{get_data_type_size(type1)}load", tmp2, tmp, ""]
                        )
                        activation_record.append(
                            [
                                f"{get_data_type_size(type1)}load",
                                tmp_offset_string2,
                                tmp_offset_string,
                                "",
                            ]
                        )

                    else:
                        code_gen.append(
                            [
                                f"{get_data_type_size(type1)}non_primitive_load",
                                tmp2,
                                tmp,
                                "",
                            ]
                        )
                        activation_record.append(
                            [
                                f"{get_data_type_size(type1)}non_primitive_load",
                                tmp_offset_string2,
                                tmp_offset_string,
                                "",
                            ]
                        )
                    ## load instruction may be redundant or not required sometimes

            if flag == 0:
                ST.error(
                    Error(
                        p[1].lno,
                        rule_name,
                        "compilation error",
                        f"Field not declared in {struct_name}",
                    )
                )

    elif len(p) == 5:
        ##multidimensional array mei multiply galat cheez se karrahe
        if p[2] == "[":
            p[0] = Node(
                name="ArrayExpression",
                val=p[1].val,
                lno=p[1].lno,
                type=p[1].type,
                children=[p[1], p[3]],
                is_func=p[1].is_func,
                parentStruct=p[1].parentStruct,
                place=p[1].place,
                offset=p[1].offset,
            )
            p[0].ast = build_AST_2(p, [1, 3], "[]")
            # p[0].ast = build_AST(p, rule_name)
            p[0].array = copy.deepcopy(p[1].array[1:])
            p[0].array.append(p[3].val)
            p[0].level = p[1].level - 1
            if p[0].level == -1:
                ST.error(
                    Error(
                        p[1].lno,
                        rule_name,
                        "compilation error",
                        f"Incorrect number of dimensions specified for {p[1].val}",
                    )
                )
            ##begin AKSHAY ADDED THIS..ASK FOR HELP
            elif p[1].type.count("*") > 0:
                p[0].type = p[1].type[:-2]
            ##end of AKSHAY ADDED THIS..ASK FOR HELP
            temp_var = p[3].place
            temp_offset_string = cal_offset(p[3])

            if p[3].type.upper() not in TYPE_INTEGER + TYPE_CHAR:
                ST.error(
                    Error(
                        p[3].lno,
                        rule_name,
                        "compilation error",
                        "Array Index is of incompatible type",
                    )
                )
                return  ## added might cause varities error later-Arka
            if p[1].name.startswith("Dot"):
                ## added by akshay to evaluate array of structs in field of struct
                p[0].name = p[1].name

            offset_string = cal_offset(p[1])
            if p[3].type.upper()[-3:] != "INT":

                temp_var, tmp_offset_string = ST.get_tmp_var("int")
                code_gen.append([p[3].type + "2" + "int", temp_var, p[3].place])
                activation_record.append(
                    [p[3].type + "2" + "int", tmp_offset_string, offset_string,]
                )

            d = len(p[1].array) - p[0].level - 1
            v1, v_offset_string = ST.get_tmp_var("int")
            # print(p[1].array)
            if isinstance(p[1].array[-1], int):
                code_gen.append(["int^", v1, v1, v1])
                activation_record.append(
                    ["int^", v_offset_string, v_offset_string, v_offset_string,]
                )

            # if d != 0:
            # print(p[1].array)
            # code_gen.append(["long=", temp_var, p[3].place, ""])
            if isinstance(p[0].array[0], str):
                code_gen.append(["int+", v1, v1, temp_var])
                activation_record.append(
                    ["int+", v_offset_string, v_offset_string, temp_offset_string,]
                )

                code_gen.append(["long*", v1, v1, str(get_data_type_size(p[0].type))])
                activation_record.append(
                    [
                        "long*",
                        v_offset_string,
                        v_offset_string,
                        str(get_data_type_size(p[0].type)),
                    ]
                )
            elif isinstance(p[1].array[-1], int):
                code_gen.append(["int+", v1, v1, temp_var])
                activation_record.append(
                    ["int+", v_offset_string, v_offset_string, temp_offset_string,]
                )

                code_gen.append(["int*", v1, v1, str(p[1].array[0])])
                activation_record.append(
                    ["int*", v_offset_string, v_offset_string, str(p[1].array[0]),]
                )
                p[0].index = v1

            else:
                code_gen.append(["int+", v1, p[1].index, temp_var])
                activation_record.append(
                    ["int+", v_offset_string, p[1].index, temp_offset_string,]
                )

                code_gen.append(["int*", v1, v1, str(p[1].array[0])])
                activation_record.append(
                    ["int*", v_offset_string, v_offset_string, str(p[1].array[0]),]
                )
                p[0].index = v1

            # if p[0].level == 0 and len(p[0].array) > 0:
            if isinstance(p[0].array[0], str):
                # , tmp_offsetv1=ST.get_tmp_var('int')
                v2, v2_offset_string = ST.get_tmp_var(p[1].type)
                # p[]
                if p[1].place[0:10] == "__tmp_var_":
                    code_gen.append(["addr", v2, p[1].addr, ""])
                    activation_record.append(
                        ["addr", v2_offset_string, offset_string[0:-5], ""]
                    )

                else:
                    code_gen.append(["addr", v2, p[1].place, ""])
                    activation_record.append(
                        ["addr", v2_offset_string, offset_string[0:-5], ""]
                    )

                code_gen.append(["long-", v2, v1, v2])
                activation_record.append(
                    ["long-", v2_offset_string, v_offset_string, tmp_offset_string,]
                )

                type1 = p[0].type  # TODO: BUGGED
                v3, v3_offset_string = ST.get_tmp_var(type1)
                p[0].place = v3
                p[0].addr = v2

                # agar isko stack pe liya to p[0].place ko v3 me store krne se gayab hojayega
                if type1.upper() in PRIMITIVE_TYPES:
                    code_gen.append([f"{get_data_type_size(type1)}load", v3, v2, ""])
                    activation_record.append(
                        [
                            f"{get_data_type_size(type1)}load",
                            v3_offset_string,
                            v2_offset_string,
                            "",
                        ]
                    )

                else:
                    code_gen.append(
                        [f"{get_data_type_size(type1)}non_primitive_load", v3, v2, ""]
                    )
                    activation_record.append(
                        [
                            f"{get_data_type_size(type1)}non_primitive_load",
                            v3_offset_string,
                            v2_offset_string,
                            "",
                        ]
                    )
                ## load instruction may be redundant or not required sometimes

            # elif len(p[0].array) > 0:
            #     if d == 0:
            #         p[0].index = temp_var
            #     else:
            #         p[0].index = v1
        else:
            p[0] = Node(
                name="FunctionCall2",
                val=p[1].val,
                lno=p[1].lno,
                type=p[1].type,
                children=[],
                is_func=0,
                place=p[1].place,
                lhs=1,
            )
            p[0].ast = build_AST_2(p, [1, 3], "()")
            # p[0].ast = build_AST(p, rule_name)
            p1v_node = ST.find(p[1].val)

            if p1v_node is None or p1v_node.is_func == 0:
                ST.error(
                    Error(
                        p[1].lno,
                        rule_name,
                        "compilation error",
                        f"No function of name {p[1].val} declared",
                    )
                )
                return
            elif len(p1v_node.argument_list) != len(p[3].children):
                ST.error(
                    Error(
                        p[1].lno,
                        rule_name,
                        "semantic error",
                        "Incorrect number of arguments for function call",
                    )
                )
                return
            else:
                i = len(p1v_node.argument_list) - 1
                temp_act = []
                temp_3ac = []
                func_offset = 0
                for arguments in reversed(p1v_node.argument_list):
                    # HAVE TO THINK
                    # MODIFIED
                    # curVal = p[3].children[i].val
                    # cv_node = ST.current_table.find(curVal)
                    # if cv_node is None:
                    #   continue
                    # ST.curType = cv_node.type
                    if p[3].children[i].type in PRIMITIVE_TYPES:
                        p[3].children[i].type = TYPE_EASY[
                            p[3].children[i].type.upper()
                        ].lower()
                    ST.curType.append(p[3].children[i].type)
                    # according to akshay TODO
                    offset_string = cal_offset(p[3].children[i])
                    tmp_var, tmp_offset_string = ST.get_tmp_var(arguments)

                    if (
                        ST.curType[-1].split()[-1] != arguments.split()[-1]
                        and p[3].children[i].type.upper() in PRIMITIVE_TYPES
                        and arguments.upper() in PRIMITIVE_TYPES
                    ):
                        ST.error(
                            Error(
                                p[1].lno,
                                rule_name,
                                "warning",
                                f"Type mismatch in argument {i+1} of function call. Expected: {arguments}, Received: {ST.curType[-1]}",
                            )
                        )
                        code_gen.append(
                            [
                                f"{ST.curType[-1]}2{arguments}",
                                tmp_var,
                                p[3].children[i].val,
                                " ",
                            ]
                        )
                        activation_record.append(
                            [
                                f"{ST.curType[-1]}2{arguments}",
                                tmp_offset_string,
                                offset_string,
                                " ",
                            ]
                        )

                    elif (p[3].children[i].type.upper() in PRIMITIVE_TYPES) ^ (
                        arguments.upper() in PRIMITIVE_TYPES
                    ):
                        ST.error(
                            Error(
                                p[1].lno,
                                rule_name,
                                "compilation error",
                                f"Type mismatch in argument {i+1} of function call. Expected: {arguments}, Received: {ST.curType[-1]}",
                            )
                        )
                        return

                    elif (
                        ST.curType[-1] != arguments
                        and p[3].children[i].type.upper() not in PRIMITIVE_TYPES
                        and arguments.upper() not in PRIMITIVE_TYPES
                    ):
                        ST.error(
                            Error(
                                p[1].lno,
                                rule_name,
                                "compilation error",
                                f"Type mismatch in argument {i+1} of function call. Expected: {arguments}, Received: {ST.curType[-1]}",
                            )
                        )
                        return

                    else:
                        code_gen.append(
                            [f"{arguments}=", tmp_var, p[3].children[i].val, ""]
                        )
                        activation_record.append(
                            [f"{arguments}=", tmp_offset_string, offset_string, "",]
                        )

                    temp_3ac.append(
                        [f"param", p[1].val, tmp_var, " ",]
                    )
                    temp_act.append([f"param", p[1].val, f"{func_offset}($fp)", " "])
                    if p[1].type.upper() in PRIMITIVE_TYPES or p[1].type.endswith("*"):
                        func_offset += 8
                    else:
                        t = get_data_type_size(arguments)
                        t += (8 - t % 8) % 8
                        func_offset += t
                    i -= 1

                for t3ac, tact in zip(temp_3ac, temp_act):
                    code_gen.append(t3ac)
                    activation_record.append(tact)

                func_size = 0
                offset_update = 0
                for scope_table in ST.scope_tables:
                    if scope_table.name == p[1].val:
                        for node in scope_table.nodes:
                            func_size += node.size

                code_gen.append([f"call_{func_size}", p[1].val, "", ""])
                activation_record.append(
                    [f"call_{func_size}", p[1].val, "", f"__{p[1].val}"]
                )


def p_argument_expression_list(p):
    """argument_expression_list : assignment_expression
    | argument_expression_list COMMA assignment_expression
    """
    rule_name = "argument_expression_list"
    if len(p) == 2:
        p[0] = Node(
            name="ArgumentExpressionList",
            val="",
            lno=p[1].lno,
            type=p[1].type,
            children=[p[1]],
        )
        p[0].ast = p[1].ast
        # p[0].ast = build_AST(p, rule_name)
    else:
        # check if name will always be equal to ArgumentExpressionList
        # heavy doubt
        p[0] = p[1]
        p[0].children.append(p[3])
        p[0].ast = build_AST_2(p, [1, 3], ",")
        # p[0].ast = build_AST(p, rule_name)


def p_unary_expression(p):
    """unary_expression : postfix_expression
    | INC_OP unary_expression
    | DEC_OP unary_expression
    | unary_operator cast_expression
    | SIZEOF unary_expression
    | SIZEOF LEFT_BRACKET type_name RIGHT_BRACKET
    """
    rule_name = "unary_expression"
    if len(p) == 2:

        if len(p[1].array) > 1 and isinstance(p[1].array[1], int):

            ST.error(
                Error(
                    p[1].lno,
                    rule_name,
                    "compilation error",
                    f"Cannot assign or operate with an array indexed with level greater than 1",
                )
            )
            p[0] = p[1]

        elif len(p[1].array) > 0 and isinstance(p[1].array[0], int):
            p[0] = p[1]
            p[0].array = []
            # print(p[0].index, "1")
            v2, v2_offset_string = ST.get_tmp_var(p[1].type)
            # p[]
            # code_gen.append(["OKAY"])
            code_gen.append(["addr", v2, p[1].place, ""])
            code_gen.append(["long-", v2, code_gen[-2][1], v2])
            offset_string = cal_offset(p[1])
            activation_record.append(
                ["addr", v2_offset_string, offset_string[0:-5], ""]
            )
            activation_record.append(
                ["long-", v2_offset_string, code_gen[-2][1], v2_offset_string]
            )
            p[0].val = p[0].place = v2
        else:
            p[0] = p[1]
        p[0].ast = build_AST(p, rule_name)

    elif len(p) == 3:
        offset_string = cal_offset(p[2])
        if p[1].val == "++" or p[1].val == "--":
            if len(p[2].array) > 0 and isinstance(p[2].array[0], int):
                ST.error(
                    Error(
                        p[1].lno,
                        rule_name,
                        "compilation error",
                        f"Array {p[2].val} pointer increment",
                    )
                )
            tempNode = Node(name="", val=p[1], lno=p[2].lno, type="", children="")

            p[0] = Node(
                name="UnaryOperation" + p[1],
                val=p[2].val,
                lno=p[2].lno,
                type=p[2].type,
                children=[tempNode, p[2]],
                place=p[2].place,
                level=p[2].level,
                lhs=1,
                offset=p[2].offset,
            )
            check_identifier(p[2], p.lineno(2))

            # DONE: FLOAT not supported yet and neither are pointers dhang se
            if p[1].val == "++":
                if p[2].type.endswith("*"):
                    code_gen.append(
                        [
                            "long-",
                            p[2].place,
                            p[2].place,
                            str(get_data_type_size(p[2].type[:-2])),
                        ]
                    )
                    activation_record.append(
                        [
                            "long-",
                            offset_string,
                            offset_string,
                            str(get_data_type_size(p[2].type[:-2])),
                        ]
                    )
                else:
                    code_gen.append([p[2].type + "+", p[2].place, p[2].place, "1"])
                    activation_record.append(
                        [p[2].type + "+", offset_string, offset_string, "1",]
                    )

                # code_gen.append(f"{p[1].place} := {p[1].place} + 1")
            elif p[1].val == "--":
                if p[2].type.endswith("*"):
                    code_gen.append(
                        [
                            "long-",
                            p[2].place,
                            p[2].place,
                            -get_data_type_size(p[2].type[:-2]),
                        ]
                    )
                    activation_record.append(
                        [
                            "long-",
                            offset_string,
                            offset_string,
                            str(get_data_type_size(p[2].type[:-2])),
                        ]
                    )
                else:
                    code_gen.append([p[2].type + "+", p[2].place, p[2].place, "-1"])
                    activation_record.append(
                        [p[2].type + "+", offset_string, offset_string, "1",]
                    )

                # code_gen.append(f"{p[1].place} := {p[1].place} - 1")
            #
            # code_gen.append()
            # p[0].ast = build_AST(p, rule_name)

        elif p[1].val == "sizeof":
            # MODIFIED
            tmp_var, tmp_offset_string = ST.get_tmp_var("int")

            p[0] = Node(
                name="SizeOf",
                val=tmp_var,
                lno=p[2].lno,
                type="int",
                children=[p[2]],
                place=tmp_var,
                lhs=1,
                offset=p[2].offset,
            )

            # p[0].ast = build_AST(p, rule_name)
            type_size = get_data_type_size(p[2].type)
            if type_size == -1:
                ST.error(
                    Error(
                        p.lineno(1),
                        rule_name,
                        "Syntax error",
                        f"Size of doesn't exist for '{p[2].type}' type",
                    )
                )
            code_gen.append(["4=", tmp_var, type_size])
            activation_record.append(["4=", tmp_offset_string, type_size])

        elif p[1].val == "&":
            # TODO:3ac
            p[0] = Node(
                name="AddressOfVariable",
                val=p[2].val,
                lno=p[2].lno,
                type=p[2].type + " *",
                level=p[1].level + 1,
                children=[p[2]],
                lhs=1,
                offset=p[2].offset,
            )
            temp_var, tmp_offset_string = ST.get_tmp_var(p[2].type + " *")
            p[0].place = temp_var
            code_gen.append(["addr", temp_var, p[2].place, ""])
            activation_record.append(
                ["addr", tmp_offset_string, offset_string[0:-5], ""]
            )

        elif p[1].val == "*":
            # TODO:3ac
            if not p[2].type.endswith("*"):
                ST.error(
                    Error(
                        p[1].lno,
                        rule_name,
                        "compilation error",
                        f"Cannot dereference variable of type {p[2].type}",
                    )
                )
            p[0] = Node(
                name="PointerVariable",
                val=p[2].val,
                lno=p[2].lno,
                children=[p[2]],
                level=p[2].level - 1,
                type=p[2].type[:-2],
                offset=p[2].offset,
            )
            temp_var, tmp_offset_string = ST.get_tmp_var(p[2].type[:-2])
            p[0].place = temp_var
            p[0].addr = p[2].place
            type1 = p[2].type[:-2]
            if type1.upper() in PRIMITIVE_TYPES:
                code_gen.append(
                    [f"{get_data_type_size(type1)}load", temp_var, p[2].place, ""]
                )
                activation_record.append(
                    [
                        f"{get_data_type_size(type1)}load",
                        tmp_offset_string,
                        offset_string,
                        "",
                    ]
                )
            else:
                # print(p[2].level)
                if p[2].level > 1:
                    code_gen.append(
                        ["long^", temp_var, p[2].place, "0",]
                    )
                    activation_record.append(
                        ["long^", tmp_offset_string, offset_string, "0",]
                    )
                else:
                    code_gen.append(
                        [
                            f"{get_data_type_size(type1)}non_primitive_load",
                            temp_var,
                            p[2].place,
                            "",
                        ]
                    )
                    activation_record.append(
                        [
                            f"{get_data_type_size(type1)}non_primitive_load",
                            tmp_offset_string,
                            offset_string,
                            "",
                        ]
                    )
            ## load instruction may be redundant or not required sometimes

            p[0].addr = p[2].place

        elif p[1].val == "-":
            if p[2].type.upper() not in PRIMITIVE_TYPES:
                ST.error(
                    Error(
                        p[1].lno,
                        rule_name,
                        "compilation error",
                        f"Unary minus is not allowed for  {p[2].type}",
                    )
                )
            tmp_var, tmp_offset_string = ST.get_tmp_var(p[2].type)
            p[0] = Node(
                name="UnaryOperationMinus",
                val=tmp_var,
                lno=p[2].lno,
                type=p[2].type,
                children=[p[2]],
                place=tmp_var,
                level=p[2].level,
                lhs=1,
                offset=p[2].offset,
            )
            code_gen.append([p[2].type + "_uminus", tmp_var, "0", p[2].place])
            activation_record.append(
                [p[2].type + "_uminus", tmp_offset_string, "0", offset_string,]
            )

        elif p[1].val == "+":
            if p[2].type.upper() not in PRIMITIVE_TYPES:
                ST.error(
                    Error(
                        p[1].lno,
                        rule_name,
                        "compilation error",
                        f"Unary plus is not allowed for  {p[2].type}",
                    )
                )
            p[0] = p[2]
        elif p[1].val == "~":
            if p[2].type.upper() not in TYPE_CHAR + TYPE_INTEGER:
                ST.error(
                    Error(
                        p[1].lno,
                        rule_name,
                        "compilation error",
                        f"{p[1].val} is not allowed for  {p[2].type}",
                    )
                )
            else:
                tmp_var, tmp_offset_string = ST.get_tmp_var(p[2].type)
                p[0] = Node(
                    name="UnaryOperationBitwiseNot",
                    val=tmp_var,
                    lno=p[2].lno,
                    type=p[2].type,
                    children=[p[2]],
                    place=tmp_var,
                    lhs=1,
                    level=p[2].level,
                    offset=p[2].offset,
                )
                code_gen.append([p[2].type + "~", tmp_var, p[2].place, ""])
                activation_record.append(
                    [p[2].type + "~", tmp_offset_string, offset_string, "",]
                )

        elif p[1].val == "!":
            # print(p[2].type, p[2].place)
            if p[2].type.upper() not in TYPE_CHAR + TYPE_INTEGER:
                ST.error(
                    Error(
                        p[1].lno,
                        rule_name,
                        "compilation error",
                        f"{p[1].val} is not allowed for  {p[2].type}",
                    )
                )
            else:
                tmp_var, tmp_offset_string = ST.get_tmp_var(p[2].type)
                p[0] = Node(
                    name="UnaryOperationLogicalNot",
                    val=tmp_var,
                    lno=p[2].lno,
                    type="int",
                    children=[p[2]],
                    place=tmp_var,
                    lhs=1,
                    level=p[2].level,
                    offset=p[2].offset,
                )
                label1 = ST.get_tmp_label()
                label2 = ST.get_tmp_label()
                # print(p[2].place, 1)
                code_gen.append(["beq", p[2].place, "0", label1])
                code_gen.append(["4=", tmp_var, "1", ""])
                code_gen.append(["goto", "", "", label2])
                code_gen.append(["label", label1, ":", ""])
                code_gen.append(["4=", tmp_var, "0", ""])
                code_gen.append(["label", label2, ":", ""])

                activation_record.append(["beq", offset_string, "0", label1])
                activation_record.append(["4=", tmp_offset_string, "1", ""])
                activation_record.append(["goto", "", "", label2])
                activation_record.append(["label", label1, ":", ""])
                activation_record.append(["4=", tmp_offset_string, "0", ""])
                activation_record.append(["label", label2, ":", ""])

                # code_gen.append([p[2].type + "!", tmp_var, p[2].place, ""])
        elif p[1].val not in ["!", "+"] and p[2].type.upper() not in PRIMITIVE_TYPES:
            ST.error(
                Error(
                    p[1].lno,
                    rule_name,
                    "compilation error",
                    f"{p[1].val} is not allowed for  {p[2].type}",
                )
            )
            p[0] = Node(
                name="UnaryOperation",
                val=p[2].val,
                lno=p[2].lno,
                type=p[2].type,
                children=[],
                lhs=1,
                offset=p[2].offset,
            )
        p[0].ast = build_AST(p, rule_name)
    else:
        # MODIFIED
        tmp_var, tmp_offset_string = ST.get_tmp_var("int")
        # p[0] = Node(
        #     name="SizeOf",
        #     val=tmp_var,
        #     lno=p[3].lno,
        #     type="int",
        #     children=[p[3]],
        #     place=tmp_var,
        #     lhs=1,
        #     offset=0,
        # )
        node = ST.find(tmp_var)
        node.children = [p[3]]
        node.lno = p[3].lno
        node.lhs = 1
        node.name = "SizeOf"
        p[0] = node
        # p[0].ast = build_AST(p, rule_name)
        type_size = get_data_type_size(p[3].type)
        if type_size == -1:
            ST.error(
                Error(
                    p.lineno(1),
                    rule_name,
                    "Syntax error",
                    f"Size of doesn't exist for '{p[3].type}' type",
                )
            )
        code_gen.append(["4=", tmp_var, str(type_size)])
        activation_record.append(["4=", tmp_offset_string, str(type_size)])

        p[0].ast = build_AST_2(p, [1, 3], p[2])


def p_unary_operator(p):
    """unary_operator : BITWISE_AND
    | MULTIPLY
    | PLUS
    | MINUS
    | BITWISE_NOT
    | LOGICAL_NOT
    """
    rule_name = "unary_operator"
    p[0] = Node(
        name="UnaryOperator",
        val=p[1],
        lno=p.lineno(1),
        type="",
        children=[],
        place=p[1],
    )
    # p[0].ast = build_AST(p, rule_name)


def p_cast_expression(p):
    """cast_expression : unary_expression
    | LEFT_BRACKET type_name RIGHT_BRACKET cast_expression
    """
    rule_name = "cast_expression"
    if len(p) == 2:
        p[0] = p[1]
        # p[0].ast = build_AST(p, rule_name)
    else:
        # confusion about val

        if p[2].type == p[4].type:
            p[0] = p[4]
            return
        if p[2].type.startswith("struct ") and p[4].type.startswith("struct "):
            ST.error(
                Error(
                    p.lineno(1),
                    rule_name,
                    "Syntax error",
                    f"Cannot cast {p[2].type} to {p[4].type}",
                )
            )
        elif p[2].type.startswith("struct ") or p[4].type.startswith("struct "):
            ST.error(
                Error(
                    p.lineno(1),
                    rule_name,
                    "Syntax error",
                    f"Cannot cast {p[2].type} to {p[4].type}",
                )
            )
        # print(p[2].type, p[4].type)
        # TODO: EXPLICIT TYPE CONVERSION of pointers of different levels
        # till now it has not been done
        if p[2].type.count("*") != p[4].type.count("*"):
            ST.error(
                Error(
                    p.lineno(1),
                    rule_name,
                    "Syntax error",
                    f"Cannot cast {p[2].type} to {p[4].type} as pointer levels are different",
                )
            )
        tmp_var, tmp_offset_string = ST.get_tmp_var(p[2].type)
        p[0] = Node(
            name="TypeCasting",
            val=p[2].val,
            lno=p[2].lno,
            type=p[2].type,
            level=p[2].type.count("*"),
            children=[],
            place=tmp_var,
            offset=p[4].offset,
        )
        offset_string = cal_offset(p[4])
        code_gen.append([f"{p[4].type}2{p[2].type}", tmp_var, p[4].place, " "])
        activation_record.append(
            [f"{p[4].type}2{p[2].type}", tmp_offset_string, offset_string, " ",]
        )

        # p[0].ast = build_AST(p, rule_name)
        p[0].ast = build_AST_2(p, [2, 4], "()")


def p_multipicative_expression(p):
    """multiplicative_expression : cast_expression
    | multiplicative_expression MULTIPLY cast_expression
    | multiplicative_expression DIVIDE cast_expression
    | multiplicative_expression MOD cast_expression
    """
    if len(p) == 2:
        p[0] = p[1]
        # p[0].ast = build_AST(p, rule_name)
    else:
        rule_name = p[2]
        _op = p[2][0] if p[2] is tuple else p[2]
        p[0] = type_util(p[1], p[3], _op)

        if is_const(p[1].place) and is_const(p[3].place):
            if p[2] == "*":
                if p[0].type.upper() in TYPE_FLOAT:
                    p[0].place = float(p[1].place) * float(p[3].place)
                else:
                    p[0].place = int(p[1].place) * int(p[3].place)

            elif p[2] == "/":
                if p[0].type.upper() in TYPE_FLOAT:
                    p[0].place = float(p[1].place) / float(p[3].place)
                else:
                    p[0].place = int(p[1].place) // int(p[3].place)

            else:
                p[0].place = int(p[1].place) % int(p[3].place)

            p[0].place = str(p[0].place)
        else:
            tmp_var1 = p[1].place
            tmp_var3 = p[3].place
            offset_string1 = cal_offset(p[1])
            offset_string3 = cal_offset(p[3])
            tmp_offset_string1 = offset_string1
            tmp_offset_string3 = offset_string3

            if p[1].type != p[0].type:
                tmp_var1, tmp_offset_string1 = ST.get_tmp_var(p[0].type)
                code_gen.append([p[1].type + "2" + p[0].type, tmp_var1, p[1].place])
                activation_record.append(
                    [p[1].type + "2" + p[0].type, tmp_offset_string1, offset_string1,]
                )

            if p[3].type != p[0].type:
                tmp_var3, tmp_offset_string3 = ST.get_tmp_var(p[0].type)
                code_gen.append([p[3].type + "2" + p[0].type, tmp_var3, p[3].place])
                activation_record.append(
                    [
                        p[3].type + "2" + p[0].type,
                        tmp_offset_string3,
                        p[3].place + offset_string3,
                    ]
                )

            code_gen.append([p[0].type + _op, p[0].place, tmp_var1, tmp_var3])
            activation_record.append(
                [
                    p[0].type + _op,
                    cal_offset(p[0]),
                    tmp_offset_string1,
                    tmp_offset_string3,
                ]
            )
        p[0].ast = build_AST_2(p, [1, 3], rule_name)


def p_additive_expression(p):
    """additive_expression : multiplicative_expression
    | additive_expression PLUS multiplicative_expression
    | additive_expression MINUS multiplicative_expression
    """
    if len(p) == 2:
        p[0] = p[1]
        # p[0].ast = build_AST(p, rule_name)
    else:
        rule_name = p[2]
        _op = p[2][0] if p[2] is tuple else p[2]
        p[0] = type_util(p[1], p[3], _op)
        if is_const(p[1].place) and is_const(p[3].place):
            if p[2] == "+":
                if p[0].type.upper() in TYPE_FLOAT:
                    p[0].place = float(p[1].place) + float(p[3].place)
                else:
                    p[0].place = int(p[1].place) + int(p[3].place)

            else:
                if p[0].type.upper() in TYPE_FLOAT:
                    p[0].place = float(p[1].place) - float(p[3].place)
                else:
                    p[0].place = int(p[1].place) - int(p[3].place)
            p[0].place = str(p[0].place)

        else:
            tmp_var1 = p[1].place
            tmp_var3 = p[3].place
            offset_string1 = cal_offset(p[1])
            offset_string3 = cal_offset(p[3])
            tmp_offset_string1 = offset_string1
            tmp_offset_string3 = offset_string3
            if p[1].type != p[0].type:
                tmp_var1, tmp_offset_string1 = ST.get_tmp_var(p[0].type)
                code_gen.append([p[1].type + "2" + p[0].type, tmp_var1, p[1].place])
                activation_record.append(
                    [p[1].type + "2" + p[0].type, tmp_offset_string1, offset_string1,]
                )

            if p[3].type != p[0].type:
                tmp_var3, tmp_offset_string3 = ST.get_tmp_var(p[0].type)
                code_gen.append([p[3].type + "2" + p[0].type, tmp_var3, p[3].place])
                activation_record.append(
                    [p[3].type + "2" + p[0].type, tmp_offset_string3, offset_string3,]
                )

            code_gen.append([p[0].type + _op, p[0].place, tmp_var1, tmp_var3])
            activation_record.append(
                [
                    p[0].type + _op,
                    cal_offset(p[0]),
                    tmp_offset_string1,
                    tmp_offset_string3,
                ]
            )
        p[0].ast = build_AST_2(p, [1, 3], rule_name)


def p_shift_expression(p):
    """shift_expression : additive_expression
    | shift_expression LEFT_OP additive_expression
    | shift_expression RIGHT_OP additive_expression
    """
    if len(p) == 2:
        p[0] = p[1]
        # p[0].ast = build_AST(p, rule_name)
    else:
        rule_name = p[2]
        _op = p[2][0] if p[2] is tuple else p[2]
        p[0] = type_util(p[1], p[3], _op)
        if is_const(p[1].place) and is_const(p[3].place):
            if p[2] == "<<":
                p[0].place = int(p[1].place) << int(p[3].place)
            else:
                p[0].place = int(p[1].place) >> int(p[3].place)
            p[0].place = str(p[0].place)

        else:
            tmp_var1 = p[1].place
            tmp_var3 = p[3].place
            offset_string1 = cal_offset(p[1])
            offset_string3 = cal_offset(p[3])
            tmp_offset_string1 = offset_string1
            tmp_offset_string3 = offset_string3

            if p[1].type != p[0].type:
                tmp_var1, tmp_offset_string1 = ST.get_tmp_var(p[0].type)
                code_gen.append([p[1].type + "2" + p[0].type, tmp_var1, p[1].place])
                activation_record.append(
                    [p[1].type + "2" + p[0].type, tmp_offset_string1, offset_string1,]
                )

            if p[3].type != p[0].type:
                tmp_var3, tmp_offset_string3 = ST.get_tmp_var(p[0].type)
                code_gen.append([p[3].type + "2" + p[0].type, tmp_var3, p[3].place])
                activation_record.append(
                    [p[3].type + "2" + p[0].type, tmp_offset_string3, offset_string3,]
                )

            code_gen.append([p[0].type + _op, p[0].place, tmp_var1, tmp_var3])
            activation_record.append(
                [
                    p[0].type + _op,
                    cal_offset(p[0]),
                    tmp_offset_string1,
                    tmp_offset_string3,
                ]
            )
        p[0].ast = build_AST_2(p, [1, 3], rule_name)


def p_relational_expression(p):
    """relational_expression : shift_expression
    | relational_expression LESS shift_expression
    | relational_expression GREATER shift_expression
    | relational_expression LE_OP shift_expression
    | relational_expression GE_OP shift_expression
    """
    if len(p) == 2:
        p[0] = p[1]
        # p[0].ast = build_AST(p, rule_name)
    else:
        rule_name = p[2]
        _op = p[2][0] if p[2] is tuple else p[2]
        p[0] = type_util(p[1], p[3], _op)

        if is_const(p[1].place) and is_const(p[3].place):
            if p[2] == "<":
                if p[0].type.upper() in TYPE_FLOAT:
                    p[0].place = "1" if float(p[1].place) < float(p[3].place) else "0"
                else:
                    p[0].place = "1" if int(p[1].place) < int(p[3].place) else "0"

            elif p[2] == "<=":
                if p[0].type.upper() in TYPE_FLOAT:
                    p[0].place = "1" if float(p[1].place) <= float(p[3].place) else "0"
                else:
                    p[0].place = "1" if int(p[1].place) <= int(p[3].place) else "0"

            elif p[2] == ">":
                if p[0].type.upper() in TYPE_FLOAT:
                    p[0].place = "1" if float(p[1].place) > float(p[3].place) else "0"
                else:
                    p[0].place = "1" if int(p[1].place) > int(p[3].place) else "0"

            elif p[2] == ">=":
                if p[0].type.upper() in TYPE_FLOAT:
                    p[0].place = "1" if float(p[1].place) >= float(p[3].place) else "0"
                else:
                    p[0].place = "1" if int(p[1].place) >= int(p[3].place) else "0"

        else:
            tmp_var1 = p[1].place
            tmp_var3 = p[3].place
            offset_string1 = cal_offset(p[1])
            offset_string3 = cal_offset(p[3])
            tmp_offset_string1 = offset_string1
            tmp_offset_string3 = offset_string3

            if p[1].type != p[0].type:
                tmp_var1, tmp_offset_string1 = ST.get_tmp_var(p[0].type)
                code_gen.append([p[1].type + "2" + p[0].type, tmp_var1, p[1].place])
                activation_record.append(
                    [p[1].type + "2" + p[0].type, tmp_offset_string1, offset_string1,]
                )

            if p[3].type != p[0].type:
                tmp_var3, tmp_offset_string3 = ST.get_tmp_var(p[0].type)
                code_gen.append([p[3].type + "2" + p[0].type, tmp_var3, p[3].place])
                activation_record.append(
                    [p[3].type + "2" + p[0].type, tmp_offset_string3, offset_string3,]
                )

            code_gen.append([p[0].type + _op, p[0].place, tmp_var1, tmp_var3])
            activation_record.append(
                [
                    p[0].type + _op,
                    cal_offset(p[0]),
                    tmp_offset_string1,
                    tmp_offset_string3,
                ]
            )
        p[0].ast = build_AST_2(p, [1, 3], rule_name)


def p_equality_expresssion(p):
    """equality_expression : relational_expression
    | equality_expression EQ_OP relational_expression
    | equality_expression NE_OP relational_expression
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        rule_name = p[2]
        _op = p[2][0] if p[2] is tuple else p[2]
        p[0] = type_util(p[1], p[3], _op)
        if is_const(p[1].place) and is_const(p[3].place):
            if p[2] == "==":
                if p[0].type.upper() in TYPE_FLOAT:
                    p[0].place = float(p[1].place) == float(p[3].place)
                else:
                    p[0].place = int(p[1].place) == int(p[3].place)

            else:
                if p[0].type.upper() in TYPE_FLOAT:
                    p[0].place = float(p[1].place) != float(p[3].place)
                else:
                    p[0].place = int(p[1].place) != int(p[3].place)
            p[0].place = str(p[0].place)

        else:
            tmp_var1 = p[1].place
            tmp_var3 = p[3].place
            offset_string1 = cal_offset(p[1])
            offset_string3 = cal_offset(p[3])
            tmp_offset_string1 = offset_string1
            tmp_offset_string3 = offset_string3

            if p[1].type != p[0].type:
                tmp_var1, tmp_offset_string1 = ST.get_tmp_var(p[0].type)
                code_gen.append([p[1].type + "2" + p[0].type, tmp_var1, p[1].place])
                activation_record.append(
                    [p[1].type + "2" + p[0].type, tmp_offset_string1, offset_string1,]
                )

            if p[3].type != p[0].type:
                tmp_var3, tmp_offset_string3 = ST.get_tmp_var(p[0].type)
                code_gen.append([p[3].type + "2" + p[0].type, tmp_var3, p[3].place])
                activation_record.append(
                    [p[3].type + "2" + p[0].type, tmp_offset_string3, offset_string3,]
                )

            code_gen.append([p[0].type + _op, p[0].place, tmp_var1, tmp_var3])
            activation_record.append(
                [
                    p[0].type + _op,
                    cal_offset(p[0]),
                    tmp_offset_string1,
                    tmp_offset_string3,
                ]
            )
        p[0].ast = build_AST_2(p, [1, 3], rule_name)


def p_and_expression(p):
    """and_expression : equality_expression
    | and_expression BITWISE_AND equality_expression
    """
    if len(p) == 2:
        p[0] = p[1]
        # p[0].ast = build_AST(p, rule_name)
    else:
        rule_name = p[2]
        _op = p[2][0] if p[2] is tuple else p[2]
        p[0] = type_util(p[1], p[3], _op)
        p[0].type = "int"  ##forced
        if is_const(p[1].place) and is_const(p[3].place):
            p[0].place = int(p[1].place) & int(p[3].place)
            p[0].place = str(p[0].place)

        else:
            tmp_var1 = p[1].place
            tmp_var3 = p[3].place
            offset_string1 = cal_offset(p[1])
            offset_string3 = cal_offset(p[3])
            tmp_offset_string1 = offset_string1
            tmp_offset_string3 = offset_string3

            if p[1].type != p[0].type:
                tmp_var1, tmp_offset_string1 = ST.get_tmp_var(p[0].type)
                code_gen.append([p[1].type + "2" + p[0].type, tmp_var1, p[1].place])
                activation_record.append(
                    [p[1].type + "2" + p[0].type, tmp_offset_string1, offset_string1,]
                )

            if p[3].type != p[0].type:
                tmp_var3, tmp_offset_string3 = ST.get_tmp_var(p[0].type)
                code_gen.append([p[3].type + "2" + p[0].type, tmp_var3, p[3].place])
                activation_record.append(
                    [p[3].type + "2" + p[0].type, tmp_offset_string3, offset_string3,]
                )

            code_gen.append([p[0].type + _op, p[0].place, tmp_var1, tmp_var3])
            activation_record.append(
                [
                    p[0].type + _op,
                    cal_offset(p[0]),
                    tmp_offset_string1,
                    tmp_offset_string3,
                ]
            )
        p[0].ast = build_AST_2(p, [1, 3], rule_name)


def p_exclusive_or_expression(p):
    """exclusive_or_expression : and_expression
    | exclusive_or_expression BITWISE_XOR and_expression
    """
    if len(p) == 2:
        p[0] = p[1]
        # p[0].ast = build_AST(p, rule_name)
    else:
        rule_name = p[2]
        _op = p[2][0] if p[2] is tuple else p[2]
        p[0] = type_util(p[1], p[3], _op)
        if is_const(p[1].place) and is_const(p[3].place):
            p[0].place = int(p[1].place) ^ int(p[3].place)
            p[0].place = str(p[0].place)

        else:
            tmp_var1 = p[1].place
            tmp_var3 = p[3].place
            offset_string1 = cal_offset(p[1])
            offset_string3 = cal_offset(p[3])
            tmp_offset_string1 = offset_string1
            tmp_offset_string3 = offset_string3

            if p[1].type != p[0].type:
                tmp_var1, tmp_offset_string1 = ST.get_tmp_var(p[0].type)
                code_gen.append([p[1].type + "2" + p[0].type, tmp_var1, p[1].place])
                activation_record.append(
                    [p[1].type + "2" + p[0].type, tmp_offset_string1, offset_string1,]
                )

            if p[3].type != p[0].type:
                tmp_var3, tmp_offset_string3 = ST.get_tmp_var(p[0].type)
                code_gen.append([p[3].type + "2" + p[0].type, tmp_var3, p[3].place])
                activation_record.append(
                    [p[3].type + "2" + p[0].type, tmp_offset_string3, offset_string3,]
                )

            code_gen.append([p[0].type + _op, p[0].place, tmp_var1, tmp_var3])
            activation_record.append(
                [
                    p[0].type + _op,
                    cal_offset(p[0]),
                    tmp_offset_string1,
                    tmp_offset_string3,
                ]
            )
        p[0].ast = build_AST_2(p, [1, 3], rule_name)


def p_inclusive_or_expression(p):
    """inclusive_or_expression : exclusive_or_expression
    | inclusive_or_expression BITWISE_OR exclusive_or_expression
    """
    if len(p) == 2:
        p[0] = p[1]
        # p[0].ast = build_AST(p, rule_name)
    else:
        rule_name = p[2]
        _op = p[2][0] if p[2] is tuple else p[2]
        p[0] = type_util(p[1], p[3], _op)
        if is_const(p[1].place) and is_const(p[3].place):
            p[0].place = int(p[1].place) | int(p[3].place)
            p[0].place = str(p[0].place)

        else:
            tmp_var1 = p[1].place
            tmp_var3 = p[3].place
            offset_string1 = cal_offset(p[1])
            offset_string3 = cal_offset(p[3])
            tmp_offset_string1 = offset_string1
            tmp_offset_string3 = offset_string3

            if p[1].type != p[0].type:
                tmp_var1, tmp_offset_string1 = ST.get_tmp_var(p[0].type)
                code_gen.append([p[1].type + "2" + p[0].type, tmp_var1, p[1].place])
                activation_record.append(
                    [p[1].type + "2" + p[0].type, tmp_offset_string1, offset_string1,]
                )

            if p[3].type != p[0].type:
                tmp_var3, tmp_offset_string3 = ST.get_tmp_var(p[0].type)
                code_gen.append([p[3].type + "2" + p[0].type, tmp_var3, p[3].place])
                activation_record.append(
                    [p[3].type + "2" + p[0].type, tmp_offset_string3, offset_string3,]
                )

            code_gen.append([p[0].type + _op, p[0].place, tmp_var1, tmp_var3])
            activation_record.append(
                [
                    p[0].type + _op,
                    cal_offset(p[0]),
                    tmp_offset_string1,
                    tmp_offset_string3,
                ]
            )
        p[0].ast = build_AST_2(p, [1, 3], rule_name)


def p_logical_and_expression(p):
    """logical_and_expression : inclusive_or_expression
    | logical_and_expression and_m1 LOGICAL_AND_OP inclusive_or_expression and_m2
    """
    if len(p) == 2:
        p[0] = p[1]
        # p[0].ast = build_AST(p, rule_name)
    else:
        rule_name = p[3]
        _op = p[3][0] if p[3] is tuple else p[3]
        p[0] = type_util(p[1], p[4], _op)
        if is_const(p[1].place) and is_const(p[4].place):
            p[0].place = int(p[1].place) and int(p[4].place)
            p[0].place = str(p[0].place)
        else:
            tmp_var1 = p[1].place
            tmp_var3 = p[3].place
            offset_string1 = cal_offset(p[1])
            offset_string3 = cal_offset(p[3])
            tmp_offset_string1 = offset_string1
            tmp_offset_string3 = offset_string3

            if p[1].type != p[0].type:
                tmp_var1, tmp_offset_string1 = ST.get_tmp_var(p[0].type)
                code_gen.append([p[1].type + "2" + p[0].type, tmp_var1, p[1].place])
                activation_record.append(
                    [p[1].type + "2" + p[0].type, tmp_offset_string1, offset_string1,]
                )

            if p[3].type != p[0].type:
                tmp_var3, tmp_offset_string3 = ST.get_tmp_var(p[0].type)
                code_gen.append([p[3].type + "2" + p[0].type, tmp_var3, p[3].place])
                activation_record.append(
                    [p[3].type + "2" + p[0].type, tmp_offset_string3, offset_string3,]
                )

            code_gen.append([p[0].type + _op, p[0].place, tmp_var1, tmp_var3])
            activation_record.append(
                [
                    p[0].type + _op,
                    cal_offset(p[0]),
                    tmp_offset_string1,
                    tmp_offset_string3,
                ]
            )
        p[0].ast = build_AST_2(p, [1, 3], rule_name)


def p_and_m1(p):
    """and_m1 :"""
    label1 = ST.get_tmp_label()
    # code_gen.append(["beq", p[-1].place, "0", label1])
    # p[0] = [label1]


def p_and_m2(p):
    """and_m2 :"""
    # code_gen.append(["label", p[-3][0], ":", ""])


def p_logical_or_expression(p):
    """logical_or_expression : logical_and_expression
    | logical_or_expression or_m1 LOGICAL_OR_OP logical_and_expression or_m2
    """
    if len(p) == 2:
        p[0] = p[1]
        # p[0].ast = build_AST(p, rule_name)
    else:
        rule_name = p[3]
        _op = p[3][0] if p[3] is tuple else p[3]
        p[0] = type_util(p[1], p[4], _op)
        if is_const(p[1].place) and is_const(p[4].place):
            p[0].place = int(p[1].place) or int(p[4].place)
            p[0].place = str(p[0].place)
        else:
            tmp_var1 = p[1].place
            tmp_var3 = p[3].place
            offset_string1 = cal_offset(p[1])
            offset_string3 = cal_offset(p[3])
            tmp_offset_string1 = offset_string1
            tmp_offset_string3 = offset_string3

            if p[1].type != p[0].type:
                tmp_var1, tmp_offset_string1 = ST.get_tmp_var(p[0].type)
                code_gen.append([p[1].type + "2" + p[0].type, tmp_var1, p[1].place])
                activation_record.append(
                    [p[1].type + "2" + p[0].type, tmp_offset_string1, offset_string1,]
                )

            if p[3].type != p[0].type:
                tmp_var3, tmp_offset_string3 = ST.get_tmp_var(p[0].type)
                code_gen.append([p[3].type + "2" + p[0].type, tmp_var3, p[3].place])
                activation_record.append(
                    [p[3].type + "2" + p[0].type, tmp_offset_string3, offset_string3,]
                )

            code_gen.append([p[0].type + _op, p[0].place, tmp_var1, tmp_var3])
            activation_record.append(
                [
                    p[0].type + _op,
                    cal_offset(p[0]),
                    tmp_offset_string1,
                    tmp_offset_string3,
                ]
            )
        p[0].ast = build_AST_2(p, [1, 3], rule_name)


def p_or_m1(p):
    """or_m1 :"""
    # label1 = ST.get_tmp_label()
    # code_gen.append(["bne", p[-1].place, "0", label1])
    # p[0] = [label1]


def p_or_m2(p):
    """or_m2 :"""
    # code_gen.append(["label", p[-3][0], ":", ""])


def p_conditional_expression(p):
    """conditional_expression : logical_or_expression
    | logical_or_expression QUESTION expression COLON conditional_expression
    """
    rule_name = "conditional_expression"
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node(
            name="ConditionalOperation",
            val="",
            lno=p[1].lno,
            type=p[3].type,
            children=[],
        )

        if is_const(p[1].place):
            if int(p[1].place):
                p[0].place = p[3].place
            else:
                p[0].place = p[5].place
        else:
            # TODO:Ternary operator
            pass

        p[0].ast = build_AST_2(p, [3, 5], ":")
        p[0].ast = build_AST_2(p, [1, 0], "?")


def p_assignment_expression(p):
    """assignment_expression : conditional_expression
    | unary_expression assignment_operator assignment_expression
    """
    rule_name = "assignment_expression"

    if len(p) == 2:
        p[0] = p[1]

    else:
        if p[1].lhs == 1:
            ST.error(
                Error(
                    p[1].lno,
                    rule_name,
                    "syntax error",
                    "Left side of assignment cannot be expression",
                )
            )
        if p[1].type == "" or p[3].type == "":
            p[0] = Node(
                name="AssignmentOperation",
                val="",
                lno=p[1].lno,
                type="int",
                children=[],
                place=p[1].place,
            )
            p[0].ast = build_AST_2(p, [1, 3], p[2].val)
            # p[0].ast = build_AST(p, rule_name)
            return
        if p[1].type == "-1" or p[3].type == "-1":
            return
        if "const" in p[1].type.split():
            ST.error(Error(p[1].lno, rule_name, "error", "Modifying const variable"))
        if "struct" in p[1].type.split() or "struct" not in p[3].type.split():
            op1 = "struct" in p[1].type.split()
            op2 = "struct" in p[3].type.split()
            if op1 ^ op2:
                ST.error(
                    Error(
                        p[1].lno,
                        rule_name,
                        "compilation error",
                        f"Cannot assign variable of type {p[3].type} to {p[1].type}",
                    )
                )
            elif op1 and op2 and (p[1].type != p[3].type):
                ST.error(
                    Error(
                        p[1].lno,
                        rule_name,
                        "compilation error",
                        f"Struct {p[3].type}, {p[1].type} are of different types",
                    )
                )
        elif len(p[1].array) > 0 and isinstance(p[1].array[0], int):
            ST.error(
                Error(
                    p[1].lno,
                    rule_name,
                    "compilation error",
                    f"Invalid operation on array pointer {p[1].val}",
                )
            )
        if p[1].level != p[3].level:
            ST.error(
                Error(
                    p[1].lno,
                    rule_name,
                    "compilation error",
                    "Type mismatch in assignment: Pointers of different levels",
                )
            )
        # elif (p[1].level and len(p[1].array) > 0) and (
        #     p[3].level and len(p[3].array) > 0
        # ):
        #     ST.error(
        #         Error(
        #             p[1].lno,
        #             rule_name,
        #             "compilation error",
        #             "Invalid array assignment",
        #         )
        #     )
        elif p[1].type.split()[-1] != p[3].type.split()[-1]:
            ST.error(
                Error(p[1].lno, rule_name, "warning", "Type mismatch in assignment",)
            )

        if len(p[1].parentStruct) > 0:
            node = ST.find(p[1].parentStruct)
            for curr_list in node.field_list:
                if curr_list[1] == p[1].val:
                    if len(curr_list) < 5 and len(p[1].array) == 0:
                        break
                    if len(curr_list) < 5 or (len(curr_list[4]) < len(p[1].array)):
                        ST.error(
                            Error(
                                p[1].lno,
                                rule_name,
                                "compilation error",
                                "Incorrect number of dimensions",
                            )
                        )
                        return

        p1_node = ST.find(p[1].val)
        if (p1_node is not None) and ((p[1].is_func >= 1)):
            ST.error(
                Error(
                    p[1].lno,
                    rule_name,
                    "compilation error",
                    f"Invalid operation on {p[1].val}",
                )
            )
            return
        p3_node = ST.find(p[3].val)
        if (p3_node is not None) and ((p[3].is_func >= 1)):
            ST.error(
                Error(
                    p[1].lno,
                    rule_name,
                    "compilation error",
                    f"Invalid operation on {p[3].val}",
                )
            )
            return

        if p[2].val != "=":
            if ("struct" in p[1].type.split()) or ("struct" in p[3].type.split()):
                ST.error(
                    Error(
                        p[1].lno,
                        rule_name,
                        "compilation error",
                        f"Invalid operation on {p[1].val}",
                    )
                )
                return
        p[0] = Node(
            name="AssignmentOperation",
            val=p[1].val,
            type=p[1].type,
            lno=p[1].lno,
            children=[],
            level=p[1].level,
        )
        temp_node = p[3]
        # print(temp_node)
        offset_string1 = cal_offset(p[1])
        offset_string3 = cal_offset(p[3])

        if p[2].val != "=":
            _op = p[2].val[:-1]
            temp_node = type_util(p[1], p[3], _op)
            tmp_var1 = p[1].place
            tmp_var3 = p[3].place
            tmp_offset_string1 = offset_string1
            tmp_offset_string3 = offset_string3
            temp_offset_string = cal_offset(temp_node)

            if p[1].type != temp_node.type:
                tmp_var1, tmp_offset_string1 = ST.get_tmp_var(temp_node.type)
                code_gen.append(
                    [p[1].type + "2" + temp_node.type, tmp_var1, p[1].place]
                )
                activation_record.append(
                    [
                        p[1].type + "2" + temp_node.type,
                        tmp_offset_string1,
                        offset_string1,
                    ]
                )
            if p[3].type != temp_node.type:
                tmp_var3, tmp_offset_string3 = ST.get_tmp_var(p[0].type)
                code_gen.append(
                    [p[3].type + "2" + temp_node.type, tmp_var3, p[3].place]
                )
                activation_record.append(
                    [
                        p[3].type + "2" + temp_node.type,
                        tmp_offset_string3,
                        offset_string3,
                    ]
                )
            code_gen.append([temp_node.type + _op, temp_node.place, tmp_var1, tmp_var3])
            activation_record.append(
                [
                    temp_node.type + _op,
                    temp_offset_string,
                    tmp_offset_string1,
                    tmp_offset_string3,
                ]
            )

            if p[0].type != temp_node.type:
                temp_node1, tmp_offset_string = ST.get_tmp_var(p[0].type)
                code_gen.append(
                    [temp_node.type + "2" + p[0].type, temp_node1, p[1].place]
                )
                activation_record.append(
                    [
                        temp_node.type + "2" + p[0].type,
                        tmp_offset_string,
                        offset_string1,
                    ]
                )
                if len(p[1].array) == 0 and p[1].name != "PointerVariable":
                    code_gen.append([p[0].type + "=", p[1].place, temp_node1, ""])
                    activation_record.append(
                        [p[0].type + "=", offset_string1, tmp_offset_string, "",]
                    )
                else:
                    code_gen.append([p[0].type + "=", p[1].addr, temp_node1, "*"])
                    activation_record.append(
                        [p[0].type + "=", offset_string1, tmp_offset_string, "*",]
                    )
            else:
                if len(p[1].array) == 0 and p[1].name != "PointerVariable":
                    code_gen.append(
                        [temp_node.type + "=", p[1].place, temp_node.place, ""]
                    )
                    activation_record.append(
                        [temp_node.type + "=", offset_string1, temp_offset_string, "",]
                    )
                else:
                    code_gen.append(
                        [temp_node.type + "=", p[1].addr, temp_node.place, "*"]
                    )
                    activation_record.append(
                        [temp_node.type + "=", offset_string1, temp_offset_string, "*",]
                    )

        else:
            if p[0].type != temp_node.type:
                temp_node1, tmp_offset_string = ST.get_tmp_var(p[0].type)
                code_gen.append(
                    [temp_node.type + "2" + p[0].type, temp_node1, p[3].place]
                )
                activation_record.append(
                    [
                        temp_node.type + "2" + p[0].type,
                        tmp_offset_string,
                        offset_string3,
                    ]
                )

                if len(p[1].array) == 0 and p[1].name != "PointerVariable":
                    code_gen.append([p[0].type + "=", p[1].place, temp_node1, ""])
                    activation_record.append(
                        [p[0].type + "=", offset_string1, tmp_offset_string, "",]
                    )

                else:
                    code_gen.append([p[0].type + "=", p[1].addr, temp_node1, "*"])
                    activation_record.append(
                        [p[0].type + "=", offset_string1, tmp_offset_string, "",]
                    )

            else:
                if len(p[1].array) == 0 and p[1].name != "PointerVariable":
                    # print("if", p[0].type, temp_node.type)

                    code_gen.append(
                        [temp_node.type + "=", p[1].place, temp_node.place, ""]
                    )
                    if temp_node.type.endswith("*"):
                        activation_record.append(
                            ["long=", offset_string1, offset_string3, "",]
                        )
                    elif temp_node.type.startswith("struct "):
                        activation_record.append(
                            [
                                ";",
                                temp_node.type + "=",
                                offset_string1,
                                offset_string3,
                                "",
                            ]
                        )
                        size_of_struct = ST.find(temp_node.type).size
                        for long_offset in range(0, size_of_struct, 8):
                            activation_record.append(
                                [
                                    "long=",
                                    f"{int(offset_string1[0:-5])-long_offset}($fp)",
                                    f"{int(offset_string3[0:-5])-long_offset}($fp)",
                                    "",
                                ]
                            )

                    else:
                        activation_record.append(
                            [temp_node.type + "=", offset_string1, offset_string3, "",]
                        )
                else:
                    # ARKA DOUBTS
                    print("else", p[0].type, temp_node.type)
                    code_gen.append(
                        [temp_node.type + "=", p[1].addr, temp_node.place, "*"]
                    )

                    activation_record.append(
                        [temp_node.type + "=", offset_string1, offset_string3, "*",]
                    )
        # p[0].ast = build_AST(p, rule_name)
        p[0].ast = build_AST_2(p, [1, 3], p[2].val)


def p_assignment_operator(p):
    """assignment_operator : EQ
    | MUL_ASSIGN
    | DIV_ASSIGN
    | MOD_ASSIGN
    | ADD_ASSIGN
    | SUB_ASSIGN
    | LEFT_ASSIGN
    | RIGHT_ASSIGN
    | AND_ASSIGN
    | XOR_ASSIGN
    | OR_ASSIGN
    """
    rule_name = "assignment_operator"
    p[0] = Node(
        name="AssignmentOperator", val=p[1], type="", lno=p.lineno(1), children=[p[1]],
    )
    # p[0].ast = build_AST(p, rule_name)


def p_expression(p):
    """expression : assignment_expression
    | expression COMMA assignment_expression
    """
    rule_name = "expression"
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1]
        p[0].children.append(p[3])
        p[0].lhs = 1
        # p[0].ast = build_AST_2([p[1],[3]],',');
    # FIXME
    p[0].ast = build_AST(p, rule_name)


def p_constant_expression(p):
    """constant_expression : conditional_expression"""
    rule_name = "constant_expression"
    p[0] = p[1]
    # p[0].ast = build_AST(p, rule_name)


def p_declaration(p):
    """declaration : declaration_specifiers SEMICOLON
    | declaration_specifiers init_declarator_list SEMICOLON
    """
    # global typedef_list
    # global all_typedef
    rule_name = "declaration"
    if p[1].type.upper() in PRIMITIVE_TYPES:
        p[1].type = TYPE_EASY[p[1].type.upper()].lower()
    if len(p) == 3:

        p[0] = p[1]
        p[0].ast = build_AST(p, rule_name)
    else:
        p[0] = Node(
            name="Declaration", val=p[1], type=p[1].type, lno=p.lineno(1), children=[],
        )
        p[0].ast = build_AST(p, rule_name)
        flag = 1
        if "void" in p[1].type.split():
            flag = 0
        for child in p[2].children:

            if child.name == "InitDeclarator":
                if p[1].type.startswith("typedef"):
                    ST.error(
                        Error(
                            p[1].lno,
                            rule_name,
                            "compilation error",
                            "Typedef Initialized",
                        )
                    )
                    continue
                if ST.current_table.find(child.children[0].val):
                    ST.error(
                        Error(
                            p.lineno(1),
                            rule_name,
                            "compilation error",
                            f"Identifier {child.children[0].val} already declared",
                        )
                    )
                node = Node(
                    name=child.children[0].val,
                    type=child.type,
                    val=child.children[1].val,
                    size=get_data_type_size(p[1].type),
                    offset=offsets[ST.currentScope],
                )
                # print(offsets[ST.currentScope])
                ST.current_table.insert(node)
                totalEle = 1
                if len(child.children[0].array) > 0:
                    node.array = child.children[0].array
                    for i in child.children[0].array:
                        if i == 0:
                            continue
                        totalEle = totalEle * i
                if len(child.children[0].type) > 0:
                    node.size = 8
                    node.type = p[1].type + " " + child.children[0].type
                elif flag == 0:
                    ST.error(
                        Error(
                            p[1].lno,
                            rule_name,
                            "compilation error",
                            f"Identifier {child.children[0].val} cannot have type void",
                        )
                    )
                node.size *= totalEle
                offsets[ST.currentScope] += node.size
                offsets[ST.currentScope] += (8 - offsets[ST.currentScope] % 8) % 8

                if child.type != child.children[1].type:

                    temp_node1, tmp_offset_string = ST.get_tmp_var(child.type)
                    offset_string = cal_offset(child.children[1])
                    code_gen.append(
                        [
                            child.children[1].type + "2" + child.type,
                            temp_node1,
                            child.children[1].place,
                        ]
                    )
                    activation_record.append(
                        [
                            child.children[1].type + "2" + child.type,
                            tmp_offset_string,
                            offset_string,
                        ]
                    )
                    offset_string = cal_offset(child.children[0])
                    if len(p[1].array) == 0 and p[1].name != "Pointer":
                        code_gen.append(
                            [child.type + "=", child.children[0].place, temp_node1, ""]
                        )
                        activation_record.append(
                            [child.type + "=", offset_string, tmp_offset_string, "",]
                        )
                    else:
                        code_gen.append(
                            # [p[1].type + "=", child.children[0].place, temp_node1, "*"]
                            [child.type + "=", child.children[0].addr, temp_node1, "*"]
                        )
                        activation_record.append(
                            [
                                child.type + "=",
                                # child.children[0].place + offset_string,
                                offset_string,
                                tmp_offset_string,
                                "*",
                            ]
                        )
                else:
                    # DECLARATION KA PANGA OFFSET UNKNOWN
                    offset_string0 = cal_offset(child.children[0])
                    offset_string1 = cal_offset(child.children[1])
                    if len(p[1].array) == 0 and p[1].name != "Pointer":
                        code_gen.append(
                            [
                                child.type + "=",
                                child.children[0].place,
                                child.children[1].place,
                                "",
                            ]
                        )
                        activation_record.append(
                            [child.type + "=", offset_string0, offset_string1, "",]
                        )
                    else:
                        code_gen.append(
                            [
                                child.type + "=",
                                child.children[0].place,
                                child.children[1].place,
                                "*",
                            ]
                        )
                        activation_record.append(
                            [child.type + "=", offset_string0, offset_string1, "*",]
                        )
                # above line maybe necessary to be commented
            else:

                if (
                    ST.current_table.find(child.val)
                    and ST.current_table.find(child.val).is_func > 0
                ):
                    continue
                if ST.current_table.find(child.val):
                    ST.error(
                        Error(
                            p.lineno(1),
                            rule_name,
                            "compilation error",
                            f"Identifier {child.val} already declared",
                        )
                    )

                node = Node(
                    name=child.val,
                    type=child.type,
                    size=get_data_type_size(p[1].type),
                    offset=offsets[ST.currentScope],
                )
                ST.current_table.insert(node)
                totalEle = 1
                if len(child.array) > 0:
                    node.array = child.array
                    for i in child.array:
                        if i == 0:
                            continue
                        totalEle = totalEle * i
                if child.type[-1] == "*":
                    # node.type = p[1].type + " " + child.type
                    node.size = 8
                elif flag == 0:
                    ST.error(
                        Error(
                            p[1].lno,
                            rule_name,
                            "compilation error",
                            f"Identifier {child.val} cannot have type void",
                        )
                    )
                node.size *= totalEle
                offsets[ST.currentScope] += node.size
                offsets[ST.currentScope] += (8 - offsets[ST.currentScope] % 8) % 8


def p_declaration_specifiers(p):
    """declaration_specifiers : storage_class_specifier
    | storage_class_specifier declaration_specifiers
    | type_specifier
    | type_specifier declaration_specifiers
    | type_qualifier
    | type_qualifier declaration_specifiers
    """
    rule_name = "declaration_specifiers"

    if len(p) == 2:
        p[0] = p[1]
        p[0].ast = build_AST(p, rule_name)
        if p[1].type.upper() in PRIMITIVE_TYPES:
            p[1].type = TYPE_EASY[p[1].type.upper()].lower()
        ST.curType.append(p[1].type)

    elif len(p) == 3:
        if p[1].name == "StorageClassSpecifier" and p[2].name.startswith(
            "StorageClassSpecifier"
        ):
            ST.error(
                Error(
                    p[1].lno,
                    rule_name,
                    "semantic error",
                    f"{p[2].type} not allowed after {p[1].type}",
                )
            )
        if p[1].name == "TypeSpecifier1" and (
            p[2].name.startswith("TypeSpecifier1")
            or p[2].name.startswith("StorageClassSpecifier")
            or p[2].name.startswith("TypeQualifier")
        ):
            if (p[1].type + " " + p[2].type).upper() not in PRIMITIVE_TYPES:
                ST.error(
                    Error(
                        p[1].lno,
                        rule_name,
                        "semantic error",
                        f"{p[2].type} not allowed after {p[1].type}",
                    )
                )
        if p[1].name == "TypeQualifier" and (
            p[2].name.startswith("StorageClassSpecifier")
            or p[2].name.startswith("TypeQualifier")
        ):
            ST.error(
                Error(
                    p[1].lno,
                    rule_name,
                    "semantic error",
                    f"{p[2].type} not allowed after {p[1].type}",
                )
            )

        ST.curType.pop()
        if (p[1].type + " " + p[2].type).upper() in PRIMITIVE_TYPES:
            ST.curType.append(TYPE_EASY[(p[1].type + " " + p[2].type).upper()].lower())
        else:
            ST.curType.append(p[1].type + " " + p[2].type)

        ty = ""
        if len(p[1].type) > 0:
            ty = p[1].type + " " + p[2].type
            ST.curType.pop()  # added by arka can be bugged
        else:
            ty = p[2].type
        if ty.upper() in PRIMITIVE_TYPES:
            ty = TYPE_EASY[ty.upper()].lower()
        ST.curType.append(ty)
        p[0] = Node(
            name=p[1].name + p[2].name, val=p[1], type=ty, lno=p[1].lno, children=[],
        )
        p[0].ast = build_AST(p, rule_name)


def p_init_declarator_list(p):
    """init_declarator_list : red init_declarator
    | init_declarator_list COMMA init_declarator
    """
    rule_name = "init_declarator_list"
    if len(p) == 3:
        p[0] = Node(
            name="InitDeclaratorList",
            val="",
            type=p[-1].type,
            lno=p.lineno(1),
            children=[p[2]],
        )
        # print(p[1].val, "no clue")
        array = copy.deepcopy(p[2].array)

        # p[0].ast = p[1].ast
        p[0].ast = build_AST_2(p, [2], rule_name)
    else:
        p[0] = p[1]
        p[0].children.append(p[3])
        p[0].ast = build_AST(p, rule_name)
        # p[0].ast = build_AST_2(p,[1,3],',')


def p_red(p):
    """red :"""
    p[0] = "red_mark"


def p_init_declarator(p):
    """init_declarator : declarator
    | declarator EQ initializer
    """
    rule_name = "init_declarator"
    if len(p) == 2:
        p[0] = p[1]
        p[0].type = p[-2].type + p[1].type
        # p[0].ast = p[1].ast
        p[0].ast = build_AST(p, rule_name)
    else:
        p[0] = Node(
            name="InitDeclarator",
            val="",
            type=p[-2].type + p[1].type,
            lno=p.lineno(1),
            children=[p[1], p[3]],
            array=p[1].array,
            level=p[1].level,
        )
        p[0].ast = build_AST_2(p, [1, 3], "=")
        if len(p[1].array) > 0 and (
            p[3].max_depth == 0 or p[3].max_depth > len(p[1].array)
        ):
            ST.error(
                Error(
                    p.lineno(1), rule_name, "compilation error", "Invalid Initializer",
                )
            )
        if p[1].level != p[3].level:
            ST.error(Error(p[1].lno, rule_name, "compilation error", "Type Mismatch"))


def p_storage_class_specifier(p):
    """storage_class_specifier : TYPEDEF
    | AUTO
    """
    p[0] = Node(
        name="StorageClassSpecifier", val="", type=p[1], lno=p.lineno(1), children=[],
    )


def p_type_specifier_1(p):
    """type_specifier : VOID
    | CHAR
    | SHORT
    | INT
    | LONG
    | FLOAT
    | DOUBLE
    | SIGNED
    | UNSIGNED
    | TYPE_NAME
    | BOOL
    """
    # | class_definition
    # rule_name = "type_specifier_1"
    p[0] = Node(name="TypeSpecifier1", val="", type=p[1], lno=p.lineno(1), children=[])
    # p[0].ast = build_AST(p,rule_name)


def p_type_specifier_2(p):
    """type_specifier : struct_or_union_specifier"""
    rule_name = "type_specifier_2"
    p[0] = p[1]
    p[0].ast = build_AST(p, rule_name)


def p_struct_declaration_with_linked_list(p):
    """struct_declaration_with_linked_list : struct_or_union IDENTIFIER push_scope_lcb"""

    p[0] = p[1]
    p[0].name = "LinkedList"
    val_name = p[1].type
    p[0].type = p[1].type + " " + p[2]
    p[0].val = p[0].type

    if ST.current_table.find(p[0].type):
        ST.error(
            Error(
                p[1].lno,
                "ABC",
                "compilation error",
                f"Struct {p[0].type} already declared",
            )
        )

    valptr_name = p[0].type + " *"
    val_node = Node(name=p[0].type, type=p[0].type)
    valptr_node = Node(name=valptr_name, type=valptr_name)
    ST.current_table.nodes += [val_node, valptr_node]


def p_struct_or_union_specifier(p):
    """struct_or_union_specifier : struct_declaration_with_linked_list struct_declaration_list pop_scope_rcb
    | struct_or_union push_scope_lcb struct_declaration_list pop_scope_rcb
    | struct_or_union IDENTIFIER
    """
    # p[0] = build_AST(p)
    # TODO : check the semicolon thing after pop_scope_rcb in gramamar
    rule_name = "struct_or_union_specifier"
    p[0] = Node(
        name="StructOrUnionSpecifier", val="", type="", lno=p[1].lno, children=[],
    )

    if len(p) == 4 and p[1].name == "LinkedList":

        p[0].ast = build_AST(p, rule_name)
        val_name = p[1].type
        valptr_name = val_name + " *"
        val_node = Node(name=val_name, type=val_name)
        valptr_node = Node(name=valptr_name, type=valptr_name)
        ST.current_table.nodes += [val_node, valptr_node]

        temp_list = []
        curr_offset = 0
        max_size = 0
        for child in p[2].children:
            for prev_list in temp_list:
                if prev_list[1] == child.val:
                    ST.error(
                        Error(
                            p[4].lno,
                            rule_name,
                            "compilation error",
                            f"{child.val} already declared",
                        )
                    )
            if get_data_type_size(child.type) == -1:
                ST.error(
                    Error(
                        child.lno,
                        rule_name,
                        "compilation error",
                        f"Datatype {child.type} not defined",
                    )
                )
            SZ = get_data_type_size(child.type)
            curr_list = [child.type, child.val, SZ, curr_offset]
            totalEle = 1
            if len(child.array) > 0:
                curr_list.append(child.array)
                for ele in child.array:
                    totalEle *= ele
            curr_offset = curr_offset + get_data_type_size(child.type) * totalEle
            curr_offset += (8 - curr_offset) % 8
            curr_list[2] *= totalEle
            SZ *= totalEle
            max_size = max(max_size, SZ)
            temp_list.append(curr_list)

        val_node.field_list = temp_list
        valptr_node.field_list = temp_list
        val_node.size = curr_offset
        valptr_node.size = 8

    elif len(p) == 3:
        p[0].type = p[1].type + " " + p[2]
        p[0].val = p[0].type
        p[0].ast = build_AST(p, rule_name)
        p0t_node = ST.find(p[0].type)
        if p0t_node is None:
            ST.error(
                Error(
                    p[1].lno,
                    rule_name,
                    "compilation error",
                    f"{p[0].type} is not a type",
                )
            )
    else:
        p[0].ast = build_AST(p, rule_name)


def p_struct_or_union(p):
    """struct_or_union : STRUCT"""
    rule_name = "struct_or_union"
    p[0] = Node(
        name="StructOrUNion", val="", type="struct", lno=p.lineno(1), children=[],
    )
    p[0].ast = build_AST(p, rule_name)


def p_struct_declaration_list(p):
    """struct_declaration_list : struct_declaration
    | struct_declaration_list struct_declaration
    """
    rule_name = "struct_declaration_list"
    p[0] = Node(
        name="StructDeclarationList", val="", type=p[1].type, lno=p[1].lno, children=[],
    )
    p[0].ast = build_AST(p, rule_name)
    if len(p) == 2:
        p[0].children = p[1].children
    else:
        p[0].children = p[1].children
        p[0].children.extend(p[2].children)


def p_struct_declaration(p):
    """struct_declaration : specifier_qualifier_list struct_declarator_list SEMICOLON"""
    rule_name = "struct_declaration"
    p[0] = Node(
        name="StructDeclaration", val="", type=p[1].type, lno=p[1].lno, children=[],
    )
    p[0].ast = build_AST(p, rule_name)
    p[0].children = p[2].children
    for child in p[0].children:
        if len(child.type) > 0:
            child.type = p[1].type + " " + child.type
        else:
            if "void" in p[1].type.split():
                ST.error(
                    Error(
                        p[1].lno,
                        rule_name,
                        "compilation error",
                        f"Identifier {child.val} cannot have type void",
                    )
                )
            child.type = p[1].type


def p_specifier_qualifier_list(p):
    """specifier_qualifier_list : type_specifier specifier_qualifier_list
    | type_specifier
    | type_qualifier specifier_qualifier_list
    | type_qualifier
    """
    rule_name = "specifier_qualifier_list"
    if len(p) == 2:
        p[0] = Node(
            name="SpecifierQualifierList",
            val="",
            type=p[1].type,
            lno=p[1].lno,
            children=[],
        )
    if len(p) == 3:
        p[0] = Node(
            name="SpecifierQualifierList",
            val="",
            type=p[1].type + " " + p[2].type,
            lno=p[1].lno,
            children=[],
        )
    p[0].ast = build_AST(p, rule_name)


def p_struct_declarator_list(p):
    """struct_declarator_list : struct_declarator
    | struct_declarator_list COMMA struct_declarator
    """
    rule_name = "struct_declarator"
    p[0] = Node(
        name="StructDeclaratorList", val="", type=p[1].type, lno=p[1].lno, children=[],
    )
    if len(p) == 2:
        p[0].children.append(p[1])
    else:
        p[0].children = p[1].children
        p[0].children.append(p[3])
    p[0].ast = build_AST(p, rule_name)


def p_struct_declarator(p):
    """struct_declarator : declarator
    | COLON constant_expression
    | declarator COLON constant_expression
    """
    rule_name = "struct_declarator"
    if len(p) == 2 or len(p) == 4:
        p[0] = p[1]
    if len(p) == 3:
        p[0] = p[2]
    p[0].ast = build_AST(p, rule_name)


def p_type_qualifier(p):
    """type_qualifier : CONST"""
    p[0] = Node(name="TypeQualifier", val="", type=p[1], lno=p.lineno(1), children=[])


def p_declarator_1(p):
    """declarator : pointer direct_declarator
    | direct_declarator
    """
    rule_name = "declarator_1"
    if len(p) == 2:
        p[0] = p[1]
        p[0].name = "Declarator"
        p[0].ast = build_AST(p, rule_name)

    else:
        p[0] = p[2]
        p[0].name = "Declarator"
        p[0].type = p[1].type
        p[0].ast = build_AST(p, rule_name)
        p2v_node = ST.parent_table.find(p[2].val)
        if p2v_node is not None and p2v_node.is_func:
            p2v_node.type = p2v_node.type + " " + p[1].type
            ST.curFuncReturnType = ST.curFuncReturnType + " " + p[1].type
        p[0].val = p[2].val
        p[0].array = p[2].array
        p[0].level = p[1].type.count("*")


def p_direct_declarator_2(p):
    """direct_declarator : IDENTIFIER
    | LEFT_BRACKET declarator RIGHT_BRACKET
    | direct_declarator push_scope_lb parameter_type_list RIGHT_BRACKET
    | direct_declarator push_scope_lb identifier_list RIGHT_BRACKET
    """
    rule_name = "direct_declarator_2"

    if len(p) == 2:
        p[0] = Node(
            name="ID", val=p[1], type="", lno=p.lineno(1), children=[], place=p[1]
        )
        p[0].name = "ID"
        # p[0].ast = p[1].ast
        p[0].ast = build_AST(p, rule_name)
    elif len(p) == 4:
        p[0] = p[2]
        # p[0].ast = build_AST(p, rule_name)
    else:
        p[0] = p[1]
        p[0].ast = build_AST_2(p, [1, 3], rule_name)
        p[0].children = p

    if len(p) == 5 and p[3].name == "ParameterList":
        p[0].children = p[3].children
        p[0].type = ST.curType[-1]
        p1v_node = ST.parent_table.find(p[1].val)
        if p1v_node is not None:
            ST.error(
                Error(
                    p[1].lno,
                    rule_name,
                    "compilation error",
                    f"Function {p[1].val} already declared",
                )
            )
        node = Node(name=p[1].val, is_func=1)
        tempList = []
        total_size = 0
        for child in p[3].children:
            tempList.append(child.type)
            total_size += get_data_type_size(child.type)
            total_size += (8 - total_size % 8) % 8
        total_size = -total_size
        for child in p[3].children:
            node1 = ST.find(child.val)
            node1.offset = total_size
            total_size += get_data_type_size(child.type)
            total_size += (8 - total_size % 8) % 8
        node.argument_list = tempList
        node.type = ST.curType[-1 - len(tempList)]
        ST.parent_table.insert(node)
        ST.curFuncReturnType = copy.deepcopy(ST.curType[-1 - len(tempList)])
        ST.current_table.name = p[1].val
        # code_gen.append(["funcstart", p[1].val, "", ""])
        funcstack.append(p[1].val)


def p_direct_declarator_3(p):
    """direct_declarator : direct_declarator LEFT_THIRD_BRACKET constant_expression RIGHT_THIRD_BRACKET"""
    rule_name = "direct_declarator_3"
    p[0] = Node(
        name="ArrayDeclarator", val=p[1].val, type="", lno=p.lineno(1), children=[],
    )
    p[0].ast = build_AST(p, rule_name)
    p[0].array = copy.deepcopy(p[1].array)
    p[0].array.append(int(p[3].place))


def p_direct_declarator_4(p):
    """direct_declarator : direct_declarator LEFT_THIRD_BRACKET RIGHT_THIRD_BRACKET
    | direct_declarator push_scope_lb RIGHT_BRACKET"""
    rule_name = "direct_declarator_4"
    p[0] = p[1]
    if p[3] == ")":
        p[0].ast = p[1].ast
        # p[0].ast = build_AST(p, rule_name)
    else:
        if p[2] == "[":
            p[0].array = copy.deepcopy(p[1].array)
            if len(p[0].array) > 0:
                ST.error(
                    Error(
                        p[1].lno,
                        rule_name,
                        "compilation error",
                        f"Array {p[1].val} cannot have variable dimension except first",
                    )
                )
            p[0].array.append(0)
        p[0].ast = build_AST(p, rule_name)

    if p[3] == ")":
        if ST.parent_table.find(p[1].val):
            ST.error(
                Error(
                    p[1].lno,
                    rule_name,
                    "compilation error",
                    f"Function {p[1].val} already declared",
                )
            )
            return
        node = Node(name=p[1].val, type=ST.curType[-1], is_func=1, argument_list=[])
        # Modified
        ST.parent_table.insert(node)
        ST.curFuncReturnType = copy.deepcopy(ST.curType[-1])
        ST.current_table.name = p[1].val

        # code_gen.append(["funcstart", p[1].val, "", ""])
        funcstack.append(p[1].val)


def p_pointer(p):
    """pointer : MULTIPLY
    | MULTIPLY type_qualifier_list
    | MULTIPLY pointer
    | MULTIPLY type_qualifier_list pointer
    """
    rule_name = "pointer"
    if len(p) == 2:
        p[0] = Node(name="Pointer", val="", type=" *", lno=p.lineno(1), children=[])
        p[0].ast = build_AST(p, rule_name)
    elif len(p) == 3:
        p[0] = Node(
            name="Pointer", val="", type=p[2].type + " *", lno=p.lineno(1), children=[],
        )
        p[0].ast = build_AST(p, rule_name)
    else:
        p[0] = Node(
            name="Pointer", val="", type=p[2].type + " *", lno=p[2].lno, children=[],
        )
        p[0].ast = build_AST(p, rule_name)


def p_type_qualifier_list(p):
    """type_qualifier_list : type_qualifier
    | type_qualifier_list type_qualifier
    """
    rule_name = "type_qualifier_list"
    p[0] = p[1]
    p[0].name = "TypeQualifierList"
    p[0].ast = build_AST(p, rule_name)

    if len(p) == 2:
        p[0].children = p[1]
    else:
        p[0].children.append(p[2])
        p[0].type = p[1].type + " " + p[2].type


def p_parameter_type_list(p):
    """parameter_type_list : parameter_list"""
    rule_name = "parameter_type_list"
    p[0] = p[1]
    p[0].ast = build_AST(p, rule_name)


def p_parameter_list(p):
    """parameter_list : parameter_declaration
    | parameter_list COMMA parameter_declaration
    """
    rule_name = "parameter_list"
    p[0] = Node(name="ParameterList", val="", type="", children=[], lno=p.lineno(1))
    if len(p) == 2:
        p[0].ast = build_AST(p, rule_name)
        p[0].children.append(p[1])
    else:
        p[0].ast = build_AST(p, rule_name)
        p[0].children = p[1].children
        p[0].children.append(p[3])


def p_parameter_declaration(p):
    """parameter_declaration : declaration_specifiers declarator
    | declaration_specifiers abstract_declarator
    | declaration_specifiers
    """
    rule_name = "parameter_declaration"
    if p[1].type.upper() in PRIMITIVE_TYPES:
        p[1].type = TYPE_EASY[p[1].type.upper()].lower()

    if len(p) == 2:
        p[0] = p[1]
        p[0].ast = build_AST(p, rule_name)
        p[0].name = "ParameterDeclaration"
    else:
        p[0] = Node(
            name="ParameterDeclaration",
            val=p[2].val,
            type=p[1].type,
            lno=p[1].lno,
            level=p[2].level,
            children=[],
        )
        p[0].ast = build_AST(p, rule_name)
        if len(p[2].type) > 0:
            p[0].type = p[1].type + " " + p[2].type
    if p[2].name == "Declarator":
        p2v_node = ST.current_table.find(p[2].val)
        if p2v_node is not None:
            ST.error(
                Error(
                    p.lineno(1),
                    rule_name,
                    "compilation error",
                    f"Parameter {p[2].val} already declared",
                )
            )
        node = Node(name=p[2].val, type=p[1].type)
        ST.current_table.insert(node)
        if len(p[2].type) > 0:
            node.type = p[1].type + " " + p[2].type
            node.size = get_data_type_size(node.type)
        else:
            if "void" in p[1].type.split():
                ST.error(
                    Error(
                        p[1].lno,
                        rule_name,
                        "compilation error",
                        f"Parameter {p[2].val} cannot have type void",
                    )
                )
            node.size = get_data_type_size(p[1].type)
        if len(p[2].array) > 0:
            node.array = p[2].array


def p_identifier_list(p):
    """identifier_list : IDENTIFIER
    | identifier_list COMMA IDENTIFIER
    """
    rule_name = "identifier_list"
    if len(p) == 2:
        p[0] = Node(
            name="IdentifierList", val=p[1], type="", lno=p.lineno(1), children=[p[1]],
        )
    else:
        p[0] = p[1]
        p[0].children.append(p[3])
        p[0].name = "IdentifierList"
    p[0].ast = build_AST(p, rule_name)


def p_type_name(p):
    """type_name : specifier_qualifier_list
    | specifier_qualifier_list abstract_declarator
    """
    rule_name = "type_name"
    if len(p) == 2:
        p[1].type = TYPE_EASY[p[1].type.upper()].lower()
        p[0] = p[1]
        p[0].name = "TypeName"
    else:
        p[1].type = TYPE_EASY[p[1].type.upper()].lower()

        p[0] = Node(name="TypeName", val="", type=p[1].type, lno=p[1].lno, children=[])
        if p[2].type.endswith("*"):
            p[0].type = p[0].type + " *" * (p[2].type.count("*"))
    p[0].ast = build_AST(p, rule_name)


def p_abstract_declarator(p):
    """abstract_declarator : pointer
    | direct_abstract_declarator
    | pointer direct_abstract_declarator
    """
    rule_name = "abstract_declarator"
    if len(p) == 2:
        p[0] = p[1]
        p[0].name = "AbstractDeclarator"

    elif len(p) == 3:
        p[0] = Node(
            name="AbstractDeclarator",
            val=p[2].val,
            type=p[1].type + " *",
            lno=p[1].lno,
            children=[],
        )
    p[0].ast = build_AST(p, rule_name)


def p_direct_abstract_declarator_1(p):
    """direct_abstract_declarator : LEFT_BRACKET abstract_declarator RIGHT_BRACKET
    | LEFT_THIRD_BRACKET RIGHT_THIRD_BRACKET
    | LEFT_THIRD_BRACKET constant_expression RIGHT_THIRD_BRACKET
    | direct_abstract_declarator LEFT_BRACKET constant_expression RIGHT_BRACKET
    | LEFT_BRACKET RIGHT_BRACKET
    | LEFT_BRACKET parameter_type_list RIGHT_BRACKET
    | direct_abstract_declarator LEFT_BRACKET parameter_type_list RIGHT_BRACKET
    """
    rule_name = "abstract_declarator_1"
    if len(p) == 3:
        p[0] = Node(
            name="DirectAbstractDeclarator1",
            val="",
            type="",
            lno=p.lineno(1),
            children=[],
        )
    elif len(p) == 4:
        p[0] = p[2]
        p[0].name = "DirectAbstractDeclarator1"
        p[0].ast = build_AST(p, rule_name)
    else:
        p[0] = Node(
            name="DirectAbstractDeclarator1",
            val=p[1].val,
            type=p[1].val,
            lno=p[1].lno,
            children=[p[3]],
        )
        p[0].ast = build_AST(p, rule_name)


def p_direct_abstract_declarator_2(p):
    """direct_abstract_declarator : direct_abstract_declarator LEFT_BRACKET RIGHT_BRACKET"""
    rule_name = "abstract_declarator_2"
    p[0] = Node(
        name="DirectAbstractDEclarator2",
        val=p[1].val,
        type=p[1].type,
        lno=p[1].lno,
        children=[],
    )
    p[0].ast = build_AST(p, rule_name)


def p_initializer(p):
    """initializer : assignment_expression"""
    # | LEFT_CURLY_BRACKET initializer_list RIGHT_CURLY_BRACKET
    # | LEFT_CURLY_BRACKET initializer_list COMMA RIGHT_CURLY_BRACKET

    rule_name = "initializer"
    # if len(p) == 2:
    p[0] = p[1]
    # print(p[0].type)
    p[0].ast = build_AST(p, rule_name)
    # else:
    #     p[0] = p[2]
    #     p[0].is_array = True

    p[0].name = "Initializer"
    # if len(p) == 4:
    #     p[0].max_depth = p[2].max_depth + 1
    #     p[0].ast = build_AST(p, rule_name)
    # elif len(p) == 5:
    #     p[0].ast = build_AST(p, rule_name)


def p_initializer_list(p):
    """initializer_list : initializer
    | initializer_list COMMA initializer
    """
    rule_name = "initializer_list"
    p[0] = Node(
        name="InitializerList",
        val="",
        type="",
        children=[p[1]],
        lno=p.lineno(1),
        max_depth=p[1].max_depth,
    )
    p[0].ast = build_AST(p, rule_name)
    if len(p) == 3:
        if p[1].name != "InitializerList":
            p[0].children.append(p[1])
        else:
            p[0].children = p[1].children
        p[0].children.append(p[3])
        p[0].max_depth = max(p[1].max_depth, p[3].max_depth)


def p_statement(p):
    """statement : labeled_statement
    | compound_statement
    | expression_statement
    | selection_statement
    | iteration_statement
    | jump_statement
    """
    rule_name = "statement"
    p[0] = Node(name="Statement", val="", type="", children=[], lno=p.lineno(1),)
    if isinstance(p[1], Node):
        p[0].label = p[1].label
        p[0].expr = p[1].expr
    p[0].ast = build_AST(p, rule_name)


def p_label_marker(p):
    """label_marker :"""
    code_gen.append(["label", "__label_" + p[-1], ":", ""])
    valid_goto_labels.append(p[-1])


def p_labeled_statement(p):
    """labeled_statement : IDENTIFIER label_marker COLON statement
    | Switch_M CASE constant_expression COLON statement
    | Switch_M DEFAULT COLON statement"""
    rule_name = "labeled_statement"
    name = ""
    # if isinstance(p[2], str) and p[2] == "":
    #     code_gen.append(["__label_" + p[1], ":", "", ""])
    if p[2] == "case":
        if p[3].type.upper() not in (TYPE_INTEGER + TYPE_CHAR) or (
            not p[3].name.startswith("Constant")
        ):
            ST.error(
                Error(
                    p.lineno(2),
                    rule_name,
                    "compilation error",
                    f"Invalid datatype {p[3].type} for case. Expected char or int constant",
                )
            )

        name = "CaseStatement"

    elif p[2] == "default":
        name = "DefaultStatement"
    else:
        name = "LabeledStatement"
    p[0] = Node(name=name, val="", type="", children=[], lno=p.lineno(1))
    if p[2] == "case":
        p[0].expr.append(p[3].val)
    elif p[2] == "default":
        p[0].expr.append("")
    p[0].label.append(p[1])
    p[0].ast = build_AST(p, rule_name)


def p_Switch_M(p):
    """Switch_M :"""
    tmp_label = ST.get_tmp_label()
    code_gen.append(["label", tmp_label, ":", ""])
    activation_record.append(["label", tmp_label, ":", ""])
    p[0] = tmp_label


def p_compound_statement(p):
    """compound_statement : push_scope_lcb pop_scope_rcb
    | push_scope_lcb statement_list pop_scope_rcb
    | push_scope_lcb declaration_list pop_scope_rcb
    | push_scope_lcb declaration_list statement_list pop_scope_rcb
    """
    # TODO : see what to do in in first case
    rule_name = "compound_statement"
    if len(p) == 3:
        p[0] = Node(
            name="CompoundStatement",
            val="",
            type="",
            lno=p.lineno(1),
            children=[],
            label=[],
            expr=[],
        )

    elif len(p) == 4:
        p[0] = Node(
            name="CompoundStatement",
            val="",
            type="",
            children=[],
            lno=p.lineno(1),
            label=p[2].label,
            expr=p[2].expr,
        )
        p[0].ast = build_AST(p, rule_name)
    else:
        p[0] = Node(
            name="CompoundStatement",
            val="",
            type="",
            children=[],
            lno=p.lineno(1),
            label=p[2].label,  # p[1].label + p[2].label,
            expr=p[2].expr,  # p[1].expr + p[2].expr,
        )
        p[0].ast = build_AST(p, rule_name)


def p_new_compound_statement(p):
    """new_compound_statement : LEFT_CURLY_BRACKET pop_scope_rcb
    | LEFT_CURLY_BRACKET statement_list pop_scope_rcb
    | LEFT_CURLY_BRACKET declaration_list pop_scope_rcb
    | LEFT_CURLY_BRACKET declaration_list statement_list pop_scope_rcb
    """
    rule_name = "new_compound_statement"
    if len(p) == 3:
        p[0] = Node(
            name="CompoundStatement", val="", type="", lno=p.lineno(1), children=[],
        )
        ST.error(
            Error(
                p.lineno(1),
                rule_name,
                "compilation error",
                f"Empty function not allowed",
            )
        )
    elif len(p) == 4:
        p[0] = p[2]
        p[0].name = "CompoundStatement"
        p[0].ast = p[2].ast
        # p[0].ast = build_AST(p, rule_name)
    # elif len(p) == 4:
    #     p[0] = Node(
    #         name="CompoundStatement",
    #         val="",
    #         type="",
    #         children=[],
    #         lno=p.lineno(1),
    #     )
    #     p[0].ast = build_AST(p, rule_name)
    else:
        p[0] = Node(
            name="CompoundStatement", val="", type="", children=[], lno=p.lineno(1),
        )
        # FIXME
        p[0].ast = build_AST(p, rule_name)


def p_function_compound_statement(p):
    """function_compound_statement : new_compound_statement"""
    rule_name = "function_compound_statement"
    p[0] = p[1]
    p[0].ast = build_AST(p, rule_name)


def p_declaration_list(p):
    """declaration_list : declaration
    | declaration_list declaration
    """
    rule_name = "declaration_list"
    if len(p) == 2:
        p[0] = p[1]
        p[0].ast = build_AST(p, rule_name)
    else:
        p[0] = Node(
            name="DeclarationList", val="", type="", children=[], lno=p.lineno(1),
        )
        p[0].ast = build_AST(p, rule_name)
        if p[1].name != "DeclarationList":
            p[0].children.append(p[1])
        else:
            p[0].children = p[1].children
        p[0].children.append(p[2])


def p_statement_list(p):
    """statement_list : statement
    | statement_list statement
    """
    rule_name = "statement_list"
    if len(p) == 2:
        p[0] = p[1]
        p[0].ast = build_AST(p, rule_name)
    else:

        p[0] = Node(name="StatementList", val="", type="", children=[], lno=p.lineno(1))
        p[0].ast = build_AST(p, rule_name)
        if p[1].name != "StatmentList":
            p[0].children.append(p[1])
        else:
            p[0].children = p[1].children
        p[0].children.append(p[2])
        p[0].label = p[1].label + p[2].label
        p[0].expr = p[1].expr + p[2].expr


def p_expression_statement(p):
    """expression_statement : SEMICOLON
    | expression SEMICOLON
    """
    rule_name = "expression_statement"
    p[0] = Node(
        name="ExpressionStatement", val="", type="", children=[], lno=p.lineno(1),
    )
    if len(p) == 3:
        p[0].ast = build_AST(p, rule_name)
        p[0].val = p[1].val
        p[0].type = p[1].type
        p[0].children = p[1].children
    # TODO : see what to do in case of only semicolon in rhs


def p_selection_statement(p):
    """selection_statement : if LEFT_BRACKET expression  RIGHT_BRACKET if_M1 compound_statement
    | if LEFT_BRACKET expression RIGHT_BRACKET if_M1 compound_statement else if_M2 compound_statement
    | switch LEFT_BRACKET expression RIGHT_BRACKET Switch_M2 compound_statement Switch_M3"""
    rule_name = "selection_statement"
    if p[1] == "if":
        if len(p) == 7:
            # ST.subscope_name = "if"
            p[0] = Node(
                name="IfStatment", val="", type="", children=[], lno=p.lineno(1),
            )
            code_gen.append(["label", p[5][0], ":", ""])
            activation_record.append(["label", p[5][0], ":", ""])

        else:
            # ST.subscope_name = "if"
            p[0] = Node(
                name="IfElseStatement", val="", type="", children=[], lno=p.lineno(1),
            )
            code_gen.append(["label", p[5][1], ":", ""])
            activation_record.append(["label", p[5][1], ":", ""])
    else:
        # e_type = TYPE_EASY[p[3].type.upper()].lower()
        # if (
        #     e_type == "float"
        #     or e_type == "double"
        #     or e_type == "void"
        #     or e_type == "long double"
        # ):

        if TYPE_EASY[p[3].type.upper()] not in TYPE_INTEGER + TYPE_CHAR:
            ST.error(
                Error(
                    p.lineno(1),
                    rule_name,
                    "compilation error",
                    f"Switch doesn't support '{p[3].type}' expression type",
                )
            )
        p[0] = Node(
            name="SwitchStatement", val="", type="", children=[], lno=p.lineno(1),
        )

    p[0].ast = build_AST(p, rule_name)


def p_if_M1(p):
    """if_M1 :"""
    label1 = ST.get_tmp_label()
    label2 = ST.get_tmp_label()
    offset_string = cal_offset(p[-2])
    code_gen.append(["beq", p[-2].place, "0", label1])
    activation_record.append(["beq", offset_string, "0", label1])
    p[0] = [label1, label2]


def p_if_M2(p):
    """if_M2 :"""
    code_gen.append(["goto", "", "", p[-3][1]])
    code_gen.append(["label", p[-3][0], ":", ""])
    activation_record.append(["goto", "", "", p[-3][1]])
    activation_record.append(["label", p[-3][0], ":", ""])


def p_Switch_M2(p):
    """Switch_M2 :"""
    label1 = ST.get_tmp_label()
    code_gen.append(["goto", "", "", label1])
    activation_record.append(["goto", "", "", label1])
    label2 = ST.get_tmp_label()
    brkStack.append(label2)
    p[0] = [label1, label2]


def p_Switch_M3(p):
    """Switch_M3 :"""
    code_gen.append(["goto", "", "", p[-2][1]])
    ### after all cases break from switch case

    code_gen.append(["label", p[-2][0], ":", ""])

    activation_record.append(["goto", "", "", p[-2][1]])
    activation_record.append(["label", p[-2][0], ":", ""])

    flag = False
    default_array = None
    # print(p[-1].expr)
    if len(set(p[-1].expr)) < len(p[-1].expr):
        ST.error(
            Error(
                "undefined",
                "Switch case Labels",
                "compilation error",
                f"Switch case has repeated labels",
            )
        )
    tmp_var = p[-4].place
    offset_string = cal_offset(p[-4])
    tmp_offset_string = offset_string

    if p[-4].type[-4:] == "char":

        tmp_var, tmp_offset_string = ST.get_tmp_var("int")
        code_gen.append([p[-4].type + "2" + "int", tmp_var, p[-4].place])
        activation_record.append(
            [
                p[-4].type + "2" + "int",
                tmp_var + tmp_offset_string,
                p[-4].place + offset_string,
            ]
        )

    for i in range(0, len(p[-1].expr)):
        case = p[-1].expr[i]
        if case == "":
            flag = True
            default_array = p[-1].label[i]
        else:
            if case[0] == "'":
                case = str(ord(case[1:-1]))

            ## TODO: difference when p[-4] is long or unsigned long
            # if p[-4].type=="unsigned long" or p[-4].type=="long":

            ##IS offset needed here ?
            offset_string = cal_offset(p[-1].label[i])
            code_gen.append(["beq", tmp_var, case, p[-1].label[i]])
            activation_record.append(
                [
                    "beq",
                    tmp_var + tmp_offset_string,
                    case,
                    p[-1].label[i] + offset_string,
                ]
            )

    if flag:
        code_gen.append(["goto", "", "", default_array])
        activation_record.append(["goto", "", "", default_array])

    brkStack.pop()
    code_gen.append(["label", p[-2][1], ":", ""])
    activation_record.append(["label", p[-2][1], ":", ""])


def p_if(p):
    """if : IF"""
    rule_name = "if"
    ST.subscope_name = "if"
    p[0] = p[1]
    p[0] = build_AST(p, rule_name)


def p_else(p):
    """else : ELSE"""
    rule_name = "else"
    ST.subscope_name = "if"
    p[0] = p[1]
    p[0] = build_AST(p, rule_name)


def p_switch(p):
    """switch : SWITCH"""
    rule_name = "switch"
    ST.subscope_name = "switch"
    p[0] = p[1]
    ST.switch_depth += 1
    p[0] = build_AST(p, rule_name)


def p_iteration_statement(p):
    """iteration_statement : while while_M1 LEFT_BRACKET expression RIGHT_BRACKET while_M2 compound_statement while_M3
    | do do_M1 compound_statement WHILE do_M2 LEFT_BRACKET expression RIGHT_BRACKET do_M3 SEMICOLON
    | for push_scope_lb for_init_statement FM1 expression SEMICOLON FM2 RIGHT_BRACKET new_compound_statement FM3
    | for push_scope_lb for_init_statement FM1 SEMICOLON  RIGHT_BRACKET new_compound_statement FM8
    | for push_scope_lb for_init_statement FM1 expression SEMICOLON FM4 expression FM5 RIGHT_BRACKET FM6  new_compound_statement FM7
    | for push_scope_lb for_init_statement FM1 SEMICOLON FM9 expression FM10 RIGHT_BRACKET FM11  new_compound_statement FM12
    """
    # TODO: Scope names for while and do-while
    rule_name = "iteration_statement"
    if p[1] == "do":
        p[0] = Node(
            name="DoWhileStatement", val="", type="", children=[], lno=p.lineno(1),
        )
        p[0].ast = build_AST(p, rule_name)
    elif p[1] == "while":
        p[0] = Node(
            name="WhileStatement", val="", type="", children=[], lno=p.lineno(1),
        )
        p[0].ast = build_AST(p, rule_name)
    else:
        p[0] = Node(name="ForStatement", val="", type="", children=[], lno=p.lineno(1))
        p[0].ast = build_AST(p, rule_name)

    ST.looping_depth -= 1


def p_while_M1(p):
    """while_M1 :"""
    l1 = ST.get_tmp_label()
    # l2 = ST.get_tmp_label()  ## non useful
    l3 = ST.get_tmp_label()
    contStack.append(l1)
    brkStack.append(l3)
    code_gen.append(["label", l1, ":", ""])
    activation_record.append(["label", l1, ":", ""])
    p[0] = [l1, l3]


def p_while_M2(p):
    """while_M2 :"""
    offset_string = cal_offset(p[-2])
    code_gen.append(["beq", p[-2].place, "0", p[-4][1]])
    activation_record.append(["beq", offset_string, "0", p[-4][1]])
    # code_gen.append(["goto", "", "", p[-4][1]])  ## non useful
    # code_gen.append(["label", p[-4][1], ":", ""])  ## non useful


def p_while_M3(p):
    """while_M3 :"""

    code_gen.append(["goto", "", "", p[-6][0]])
    code_gen.append(["label", p[-6][1], ":", ""])
    activation_record.append(["goto", "", "", p[-6][0]])
    activation_record.append(["label", p[-6][1], ":", ""])

    brkStack.pop()
    contStack.pop()


def p_do_M1(p):
    """do_M1 :"""
    l1 = ST.get_tmp_label()
    l2 = ST.get_tmp_label()  ## non useful
    l3 = ST.get_tmp_label()
    contStack.append(l2)
    brkStack.append(l3)
    code_gen.append(["label", l1, ":", ""])
    activation_record.append(["label", l1, ":", ""])

    p[0] = [l1, l2, l3]


def p_do_M2(p):
    """do_M2 :"""

    code_gen.append(["label", p[-3][1], ":", ""])
    activation_record.append(["label", p[-3][1], ":", ""])


def p_do_M3(p):
    """do_M3 :"""

    offset_string = cal_offset(p[-2])
    code_gen.append(["beq", p[-2].place, "0", p[-7][2]])
    code_gen.append(["goto", "", "", p[-7][0]])  ## non useful
    code_gen.append(["label", p[-7][2], ":", ""])  ## non useful
    activation_record.append(["beq", offset_string, "0", p[-7][2]])
    activation_record.append(["goto", "", "", p[-7][0]])  ## non useful
    activation_record.append(["label", p[-7][2], ":", ""])  ## non useful

    brkStack.pop()
    contStack.pop()


def p_FM1(p):
    """FM1 :"""
    l1 = ST.get_tmp_label()
    l2 = ST.get_tmp_label()
    l3 = ST.get_tmp_label()
    l4 = ST.get_tmp_label()
    contStack.append(l1)
    brkStack.append(l2)
    code_gen.append(["label", l1, ":", ""])
    activation_record.append(["label", l1, ":", ""])

    p[0] = [l1, l2, l3, l4]


def p_FM2(p):
    """FM2 :"""
    offset_string = cal_offset(p[-2])
    code_gen.append(["beq", p[-2].place, "0", p[-3][1]])
    activation_record.append(["beq", offset_string, "0", p[-3][1]])


def p_FM8(p):
    """FM8 :"""
    code_gen.append(["goto", "", "", p[-4][0]])
    code_gen.append(["label", p[-4][1], ":", ""])
    activation_record.append(["goto", "", "", p[-4][0]])
    activation_record.append(["label", p[-4][1], ":", ""])

    contStack.pop()
    brkStack.pop()


def p_FM4(p):
    """FM4 :"""
    offset_string = cal_offset(p[-2])
    code_gen.append(["beq", p[-2].place, "0", p[-3][1]])
    code_gen.append(["goto", "", "", p[-3][2]])
    code_gen.append(["label", p[-3][3], ":", ""])
    activation_record.append(["beq", offset_string, "0", p[-3][1]])
    activation_record.append(["goto", "", "", p[-3][2]])
    activation_record.append(["label", p[-3][3], ":", ""])


def p_FM9(p):
    """FM9 :"""
    # code_gen.append(["beq", p[-2].place, "0", p[-3][1]])
    code_gen.append(["goto", "", "", p[-2][2]])
    code_gen.append(["label", p[-2][3], ":", ""])
    activation_record.append(["goto", "", "", p[-2][2]])
    activation_record.append(["label", p[-2][3], ":", ""])


def p_FM3(p):
    """FM3 :"""
    code_gen.append(["goto", "", "", p[-6][0]])
    code_gen.append(["label", p[-6][1], ":", ""])
    activation_record.append(["goto", "", "", p[-6][0]])
    activation_record.append(["label", p[-6][1], ":", ""])

    contStack.pop()
    brkStack.pop()


def p_FM5(p):
    """FM5 :"""
    code_gen.append(["goto", "", "", p[-5][0]])
    activation_record.append(["goto", "", "", p[-5][0]])


def p_FM6(p):
    """FM6 :"""
    code_gen.append(["label", p[-7][2], ":", ""])
    activation_record.append(["label", p[-7][2], ":", ""])


def p_FM7(p):
    """FM7 :"""
    code_gen.append(["goto", "", "", p[-9][3]])
    code_gen.append(["label", p[-9][1], ":", ""])
    activation_record.append(["goto", "", "", p[-9][3]])
    activation_record.append(["label", p[-9][1], ":", ""])

    brkStack.pop()
    contStack.pop()


def p_FM10(p):
    """FM10 :"""
    code_gen.append(["goto", "", "", p[-4][0]])
    activation_record.append(["goto", "", "", p[-4][0]])


def p_FM11(p):
    """FM11 :"""
    code_gen.append(["label", p[-6][2], ":", ""])
    activation_record.append(["label", p[-6][2], ":", ""])


def p_FM12(p):
    """FM12 :"""
    code_gen.append(["goto", "", "", p[-8][3]])
    code_gen.append(["label", p[-8][1], ":", ""])
    activation_record.append(["goto", "", "", p[-8][3]])
    activation_record.append(["label", p[-8][1], ":", ""])

    brkStack.pop()
    contStack.pop()


def p_for_init_statement(p):
    """for_init_statement : expression_statement
    | declaration
    """
    rule_name = "for_init_statement"
    p[0] = p[1]
    p[0].ast = build_AST(p, rule_name)
    # ST.current_table.name = (
    #     f"{ST.parent_table.name}-for-{ST.parent_table.loop_num}"
    # )
    ST.subscope_name = "for"


def p_while(p):
    """while : WHILE"""
    rule_name = "while"
    ST.subscope_name = "while"
    ST.looping_depth += 1
    p[0] = p[1]
    p[0] = build_AST(p, rule_name)


def p_do(p):
    """do : DO"""
    rule_name = "do"
    ST.subscope_name = "do"
    ST.looping_depth += 1
    p[0] = p[1]
    p[0] = build_AST(p, rule_name)


def p_for(p):
    """for : FOR"""
    rule_name = "for"
    ST.subscope_name = "for"
    ST.looping_depth += 1
    p[0] = p[1]
    p[0] = build_AST(p, rule_name)


def p_jump_statemen_1(p):
    """jump_statement : GOTO IDENTIFIER SEMICOLON
    | CONTINUE SEMICOLON
    | BREAK SEMICOLON"""
    rule_name = "jump_statement_1"

    p[0] = Node(name="JumpStatement", val="", type="", lno=p.lineno(1), children=[])
    p[0].ast = build_AST(p, rule_name)
    temp = p[1][0] if isinstance(p[1], tuple) else p[1]

    if temp == "continue" and ST.looping_depth == 0:
        ST.error(
            Error(
                p.lineno(1), rule_name, "compilation error", "continue not inside loop",
            )
        )
    elif temp == "continue":
        code_gen.append(["goto", "", "", contStack[-1]])
        activation_record.append(["goto", "", "", contStack[-1]])
    elif temp == "break" and ST.looping_depth == 0 and ST.switch_depth == 0:
        ST.error(
            Error(
                p.lineno(1),
                rule_name,
                "compilation error",
                "break not inside switch/loop",
            )
        )
    elif temp == "break":
        code_gen.append(["goto", "", "", brkStack[-1]])
        activation_record.append(["goto", "", "", brkStack[-1]])
    elif temp == "goto":
        if p[2][0] not in valid_goto_labels:
            ST.error(
                Error(
                    p.lineno(1),
                    rule_name,
                    "compilation error",
                    "Not a valid goto label",
                )
            )
        code_gen.append(["goto", "", "", "__label_" + p[2][0]])


def p_jump_statemen_2(p):
    """jump_statement : RETURN SEMICOLON
    | RETURN expression SEMICOLON"""
    rule_name = "jump_statement_2"
    p[0] = Node(name="JumpStatement", val="", type="", lno=p.lineno(1), children=[])
    p[0].ast = build_AST(p, rule_name)
    if len(p) == 3:
        if ST.curFuncReturnType != "void":
            ST.error(
                Error(
                    p.lineno(1),
                    rule_name,
                    "compilation error",
                    "Function return type is not void",
                )
            )
        code_gen.append(["return0", "", "", ""])
        activation_record.append(["return0", "", "", ""])

    else:
        offset_string = cal_offset(p[2])
        if p[2].type != "" and ST.curFuncReturnType != p[2].type:
            ST.error(
                Error(
                    p.lineno(1),
                    rule_name,
                    "warning",
                    f"Function return type is not {p[2].type}",
                )
            )

        code_gen.append([f"return{get_data_type_size(p[2].type)}", p[2].place, "", ""])
        activation_record.append(
            [f"return{get_data_type_size(p[2].type)}", offset_string, "", "",]
        )


def p_translation_unit(p):
    """translation_unit : external_declaration
    | translation_unit external_declaration
    """
    rule_name = "translation_unit"
    p[0] = Node(name="JumpStatement", val="", type="", lno=p.lineno(1), children=[])
    if len(p) == 2:
        p[0].children.append(p[1])
    else:
        p[0].children.append(p[2])
    p[0].ast = build_AST(p, rule_name)


def p_external_declaration(p):
    """external_declaration : function_definition
    | declaration
    """
    rule_name = "external_declaration"
    p[0] = p[1]
    p[0].name = "ExternalDeclaration"
    # p[0].ast = build_AST(p, rule_name)


# def p_function_definition_1(p):
#     """function_definition : declaration_specifiers declarator declaration_list compound_statement
#     | declarator declaration_list function_compound_statement
#     | declarator function_compound_statement
#     """
#     rule_name = "function_definition_1"
#     if len(p) == 3:
#         p[0] = Node(
#             name="FuncDeclWithoutType",
#             val=p[1].val,
#             type="int",
#             lno=p[1].lno,
#             children=[],
#         )
#     elif len(p) == 4:
#         p[0] = Node(
#             name="FuncDeclWithoutType",
#             val=p[1].val,
#             type="int",
#             lno=p[1].lno,
#             children=[],
#         )
#     else:
#         p[0] = Node(
#             name="FuncDecl",
#             val=p[2].val,
#             type=p[1].type,
#             lno=p[1].lno,
#             children=[],
#         )
#     p[0].ast = build_AST(p, rule_name)


def p_function_definition_2(p):
    """function_definition : declaration_specifiers declarator funcmark1 function_compound_statement"""
    rule_name = "function_definition_2"
    if p[1].type.upper() in PRIMITIVE_TYPES:
        p[1].type = TYPE_EASY[p[1].type.upper()].lower()

    p[0] = Node(
        name="FuncDecl", val=p[2].val, type=p[1].type, lno=p.lineno(1), children=[],
    )
    p[0].ast = build_AST_2(p, [1, 2, 4], rule_name)
    code_gen.append(["endfunc", "", "", ""])
    activation_record.append(["endfunc", "", "", ""])
    # funcstack.pop()


def p_funcmark1(p):
    """funcmark1 :"""
    # ST.scope_tables[ST.currentScope].in_whose_scope = ST.currentScope
    # print(p[-1])

    ##Yha bhi offset krna hai -- Akshay ?
    code_gen.append(["funcstart", p[-1].val, "", ""])
    activation_record.append(["funcstart", p[-1].val, "", ""])


# def p_func_m1(p):
#     """func_m1 :"""
#     label = ST.get_tmp_label()
#     code_gen.append(["label", label, ":", ""])
#     funcstack.append(label)


def p_push_scope_lcb(p):
    """push_scope_lcb : LEFT_CURLY_BRACKET"""
    ST.push_scope()
    offsets[ST.currentScope] = 0

    p[0] = p[1]


def p_push_scope_lb(p):
    """push_scope_lb : LEFT_BRACKET"""
    ST.push_scope()
    offsets[ST.currentScope] = 0

    p[0] = p[1]


def p_pop_scope_rcb(p):
    """pop_scope_rcb : RIGHT_CURLY_BRACKET"""
    # ST.scope_tables[ST.currentScope].assign_in_whose_scope()
    ST.pop_scope()

    p[0] = p[1]


# def p_inheritance_specifier(p):
#     """inheritance_specifier : access_specifier IDENTIFIER"""
#     p[0] = ["inheritance_specifier"] + p[1:]


# def p_inheritance_specifier_list(p):
#     """inheritance_specifier_list : inheritance_specifier
#     | inheritance_specifier_list COMMA inheritance_specifier"""
#     p[0] = ["inheritance_specifier_list"] + p[1:]


# def p_access_specifier(p):
#     """access_specifier : PRIVATE
#     | PUBLIC
#     | PROTECTED"""
#     p[0] = p[1:]


# def p_class_definition_head(p):
#     """class_definition_head : CLASS IDENTIFIER  INHERITANCE_OP inheritance_specifier_list
#     | CLASS IDENTIFIER
#     | CLASS INHERITANCE_OP inheritance_specifier_list
#     | CLASS"""
#     p[0] = ["class_definition_head"] + p[1:]


# def p_class_definition(p):
#     """class_definition : class_definition_head LEFT_CURLY_BRACKET class_internal_definition_list RIGHT_CURLY_BRACKET
#     | class_definition_head"""
#     p[0] = ["class_definition"] + p[1:]


# def p_class_internal_definition_list(p):
#     """class_internal_definition_list : class_internal_definition
#     | class_internal_definition_list class_internal_definition"""
#     p[0] = ["class_internal_definition_list"] + p[1:]


# def p_class_internal_definition(p):
#     """class_internal_definition : access_specifier LEFT_CURLY_BRACKET class_member_list RIGHT_CURLY_BRACKET SEMICOLON"""
#     p[0] = ["class_internal_definition"] + p[1:]


# def p_class_member_list(p):
#     """class_member_list : class_member
#     | class_member_list class_member"""
#     p[0] = ["class_member_list"] + p[1:]


# def p_class_member(p):
#     """class_member : function_definition
#     | declaration"""
#     p[0] = ["class_member"] + p[1:]


# Error rule for syntax errors
def p_error(p):
    if p:
        ST.error(Error(p.lineno, "error", "semantic/syntax error", "Unknown"))


# Build the parser
parser = yacc.yacc(start="translation_unit")


def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-input", type=str, required=True, help="Input file")
    parser.add_argument("-o", "--output", type=str, default="AST", help="Output file")
    parser.add_argument("-v", action="store_true", help="Verbose output")
    parser.add_argument("-w", action="store_true", help="Warning")
    return parser


class TimeoutException(Exception):  # Custom exception class
    pass


def timeout_handler(signum, frame):  # Custom signal handler
    raise TimeoutException


def async_parse(data, seconds=10):
    # signal.signal(signal.SIGALRM, timeout_handler)
    # signal.alarm(seconds)
    try:
        res = parser.parse(data)
        # signal.alarm(0)  # Clear alarm
        return res
    except TimeoutException:
        lineno = parser.token().lineno
        print("Compiler Timed Out at Line", lineno)
        # Change final error from syntax/semantic to compilation?
        ST.errors[-1].err_type = "compilation error"
    return


if __name__ == "__main__":
    args = getArgs().parse_args()
    graph = Digraph(format="dot")
    with open(str(args.input), "r+") as file:
        data = file.read()
    pre_append_to_table()
    tree = async_parse(data)

    ST.display_errors(args.w)
    if ST.error_flag == 0:

        # if args.output[-4:] == ".dot":
        #     args.output = args.output[:-4]
        #     graph.render(filename=args.output, cleanup=True)
        # else:
        #     graph.render(filename="ast", cleanup=True)
        file = open("3ac.txt", "w")

        # Saving the array in a text file
        # for content in code_gen:
        #     file.write(str(content))
        #     file.write("\n")
        # file.close()
        # remove_redundant_label(code_gen)
        write_code(code_gen, file)
        file = open("activation_record.txt", "w")
        write_code(activation_record, file)
        file = open("mips_generated.s", "w")
        write_code(mips_generation(activation_record), file)

    dump_symbol_table_csv(args.v)

    # print(ST.scope_tables[])
