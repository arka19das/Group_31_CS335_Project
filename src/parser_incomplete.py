import ply.yacc as yacc
from  scanner import *
import pydot

myobj = Mylexer()
myobj.build()        
tokens = myobj.tokens    

#CAN BE CHANGED
def p_error(p):
    # global flag_for_error
    # flag_for_error = 1

    if p is not None:
        print("error at line no:  %s :: %s" % ((p.lineno), (p.value)))
        parser.errok()
    else:
        print("Unexpected end of input")

def p_primary_expression(p):
    """primary_expression : IDENTIFIER
    | FLOAT_CONSTANT
    | HEX_CONSTANT
    | OCT_CONSTANT
    | INT_CONSTANT
    | CHAR_CONSTANT
    | STRING_LITERAL
    | LEFT_BRACKET expression RIGHT_BRACKET"""

    p[0] = ['primary_expression'] + p[1:]

def p_postfix_expression(p):
    """postfix_expression : primary_expression
    | postfix_expression LEFT_THIRD_BRACKET expression RIGHT_THIRD_BRACKET
    | postfix_expression LEFT_BRACKET RIGHT_BRACKET
    | postfix_expression LEFT_BRACKET argument_expression_list RIGHT_BRACKET
    | postfix_expression DOT IDENTIFIER
    | postfix_expression PTR_OP IDENTIFIER
    | postfix_expression INC_OP
    | postfix_expression DEC_OP"""

    p[0] = ['postfix_expression'] + p[1:]

def p_argument_expression_list(p):
    """argument_expression_list : assignment_expression
    | argument_expression_list COMMA assignment_expression"""

    p[0] = ['argument_expression_list'] + p[1:]

def p_unary_expression(p):
    """unary_expression : postfix_expression
    | INC_OP unary_expression
    | DEC_OP unary_expression
    | unary_operator cast_expression
    | SIZEOF unary_expression
    | SIZEOF LEFT_BRACKET type_name RIGHT_BRACKET"""

    p[0] = ['unary_expression'] + p[1:]
    
def p_unary_operator(p):
    """unary_operator : LOGICAL_AND
    | MULTIPLY
    | PLUS
    | MINUS
    | BITWISE_NOT
    | LOGICAL_NOT"""

    p[0] = ['unary_operator'] + p[1:]

def p_cast_expression(p):
    """cast_expression : unary_expression
    | '(' type_name ')' cast_expression
    ;"""
    
    p[0] = ['cast_expression'] + p[1:]

def p_multiplicative_expression(p):
    """multiplicative_expression : cast_expression
    | multiplicative_expression '*' cast_expression
    | multiplicative_expression '/' cast_expression
    | multiplicative_expression '%' cast_expression
    ;"""
    
    p[0] = ['multiplicative_expression'] + p[1:]


def p_additive_expression(p):
    """additive_expression : multiplicative_expression
    | additive_expression '+' multiplicative_expression
    | additive_expression '-' multiplicative_expression
    ;"""

    p[0] = ['additive_expression'] + p[1:]

def p_shift_expression(p):
    """shift_expression : additive_expression
    | shift_expression LEFT_OP additive_expression
    | shift_expression RIGHT_OP additive_expression
    ;"""

    p[0] = ['shift_expression'] + p[1:]

def p_relational_expression(p):
    """relational_expression : shift_expression
    | relational_expression LESS shift_expression
    | relational_expression GREATER shift_expression
    | relational_expression LE_OP shift_expression
    | relational_expression GE_OP shift_expression
    ;"""

    p[0] = ['relation_expression'] + p[1:]

def p_equality_expression(p):
    """equality_expression : relational_expression
    | equality_expression EQ_OP relational_expression
    | equality_expression NE_OP relational_expression
    ;"""

    p[0] = ['equality_expression'] + p[1:]

def p_and_expression(p):
    """and_expression : equality_expression
    | and_expression BITWISE_AND equality_expression
    ;"""

    p[0] = ['and_expression'] + p[1:]

def p_exclusive_or_expression(p):
    """exclusive_or_expression : and_expression
    | exclusive_or_expression BITWISE_XOR and_expression
    ;"""

    p[0] = ['exclusive_or_expression'] + p[1:]

#Corrected
def p_inclusive_or_expression(p):
    """inclusive_or_expression : exclusive_or_expression
    | inclusive_or_expression BITWISE_OR exclusive_or_expression
    ;"""

    p[0] = ['inclusive_or_expression'] + p[1:]

def p_logical_and_expression(p):
    """logical_and_expression : inclusive_or_expression
    | logical_and_expression LOGICAL_AND_OP inclusive_or_expression
    ;"""

    p[0] = ['logical_and_expression'] + p[1:]

def p_logical_or_expression(p):
    """logical_or_expression : logical_and_expression
    | logical_or_expression LOGICAL_OR_OP logical_and_expression
    ;"""

    p[0] = ['logical_or_expression'] + p[1:]

def p_conditional_expression(p):
    """conditional_expression : logical_or_expression
    | logical_or_expression QUESTION expression COLON conditional_expression"""

    p[0] = ['conditional_expression'] + p[1:]

def p_assignment_expression(p):
    """assignment_expression : conditional_expression
    | unary_expression assignment_operator assignment_expression
    ;"""

    p[0] = ['assignment_expression'] + p[1:]

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
    ;"""

    p[0] = ['assignment_operator'] + p[1]

#Are we allowing colon assignment
def p_expression(p):
    """expression : assignment_expression
    | expression COMMA assignment_expression"""

    p[0] = ['expression'] + p[1:]

def p_constant_expression(p):
    """constant_expression : conditional_expression"""

    p[0] = ['constant_expression'] + p[1]

#Declaration MISSING if allowing

# Have to rethink, function specifier MISSING 
def p_declaration_specifiers(p):
    """declaration_specifiers : storage_class_specifier declaration_specifiers
    | storage_class_specifier
    | type_specifier declaration_specifiers
    | type_specifier
    | type_qualifier declaration_specifiers
    | type_qualifier
    | function_specifier declaration_specifiers
    | function_specifier
    r"""

    p[0] = ['declaration_specifier'] + p[1:]

def p_init_declarator_list(p):
    """init_declarator_list : init_declarator
    | init_declarator_list COMMA init_declarator"""

    p[0] = ['init_declaration_list'] + p[1:]

def p_init_declarator(p):
    """init_declarator : declarator
    | declarator EQ initializer"""

    p[0] = ['init_declaration'] + p[1:]

def p_storage_class_specifier(p):
    """storage_class_specifier : TYPEDEF"""

    p[0] = ['storage_class_specifier'] + p[1]

# p_class_defifnition MISSING
#What TYPE_NAME specifies, Avik-pal ke tokens mein hai apne mein nahi hai 
#CHANGED
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
    | BOOL
    | struct_specifier
    | class_definition
    | TYPE_NAME"""

    p[0] = ['type_specifier'] + p[1:]

def p_struct_specifier(p):
    """struct_specifier : STRUCT IDENTIFIER LEFT_CURLY_BRACKET struct_declaration_list RIGHT_CURLY_BRACKET
    | STRUCT LEFT_CURLY_BRACKET struct_declaration_list RIGHT_CURLY_BRACKET
    | STRUCT IDENTIFIER"""

    p[0] = ['struct_specifier'] + p[1:]

def p_struct_declaration_list(p):
    """struct_declaration_list : struct_declaration
    | struct_declaration_list struct_declaration"""
   
    p[0] = ['struct_declaration_list'] + p[1:]

def p_struct_declaration(p):
    """struct_declaration : specifier_qualifier_list struct_declarator_list SEMICOLON"""
   
    p[0] = ['struct_declaration'] + p[1:]

# Is it correct ? Mean are we allowing all such rules or restrictive
def p_specifier_qualifier_list(p):
    """specifier_qualifier_list : type_specifier specifier_qualifier_list
    | type_specifier
    | type_qualifier specifier_qualifier_list
    | type_qualifier"""

    p[0] = ['specifier_qualifier_list'] + p[1:]

def p_struct_declarator_list(p):
    """struct_declarator_list : struct_declarator
    | struct_declarator_list COMMA struct_declarator"""

    p[0] = ['struct_declaration_list'] + p[1:]

# Is colon assignment allowed ?
def p_struct_declarator(p):
    """struct_declarator : declarator
    | COLON constant_expression
    | declarator COLON constant_expression"""
    
    p[0] = ['struct_declaration'] + p[1:]

# Are we allowing volatile
def p_type_qualifier(p):
    """type_qualifier
    : CONST
    | VOLATILE"""

    p[0] = ['type_qualifier'] + p[1]

def p_declarator(p):
    """declarator : pointer direct_declarator
    | direct_declarator"""

    p[0] = ['declarator'] + p[1:]

# All type allowed ?
def p_direct_declarator(p):
    """direct_declarator : IDENTIFIER
    | LEFT_BRACKET declarator RIGHT_BRACKET
    | direct_declarator LEFT_THIRD_BRACKET constant_expression RIGHT_THIRD_BRACKET
    | direct_declarator LEFT_THIRD_BRACKET RIGHT_THIRD_BRACKET
    | direct_declarator LEFT_BRACKET parameter_type_list RIGHT_BRACKET
    | direct_declarator LEFT_BRACKET identifier_list RIGHT_BRACKET
    | direct_declarator LEFT_BRACKET RIGHT_BRACKET"""

    p[0] = ['direct_declarator'] + p[1:]

def p_pointer(p):
    """pointer : MULTIPLY
    | MULTIPLY type_qualifier_list
    | MULTIPLY pointer
    | MULTIPLY type_qualifier_list pointer"""

    p[0] = ['pointer'] + p[1:]

def p_type_qualifier_list(p):
    """type_qualifier_list : type_qualifier
    | type_qualifier_list type_qualifier"""

    p[0] = ['type_qualifier_list'] + p[1:]

#Are we allowing ellipsis
def p_parameter_type_list(p):
    """parameter_type_list : parameter_list
    | parameter_list COMMA ELLIPSIS"""

    p[0] = ['parameter_type_list'] + p[1:]

def p_parameter_list(p):
    """parameter_list : parameter_declaration
    | parameter_list COMMA parameter_declaration"""

    p[0] = ['parameter_list'] + p[1:]

def p_parameter_declaration(p):
    """parameter_declaration : declaration_specifiers declarator
    | declaration_specifiers abstract_declarator
    | declaration_specifiers"""

    p[0] = ['parameter_declaration'] + p[1:]

def p_identifier_list(p):
    """identifier_list : IDENTIFIER
    | identifier_list COMMA IDENTIFIER"""

    p[0] = ['indentifier_list'] + p[1:]

def p_type_name(p):
    """type_name : specifier_qualifier_list
    | specifier_qualifier_list abstract_declarator"""

    p[0] = ['type_name'] + p[1:]

def p_abstract_declarator(p):
    """abstract_declarator : pointer
    | direct_abstract_declarator
    | pointer direct_abstract_declarator"""

    p[0] = ['abstract_declaration'] + p[1:]

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

    p[0] = ['direct_abstract_declaration'] + p[1:]

def p_initializer(p):
    """initializer : assignment_expression
    | LEFT_CURLY_BRACKET initializer_list RIGHT_CURLY_BRACKET
    | LEFT_CURLY_BRACKET initializer_list COMMA RIGHT_CURLY_BRACKET"""

    p[0] = ['initializer'] + p[1:]

def p_initializer_list(p):
    """initializer_list : initializer
    | initializer_list COMMA initializer"""

    p[0] = ['initializer_list'] + p[1:]

def p_statement(p):
    """statement : labeled_statement
    | compound_statement
    | expression_statement
    | selection_statement
    | iteration_statement
    | jump_statement"""

    p[0] = ['statement'] + p[1:]

def p_labeled_statement(p):
    """labeled_statement : IDENTIFIER COLON statement
    | CASE constant_expression COLON statement
    | DEFAULT COLON statement"""
    
    p[0] = ['labeled_statement'] + p[1:]

##HIGHLY ERROR PRONE FROM HERE TO END
##This portion is different for my code
## DOUBT FROM 456-473 Afterwards OK
def p_compound_statement(p):
    """compound_statement : LEFT_CURLY_BRACKET RIGHT_CURLY_BRACKET
    | LEFT_CURLY_BRACKET block_list RIGHT_CURLY_BRACKET"""

    p[0] = ['compound_statement'] + p[1:]

def p_block_item_list(p):
    """block_item_list : block_item
    | block_item_list block_item"""

    p[0] = ['block_item_list'] + p[1:]

def p_block_item(p):
    """block_item : declaration
    | statement"""

    p[0] = ['block_item'] + p[1:]

def p_expression_statement(p):
    """expression_statement : SEMICOLON
    | expression SEMICOLON"""

    p[0] = ['expression_statement'] + p[1:]

#CHANGED
def p_selection_statement(p):
    """selection_statement : IF LEFT_BRACKET expression RIGHT_BRACKET compound_statement
    | IF LEFT_BRACKET expression RIGHT_BRACKET compound_statement ELSE compound_statement
    | SWITCH LEFT_BRACKET expression RIGHT_BRACKET compound_statement"""

    p[0] = ['selection_statement'] + p[1:]

# To be changed compound statement and expressions
def p_iteration_statement(p):
    """iteration_statement : WHILE LEFT_BRACKET expression RIGHT_BRACKET statement
    | DO statement WHILE LEFT_BRACKET expression RIGHT_BRACKET SEMICOLON
    | FOR LEFT_BRACKET expression_statement expression_statement RIGHT_BRACKET statement
    | FOR LEFT_BRACKET expression_statement expression_statement expression RIGHT_BRACKET statement"""

    p[0] = ['iteration_statement'] + p[1:]

def p_jump_statement(p):
    """jump_statement : GOTO IDENTIFIER SEMICOLON
    | CONTINUE SEMICOLON
    | BREAK SEMICOLON
    | RETURN SEMICOLON
    | RETURN expression SEMICOLON"""

    p[0] = ['jump_statement'] + p[1:]

def p_translation_unit(p):
    """translation_unit : external_declaration
    | translation_unit external_declaration"""

    p[0] = ['translation_unit'] + p[1:]

def p_external_declaration(p):
    """external_declaration : function_definition
    | declaration"""

    p[0] = ['external_declaration'] + p[1:]

#Changed
def p_function_definition(p):
    """function_definition : declaration_specifiers declarator declaration_list compound_statement
    | declaration_specifiers declarator compound_statement
    | declarator declaration_list compound_statement
    | declarator compound_statement"""

    p[0] = ['function_definition'] + p[1:]

def p_declaration_list(p):
    """declaration_list : declaration
    | declaration_list declaration"""

    p[0] = ['declaration'] + p[1:]

# Build the parser
parser = yacc.yacc()

# def getArgs():
#     parser = argparse.ArgumentParser()
#     parser.add_argument("input", type=str, default=None, help="Input file")
#     parser.add_argument("-o", "--output", type=str, default="AST", help="Output file")
#     parser.add_argument("-t", "--trim", action="store_true", help="Trimmed ast")
#     return parser
