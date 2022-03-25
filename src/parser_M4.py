from binascii import Incomplete
from pickle import GLOBAL
import struct
import ply.yacc as yacc
from scanner import *
import pydot
import pprint
from symtable_new import (
    BASIC_TYPES,
    pop_scope,
    push_scope,
    new_scope,
    get_current_symtab,
    get_tmp_label,
    get_tmp_var,
    get_tmp_closure,
    get_default_value,
    compute_storage_size,
    NUMERIC_TYPES,
    CHARACTER_TYPES,
    DATATYPE2SIZE,
    BASIC_TYPES,
    FLOATING_POINT_TYPES,
    INTEGER_TYPES,
    SYMBOL_TABLES,
    STATIC_VARIABLE_MAPS,
)

lexer = Lexer()
lexer.build()
tokens = lexer.tokens
GLOBAL_ERROR_LIST = []


def _get_conversion_function_expr():
    pass


def op_util(p):
    if len(p) == 2:
        p[0] = p[1]
    else:
        fname, entry, args = resolve_function_name_uniform_types(p[2], [p[1], p[3]])
        p[0] = {
            "value": fname,
            "type": entry["return type"],
            "arguments": args,
            "kind": "FUNCTION CALL",
        }
        nvar = get_tmp_var(p[0]["type"])
        codes = []
        for _a in args:
            if len(_a["code"]) == 0:
                continue
            codes += _a["code"]
            _a["code"] = []
        p[0]["code"] = codes + [[p[0]["kind"], p[0]["type"], p[0]["value"], p[0]["arguments"], nvar]]
        p[0]["value"] = nvar
        del p[0]["arguments"]

start = "translation_unit"


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
    p[0] = {"value": p[1], "code": [], "type": "float", "kind": "CONSTANT"}


def p_hex_constant(p):
    """hex_constant : HEX_CONSTANT"""
    p[0] = {"value": p[1], "code": [], "type": "int", "kind": "CONSTANT"}


def p_oct_constant(p):
    """oct_constant : OCT_CONSTANT"""
    p[0] = {"value": p[1], "code": [], "type": "int", "kind": "CONSTANT"}


def p_int_constant(p):
    """int_constant : INT_CONSTANT"""
    p[0] = {"value": p[1], "code": [], "type": "int", "kind": "CONSTANT"}


def p_char_constant(p):
    """char_constant : CHAR_CONSTANT"""
    p[0] = {"value": p[1], "code": [], "type": "char", "kind": "CONSTANT"}


def p_string_literal(p):
    """string_literal : STRING_LITERAL"""
    p[0] = {
        "value": p[1],
        "code": [],
        "type": "char",
        "pointr_lvl": 1,
        "kind": "CONSTANT",
    }


def p_identifier(p):
    """identifier : IDENTIFIER"""
    # TODO: COMPLETE
    symtable = get_current_symtab()
    entry = symtable.lookup(p[1])
    if entry == None:
        GLOBAL_ERROR_LIST.append(
            f"Error in line number {str(p.lineno(1))} : usage of undeclared identifier"
        )
    if entry["kind"] == 0:
        p[0] = { "value": p[1], "code": [], "type": entry["type"], "pointer_lvl": entry.get("pointer_lvl", 0),
            "kind": "IDENTIFIER", "is_array": entry.get("is_array", False),"dimensions": entry.get("dimensions", [])
            # "entry": entry,  # FIXME: Add this back in the final code
        }
    elif entry["kind"] == 1:
        p[0] = { "value": p[1], "code": [], "type": entry["return type"], "pointer_lvl": entry.get("pointer_lvl", 0), "kind": "IDENTIFIER",
            # "entry": entry,  # FIXME: Add this back in the final code
        }
def p_postfix_expression_1(p):
    """postfix_expression : primary_expression"""
    p[0] = p[1]

def p_postfix_expression_2(p):
    """postfix_expression : postfix_expression LEFT_THIRD_BRACKET expression RIGHT_THIRD_BRACKET"""
    if p[3]["type"] == "int":
        ##TO_DO Multi-dimensional check
        symTab = get_current_symtab()
        temp_dict = copy.deepcopy(p[1])
        temp_dict["is_array"] = False
        funcname = "__get_array_element" + f"({_get_type_info(temp_dict)}*,int)"
        nvar = get_tmp_var(_get_type_info(temp_dict))
        c1 = p[1]["code"]
        c2 = p[3]["code"]
        p[1]["code"] = []
        p[3]["code"] = []
        p[0] = {
            "value": nvar,
            "type": temp_dict["type"],
            "code": c1 + c2 + [["FUNCTION CALL", temp_dict["type"], funcname, [p[1], p[3]], nvar]],
        }
        del temp_dict
    else:
        err_msg = "Error at line number " + str(p.lineno(3)) + ": Not an integr index"
        GLOBAL_ERROR_LIST.append(err_msg)
        raise SyntaxError

def p_postfix_expression_3(p):
    """postfix_expression : postfix_expression LEFT_BRACKET RIGHT_BRACKET"""
    symTab = get_current_symtab()
    funcname = p[1]["value"] + "()"
    entry = symTab.lookup(funcname)
    if entry is None:
        err_msg = "Error at line number " + str(p.lineno(1)) + ": No such function in symbol table"
        GLOBAL_ERROR_LIST.append(err_msg)
        raise SyntaxError
        # raise Exception
    p[0] = {
        "value": funcname,
        "type": entry["return type"],
        "arguments": [],
        "kind": "FUNCTION CALL",
    }
    nvar = get_tmp_var(p[0]["type"])
    p[0]["code"] = [[p[0]["kind"], p[0]["type"], p[0]["value"], p[0]["arguments"], nvar]]
    p[0]["value"] = nvar
    print(nvar)
    del p[0]["arguments"]

def p_postfix_expression_4(p):
    """postfix_expression : LEFT_BRACKET argument_expression_list RIGHT_BRACKET"""

    symTab = get_current_symtab()
    proper_funcname = p[1].value + p[2] + ",".join(p[3].type) + p[4]
    entry = symTab.lookup(proper_funcname)
    if entry == None:
        GLOBAL_ERROR_LIST.append( f"ERROR in line {p.lineno(3)} : {proper_funcname}This function doesnt exist")
        raise SyntaxError
    
    p[0] = {
        "value": proper_funcname,
        "type": entry["return type"],
        "arguments": p[3]["value"],
        "kind": "FUNCTION CALL",
    }
    
    nvar = get_tmp_var(p[0]["type"])
    p[0]["code"] = [
        [p[0]["kind"], p[0]["type"], p[0]["value"], p[0]["arguments"], nvar]
    ]
    p[0]["value"] = nvar
    del p[0]["arguments"]

def p_postfix_expression_5(p):
    """postfix_expression : postfix_expression DOT IDENTIFIER
    | postfix_expression PTR_OP IDENTIFIER"""
    
    symTab = get_current_symtab()
    entry = symTab.lookup(p[1]["value"])
    if entry is None:
        err_msg = "Error at line number " + str(p.lineno(1)) + ": Undeclared identifier used"
        GLOBAL_ERROR_LIST.append(err_msg)
        raise SyntaxError
    elif (entry["pointer_lvl"] and p[2]==".") or (entry["pointer_lvl"]==0 and p[2]=="->"):
        err_msg = "Error at line number " + str(p.lineno(1)) + ": Invalid operator used used"
        GLOBAL_ERROR_LIST.append(err_msg)
        raise SyntaxError
        
    struct_entry = symTab.lookup_type(entry["type"])  # not needed if already checked at time of storing
    if struct_entry is None:
        err_msg = "Error at line number " + str(p.lineno(1)) + ": Undeclared Struct used"
        GLOBAL_ERROR_LIST.append(err_msg)
        raise SyntaxError
    else:
        if struct_entry["kind"] in [2, 5]:
            if p[3] not in struct_entry["field names"]:
                err_msg = "Error at line number " + str(p.lineno(3)) + ": No such field exists"
                GLOBAL_ERROR_LIST.append(err_msg)
                raise SyntaxError
            else:
                p[0] = {
                    "type": struct_entry["field types"][struct_entry["field names"].index(p[3])],
                    "value": p[1]["value"] + p[2] + p[3],
                    "code": [],
                }
                # print(p[0])
        else:
            err_msg = "Error at line number " + str(p.lineno(1)) + ": No such Struct definition"
            GLOBAL_ERROR_LIST.append(err_msg)
            raise SyntaxError

def p_postfix_expression_6(p):
    """postfix_expression : postfix_expression INC_OP
    | postfix_expression DEC_OP"""
    symTab = get_current_symtab()
    if p[1]["type"].startswith("struct"):
        error =  "Error at line" + str(p.lineno(1)) + " :Invalid operation on " + p[1]["value"]
        GLOBAL_ERROR_LIST.append(error)
        raise SyntaxError

    if p[1].get("pointer_lvl", 0) > 0:
        # obtain offset
        offset = DATATYPE2SIZE[p[1]["type"].upper()]
        arg_type = "long"
    else:
        offset = 0
        arg_type = p[1]["type"]

    funcname = p[2] + f"({arg_type})"
    entry = symTab.lookup(funcname)
    if entry is None:
        err_msg = "Error at line number " + str(p.lineno(2)) + ": No entry found in symbol table"
        GLOBAL_ERROR_LIST.append(err_msg)
        raise SyntaxError

    p[0] = {
        "value": funcname,
        "type": entry["return type"],
        "arguments": [p[1]],
        "kind": "FUNCTION CALL",
        "p_offset": offset,
    }

    nvar = get_tmp_var(p[0]["type"])
    p[0]["code"] = [[p[0]["kind"], p[0]["type"], p[0]["value"], p[0]["arguments"], nvar]]
    p[0]["value"] = nvar
    print(nvar)
    del p[0]["arguments"]
        
def p_argument_expression_list(p):
    """argument_expression_list : assignment_expression
    | argument_expression_list COMMA assignment_expression"""

    p[0] = {"code": [], "type": [], "value": []}
    # TODO: INCOMPLETE
    if len(p) == 2:
        ind = 1
    else:
        ind = 3
        p[0]["code"] += p[1]["code"]
        p[0]["type"] += p[1]["type"]
        p[0]["value"] += p[1]["value"]
    # print(f"arg_expr_list {p[1]}")
    out_dict = copy.deepcopy(p[ind])
    if p[ind].get("is_array", False):
       out_dict["dimensions"][0] = "variable"
    p[0]["code"].append(out_dict["code"])
    p[0]["type"].append(_get_type_info(out_dict))
    p[0]["value"].append(out_dict["value"])
    del out_dict

def p_unary_expression_1(p):
    """unary_expression : postfix_expression
    | INC_OP unary_expression
    | DEC_OP unary_expression
    """
    if len(p) == 2:
        p[0] = p[1]

    else:
        symTab = get_current_symtab()
        # check for pointer arguments
        if p[2].get("pointer_lvl", 0) > 0:
            # obtain offset
            offset = DATATYPE2SIZE[p[2]["type"].upper()]
            arg_type = "long"

        else:
            offset = 0
            arg_type = p[2]["type"]

        funcname = p[1] + f"({arg_type})"
        entry = symTab.lookup(funcname)

        if entry is None:
            err_msg = "Error at line number " + str(p.lineno(1)) + ": No such function in symbol table"
            GLOBAL_ERROR_LIST.append(err_msg)
            raise SyntaxError
            # raise Exception

        p[0] = {
            "value": funcname,
            "type": entry["return type"],
            "arguments": [p[2]],
            "kind": "FUNCTION CALL",
            "p_offset": offset,
        }

        nvar = get_tmp_var(p[0]["type"])
        p[0]["code"] = [[p[0]["kind"], p[0]["type"], p[0]["value"], p[0]["arguments"], nvar]]
        p[0]["value"] = nvar
        del p[0]["arguments"]

    
def p_unary_expression_2(p):
    """unary_expression : unary_operator cast_expression
    """
    if p[1].startswith("*"):
        # print(p[1])
        p[0] = p[2]
        # p[0]["deref"] = p[0].get("deref", 0) + len(p[1])
        if p[2].get("pointer_lvl", 0) > 0:
            nvar = get_tmp_var(_get_type_info(p[2]))
            p[0]["code"] = [
                [
                    "FUNCTION CALL",
                    _get_type_info(p[2]),
                    f"__deref({p[0]['value']})",
                    [
                        {
                            "value": get_default_value(_get_type_info(p[2])),
                            "type": _get_type_info(p[2]),
                            "kind": p[2].get("kind", "CONSTANT"),
                        }
                    ],
                    nvar,
                ]
            ]
            p[0]["pointer_lvl"] -= 1
        else:
            err_msg = "Cannot Dereference a non-pointer : %s" % ((p[0]["value"]))
            GLOBAL_ERROR_LIST.append(err_msg)

    elif p[1].startswith("&"):
        p[0] = p[2]
        nvar = get_tmp_var(_get_type_info(p[2]))
        p[0]["code"] = [
            [
                "FUNCTION CALL",
                _get_type_info(p[2]),
                f"__deref({p[0]['value']})",
                [
                    {
                        "value": get_default_value(_get_type_info(p[2])),
                        "type": _get_type_info(p[2]),
                        "kind": p[2].get("kind", "CONSTANT"),
                    }
                ],
                nvar,
            ]
        ]
        p[0]["pointer_lvl"] = p[0].get("pointer_lvl", 0) + 1
        # print(p[0])

    elif p[1] == "+" or p[1] == "-":

        symTab = get_current_symtab()
        arg = p[2]["type"]
        funcname = p[1] + f"({arg})"
        entry = symTab.lookup(funcname)

        if entry is None:
            err_msg = "Error at line number " + str(p.lineno(1)) + ": No such function in symbol table"
            GLOBAL_ERROR_LIST.append(err_msg)
            raise SyntaxError
            # raise Exception

        p[0] = {
            "value": funcname,
            "type": entry["return type"],
            "arguments": [p[2]],
            "kind": "FUNCTION CALL",
        }

        nvar = get_tmp_var(p[0]["type"])
        p[0]["code"] = [[p[0]["kind"], p[0]["type"], p[0]["value"], p[0]["arguments"], nvar]]
        p[0]["value"] = nvar
        del p[0]["arguments"]

    else:
        # TODO: depends on cast expression
        pass

def p_unary_expression_2(p):
    """unary_expression :  SIZEOF unary_expression
    | SIZEOF LEFT_BRACKET type_name RIGHT_BRACKET"""
    
    if len(p)==3:
        symTab = get_current_symtab()
        entry = symTab.lookup(p[2]["value"])
        typeentry = symTab.lookup_type(entry["type"])
        p[0] = {
            "type": "int",
            "value": compute_storage_size(entry, typeentry),
            "code": p[2]["code"]
        }

    else:
        p[0] = {
            "type": "int",
            "value": compute_storage_size({"value": p[3]["value"], "type": p[3]["value"]}, None),
            "code": p[3]["code"],
        }

    


def p_unary_operator(p):
    """unary_operator : BITWISE_AND
    | MULTIPLY
    | PLUS
    | MINUS
    | BITWISE_NOT
    | LOGICAL_NOT"""

    p[0] = p[1]


def p_cast_expression(p):
    """cast_expression : unary_expression
    | LEFT_BRACKET type_name RIGHT_BRACKET cast_expression
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = _get_conversion_function_expr(
            p[4], {"type": p[2]["value"], "pointer_lvl": p[2].get("pomiter_lvl", 0)}
        )


def p_multiplicative_expression(p):
    """multiplicative_expression : cast_expression
    | multiplicative_expression MULTIPLY cast_expression
    | multiplicative_expression DIVIDE cast_expression
    | multiplicative_expression MOD cast_expression
    """
    op_util(p)
    
def p_additive_expression(p):
    """additive_expression : multiplicative_expression
    | additive_expression PLUS multiplicative_expression
    | additive_expression MINUS multiplicative_expression
    """
    op_util(p)
    
def p_shift_expression(p):
    """shift_expression : additive_expression
    | shift_expression LEFT_OP additive_expression
    | shift_expression RIGHT_OP additive_expression
    """
    op_util(p)
    
def p_relational_expression(p):
    """relational_expression : shift_expression
    | relational_expression LESS shift_expression
    | relational_expression GREATER shift_expression
    | relational_expression LE_OP shift_expression
    | relational_expression GE_OP shift_expression
    """
    op_util(p)
    
def p_equality_expression(p):
    """equality_expression : relational_expression
    | equality_expression EQ_OP relational_expression
    | equality_expression NE_OP relational_expression
    """
    op_util(p)
    
def p_and_expression(p):
    """and_expression : equality_expression
    | and_expression BITWISE_AND equality_expression
    """
    op_util(p)
    
def p_exclusive_or_expression(p):
    """exclusive_or_expression : and_expression
    | exclusive_or_expression BITWISE_XOR and_expression
    """
    op_util(p)
    
def p_inclusive_or_expression(p):
    """inclusive_or_expression : exclusive_or_expression
    | inclusive_or_expression BITWISE_OR exclusive_or_expression
    """
    op_util(p)
    
def p_logical_and_expression(p):
    """logical_and_expression : inclusive_or_expression
    | logical_and_expression LOGICAL_AND_OP inclusive_or_expression
    """
    op_util(p)
    
def p_logical_or_expression(p):
    """logical_or_expression : logical_and_expression
    | logical_or_expression LOGICAL_OR_OP logical_and_expression
    """
    op_util(p)
    
    
def p_conditional_expression(p):
    """conditional_expression : logical_or_expression
    | logical_or_expression QUESTION expression COLON conditional_expression"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        # TODO: RESOLUTION OF FUNCTION name and type same as above
        pass
    # p[0] = ["conditional_expression"] + p[1:]


def p_assignment_expression(p):
    """assignment_expression : conditional_expression
    | unary_expression assignment_operator assignment_expression
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        # TODO: RESOLUTION OF FUNCTION name and type same as above
        pass
    # p[0] = ["assignment_expression"] + p[1:]


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

    p[0] = p[1]


def p_expression(p):
    """expression : assignment_expression
    | expression COMMA assignment_expression"""

    if len(p) == 2:
        p[0] = {
            "type": p[1]["type"],
            "kind": "EXP",
            "code": p[1]["code"],
            "pointer_lvl": p[1].get("pointer_lvl", 0),
            "value": p[1]["value"],
        }
    else:
        p[0] = {
            "type": p[3]["type"],
            "kind": "EXP",
            "code": p[3]["code"] + p[1]["code"],
            "pointer_lvl": p[3].get("pointer_lvl", 0),
            "value": p[3]["value"],
        }


def p_constant_expression(p):
    """constant_expression : conditional_expression"""

    p[0] = p[1]


def p_declaration(p):
    """declaration : declaration_specifiers SEMICOLON
    | declaration_specifiers init_declarator_list SEMICOLON
    """

    # TODO: INCOMPLETE


def p_declaration_specifiers(p):
    """declaration_specifiers : storage_class_specifier declaration_specifiers
    | storage_class_specifier
    | type_specifier declaration_specifiers
    | type_specifier
    | type_qualifier declaration_specifiers
    | type_qualifier
    """

    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = {"value": p[1]["value"] + " " + p[2]["value"], "code": []}


def p_init_declarator_list(p):
    """init_declarator_list : init_declarator
    | init_declarator_list COMMA init_declarator"""

    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_init_declarator(p):
    """init_declarator : declarator
    | declarator EQ initializer"""

    # p[0] = ["init_declaration"]  + p[1:]
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        # TODO: Incomplete
        pass


def p_storage_class_specifier(p):
    """storage_class_specifier : TYPEDEF
    | AUTO"""

    # p[0] = ["storage_class_specifier"] + p[1:]
    p[0] = {"value": p[1], "code": []}


def p_type_specifier(p):
    """type_specifier : VOID
    | CHAR
    | SHORT
    | INT
    | LONG
    | FLOAT
    | DOUBLE
    | SIGNED
    | UNSIGNED
    | struct_specifier
    | class_definition
    | TYPE_NAME
    """  # bool not there
    # TODO:  PART NOT DONE

    p[0] = ["type_specifier"] + p[1:]


def p_struct_specifier(p):
    """struct_specifier : STRUCT IDENTIFIER LEFT_CURLY_BRACKET struct_declaration_list RIGHT_CURLY_BRACKET
    | STRUCT LEFT_CURLY_BRACKET struct_declaration_list RIGHT_CURLY_BRACKET
    | STRUCT IDENTIFIER"""
    if len(p) == 3:
        symbtab = get_current_symtab()
        struct_entry = symtab.lookup_type(p[1] + " " + p[2])
        if struct_entry is None:
            GLOBAL_ERROR_LIST.append(f"struct {p[2]} is undeclared")
            raise Exception  # undeclared struct used
        else:
            p[0] = {"name": p[2], "kind": 2, "code": []}  # what is role of insert?????

    # p[0] = ["struct_specifier"] + p[1:]


def p_struct_declaration_list(p):
    """struct_declaration_list : struct_declaration
    | struct_declaration_list struct_declaration"""

    if len(p) == 2:
        p[0] = p[1]
    else:

        # TODO: do struct_declaration_first
        pass
    # p[0] = ["struct_declaration_list"] + p[1:]


def p_struct_declaration(p):
    """struct_declaration : specifier_qualifier_list struct_declarator_list SEMICOLON"""

    p[0] = ["struct_declaration"] + p[1:]


def p_specifier_qualifier_list(p):
    """specifier_qualifier_list : type_specifier specifier_qualifier_list
    | type_specifier
    | type_qualifier specifier_qualifier_list
    | type_qualifier"""

    if len(p) == 2:
        p[0] = p[1]
    else:
        # TODO: SAmjh nehi aya complete karna hai and modify bhi
        print(p[1], p[2], "p_specifier_qualifier_list")
        p[0] = {"value": p[1]["value"] + " " + p[2]["value"], "code": []}
    # p[0] = ["specifier_qualifier_list"] + p[1:]


def p_struct_declarator_list(p):
    """struct_declarator_list : struct_declarator
    | struct_declarator_list COMMA struct_declarator"""

    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]
    # p[0] = ["struct_declaration_list"] + p[1:]


# Is colon assignment allowed ? Assuming it is not allowed
def p_struct_declarator(p):
    """struct_declarator : declarator"""
    # | COLON constant_expression
    # | declarator COLON constant_expression
    p[0] = p[1]

    # p[0] = ["struct_declaration"] + p[1:]


def p_type_qualifier(p):
    """type_qualifier : CONST"""

    p[0] = p[1]


def p_declarator(p):
    """declarator : pointer direct_declarator
    | direct_declarator"""

    if len(p) == 2:
        p[0] = p[1]
    else:
        print(p[1])  # using for debugging
        p[0] = p[2]
        p[0]["pointer_lvl"] = 0  # TODO: Incomplete

    # p[0] = ["declarator"] + p[1:]


def p_direct_declarator(p):
    """direct_declarator : IDENTIFIER
    | LEFT_BRACKET declarator RIGHT_BRACKET
    | direct_declarator LEFT_THIRD_BRACKET constant_expression RIGHT_THIRD_BRACKET
    | direct_declarator LEFT_THIRD_BRACKET RIGHT_THIRD_BRACKET
    | direct_declarator LEFT_BRACKET parameter_type_list RIGHT_BRACKET
    | direct_declarator LEFT_BRACKET identifier_list RIGHT_BRACKET
    | direct_declarator LEFT_BRACKET RIGHT_BRACKET"""

    # TODO: Not understood at all
    # p[0] = ["direct_declarator"] + p[1:]


def p_pointer(p):
    """pointer : MULTIPLY
    | MULTIPLY type_qualifier_list
    | MULTIPLY pointer
    | MULTIPLY type_qualifier_list pointer"""

    p[0] = ["pointer"] + p[1:]


def p_type_qualifier_list(p):
    """type_qualifier_list : type_qualifier
    | type_qualifier_list type_qualifier"""

    p[0] = ["type_qualifier_list"] + p[1:]


def p_parameter_type_list(p):
    """parameter_type_list : parameter_list"""

    p[0] = ["parameter_type_list"] + p[1:]


def p_parameter_list(p):
    """parameter_list : parameter_declaration
    | parameter_list COMMA parameter_declaration"""

    p[0] = ["parameter_list"] + p[1:]


def p_parameter_declaration(p):
    """parameter_declaration : declaration_specifiers declarator
    | declaration_specifiers abstract_declarator
    | declaration_specifiers"""

    p[0] = ["parameter_declaration"] + p[1:]


def p_identifier_list(p):
    """identifier_list : IDENTIFIER
    | identifier_list COMMA IDENTIFIER"""

    p[0] = ["indentifier_list"] + p[1:]


def p_type_name(p):
    """type_name : specifier_qualifier_list
    | specifier_qualifier_list abstract_declarator"""

    p[0] = ["type_name"] + p[1:]


def p_abstract_declarator(p):
    """abstract_declarator : pointer
    | direct_abstract_declarator
    | pointer direct_abstract_declarator"""

    p[0] = ["abstract_declaration"] + p[1:]


def p_direct_abstract_declarator(p):
    """direct_abstract_declarator : LEFT_BRACKET abstract_declarator RIGHT_BRACKET
    | LEFT_THIRD_BRACKET RIGHT_THIRD_BRACKET
    | LEFT_THIRD_BRACKET constant_expression RIGHT_THIRD_BRACKET
    | direct_abstract_declarator LEFT_THIRD_BRACKET RIGHT_THIRD_BRACKET
    | direct_abstract_declarator LEFT_THIRD_BRACKET constant_expression RIGHT_THIRD_BRACKET
    | LEFT_BRACKET RIGHT_BRACKET
    | LEFT_BRACKET parameter_type_list RIGHT_BRACKET
    | direct_abstract_declarator LEFT_BRACKET RIGHT_BRACKET
    | direct_abstract_declarator LEFT_BRACKET parameter_type_list RIGHT_BRACKET"""

    p[0] = ["direct_abstract_declaration"] + p[1:]


def p_initializer(p):
    """initializer : assignment_expression
    | LEFT_CURLY_BRACKET initializer_list RIGHT_CURLY_BRACKET
    | LEFT_CURLY_BRACKET initializer_list COMMA RIGHT_CURLY_BRACKET"""

    p[0] = ["initializer"] + p[1:]


def p_initializer_list(p):
    """initializer_list : initializer
    | initializer_list COMMA initializer"""

    p[0] = ["initializer_list"] + p[1:]


def p_statement(p):
    """statement : labeled_statement
    | compound_statement
    | expression_statement
    | selection_statement
    | iteration_statement
    | jump_statement"""

    p[0] = ["statement"] + p[1:]


def p_labeled_statement(p):
    """labeled_statement : IDENTIFIER COLON statement
    | CASE constant_expression COLON statement
    | DEFAULT COLON statement"""

    p[0] = ["labeled_statement"] + p[1:]


##Have to recheck
def p_compound_statement(p):
    """compound_statement : LEFT_CURLY_BRACKET RIGHT_CURLY_BRACKET
    | LEFT_CURLY_BRACKET block_item_list RIGHT_CURLY_BRACKET"""

    p[0] = ["compound_statement"] + p[1:]


def p_block_item_list(p):
    """block_item_list : block_item
    | block_item_list block_item"""

    p[0] = ["block_item_list"] + p[1:]


def p_block_item(p):
    """block_item : declaration
    | statement"""

    p[0] = ["block_item"] + p[1:]


def p_declaration_list(p):
    """
    declaration_list : declaration
    | declaration_list declaration
    """
    p[0] = ["declaration_list"] + p[1:]


def p_expression_statement(p):
    """expression_statement : SEMICOLON
    | expression SEMICOLON"""

    p[0] = ["expression_statement"] + p[1:]


def p_selection_statement(p):
    """selection_statement : IF LEFT_BRACKET expression RIGHT_BRACKET compound_statement
    | IF LEFT_BRACKET expression RIGHT_BRACKET compound_statement ELSE compound_statement
    | SWITCH LEFT_BRACKET expression RIGHT_BRACKET compound_statement"""

    p[0] = ["selection_statement"] + p[1:]


def p_iteration_statement(p):
    """iteration_statement : WHILE LEFT_BRACKET expression RIGHT_BRACKET compound_statement
    | DO compound_statement WHILE LEFT_BRACKET expression RIGHT_BRACKET SEMICOLON
    | FOR LEFT_BRACKET expression_statement expression_statement RIGHT_BRACKET compound_statement
    | FOR LEFT_BRACKET expression_statement expression_statement expression RIGHT_BRACKET compound_statement"""

    p[0] = ["iteration_statement"] + p[1:]


def p_jump_statement(p):
    """jump_statement : GOTO IDENTIFIER SEMICOLON
    | CONTINUE SEMICOLON
    | BREAK SEMICOLON
    | RETURN SEMICOLON
    | RETURN expression SEMICOLON"""

    p[0] = ["jump_statement"] + p[1:]


def p_translation_unit(p):
    """translation_unit : external_declaration
    | translation_unit external_declaration"""

    p[0] = ["translation_unit"] + p[1:]


def p_external_declaration(p):
    """external_declaration : function_definition
    | declaration"""

    p[0] = ["external_declaration"] + p[1:]


def p_function_definition(p):
    """function_definition : declaration_specifiers declarator declaration_list compound_statement
    | declaration_specifiers declarator compound_statement
    | declarator declaration_list compound_statement
    | declarator compound_statement"""

    p[0] = ["function_definition"] + p[1:]


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
    p[0] = p[1]


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


# CAN BE CHANGED
def p_error(p):

    if p is not None:
        print("error at line no:  %s :: %s" % ((p.lineno), (p.value)))
        parser.errok()
    else:
        print("Unexpected end of input")


# Build the parser
parser = yacc.yacc()


def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-input", type=str, required=True, help="Input file")
    parser.add_argument("-o", "--output", type=str, default="AST", help="Output file")
    parser.add_argument("-v", action="store_true", help="Verbose output")
    return parser


if __name__ == "__main__":
    args = getArgs().parse_args()
    with open(str(args.input), "r+") as file:
        data = file.read()
    tree = parser.parse(data)

    if args.output[-4:] == ".dot":
        args.output = args.output[:-4]
    if args.v:
        pprint.PrettyPrinter(depth=None).pprint(tree)