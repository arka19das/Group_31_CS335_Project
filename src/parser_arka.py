# TODO: check invalid operation on function and backpatching
# TODO: small error,, in repeated cases unable to display line number
# Yacc example
from cmath import exp
import copy
import json
import pprint
import sys
from xml.sax import default_parser_list

from numpy import var

import ply.yacc as yacc
import pydot
from graphviz import Digraph

from scanner import *
from utils import *
from utils import offsets, code_gen, contStack, brkStack

# Get the token map from the lexer.  This is required.
lexer = Lexer()
lexer.build()
tokens = lexer.tokens


cur_num = 0


offsets[0] = 0


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
        p[0] = p[2]


def p_float_constant(p):
    """float_constant : FLOAT_CONSTANT"""
    p[0] = Node(
        name="Constant",
        val=p[1],
        lno=p.lineno(1),
        type="float",
        children=[],
        place=p[1],
    )
    rule_name = "float_constant"
    p[0].ast = build_AST(p, rule_name)


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
    )
    rule_name = "hex_constant"
    p[0].ast = build_AST(p, rule_name)


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
    )
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
    )
    rule_name = "int_constant"
    p[0].ast = build_AST(p, rule_name)


def p_char_constant(p):
    """char_constant : CHAR_CONSTANT"""
    p[0] = Node(
        name="Constant",
        val=p[1],
        lno=p.lineno(1),
        type="char",
        children=[],
        place=p[1],
        code="",
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
        if str(p[0].type).count("*") != 0:
            p[0].level = str(p[0].type).count("*")
        p[0].array = p1_node.array
        p[0].level += len(p1_node.array)
        p[0].is_func = p1_node.is_func
        p[0].ast = build_AST(p, rule_name)
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
        if len(p[1].array) > 0 and p[1].level > 0:
            ST.error(
                Error(
                    p[1].lno,
                    rule_name,
                    "compilation error",
                    f"Array {p[1].val} pointer increment",
                )
            )

        tmp_var = ST.get_tmp_var(p[1].type)
        p[0] = Node(
            name="IncrementOrDecrementExpression",
            val=p[1].val,
            lno=p[1].lno,
            type=p[1].type,
            children=[],
            place=tmp_var,
        )
        p[0].ast = build_AST_2(p, [1], p[2])
        check_identifier(p[1])
        if p[1].type.endswith("*"):
            code_gen.append(["8=", p[1].place, tmp_var])
        else:
            code_gen.append(
                [str(get_data_type_size(p[1].type)) + "=", p[1].place, tmp_var]
            )

        # code_gen.append(f"f{tmp_var} := {p[1].place}")
        # DONE: FLOAT not supported yet and neither are pointers dhang se
        if p[2] == "++":
            if p[1].type.endswith("*"):
                # print(p[1].type[:-1] + "1")
                code_gen.append(
                    [
                        "long+",
                        p[1].place,
                        p[1].place,
                        get_data_type_size(p[1].type[:-2]),
                    ]
                )
            else:
                code_gen.append([p[1].type + "+", p[1].place, p[1].place, 1])
            # code_gen.append(f"{p[1].place} := {p[1].place} + 1")
        elif p[2] == "--":
            if p[1].type.endswith("*"):
                code_gen.append(
                    [
                        "long+",
                        p[1].place,
                        p[1].place,
                        -get_data_type_size(p[1].type[:-2]),
                    ]
                )
            else:
                code_gen.append([p[1].type + "+", p[1].place, p[1].place, -1])
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
            elif len(p1v_node.argument_list) != 0:
                ST.error(
                    Error(
                        p[1].lno,
                        rule_name,
                        "semantic error",
                        f"Function {p[1].val} called with incorrect number of arguments",
                    )
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
            )
            p[0].ast = build_AST_2(p, [1, 3], p[2])

            struct_name = p[1].type
            if (struct_name.endswith("*") and p[2][0] == ".") or (
                not struct_name.endswith("*") and p[2][0] == "->"
            ):
                ST.error(
                    Error(
                        p[1].lno,
                        rule_name,
                        "compilation error",
                        f"Invalid operator on {struct_name}",
                    )
                )
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

            struct_node = ST.find(struct_name)
            flag = 0
            for curr_list in struct_node.field_list:
                if curr_list[1] == p[3][0]:
                    flag = 1
                    p[0].type = curr_list[0]
                    p[0].parentStruct = struct_name
                    p[0].level = curr_list[0].count("*")
                    if len(curr_list) == 5:
                        p[0].level += len(curr_list[4])

            if p[0].level == -1:
                ST.error(
                    Error(
                        p[1].lno,
                        rule_name,
                        "compilation error",
                        f"Incorrect number of dimensions for {p[1].val}",
                    )
                )
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
            temp_var = p[3].place
            if p[3].type.upper() not in TYPE_INTEGER + TYPE_CHAR:
                ST.error(
                    Error(
                        p[3].lno,
                        rule_name,
                        "compilation error",
                        "Array Index is of incompatible type",
                    )
                )
            elif p[3].type.upper()[-3:] != "INT":
                # int long unisgnedint,unsigned long,unsigned short,short,char, unsigned_char

                temp_var = ST.get_tmp_var("int")
                code_gen.append([p[3].type + "2int", temp_var, p[3].place])

        else:
            p[0] = Node(
                name="FunctionCall2",
                val=p[1].val,
                lno=p[1].lno,
                type=p[1].type,
                children=[],
                is_func=0,
                place=p[1].place,
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
            elif len(p1v_node.argument_list) != len(p[3].children):
                ST.error(
                    Error(
                        p[1].lno,
                        rule_name,
                        "semantic error",
                        "Incorrect number of arguments for function call",
                    )
                )
            else:
                i = 0
                for arguments in p1v_node.argument_list:
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

                    if ST.curType[-1].split()[-1] != arguments.split()[-1]:
                        ST.error(
                            Error(
                                p[1].lno,
                                rule_name,
                                "warning",
                                f"Type mismatch in argument {i+1} of function call. Expected: {arguments}, Received: {ST.curType}",
                            )
                        )
                    i += 1


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
        p[0] = p[1]
        # p[0].ast = build_AST(p, rule_name)
    elif len(p) == 3:
        if p[1] == "++" or p[1] == "--":
            if len(p[2].array) > 0 and p[2].level > 0:
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
                name="UnaryOperation",
                val=p[2].val,
                lno=p[2].lno,
                type=p[2].type,
                children=[tempNode, p[2]],
                place=p[2].place,
            )
            check_identifier(p[2])

            # DONE: FLOAT not supported yet and neither are pointers dhang se
            if p[1] == "++":
                if p[2].type.endswith("*"):
                    code_gen.append(
                        [
                            "long+",
                            p[2].place,
                            p[2].place,
                            get_data_type_size(p[2].type[:-2]),
                        ]
                    )
                else:
                    code_gen.append([p[2].type + "+", p[2].place, p[2].place, 1])
                # code_gen.append(f"{p[1].place} := {p[1].place} + 1")
            elif p[1] == "--":
                if p[2].type.endswith("*"):
                    code_gen.append(
                        [
                            "long+",
                            p[2].place,
                            p[2].place,
                            -get_data_type_size(p[2].type[:-2]),
                        ]
                    )
                else:
                    code_gen.append([p[2].type + "+", p[2].place, p[2].place, -1])
                # code_gen.append(f"{p[1].place} := {p[1].place} - 1")
            #
            # code_gen.append()
            # p[0].ast = build_AST(p, rule_name)

        elif p[1] == "sizeof":
            # MODIFIED
            tmp_var = ST.get_tmp_var("int")

            p[0] = Node(
                name="SizeOf",
                val=tmp_var,
                lno=p[2].lno,
                type="int",
                children=[p[2]],
                place=tmp_var,
            )

            # p[0].ast = build_AST(p, rule_name)
            # print(p[3])
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
        elif p[1].val == "&":
            # TODO:3ac
            p[0] = Node(
                name="AddressOfVariable",
                val=p[2].val,
                lno=p[2].lno,
                type=p[2].type + " *",
                level=p[1].level + 1,
                children=[p[2]],
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
                type=p[2].type[: len(p[2].type) - 2],
                children=[p[2]],
            )
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
            tmp_var = ST.get_tmp_var(p[2].type)
            tmp_var
            p[0] = Node(
                name="UnaryOperationMinus",
                val=tmp_var,
                lno=p[2].lno,
                type=p[2].type,
                children=[p[2]],
                place=tmp_var,
            )
            code_gen.append([p[2].type + "_uminus", tmp_var, "0", p[2].place])
        else:
            p[0] = Node(
                name="UnaryOperation",
                val=p[2].val,
                lno=p[2].lno,
                type=p[2].type,
                children=[],
            )
        p[0].ast = build_AST(p, rule_name)
    else:
        # MODIFIED
        tmp_var = ST.get_tmp_var("int")
        p[0] = Node(
            name="SizeOf",
            val=tmp_var,
            lno=p[3].lno,
            type="int",
            children=[p[3]],
            place=tmp_var,
        )
        # p[0].ast = build_AST(p, rule_name)
        # print(p[3])
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
        code_gen.append(["4=", tmp_var, type_size])
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
        # TODO: ERROR HANDLING
        tmp_var = ST.get_tmp_var(p[2].type)
        p[0] = Node(
            name="TypeCasting",
            val=p[2].val,
            lno=p[2].lno,
            type=p[2].type,
            level=p[2].type.count("*"),
            children=[],
            place=tmp_var,
        )
        code_gen.append(
            [f"convert ({p[2].type}, {p[4].type})", p[4].place, " ", tmp_var]
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
        # print(p[0])
        # print(p[1])
        # print(p[2])
        # print(p[3])
        tmp_var1 = p[1].place
        tmp_var3 = p[3].place
        if p[1].type != p[0].type:
            tmp_var1 = ST.get_tmp_var(p[0].type)
            code_gen.append([p[1].type + "2" + p[0].type, tmp_var1, p[1].place])
        if p[3].type != p[0].type:
            tmp_var3 = ST.get_tmp_var(p[0].type)
            code_gen.append([p[3].type + "2" + p[0].type, tmp_var3, p[3].place])
        code_gen.append([p[0].type + _op, p[0].place, tmp_var1, tmp_var3])
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
        tmp_var1 = p[1].place
        tmp_var3 = p[3].place
        if p[1].type != p[0].type:
            tmp_var1 = ST.get_tmp_var(p[0].type)
            code_gen.append([p[1].type + "2" + p[0].type, tmp_var1, p[1].place])
        if p[3].type != p[0].type:
            tmp_var3 = ST.get_tmp_var(p[0].type)
            code_gen.append([p[3].type + "2" + p[0].type, tmp_var3, p[3].place])
        code_gen.append([p[0].type + _op, p[0].place, tmp_var1, tmp_var3])
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
        tmp_var1 = p[1].place
        tmp_var3 = p[3].place
        if p[1].type != p[0].type:
            tmp_var1 = ST.get_tmp_var(p[0].type)
            code_gen.append([p[1].type + "2" + p[0].type, tmp_var1, p[1].place])
        if p[3].type != p[0].type:
            tmp_var3 = ST.get_tmp_var(p[0].type)
            code_gen.append([p[3].type + "2" + p[0].type, tmp_var3, p[3].place])
        code_gen.append([p[0].type + _op, p[0].place, tmp_var1, tmp_var3])
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
        tmp_var1 = p[1].place
        tmp_var3 = p[3].place
        if p[1].type != p[0].type:
            tmp_var1 = ST.get_tmp_var(p[0].type)
            code_gen.append([p[1].type + "2" + p[0].type, tmp_var1, p[1].place])
        if p[3].type != p[0].type:
            tmp_var3 = ST.get_tmp_var(p[0].type)
            code_gen.append([p[3].type + "2" + p[0].type, tmp_var3, p[3].place])
        code_gen.append([p[0].type + _op, p[0].place, tmp_var1, tmp_var3])
        p[0].ast = build_AST_2(p, [1, 3], rule_name)


def p_equality_expresssion(p):
    """equality_expression : relational_expression
    | equality_expression EQ_OP relational_expression
    | equality_expression NE_OP relational_expression
    """
    if len(p) == 2:
        p[0] = p[1]
        # p[0].ast = build_AST(p, rule_name)
    else:
        rule_name = p[2]
        _op = p[2][0] if p[2] is tuple else p[2]
        p[0] = type_util(p[1], p[3], _op)
        tmp_var1 = p[1].place
        tmp_var3 = p[3].place
        if p[1].type != p[0].type:
            tmp_var1 = ST.get_tmp_var(p[0].type)
            code_gen.append([p[1].type + "2" + p[0].type, tmp_var1, p[1].place])
        if p[3].type != p[0].type:
            tmp_var3 = ST.get_tmp_var(p[0].type)
            code_gen.append([p[3].type + "2" + p[0].type, tmp_var3, p[3].place])
        code_gen.append([p[0].type + _op, p[0].place, tmp_var1, tmp_var3])
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
        tmp_var1 = p[1].place
        tmp_var3 = p[3].place
        if p[1].type != p[0].type:
            tmp_var1 = ST.get_tmp_var(p[0].type)
            code_gen.append([p[1].type + "2" + p[0].type, tmp_var1, p[1].place])
        if p[3].type != p[0].type:
            tmp_var3 = ST.get_tmp_var(p[0].type)
            code_gen.append([p[3].type + "2" + p[0].type, tmp_var3, p[3].place])
        code_gen.append([p[0].type + _op, p[0].place, tmp_var1, tmp_var3])
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
        tmp_var1 = p[1].place
        tmp_var3 = p[3].place

        if p[1].type != p[0].type:
            tmp_var1 = ST.get_tmp_var(p[0].type)
            code_gen.append([p[1].type + "2" + p[0].type, tmp_var1, p[1].place])
        if p[3].type != p[0].type:
            tmp_var3 = ST.get_tmp_var(p[0].type)
            code_gen.append([p[3].type + "2" + p[0].type, tmp_var3, p[3].place])
        code_gen.append([p[0].type + _op, p[0].place, tmp_var1, tmp_var3])
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
        tmp_var1 = p[1].place
        tmp_var3 = p[3].place
        if p[1].type != p[0].type:
            tmp_var1 = ST.get_tmp_var(p[0].type)
            code_gen.append([p[1].type + "2" + p[0].type, tmp_var1, p[1].place])
        if p[3].type != p[0].type:
            tmp_var3 = ST.get_tmp_var(p[0].type)
            code_gen.append([p[3].type + "2" + p[0].type, tmp_var3, p[3].place])
        code_gen.append([p[0].type + _op, p[0].place, tmp_var1, tmp_var3])
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
        tmp_var1 = p[1].place
        tmp_var3 = p[4].place
        if p[1].type != p[0].type:
            tmp_var1 = ST.get_tmp_var(p[0].type)
            code_gen.append([p[1].type + "2" + p[0].type, tmp_var1, p[1].place])
        if p[4].type != p[0].type:
            tmp_var3 = ST.get_tmp_var(p[0].type)
            code_gen.append([p[4].type + "2" + p[0].type, tmp_var3, p[4].place])
        code_gen.append([p[0].type + _op, p[0].place, tmp_var1, tmp_var3])
        p[0].ast = build_AST_2(p, [1, 4], rule_name)


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
        tmp_var1 = p[1].place
        tmp_var3 = p[4].place

        if p[1].type != p[0].type:
            tmp_var1 = ST.get_tmp_var(p[0].type)
            code_gen.append([p[1].type + "2" + p[0].type, tmp_var1, p[1].place])
        if p[4].type != p[0].type:
            tmp_var3 = ST.get_tmp_var(p[0].type)
            code_gen.append([p[4].type + "2" + p[0].type, tmp_var3, p[4].place])
        code_gen.append([p[0].type + _op, p[0].place, tmp_var1, tmp_var3])
        p[0].ast = build_AST_2(p, [1, 3], rule_name)
        # code_gen.append(["label", p[2][0], ":", ""])


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
            type=p[4].type,
            children=[],
        )
        p[0].ast = build_AST_2(p, [3, 5], ":")
        # TODO:Ternary operator
        p[0].ast = build_AST_2(p, [1, 0], "?")


def p_assignment_expression(p):
    """assignment_expression : conditional_expression
    | unary_expression assignment_operator assignment_expression
    """
    rule_name = "assignment_expression"
    # print(p[0], "\n", p[1])
    if len(p) == 2:
        p[0] = p[1]

        # p[0].ast = build_AST(p, rule_name)
    else:
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
        if p[1].level != p[3].level:
            ST.error(
                Error(
                    p[1].lno,
                    rule_name,
                    "compilation error",
                    "Type mismatch in assignment: Pointers of different levels",
                )
            )
        elif (p[1].level and len(p[1].array) > 0) and (
            p[3].level and len(p[3].array) > 0
        ):
            ST.error(
                Error(
                    p[1].lno,
                    rule_name,
                    "compilation error",
                    "Invalid array assignment",
                )
            )
        elif p[1].type.split()[-1] != p[3].type.split()[-1]:
            ST.error(
                Error(
                    p[1].lno,
                    rule_name,
                    "warning",
                    "Type mismatch in assignment",
                )
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

        p1_node = ST.find(p[1].val)
        if (p1_node is not None) and ((p[1].is_func == 1)):
            ST.error(
                Error(
                    p[1].lno,
                    rule_name,
                    "compilation error",
                    f"Invalid operation on {p[1].val}",
                )
            )

        p3_node = ST.find(p[3].val)
        if (p3_node is not None) and ((p[3].is_func == 1)):
            ST.error(
                Error(
                    p[1].lno,
                    rule_name,
                    "compilation error",
                    f"Invalid operation on {p[3].val}",
                )
            )

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

        p[0] = Node(
            name="AssignmentOperation",
            val=p[1].val,
            type=p[1].type,
            lno=p[1].lno,
            children=[],
            level=p[1].level,
        )
        temp_node = p[3]

        if p[2].val != "=":
            _op = p[2].val[:-1]
            temp_node = type_util(p[1], p[3], _op)
            tmp_var1 = p[1].place
            tmp_var3 = p[3].place
            if p[1].type != temp_node.type:
                tmp_var1 = ST.get_tmp_var(temp_node.type)
                code_gen.append(
                    [p[1].type + "2" + temp_node.type, tmp_var1, p[1].place]
                )
            if p[3].type != temp_node.type:
                tmp_var3 = ST.get_tmp_var(p[0].type)
                code_gen.append(
                    [p[3].type + "2" + temp_node.type, tmp_var3, p[3].place]
                )
            code_gen.append([temp_node.type + _op, temp_node.place, tmp_var1, tmp_var3])
            # print(temp_node)

        if p[0].type != temp_node.type:
            temp_node1 = ST.get_tmp_var(p[0].type)
            code_gen.append([temp_node.type + "2" + p[0].type, temp_node1, p[1].place])
            code_gen.append([p[0].type + "=", p[1].place, temp_node1, ""])

        else:
            code_gen.append([temp_node.type + "=", p[1].place, temp_node.place, ""])

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
        name="AssignmentOperator",
        val=p[1],
        type="",
        lno=p.lineno(1),
        children=[p[1]],
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
        # print(p[1].type)
        p[1].type = TYPE_EASY[p[1].type.upper()].lower()
    if len(p) == 3:

        p[0] = p[1]
        # print("First one used")
        p[0].ast = build_AST(p, rule_name)
    else:

        p[0] = Node(
            name="Declaration",
            val=p[1],
            type=p[1].type,
            lno=p.lineno(1),
            children=[],
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
                    type=p[1].type,
                    val=child.children[1].val,
                    size=get_data_type_size(p[1].type),
                    offset=offsets[ST.currentScope],
                )
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
                # above line maybe necessary to be commented
            else:
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
                    type=p[1].type,
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
                if len(child.type) > 0:
                    node.type = p[1].type + " " + child.type
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
            # print(p[1].type)
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
            # print(p[1].type)
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
            name=p[1].name + p[2].name,
            val=p[1],
            type=ty,
            lno=p[1].lno,
            children=[],
        )
        p[0].ast = build_AST(p, rule_name)


def p_init_declarator_list(p):
    """init_declarator_list : init_declarator
    | init_declarator_list COMMA init_declarator
    """
    rule_name = "init_declarator_list"
    if len(p) == 2:
        p[0] = Node(
            name="InitDeclaratorList",
            val="",
            type="",
            lno=p.lineno(1),
            children=[p[1]],
        )
        # p[0].ast = p[1].ast
        p[0].ast = build_AST(p, rule_name)
    else:
        p[0] = p[1]
        p[0].children.append(p[3])
        p[0].ast = build_AST(p, rule_name)
        # p[0].ast = build_AST_2(p,[1,3],',')


def p_init_declarator(p):
    """init_declarator : declarator
    | declarator EQ initializer
    """
    rule_name = "init_declarator"
    if len(p) == 2:
        p[0] = p[1]
        # p[0].ast = p[1].ast
        p[0].ast = build_AST(p, rule_name)
    else:
        p[0] = Node(
            name="InitDeclarator",
            val="",
            type=p[1].type,
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
                    p.lineno(1),
                    rule_name,
                    "compilation error",
                    "Invalid Initializer",
                )
            )
        if p[1].level != p[3].level:
            ST.error(Error(p[1].lno, rule_name, "compilation error", "Type Mismatch"))


def p_storage_class_specifier(p):
    """storage_class_specifier : TYPEDEF
    | AUTO
    """
    p[0] = Node(
        name="StorageClassSpecifier",
        val="",
        type=p[1],
        lno=p.lineno(1),
        children=[],
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
    | class_definition
    | BOOL
    """
    # rule_name = "type_specifier_1"
    p[0] = Node(name="TypeSpecifier1", val="", type=p[1], lno=p.lineno(1), children=[])
    # p[0].ast = build_AST(p,rule_name)


def p_type_specifier_2(p):
    """type_specifier : struct_or_union_specifier"""
    rule_name = "type_specifier_2"
    p[0] = p[1]
    p[0].ast = build_AST(p, rule_name)


def p_struct_or_union_specifier(p):
    """struct_or_union_specifier : struct_or_union IDENTIFIER push_scope_lcb struct_declaration_list pop_scope_rcb
    | struct_or_union push_scope_lcb struct_declaration_list pop_scope_rcb
    | struct_or_union IDENTIFIER
    """
    # p[0] = build_AST(p)
    # TODO : check the semicolon thing after pop_scope_rcb in gramamar
    # TODO : Manage the size and offset of fields
    rule_name = "struct_or_union_specifier"
    p[0] = Node(
        name="StructOrUnionSpecifier",
        val="",
        type="",
        lno=p[1].lno,
        children=[],
    )
    if len(p) == 6:
        val_name = p[1].type + " " + p[2]
        p[0].ast = build_AST(p, rule_name)
        if ST.current_table.find(val_name):
            ST.error(
                Error(
                    p[1].lno,
                    rule_name,
                    "compilation error",
                    f"Struct {val_name} already declared",
                )
            )

        valptr_name = val_name + " *"
        val_node = Node(name=val_name, type=val_name)
        valptr_node = Node(name=valptr_name, type=valptr_name)
        ST.current_table.nodes += [val_node, valptr_node]
        temp_list = []
        curr_offset = 0
        max_size = 0
        for child in p[4].children:
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
        name="StructOrUNion",
        val="",
        type="struct",
        lno=p.lineno(1),
        children=[],
    )
    p[0].ast = build_AST(p, rule_name)


def p_struct_declaration_list(p):
    """struct_declaration_list : struct_declaration
    | struct_declaration_list struct_declaration
    """
    rule_name = "struct_declaration_list"
    p[0] = Node(
        name="StructDeclarationList",
        val="",
        type=p[1].type,
        lno=p[1].lno,
        children=[],
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
        name="StructDeclaration",
        val="",
        type=p[1].type,
        lno=p[1].lno,
        children=[],
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
        name="StructDeclaratorList",
        val="",
        type=p[1].type,
        lno=p[1].lno,
        children=[],
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
    # print(
    #     str(len(p)), "p_direct_declarator_2 is called := ", p[1], "\n", ST.curType
    # )  # "\n", tempList
    if len(p) == 2:
        p[0] = Node(name="ID", val=p[1], type="", lno=p.lineno(1), children=[])
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
        for child in p[3].children:
            tempList.append(child.type)

        node.argument_list = tempList
        node.type = ST.curType[-1 - len(tempList)]
        ST.parent_table.insert(node)
        ST.curFuncReturnType = copy.deepcopy(ST.curType[-1 - len(tempList)])
        ST.current_table.name = p[1].val


def p_direct_declarator_3(p):
    """direct_declarator : direct_declarator LEFT_THIRD_BRACKET constant_expression RIGHT_THIRD_BRACKET"""
    rule_name = "direct_declarator_3"
    p[0] = Node(
        name="ArrayDeclarator",
        val=p[1].val,
        type="",
        lno=p.lineno(1),
        children=[],
    )
    p[0].ast = build_AST(p, rule_name)
    p[0].array = copy.deepcopy(p[1].array)
    p[0].array.append(int(p[3].val))


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
        node = Node(name=p[1].val, type=ST.curType[-1], is_func=1, argument_list=[])
        # Modified
        ST.parent_table.insert(node)
        ST.curFuncReturnType = copy.deepcopy(ST.curType[-1])
        ST.current_table.name = p[1].val


def p_pointer(p):
    """pointer : MULTIPLY
    | MULTIPLY type_qualifier_list
    | MULTIPLY pointer
    | MULTIPLY type_qualifier_list pointer
    """
    rule_name = "pointer"
    if len(p) == 2:
        p[0] = Node(name="Pointer", val="", type="*", lno=p.lineno(1), children=[])
        p[0].ast = build_AST(p, rule_name)
    elif len(p) == 3:
        p[0] = Node(
            name="Pointer",
            val="",
            type=p[2].type + " *",
            lno=p.lineno(1),
            children=[],
        )
        p[0].ast = build_AST(p, rule_name)
    else:
        p[0] = Node(
            name="Pointer",
            val="",
            type=p[2].type + " *",
            lno=p[2].lno,
            children=[],
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
        # print(p[1].type)
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
            name="IdentifierList",
            val=p[1],
            type="",
            lno=p.lineno(1),
            children=[p[1]],
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
        # print(p[1])
        p[0] = p[1]
        p[0].name = "TypeName"
    else:
        # print(p[1], p[2])
        p[0] = Node(name="TypeName", val="", type=p[1].type, lno=p[1].lno, children=[])
        if p[2].type.endswith("*"):
            p[0].type = p[0].type + "*" * (p[2].type.count("*"))
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
    """initializer : assignment_expression
    | LEFT_CURLY_BRACKET initializer_list RIGHT_CURLY_BRACKET
    | LEFT_CURLY_BRACKET initializer_list COMMA RIGHT_CURLY_BRACKET
    """
    rule_name = "initializer"
    if len(p) == 2:
        p[0] = p[1]
        p[0].ast = build_AST(p, rule_name)
    else:
        p[0] = p[2]
        p[0].is_array = True

    p[0].name = "Initializer"
    if len(p) == 4:
        p[0].max_depth = p[2].max_depth + 1
        p[0].ast = build_AST(p, rule_name)
    elif len(p) == 5:
        p[0].ast = build_AST(p, rule_name)


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
    p[0] = Node(
        name="Statement",
        val="",
        type="",
        children=[],
        lno=p.lineno(1),
    )
    if isinstance(p[1], Node):
        p[0].label = p[1].label
        p[0].expr = p[1].expr
    p[0].ast = build_AST(p, rule_name)


def p_labeled_statement(p):
    """labeled_statement : IDENTIFIER COLON statement
    | Switch_M CASE constant_expression COLON statement
    | Switch_M DEFAULT COLON statement"""
    rule_name = "labeled_statement"
    name = ""
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

        # print(p[3])
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
            label=p[1].label + p[2].label,
            expr=p[1].expr + p[2].expr,
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
            name="CompoundStatement",
            val="",
            type="",
            lno=p.lineno(1),
            children=[],
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
            name="CompoundStatement",
            val="",
            type="",
            children=[],
            lno=p.lineno(1),
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
            name="DeclarationList",
            val="",
            type="",
            children=[],
            lno=p.lineno(1),
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
        # print("3", p[1].expr)


def p_expression_statement(p):
    """expression_statement : SEMICOLON
    | expression SEMICOLON
    """
    rule_name = "expression_statement"
    p[0] = Node(
        name="ExpressionStatement",
        val="",
        type="",
        children=[],
        lno=p.lineno(1),
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
                name="IfStatment",
                val="",
                type="",
                children=[],
                lno=p.lineno(1),
            )
            code_gen.append(["label", p[5][0], ":", ""])

        else:
            # ST.subscope_name = "if"
            p[0] = Node(
                name="IfElseStatement",
                val="",
                type="",
                children=[],
                lno=p.lineno(1),
            )
            code_gen.append(["label", p[5][1], ":", ""])
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
            name="SwitchStatement",
            val="",
            type="",
            children=[],
            lno=p.lineno(1),
        )
        # print(p[6])

    p[0].ast = build_AST(p, rule_name)


def p_if_M1(p):
    """if_M1 :"""
    label1 = ST.get_tmp_label()
    label2 = ST.get_tmp_label()
    code_gen.append(["beq", p[-2].place, "0", label1])
    p[0] = [label1, label2]


def p_if_M2(p):
    """if_M2 :"""
    code_gen.append(["goto", "", "", p[-3][1]])
    code_gen.append(["label", p[-3][0], ":", ""])


def p_Switch_M2(p):
    """Switch_M2 :"""
    # print(p[-2])
    label1 = ST.get_tmp_label()
    code_gen.append(["goto", "", "", label1])
    label2 = ST.get_tmp_label()
    brkStack.append(label2)
    p[0] = [label1, label2]


def p_Switch_M3(p):
    """Switch_M3 :"""
    # print(p[-2])
    # print(p[-4])
    code_gen.append(
        ["goto", "", "", p[-2][1]]
    )  ### after all cases break from switch case

    code_gen.append(["label", p[-2][0], ":", ""])
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

    if p[-4].type[-4:] == "char":

        tmp_var = ST.get_tmp_var("int")
        code_gen.append([p[-4].type + "2int", tmp_var, p[-4].place])
    for i in range(0, len(p[-1].expr)):
        case = p[-1].expr[i]
        if case == "":
            flag = True
            default_array = ["goto", "", "", p[-1].label[i]]
        else:
            if case[0] == "'":
                case = str(ord(case[1:-1]))

            ## TODO: difference when p[-4] is long or unsigned long
            # if p[-4].type=="unsigned long" or p[-4].type=="long":

            code_gen.append(["beq", tmp_var, case, p[-1].label[i]])
    if flag:
        code_gen.append(default_array)
    brkStack.pop()
    code_gen.append(["label", p[-2][1], ":", ""])


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
            name="DoWhileStatement",
            val="",
            type="",
            children=[],
            lno=p.lineno(1),
        )
        p[0].ast = build_AST(p, rule_name)
    elif p[1] == "while":
        p[0] = Node(
            name="WhileStatement",
            val="",
            type="",
            children=[],
            lno=p.lineno(1),
        )
        p[0].ast = build_AST(p, rule_name)
    else:
        p[0] = Node(name="ForStatement", val="", type="", children=[], lno=p.lineno(1))
        p[0].ast = build_AST(p, rule_name)

    ST.looping_depth -= 1


def p_while_M1(p):
    """while_M1 :"""
    l1 = ST.get_tmp_label()
    l2 = ST.get_tmp_label()  ## non useful
    l3 = ST.get_tmp_label()
    contStack.append(l1)
    brkStack.append(l3)
    code_gen.append(["goto", "", "", l1])
    p[0] = [l1, l2, l3]


def p_while_M2(p):
    """while_M2 :"""
    code_gen.append(["beq", p[-2].place, "0", p[-4][2]])
    code_gen.append(["goto", "", "", p[-4][1]])  ## non useful
    code_gen.append(["label", p[-4][1], ":", ""])  ## non useful


def p_while_M3(p):
    """while_M3 :"""
    # print(p[-8])

    code_gen.append(["goto", "", "", p[-6][0]])
    code_gen.append(["label", p[-6][2], ":", ""])
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
    # print(brkStack)
    # print(contStack)
    p[0] = [l1, l2, l3]


def p_do_M2(p):
    """do_M2 :"""
    # print(p[-8])

    code_gen.append(["label", p[-3][1], ":", ""])


def p_do_M3(p):
    """do_M3 :"""
    code_gen.append(["beq", p[-2].place, "0", p[-7][2]])
    code_gen.append(["goto", "", "", p[-7][0]])  ## non useful
    code_gen.append(["label", p[-7][2], ":", ""])  ## non useful
    # print(1, brkStack)
    # print(1, contStack)
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
    p[0] = [l1, l2, l3, l4]


def p_FM2(p):
    """FM2 :"""
    # print(p[-1].place, p[-2])
    code_gen.append(["beq", p[-2].place, "0", p[-3][1]])


def p_FM8(p):
    """FM8 :"""
    # print(p[-5])
    code_gen.append(["goto", "", "", p[-4][0]])
    code_gen.append(["label", p[-4][1], ":", ""])
    contStack.pop()
    brkStack.pop()


def p_FM4(p):
    """FM4 :"""
    # print(p[-2])
    code_gen.append(["beq", p[-2].place, "0", p[-3][1]])
    code_gen.append(["goto", "", "", p[-3][2]])
    code_gen.append(["label", p[-3][3], ":", ""])


def p_FM9(p):
    """FM9 :"""
    # print(p[-2])
    # code_gen.append(["beq", p[-2].place, "0", p[-3][1]])
    code_gen.append(["goto", "", "", p[-2][2]])
    code_gen.append(["label", p[-2][3], ":", ""])


def p_FM3(p):
    """FM3 :"""
    # print(p[-5])
    code_gen.append(["goto", "", "", p[-6][0]])
    code_gen.append(["label", p[-6][1], ":", ""])
    contStack.pop()
    brkStack.pop()


def p_FM5(p):
    """FM5 :"""
    # print(p[-4])
    code_gen.append(["goto", "", "", p[-5][0]])


def p_FM6(p):
    """FM6 :"""
    # print(p[-6])
    code_gen.append(["label", p[-7][2], ":", ""])


def p_FM7(p):
    """FM7 :"""
    # print(p[-8])
    code_gen.append(["goto", "", "", p[-9][3]])
    code_gen.append(["label", p[-9][1], ":", ""])
    brkStack.pop()
    contStack.pop()


def p_FM10(p):
    """FM10 :"""
    # print(p[-4])
    code_gen.append(["goto", "", "", p[-4][0]])


def p_FM11(p):
    """FM11 :"""
    # print(p[-6])
    code_gen.append(["label", p[-6][2], ":", ""])


def p_FM12(p):
    """FM12 :"""
    # print(p[-8])
    code_gen.append(["goto", "", "", p[-8][3]])
    code_gen.append(["label", p[-8][1], ":", ""])
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
                p.lineno(1),
                rule_name,
                "compilation error",
                "continue not inside loop",
            )
        )
    elif temp == "continue":
        code_gen.append(["goto", "", "", contStack[-1]])
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
    else:
        # print("Yeh ffunction ke baare mei", p[2].type, " HUH ", ST.curFuncReturnType)
        if p[2].type != "" and ST.curFuncReturnType != p[2].type:
            ST.error(
                Error(
                    p.lineno(1),
                    rule_name,
                    "warning",
                    f"Function return type is not {p[2].type}",
                )
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
    """function_definition : declaration_specifiers declarator function_compound_statement"""
    rule_name = "function_definition_2"
    if p[1].type.upper() in PRIMITIVE_TYPES:
        p[1].type = TYPE_EASY[p[1].type.upper()].lower()
        # print(p[1].type)

    p[0] = Node(
        name="FuncDecl",
        val=p[2].val,
        type=p[1].type,
        lno=p.lineno(1),
        children=[],
    )
    p[0].ast = build_AST_2(p, [1, 2, 3], rule_name)


def p_push_scope_lcb(p):
    """push_scope_lcb : LEFT_CURLY_BRACKET"""
    ST.push_scope()
    # print("YEH hai scope", ST.currentScope)
    offsets[ST.currentScope] = 0
    p[0] = p[1]


def p_push_scope_lb(p):
    """push_scope_lb : LEFT_BRACKET"""
    ST.push_scope()
    offsets[ST.currentScope] = 0

    p[0] = p[1]


def p_pop_scope_rcb(p):
    """pop_scope_rcb : RIGHT_CURLY_BRACKET"""
    ST.pop_scope()
    p[0] = p[1]


def p_inheritance_specifier(p):
    """inheritance_specifier : access_specifier IDENTIFIER"""
    p[0] = ["inheritance_specifier"] + p[1:]


def p_inheritance_specifier_list(p):
    """inheritance_specifier_list : inheritance_specifier
    | inheritance_specifier_list COMMA inheritance_specifier"""
    p[0] = ["inheritance_specifier_list"] + p[1:]


def p_access_specifier(p):
    """access_specifier : PRIVATE
    | PUBLIC
    | PROTECTED"""
    p[0] = p[1:]


def p_class_definition_head(p):
    """class_definition_head : CLASS IDENTIFIER  INHERITANCE_OP inheritance_specifier_list
    | CLASS IDENTIFIER
    | CLASS INHERITANCE_OP inheritance_specifier_list
    | CLASS"""
    p[0] = ["class_definition_head"] + p[1:]


def p_class_definition(p):
    """class_definition : class_definition_head LEFT_CURLY_BRACKET class_internal_definition_list RIGHT_CURLY_BRACKET
    | class_definition_head"""
    p[0] = ["class_definition"] + p[1:]


def p_class_internal_definition_list(p):
    """class_internal_definition_list : class_internal_definition
    | class_internal_definition_list class_internal_definition"""
    p[0] = ["class_internal_definition_list"] + p[1:]


def p_class_internal_definition(p):
    """class_internal_definition : access_specifier LEFT_CURLY_BRACKET class_member_list RIGHT_CURLY_BRACKET SEMICOLON"""
    p[0] = ["class_internal_definition"] + p[1:]


def p_class_member_list(p):
    """class_member_list : class_member
    | class_member_list class_member"""
    p[0] = ["class_member_list"] + p[1:]


def p_class_member(p):
    """class_member : function_definition
    | declaration"""
    p[0] = ["class_member"] + p[1:]


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


if __name__ == "__main__":
    args = getArgs().parse_args()
    graph = Digraph(format="dot")
    with open(str(args.input), "r+") as file:
        data = file.read()
    tree = parser.parse(data)

    ST.display_errors(args.w)
    if ST.error_flag == 0:

        if args.output[-4:] == ".dot":
            args.output = args.output[:-4]
            graph.render(filename=args.output, cleanup=True)
        else:
            graph.render(filename="ast", cleanup=True)
        file = open("3ac.txt", "w")

        # Saving the array in a text file
        # for content in code_gen:
        #     file.write(str(content))
        #     file.write("\n")
        # file.close()
        write_code(code_gen)
    dump_symbol_table_csv(args.v)
