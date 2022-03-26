# Yacc example
import ply.yacc as yacc
import sys
import pydot
import copy
import json
from scanner import *
from v1_parser_util import  *
# Get the token map from the lexer.  This is required.
lexer = Lexer()
lexer.build()
tokens = lexer.tokens

# precedence = (
#      ('nonassoc', 'IFX'),
#      ('nonassoc', 'ELSE')
#  )

ST.c_error = []
cur_num =0
def build_AST(p, nope = []):
  global cur_num
  calling_func_name = sys._getframe(1).f_code.co_name
  calling_rule_name = calling_func_name[2:]
  length = len(p)
  if(length == 2):
    if(type(p[1]) is Node):
      return p[1].ast
    else:
      return p[1]
  else:
    cur_num += 1
    p_count = cur_num
    open('graph1.dot','a').write("\n" + str(p_count) + "[label=\"" + calling_rule_name.replace('"',"") + "\"]") ## make new vertex in dot file
    for child in range(1,length,1):
      if(type(p[child]) is Node and p[child].ast is None):
        continue
      if(type(p[child]) is not Node):
        if(type(p[child]) is tuple):
          if(ignore_1(p[child][0]) is False):
            open('graph1.dot','a').write("\n" + str(p_count) + " -> " + str(p[child][1]))
        else:
          if(ignore_1(p[child]) is False):
            cur_num += 1
            open('graph1.dot','a').write("\n" + str(cur_num) + "[label=\"" + str(p[child]).replace('"',"") + "\"]")
            p[child] = (p[child],cur_num)
            open('graph1.dot','a').write("\n" + str(p_count) + " -> " + str(p[child][1]))
      else:
        if(type(p[child].ast) is tuple):
          if(ignore_1(p[child].ast[0]) is False):
            open('graph1.dot','a').write("\n" + str(p_count) + " -> " + str(p[child].ast[1]))
        else:
          if(ignore_1(p[child].ast) is False):
            cur_num += 1
            open('graph1.dot','a').write("\n" + str(cur_num) + "[label=\"" + str(p[child].ast).replace('"',"") + "\"]")
            p[child].ast = (p[child].ast,cur_num)
            open('graph1.dot','a').write("\n" + str(p_count) + " -> " + str(p[child].ast[1]))

    return (calling_rule_name,p_count)

ts_unit = Node('START',val = '',type ='' ,children = [])

def p_primary_expression(p):
    """primary_expression : identifier
    | float_constant
    | hex_constant
    | oct_constant
    | int_constant
    | char_constant
    | string_literal
    | LEFT_BRACKET expression RIGHT_BRACKET"""

    if len(p)==2:
        p[0]=p[1]
    else:
        p[0]=p[2]
     
def p_float_constant(p):
    """ float_constant : FLOAT_CONSTANT
    """
    p[0] = Node(name = 'Constant', val= p[1], lno = p.lineno(1), type = 'float', children = []) 
    p[0].ast = build_AST(p)

def p_hex_constant(p):
    """ hex_constant : HEX_CONSTANT
    """
    p[0] = Node(name = 'Constant', val= p[1], lno = p.lineno(1), type = 'int', children = []) 
    p[0].ast = build_AST(p)
    
def p_oct_constant(p):
    """ oct_constant : OCT_CONSTANT
    """
    p[0] = Node(name = 'Constant', val= p[1], lno = p.lineno(1), type = 'int', children = []) 
    p[0].ast = build_AST(p)

def p_int_constant(p):
    """ int_constant : INT_CONSTANT
    """
    p[0] = Node(name = 'Constant', val= p[1], lno = p.lineno(1), type = 'int', children = []) 
    p[0].ast = build_AST(p)

def p_char_constant(p):
    """ char_constant : CHAR_CONSTANT
    """
    p[0] = Node(name = 'Constant', val= p[1], lno = p.lineno(1), type = 'char', children = []) 
    p[0].ast = build_AST(p)

def p_string_literal(p):
    """ string_literal : STRING_LITERAL
    """
    p[0] = Node(name = 'Constant', val= p[1], lno = p.lineno(1), type = 'string', level=1, children = []) 
    p[0].ast = build_AST(p)

def p_identifier(p):
    """ identifier : IDENTIFIER
    """
    p[0] = Node(name = 'PrimaryExpression', val= p[1], lno = p.lineno(1), type = '', children = [])
    scope = ST.find_scope(p[1])
    if(scope != -1):
        p[0].type = ST.symbol_table[scope][p[1]]['type']
        if str(p[0].type).count("*") !=0:
            p[0].level=str(p[0].type).count("*")
        if('array' in ST.symbol_table[scope][p[1]].keys()):
            p[0].level+=len(ST.symbol_table[scope][p[1]]['array'])
            p[0].array = ST.symbol_table[scope][p[1]]['array']
        if('isFunc' in ST.symbol_table[scope][p[1]].keys()):
            p[0].isFunc = 1
        p[0].ast = build_AST(p)
    else:
        error = str(p.lineno(1)) + 'COMPILATION ERROR: IDENTIFIER: ' + str(p[1]) + ' not declared'
        ST.c_error.append(error)        

def p_postfix_expression_3(p):
  '''postfix_expression : primary_expression
  | postfix_expression LEFT_BRACKET argument_expression_list RIGHT_BRACKET
  | postfix_expression LEFT_BRACKET RIGHT_BRACKET
  | postfix_expression LEFT_THIRD_BRACKET expression RIGHT_THIRD_BRACKET
  | postfix_expression DOT IDENTIFIER
  | postfix_expression PTR_OP IDENTIFIER
  | postfix_expression INC_OP
	| postfix_expression DEC_OP
  '''
  
  if len(p)==2:
    p[0] = p[1]
    p[0].ast = build_AST(p)
      
  elif len(p)==3:
    p[0] = Node(name = 'IncrementOrDecrementExpression',val = p[1].val,lno = p[1].lno,type = p[1].type,children = [])
    p[0].ast = build_AST(p)
    is_iden(p[1])

  elif len(p)==4:
    if p[2]=='(':
      p[0] = Node(name = 'FunctionCall1',val = p[1].val,lno = p[1].lno,type = p[1].type,children = [p[1]],isFunc=0)
      p[0].ast = build_AST(p,[2,3])
      
      if(p[1].val not in ST.symbol_table[0].keys() or not ST.symbol_table[0][p[1].val].get("isFunc",False)):
        error = 'COMPILATION ERROR at line ' + str(p[1].lno) + ': no function with name ' + p[1].val + ' declared'
        ST.c_error.append(error) 
      elif(len(ST.symbol_table[0][p[1].val]['argumentList']) != 0):
        error = "Syntax Error at line" + str(p[1].lno) + "Incorrect number of arguments for function call" 
        ST.c_error.append(error)
    
    else:
      if (not p[1].name.startswith('Dot')):
        struct_scope = ST.find_scope(p[1].val)
        if struct_scope == -1 or p[1].val not in ST.symbol_table[struct_scope].keys():
          error = "COMPILATION ERROR at line " + str(p[1].lno) + " : " + p[1].val + " not declared"
          ST.c_error.append(error)

      p[0] = Node(name = 'DotOrPTRExpression',val = p[3],lno = p[1].lno,type = p[1].type,children = [])
      p[0].ast = build_AST(p)
      struct_name = p[1].type
      if (struct_name.endswith('*') and p[2][0] == '.') or (not struct_name.endswith('*') and p[2][0] == '->') :
        error = "COMPILATION ERROR at line " + str(p[1].lno) + " : invalid operator " +  " on " + struct_name
        ST.c_error.append(error)
      if(not struct_name.startswith('struct')):
        error = "COMPILATION ERROR at line " + str(p[1].lno) + ", " + p[1].val + " is not a struct"
        ST.c_error.append(error) 
        return

      found_scope = ST.find_scope(struct_name) 
      flag = 0 
      for curr_list in ST.symbol_table[found_scope][struct_name]['field_list']:
        if curr_list[1] == p[3][0]:
          flag = 1 
          p[0].type = curr_list[0]
          p[0].parentStruct = struct_name
          if(len(curr_list) == 5):
            p[0].level = len(curr_list[4])
            
      if(p[0].level == -1):
        error = "COMPILATION ERROR at line " + str(p[1].lno)+ ", incorrect number of dimensions specified for " + p[1].val
        ST.c_error.append(error)
      if flag == 0 :
          error = "COMPILATION ERROR at line " + str(p[1].lno) + " : field " + " not declared in " + struct_name
          ST.c_error.append(error)

  elif len(p)==5:
    if p[2]=='[':
      p[0] = Node(name = 'ArrayExpression',val = p[1].val,lno = p[1].lno,type = p[1].type,children = [p[1],p[3]],isFunc=p[1].isFunc, parentStruct = p[1].parentStruct)
      p[0].ast = build_AST(p)
      p[0].array = copy.deepcopy(p[1].array[1:])
      p[0].array.append(p[3].val)
      p[0].level = p[1].level - 1
      if(p[0].level == -1):
        error = "COMPILATION ERROR at line " + str(p[1].lno)+ ", incorrect number of dimensions specified for " + p[1].val
        ST.c_error.append(error)
      if p[3].type.upper() not in TYPE_INTEGER:
        error = "Compilation Error: Array index at line ", p[3].lno, " is not of compatible type"
        ST.c_error.append(error)
    
    else:
      p[0] = Node(name = 'FunctionCall2',val = p[1].val,lno = p[1].lno,type = p[1].type,children = [],isFunc=0)
      p[0].ast = build_AST(p,[2,4])
      
      if(p[1].val not in ST.symbol_table[0].keys() or 'isFunc' not in ST.symbol_table[0][p[1].val].keys()):
        error = 'COMPILATION ERROR at line :' + str(p[1].lno) + ': no function with name ' + p[1].val + ' declared'
        ST.c_error.append(error)
      elif(len(ST.symbol_table[0][p[1].val]['argumentList']) != len(p[3].children)):
        error = "Syntax Error at line " + str(p[1].lno) + " Incorrect number of arguments for function call"
        ST.c_error.append(error)
      else:
        i = 0
        for arguments in ST.symbol_table[0][p[1].val]['argumentList']:
          curVal = p[3].children[i].val
          if(curVal not in ST.symbol_table[ST.currentScope].keys()):
            continue
          ST.curType = ST.symbol_table[ST.currentScope][curVal]['type']
          if(ST.curType.split()[-1] != arguments.split()[-1]):
            error = "Warning at line " + str(p[1].lno), ": Type mismatch in argument " + str(i+1) + " of function call, " + 'actual type : ' + arguments + ', called with : ' + ST.curType
            ST.c_error.append(error)
          i += 1
  
def p_argument_expression_list(p):
  '''argument_expression_list : assignment_expression
                              | argument_expression_list COMMA assignment_expression
  '''
  if(len(p) == 2):
    #left val empty here for now
    p[0] = Node(name = 'ArgumentExpressionList',val = '',lno = p[1].lno,type = p[1].type,children = [p[1]])
    p[0].ast = build_AST(p)
  else:
    #check if name will always be equal to ArgumentExpressionList
    # heavy doubt
    p[0] = p[1]
    p[0].children.append(p[3])
    p[0].ast = build_AST(p,[2])

def p_unary_expression(p):
  '''unary_expression : postfix_expression
                      | INC_OP unary_expression
                      | DEC_OP unary_expression
                      | unary_operator cast_expression
                      | SIZEOF unary_expression
                      | SIZEOF LEFT_BRACKET type_name RIGHT_BRACKET
  '''
  if(len(p) == 2):  
    p[0] = p[1]
    p[0].ast = build_AST(p)
    
  elif len(p)==3:
    if p[1]=="++" or p[1]=="--":
      tempNode = Node(name = '',val = p[1],lno = p[2].lno,type = '',children = '')
      p[0] = Node(name = 'UnaryOperation',val = p[2].val,lno = p[2].lno,type = p[2].type,children = [tempNode,p[2]])
      is_iden(p[2])
    elif p[1].val == '&':
        p[0] = Node(name = 'AddressOfVariable',val = p[2].val,lno = p[2].lno,type = p[2].type + ' *',level=p[1].level+1, children = [p[2]])
    elif p[1].val == '*':
      if(not p[2].type.endswith('*')):
        error = 'COMPILATION ERROR at line ' + str(p[1].lno) + ' cannot dereference variable of type ' + p[2].type
        ST.c_error.append(error)
      p[0] = Node(name = 'PointerVariable',val = p[2].val,lno = p[2].lno,type = p[2].type[:len(p[2].type)-2],children = [p[2]])
    elif p[1].val == '-':
      p[0] = Node(name = 'UnaryOperationMinus',val = p[2].val,lno = p[2].lno,type = p[2].type,children = [p[2]])
    elif p[1] =='sizeof':
      # should I add SIZEOF in children
      p[0] = Node(name = 'SizeOf',val = p[2].val,lno = p[2].lno,type = p[2].type,children = [p[2]])
    else:
      p[0] = Node(name = 'UnaryOperation',val = p[2].val,lno = p[2].lno,type = p[2].type,children = []) 
    p[0].ast = build_AST(p)
  else:
    p[0] = Node(name = 'SizeOf',val = p[3].val,lno = p[3].lno,type = p[3].type,children = [p[3]])
    p[0].ast = build_AST(p,[2,4])
    
def p_unary_operator(p):
  '''unary_operator : BITWISE_AND
                    | MULTIPLY
                    | PLUS
                    | MINUS
                    | BITWISE_NOT
                    | LOGICAL_NOT
  '''
  p[0] = Node(name = 'UnaryOperator',val = p[1] ,lno = p.lineno(1),type = '',children = [])
  p[0].ast = build_AST(p)

def p_cast_expression(p):
  '''cast_expression : unary_expression
                     | LEFT_BRACKET type_name RIGHT_BRACKET cast_expression
  '''
  
  if(len(p) == 2):
    p[0] = p[1]
    p[0].ast = build_AST(p)
  else:
    # confusion about val
    p[0] = Node(name = 'TypeCasting',val = p[2].val,lno = p[2].lno,type = p[2].type,children = [])
    p[0].ast = build_AST(p,[1,3])

def p_multipicative_expression(p):
  '''multiplicative_expression : cast_expression
    | multiplicative_expression MULTIPLY cast_expression
    | multiplicative_expression DIVIDE cast_expression
    | multiplicative_expression MOD cast_expression
  '''
  if(len(p) == 2):
    p[0] = p[1]
    p[0].ast = build_AST(p)
  else:
    _op = p[2][0] if p[2] is tuple else p[2] 
    p[0] = type_util(p[1],p[3],_op)
    p[0].ast = build_AST(p)

def p_additive_expression(p):
  '''additive_expression : multiplicative_expression
	| additive_expression PLUS multiplicative_expression
	| additive_expression MINUS multiplicative_expression
  '''
  if(len(p) == 2):
    p[0] = p[1]
    p[0].ast = build_AST(p)
  else:
    _op = p[2][0] if p[2] is tuple else p[2] 
    p[0] = type_util(p[1],p[3],_op)
    p[0].ast = build_AST(p)
    
def p_shift_expression(p):
  '''shift_expression : additive_expression
  | shift_expression LEFT_OP additive_expression
  | shift_expression RIGHT_OP additive_expression
  '''
  if(len(p) == 2):
    p[0] = p[1]
    p[0].ast = build_AST(p)
  else:
    _op = p[2][0] if p[2] is tuple else p[2] 
    p[0] = type_util(p[1],p[3],_op)
    p[0].ast = build_AST(p)
##############

def p_relational_expression(p):
  '''relational_expression : shift_expression
    | relational_expression LESS shift_expression
    | relational_expression GREATER shift_expression
    | relational_expression LE_OP shift_expression
    | relational_expression GE_OP shift_expression
    '''
  if(len(p) == 2):
    p[0] = p[1]
    p[0].ast = build_AST(p)
  else:
    _op = p[2][0] if p[2] is tuple else p[2] 
    p[0] = type_util(p[1],p[3],_op)
    p[0].ast = build_AST(p)
    
def p_equality_expresssion(p):
  '''equality_expression : relational_expression
	| equality_expression EQ_OP relational_expression
	| equality_expression NE_OP relational_expression
  '''

  if(len(p) == 2):
    p[0] = p[1]
    p[0].ast = build_AST(p)
  else:
    _op = p[2][0] if p[2] is tuple else p[2] 
    p[0] = type_util(p[1],p[3],_op)
    p[0].ast = build_AST(p)
    
def p_and_expression(p):
  '''and_expression : equality_expression
	| and_expression BITWISE_AND equality_expression
  '''
  if(len(p) == 2):
    p[0] = p[1]
    p[0].ast = build_AST(p)
  else:
    _op = p[2][0] if p[2] is tuple else p[2] 
    p[0] = type_util(p[1],p[3],_op)
    p[0].ast = build_AST(p)
    
def p_exclusive_or_expression(p):
  '''exclusive_or_expression : and_expression
	| exclusive_or_expression BITWISE_XOR and_expression
	'''
  if(len(p) == 2):
    p[0] = p[1]
    p[0].ast = build_AST(p)
  else:
    _op = p[2][0] if p[2] is tuple else p[2] 
    p[0] = type_util(p[1],p[3],_op)
    p[0].ast = build_AST(p)
    
def p_inclusive_or_expression(p):
  '''inclusive_or_expression : exclusive_or_expression
	| inclusive_or_expression BITWISE_OR exclusive_or_expression
  '''
  
  if(len(p) == 2):
    p[0] = p[1]
    p[0].ast = build_AST(p)
  else:
    _op = p[2][0] if p[2] is tuple else p[2] 
    p[0] = type_util(p[1],p[3],_op)
    p[0].ast = build_AST(p)
    
def p_logical_and_expression(p):
  '''logical_and_expression : inclusive_or_expression 
  | logical_and_expression LOGICAL_AND_OP inclusive_or_expression
  '''
  
  if(len(p) == 2):
    p[0] = p[1]
    p[0].ast = build_AST(p)
  else:
    _op = p[2][0] if p[2] is tuple else p[2] 
    p[0] = type_util(p[1],p[3],_op)
    p[0].ast = build_AST(p)
    
def p_logical_or_expression(p):
  '''logical_or_expression : logical_and_expression
	| logical_or_expression LOGICAL_OR_OP logical_and_expression
  '''
  
  if(len(p) == 2):
    p[0] = p[1]
    p[0].ast = build_AST(p)
  else:
    _op = p[2][0] if p[2] is tuple else p[2] 
    p[0] = type_util(p[1],p[3],_op)
    p[0].ast = build_AST(p)
    
# TODO: everything for conditional_expression
def p_conditional_expression(p):
  '''conditional_expression : logical_or_expression
	| logical_or_expression QUESTION expression COLON conditional_expression
  '''
  
  if(len(p) == 2):
    p[0] = p[1]
    
  else:  
    p[0] = Node(name = 'ConditionalOperation',val = '',lno = p[1].lno,type = '',children = [])
  p[0].ast = build_AST(p)
  

def p_assignment_expression(p):
  '''assignment_expression : conditional_expression 
                           | unary_expression assignment_operator assignment_expression
  '''
  if(len(p) == 2):
    p[0] = p[1]
    p[0].ast = build_AST(p)
  else:
    if(p[1].type == '' or p[3].type == ''):
      p[0] = Node(name = 'AssignmentOperation',val = '',lno = p[1].lno,type = 'int',children = [])
      p[0].ast = build_AST(p)
      return
    if p[1].type == '-1' or p[3].type == '-1':
      return
    if('const' in p[1].type.split()):
      error = 'Error, modifying a variable declared with const keyword at line ' + str(p[1].lno)
      ST.c_error.append(error) 
    if('struct' in p[1].type.split() or 'struct' not in p[3].type.split()):
      op1 = 'struct' in p[1].type.split()
      op2 = 'struct' in p[3].type.split()
      if op1 ^ op2:
        error = 'COMPILATION ERROR at line ' + str(p[1].lno) + ', cannot assign variable of type ' + p[3].type + ' to ' + p[1].type
        ST.c_error.append(error)
    if(p[1].level != p[3].level):
      error = "COMPILATION ERROR at line ," + str(p[1].lno) + ", type mismatch in assignment"
      ST.c_error.append(error) 
    elif len(p[1].array)>0:
      error = "COMPILATION ERROR at line ," + str(p[1].lno) + ", Invalid Array assignment"
      ST.c_error.append(error)       
    elif(p[1].type.split()[-1] != p[3].type.split()[-1]):
      error = 'Warning at line ' + str(p[1].lno) + ': type mismatch in assignment'
      ST.c_error.append(error) 
    
    if(len(p[1].parentStruct) > 0):
      found_scope = ST.find_scope(p[1].parentStruct)
      for curr_list in ST.symbol_table[found_scope][p[1].parentStruct]['field_list']:
        if curr_list[1] == p[1].val:
          if(len(curr_list) < 5 and len(p[1].array) == 0):
            break
          if(len(curr_list) < 5 or (len(curr_list[4]) < len(p[1].array))):
            error = "COMPILATION ERROR at line " + str(p[1].lno) + ", incorrect number of dimensions"
            ST.c_error.append(error)
            #print("COMPILATION ERROR at line ", str(p[1].lno), ", incorrect number of dimensions")
    found_scope = ST.find_scope(p[1].val)
    if (found_scope != -1) and ((p[1].isFunc == 1)):
      error = "Compilation Error at line" + str(p[1].lno) + ":Invalid operation on " + p[1].val
      ST.c_error.append(error) 

    found_scope = ST.find_scope(p[3].val)
    if (found_scope != -1) and ((p[3].isFunc == 1)):
      error = "Compilation Error at line" + str(p[1].lno) + ":Invalid operation on " + p[3].val
      ST.c_error.append(error)

    if p[2].val != '=':
      if ('struct' in p[1].type.split()) or ('struct' in p[3].type.split()):
        error = "Compilation Error at line" + str(p[1].lno) + ":Invalid operation on " + p[1].val
        ST.c_error.append(error) 
    
    p[0] = Node(name = 'AssignmentOperation',val = '',type = p[1].type, lno = p[1].lno, children = [], level = p[1].level)
    p[0].ast = build_AST(p)

def p_assignment_operator(p):
  '''assignment_operator : EQ
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
    '''
  
  p[0] = Node(name = 'AssignmentOperator',val = p[1],type = '', lno = p.lineno(1), children = [p[1]])
  p[0].ast = build_AST(p)

def p_expression(p):
  '''expression : assignment_expression
	| expression COMMA assignment_expression
  '''
  
  if(len(p) == 2):
    p[0] = p[1]
  else:
    p[0] = p[1]
    p[0].children.append(p[3])
  
  p[0].ast = build_AST(p)
  
def p_constant_expression(p):
  '''constant_expression : conditional_expression'''
  p[0] = p[1]
  p[0].ast = build_AST(p)

def p_declaration(p):
  '''declaration : declaration_specifiers SEMICOLON
	| declaration_specifiers init_declarator_list SEMICOLON
  '''
  # #global typedef_list
  # #global all_typedef
  if(len(p) == 3):
    p[0] = p[1]
    p[0].ast = build_AST(p,[2])
  else:
    
    p[0] = Node(name = 'Declaration',val = p[1],type = p[1].type, lno = p.lineno(1), children = [])
    p[0].ast = build_AST(p,[3])
    flag = 1
    if('void' in p[1].type.split()):
      flag = 0
    for child in p[2].children:
      if(child.name == 'InitDeclarator'):
        if(p[1].type.startswith('typedef')):
          error = "COMPILATION ERROR at line " + str(p[1].lno) + ": typedef intialized"
          ST.c_error.append(error) 
          #print("COMPILATION ERROR at line " + str(p[1].lno) + ": typedef intialized")
          continue
        if(child.children[0].val in ST.symbol_table[ST.currentScope].keys()):
          error = str(p.lineno(1)) + 'COMPILATION ERROR : ' + child.children[0].val + ' already declared'
          ST.c_error.append(error)
          #print(p.lineno(1), 'COMPILATION ERROR : ' + child.children[0].val + ' already declared')
        ST.symbol_table[ST.currentScope][child.children[0].val] = {}
        ST.symbol_table[ST.currentScope][child.children[0].val]['type'] = p[1].type
        ST.symbol_table[ST.currentScope][child.children[0].val]['value'] = child.children[1].val
        ST.symbol_table[ST.currentScope][child.children[0].val]['size'] = get_data_type_size(p[1].type)
        totalEle = 1
        if(len(child.children[0].array) > 0):
          ST.symbol_table[ST.currentScope][child.children[0].val]['array'] = child.children[0].array
          for i in child.children[0].array:
            if i==0:
                  continue
            totalEle = totalEle*i
        if(len(child.children[0].type) > 0):
          ST.symbol_table[ST.currentScope][child.children[0].val]['type'] = p[1].type + ' ' + child.children[0].type 
          ST.symbol_table[ST.currentScope][child.children[0].val]['size'] = 8
        elif(flag == 0):
          error = "COMPILATION ERROR at line " + str(p[1].lno) + ", variable " + child.children[0].val + " cannot have type void"
          ST.c_error.append(error) 
          #print("COMPILATION ERROR at line " + str(p[1].lno) + ", variable " + child.children[0].val + " cannot have type void")
        ST.symbol_table[ST.currentScope][child.children[0].val]['size'] *= totalEle
      else:
        if(child.val in ST.symbol_table[ST.currentScope].keys()):
          error = str(p.lineno(1)) + 'COMPILATION ERROR : ' + child.val + ' already declared'
          ST.c_error.append(error)
          #print(p.lineno(1), 'COMPILATION ERROR : ' + child.val + ' already declared')
        ST.symbol_table[ST.currentScope][child.val] = {}
        ST.symbol_table[ST.currentScope][child.val]['type'] = p[1].type
        ST.symbol_table[ST.currentScope][child.val]['size'] = get_data_type_size(p[1].type)
        totalEle = 1
        if(len(child.array) > 0):
          ST.symbol_table[ST.currentScope][child.val]['array'] = child.array
          for i in child.array:
            if i==0:
                  continue
            #totalEle = totalEle*int(i)
            totalEle = totalEle*i
        if(len(child.type) > 0):
          ST.symbol_table[ST.currentScope][child.val]['type'] = p[1].type + ' ' + child.type
          ST.symbol_table[ST.currentScope][child.val]['size'] = 8
        elif(flag == 0):
          error = "COMPILATION ERROR at line " + str(p[1].lno) + ", variable " + child.val + " cannot have type void"
          ST.c_error.append(error) 
          #print("COMPILATION ERROR at line " + str(p[1].lno) + ", variable " + child.val + " cannot have type void")
        ST.symbol_table[ST.currentScope][child.val]['size'] *= totalEle
# TODO : change the below to support long, short etc.
def p_declaration_specifiers(p):
  '''declaration_specifiers : storage_class_specifier
	| storage_class_specifier declaration_specifiers
	| type_specifier
	| type_specifier declaration_specifiers
	| type_qualifier
	| type_qualifier declaration_specifiers
  '''
  if(len(p) == 2):
    p[0] = p[1]
    p[0].ast = build_AST(p)
    ST.curType.append(p[1].type)
  elif(len(p) == 3):
    if(p[1].name == 'StorageClassSpecifier' and p[2].name.startswith('StorageClassSpecifier')):
      error = "Invalid Syntax at line " + str(p[1].lno) + ", " + p[2].type + " not allowed after " + p[1].type
      ST.c_error.append(error) 
    if(p[1].name == 'TypeSpecifier1' and (p[2].name.startswith('TypeSpecifier1') or p[2].name.startswith('StorageClassSpecifier') or p[2].name.startswith('TypeQualifier'))):
      if (p[1].type +" "+p[2].type).upper() not in PRIMITIVE_TYPES:    
        error = "Invalid Syntax at line " + str(p[1].lno) + ", " + p[2].type + " not allowed after " + p[1].type
        ST.c_error.append(error) 
    if(p[1].name == 'TypeQualifier' and (p[2].name.startswith('StorageClassSpecifier') or p[2].name.startswith('TypeQualifier'))):
      error = "Invalid Syntax at line " + str(p[1].lno) + ", " + p[2].type + " not allowed after " + p[1].type
      ST.c_error.append(error) 
    
    ST.curType.pop()
    ST.curType.append(p[1].type + ' ' + p[2].type)
    
    ty = ""
    if len(p[1].type) > 0:
      ty = p[1].type + ' ' + p[2].type
    else:
      ty = p[2].type
    ST.curType.append(ty)
    p[0] = Node(name = p[1].name + p[2].name,val = p[1],type = ty, lno = p[1].lno, children = [])
    p[0].ast = build_AST(p)


def p_init_declarator_list(p):
  '''init_declarator_list : init_declarator
	| init_declarator_list COMMA init_declarator
  '''
  if(len(p) == 2):
    p[0] = Node(name = 'InitDeclaratorList', val = '', type = '', lno = p.lineno(1), children = [p[1]])
    p[0].ast = build_AST(p)
  else:
    p[0] = p[1]
    p[0].children.append(p[3])
    p[0].ast = build_AST(p,[2])

def p_init_declarator(p):
  '''init_declarator : declarator
	| declarator EQ initializer
  '''
  if(len(p) == 2):
    # extra node might be needed for error checking maybe make different function to do this
    p[0] = p[1]
    p[0].ast = build_AST(p)
  else:
    p[0] = Node(name = 'InitDeclarator',val = '',type = p[1].type,lno = p.lineno(1), children = [p[1],p[3]], array = p[1].array, level=p[1].level)
    p[0].ast = build_AST(p)
    if(len(p[1].array) > 0 and (p[3].maxDepth == 0 or p[3].maxDepth > len(p[1].array))):
      error = 'COMPILATION ERROR at line ' + str(p.lineno(1)) + ' , invalid initializer'
      ST.c_error.append(error) 
    if(p[1].level != p[3].level):
      error = "COMPILATION ERROR at line " + str(p[1].lno) + ", type mismatch" 
      ST.c_error.append(error)

def p_storage_class_specifier(p):
  '''storage_class_specifier : TYPEDEF
	| AUTO
  '''
  p[0] = Node(name = 'StorageClassSpecifier',val = '',type = p[1], lno = p.lineno(1), children = [])

def p_type_specifier_1(p):
  '''type_specifier : VOID
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
  '''
  p[0] = Node(name = 'TypeSpecifier1',val = '',type = p[1], lno = p.lineno(1), children = [])
  # p[0].ast = build_AST(p)

def p_type_specifier_2(p):
  '''type_specifier : struct_or_union_specifier
                    '''
  p[0] = p[1]
  p[0].ast = build_AST(p)

def p_struct_or_union_specifier(p):
  '''struct_or_union_specifier : struct_or_union IDENTIFIER openbrace struct_declaration_list closebrace
  | struct_or_union openbrace struct_declaration_list closebrace
  | struct_or_union IDENTIFIER
  '''
  # TODO : check the semicolon thing after closebrace in gramamar
  # TODO : Manage the size and offset of fields
  p[0] = Node(name = 'StructOrUnionSpecifier', val = '', type = '', lno = p[1].lno , children = [])
  if len(p) == 6:
    val_name = p[1].type + ' ' + p[2]
    p[0].ast = build_AST(p,[3,5])
    if val_name in ST.symbol_table[ST.currentScope].keys():
      error = 'COMPILATION ERROR : near line ' + str(p[1].lno) + ' struct already declared'
      ST.c_error.append(error) 
      #print('COMPILATION ERROR : near line ' + str(p[1].lno) + ' struct already declared')
    valptr_name = val_name + ' *'
    ST.symbol_table[ST.currentScope][val_name] = {}
    ST.symbol_table[ST.currentScope][val_name]['type'] = val_name
    ST.symbol_table[ST.currentScope][valptr_name] = {}
    ST.symbol_table[ST.currentScope][valptr_name]['type'] = valptr_name
    temp_list = []
    curr_offset = 0 
    max_size = 0
    for child in p[4].children:
      for prev_list in temp_list:
        if prev_list[1] == child.val:
          error = 'COMPILATION ERROR : line ' + str(p[4].lno) + ' : ' + child.val + ' already deaclared'
          ST.c_error.append(error)
      if get_data_type_size(child.type) == -1:
        error = "COMPILATION ERROR at line " + str(child.lno) + " : data type not defined"
        ST.c_error.append(error)
      SZ = get_data_type_size(child.type)
      curr_list = [child.type, child.val, SZ, curr_offset]
      totalEle = 1
      if(len(child.array) > 0):  
        curr_list.append(child.array)
        for ele in child.array:
          totalEle *= ele
      curr_offset = curr_offset + get_data_type_size(child.type)*totalEle
      curr_list[2] *= totalEle
      SZ *= totalEle
      max_size = max(max_size , SZ)
      temp_list.append(curr_list)
    
    ST.symbol_table[ST.currentScope][val_name]['field_list'] = temp_list
    ST.symbol_table[ST.currentScope][val_name]['size'] = curr_offset
    ST.symbol_table[ST.currentScope][valptr_name]['field_list'] = temp_list
    ST.symbol_table[ST.currentScope][valptr_name]['size'] = 8

  elif len(p) == 3:
    p[0].type = p[1].type + ' ' + p[2]
    p[0].ast = build_AST(p)
    found_scope = ST.find_scope(p[0].type)
    if(found_scope == -1):
      error = "COMPILATION ERROR : at line " + str(p[1].lno) + ", " + p[0].type + " is not a type"
      ST.c_error.append(error)
  else:
    p[0].ast = build_AST(p,[2,4])


def p_struct_or_union(p):
    '''struct_or_union : STRUCT
    '''
    p[0] = Node(name = 'StructOrUNion', val = '', type = 'struct', lno = p.lineno(1), children = [])
    p[0].ast = build_AST(p)

def p_struct_declaration_list(p):
  '''struct_declaration_list : struct_declaration
	| struct_declaration_list struct_declaration
  '''
  p[0] = Node(name = 'StructDeclarationList', val = '', type = p[1].type, lno = p[1].lno, children = [])
  p[0].ast = build_AST(p)
  if(len(p) == 2):
    p[0].children = p[1].children
  else:
    p[0].children = p[1].children
    p[0].children.extend(p[2].children)


def p_struct_declaration(p):
  '''struct_declaration : specifier_qualifier_list struct_declarator_list SEMICOLON
  '''
  p[0] = Node(name = 'StructDeclaration', val = '', type = p[1].type, lno = p[1].lno, children = [])
  p[0].ast = build_AST(p,[3])
  p[0].children = p[2].children
  for child in p[0].children:
    if len(child.type) > 0:
      child.type = p[1].type + ' ' + child.type
    else:
      if('void' in p[1].type.split()):
        error = "COMPILATION ERROR at line " + str(p[1].lno) + ", variable " + child.val + " cannot have type void" 
        ST.c_error.append(error)
      child.type = p[1].type
  
def p_specifier_qualifier_list(p):
  '''specifier_qualifier_list : type_specifier specifier_qualifier_list
  | type_specifier
  | type_qualifier specifier_qualifier_list
  | type_qualifier
  '''
  p[0] = Node(name = 'SpecifierQualifierList', val = '', type = p[1].type, lno = p[1].lno, children = [])
  p[0].ast = build_AST(p)

def p_struct_declarator_list(p):
  '''struct_declarator_list : struct_declarator
	| struct_declarator_list COMMA struct_declarator
  '''
  p[0] = Node(name = 'StructDeclaratorList', val = '', type = p[1].type, lno = p[1].lno, children = [])
  if(len(p) == 2):
    p[0].children.append(p[1])
  else:
    p[0].children = p[1].children 
    p[0].children.append(p[3])
  p[0].ast = build_AST(p)
  
def p_struct_declarator(p):  
  '''struct_declarator : declarator
	| COLON constant_expression
	| declarator COLON constant_expression
  '''
  if len(p) == 2 or len(p) == 4:
    p[0] = p[1] 
  if len(p) == 3:
    p[0] = p[2]
  p[0].ast = build_AST(p)
  
def p_type_qualifier(p):
    '''type_qualifier : CONST
    '''
    p[0] = Node(name = 'TypeQualifier', val = '', type = p[1], lno = p.lineno(1), children = [])
    #p[0] = build_AST(p)

def p_declarator_1(p):
  '''declarator : pointer direct_declarator
  | direct_declarator
  '''
  if(len(p) == 2):
    p[0] = p[1]
    p[0].name = 'Declarator'
    p[0].ast = build_AST(p)
    
  else:
    p[0] = p[2]
    p[0].name = 'Declarator'
    p[0].type = p[1].type
    p[0].ast = build_AST(p)
    if(p[2].val in ST.symbol_table[ST.parent[ST.currentScope]] and 'isFunc' in ST.symbol_table[ST.parent[ST.currentScope]][p[2].val].keys()):
      ST.symbol_table[ST.parent[ST.currentScope]][p[2].val]['type'] = ST.symbol_table[ST.parent[ST.currentScope]][p[2].val]['type'] + ' ' + p[1].type
      ST.curFuncReturnType = ST.curFuncReturnType + ' ' + p[1].type
    p[0].val = p[2].val
    p[0].array = p[2].array
    #MODIFIED
    #p[0].level = len(p[2].array)-1
    
def p_direct_declarator_2(p):
  '''direct_declarator : IDENTIFIER
                        | LEFT_BRACKET declarator RIGHT_BRACKET
                        | direct_declarator lopenparen parameter_type_list RIGHT_BRACKET
                        | direct_declarator lopenparen identifier_list RIGHT_BRACKET
  ''' 
  if(len(p) == 2):
    p[0] = Node(name = 'ID', val = p[1], type = '', lno = p.lineno(1), children = [])
    p[0].ast = build_AST(p)
    
  elif(len(p) == 4):
    p[0] = p[2]
    p[0].ast = build_AST(p,[1,3])
  else:
    p[0] = p[1]
    p[0].ast = build_AST(p,[2,4])
    p[0].children = p
  
  if(len (p) == 5 and p[3].name == 'ParameterList'):
    p[0].children = p[3].children
    p[0].type = ST.curType[-1]
    if(p[1].val in ST.symbol_table[ST.parent[ST.currentScope]].keys()):
      error = 'COMPILATION ERROR : near line ' + str(p[1].lno) + ' function already declared'
      ST.c_error.append(error)
    ST.symbol_table[ST.parent[ST.currentScope]][p[1].val] = {}    
    ST.symbol_table[ST.parent[ST.currentScope]][p[1].val]['isFunc'] = 1
    tempList = []
    for child in p[3].children:
      tempList.append(child.type)
    
    ST.symbol_table[ST.parent[ST.currentScope]][p[1].val]['argumentList'] = tempList
    ST.symbol_table[ST.parent[ST.currentScope]][p[1].val]['type'] = ST.curType[-1-len(tempList)]
    ST.curFuncReturnType = copy.deepcopy(ST.curType[-1-len(tempList)])
    ST.scope_to_function[ST.currentScope] = p[1].val
  
def p_direct_declarator_3(p):
  '''direct_declarator : direct_declarator LEFT_THIRD_BRACKET constant_expression RIGHT_THIRD_BRACKET'''
  p[0] = Node(name = 'ArrayDeclarator', val = p[1].val, type = '', lno = p.lineno(1),  children = [])
  p[0].ast = build_AST(p)
  p[0].array = copy.deepcopy(p[1].array)
  p[0].array.append(int(p[3].val))
  
  
def p_direct_declarator_4(p):
  '''direct_declarator : direct_declarator LEFT_THIRD_BRACKET RIGHT_THIRD_BRACKET
                        | direct_declarator lopenparen RIGHT_BRACKET'''
  p[0] = p[1]
  if(p[3] == ')'):
    p[0].ast = build_AST(p,[2,3])
  else:    
    if p[2]=='[':
      p[0].array = copy.deepcopy(p[1].array)    
      p[0].array.append(0)
    p[0].ast = build_AST(p)  
      
  if(p[3] == ')'):
    if(p[1].val in ST.symbol_table[ST.parent[ST.currentScope]].keys()):
      error = 'COMPILATION ERROR : near line ' + str(p[1].lno) + ' function already declared'
      ST.c_error.append(error)
    ST.symbol_table[ST.parent[ST.currentScope]][p[1].val] = {}
    ST.symbol_table[ST.parent[ST.currentScope]][p[1].val]['type'] = ST.curType[-1]
    ST.curFuncReturnType = copy.deepcopy(ST.curType[-1])
    ST.symbol_table[ST.parent[ST.currentScope]][p[1].val]['isFunc'] = 1
    ST.symbol_table[ST.parent[ST.currentScope]][p[1].val]['argumentList'] = []
    ST.scope_to_function[ST.currentScope] = p[1].val
    
def p_pointer(p):
  '''pointer : MULTIPLY 
              | MULTIPLY type_qualifier_list
              | MULTIPLY pointer
              | MULTIPLY type_qualifier_list pointer
  '''
  if(len(p) == 2):
    p[0] = Node(name = 'Pointer',val = '',type = '*', lno = p.lineno(1), children = [])
    p[0].ast = build_AST(p)
  elif(len(p) == 3):
    p[0] = Node(name = 'Pointer',val = '',type = p[2].type + ' *', lno = p.lineno(1), children = [])
    p[0].ast = build_AST(p)
  else:
    p[0] = Node(name = 'Pointer',val = '',type = p[2].type + ' *', lno = p[2].lno, children = [])
    p[0].ast = build_AST(p)

def p_type_qualifier_list(p):
  '''type_qualifier_list : type_qualifier
                        | type_qualifier_list type_qualifier
  '''
  p[0] = p[1]
  p[0].name = 'TypeQualifierList'
  p[0].ast = build_AST(p)
      
  if(len(p) == 2):
    p[0].children = p[1]
  else:
    p[0].children.append(p[2])
    p[0].type = p[1].type + " " + p[2].type

def p_parameter_type_list(p):
  '''parameter_type_list : parameter_list
  '''
  p[0] = p[1]
  p[0].ast = build_AST(p)
      
def p_parameter_list(p):
    '''parameter_list : parameter_declaration
                      | parameter_list COMMA parameter_declaration
    '''
    p[0] = Node(name = 'ParameterList', val = '', type = '', children = [], lno = p.lineno(1))
    if(len(p) == 2):
      p[0].ast = build_AST(p)
      p[0].children.append(p[1])
    else:
      p[0].ast = build_AST(p,[2])
      p[0].children = p[1].children
      p[0].children.append(p[3])

def p_parameter_declaration(p):
    '''parameter_declaration : declaration_specifiers declarator
                             | declaration_specifiers abstract_declarator
                             | declaration_specifiers
    '''
    if(len(p) == 2):
      p[0] = p[1]
      p[0].ast = build_AST(p)
      p[0].name = 'ParameterDeclaration'
    else:
      p[0] = Node(name = 'ParameterDeclaration',val = p[2].val,type = p[1].type, lno = p[1].lno, level=p[2].level, children = [])
      p[0].ast = build_AST(p)
      if(len(p[2].type) > 0):
        p[0].type = p[1].type + ' ' + p[2].type
    if(p[2].name == 'Declarator'):
      if(p[2].val in ST.symbol_table[ST.currentScope].keys()):
        error = str(p.lineno(1)) + 'COMPILATION ERROR : ' + p[2].val + ' parameter already declared' 
        ST.c_error.append(error)
      ST.symbol_table[ST.currentScope][p[2].val] = {}
      ST.symbol_table[ST.currentScope][p[2].val]['type'] = p[1].type
      if(len(p[2].type) > 0):
        ST.symbol_table[ST.currentScope][p[2].val]['type'] = p[1].type + ' ' + p[2].type
        ST.symbol_table[ST.currentScope][p[2].val]['size'] = get_data_type_size(p[1].type+ ' ' + p[2].type)
      else:
        if('void' in p[1].type.split()):
              error = "COMPILATION ERROR at line " + str(p[1].lno) + ", parameter " + p[2].val + " cannot have type void"
              ST.c_error.append(error)
        ST.symbol_table[ST.currentScope][p[2].val]['size'] = get_data_type_size(p[1].type)
      if(len(p[2].array) > 0):
        ST.symbol_table[ST.currentScope][p[2].val]['array'] = p[2].array

def p_identifier_list(p):
    '''identifier_list : IDENTIFIER
                       | identifier_list COMMA IDENTIFIER
    '''
    if(len(p) == 2):
      p[0] = Node(name = 'IdentifierList',val = p[1], type = '', lno = p.lineno(1), children = [p[1]])
    else:
      p[0] = p[1]
      p[0].children.append(p[3])
      p[0].name = 'IdentifierList'
    p[0].ast = build_AST(p,[2])

def p_type_name(p):
    '''type_name : specifier_qualifier_list
                 | specifier_qualifier_list abstract_declarator
    '''
    if(len(p) == 2):
      p[0] = p[1]
      p[0].name = 'TypeName'
    else:
      p[0] = Node(name = 'TypeName',val = '',type = p[1].type, lno = p[1].lno, children = [])
    p[0].ast = build_AST(p)

def p_abstract_declarator(p):
    '''abstract_declarator : pointer 
                           | direct_abstract_declarator
                           | pointer direct_abstract_declarator
    '''
    if(len(p) == 2):
      p[0] = p[1]
      p[0].name = 'AbstractDeclarator'
    
    elif(len(p) == 3):
      p[0] = Node(name = 'AbstractDeclarator',val = p[2].val,type = p[1].type + ' *', lno = p[1].lno, children = [])
    p[0].ast = build_AST(p)

def p_direct_abstract_declarator_1(p):
    '''direct_abstract_declarator : LEFT_BRACKET abstract_declarator RIGHT_BRACKET
                                  | LEFT_THIRD_BRACKET RIGHT_THIRD_BRACKET
                                  | LEFT_THIRD_BRACKET constant_expression RIGHT_THIRD_BRACKET
                                  | direct_abstract_declarator LEFT_BRACKET constant_expression RIGHT_BRACKET 
                                  | LEFT_BRACKET RIGHT_BRACKET
                                  | LEFT_BRACKET parameter_type_list RIGHT_BRACKET
                                  | direct_abstract_declarator LEFT_BRACKET parameter_type_list RIGHT_BRACKET
    '''
    if(len(p) == 3):
      p[0] = Node(name = 'DirectAbstractDeclarator1',val = '',type = '', lno = p.lineno(1), children = [])
    elif(len(p) == 4):
      p[0] = p[2]
      p[0].name = 'DirectAbstractDeclarator1'
      p[0].ast = build_AST(p,[1,3])
    else:
      p[0] = Node(name = 'DirectAbstractDeclarator1',val = p[1].val,type = p[1].val, lno = p[1].lno, children = [p[3]])
      p[0].ast = build_AST(p,[2,4])
      
def p_direct_abstract_declarator_2(p):
  '''direct_abstract_declarator : direct_abstract_declarator LEFT_BRACKET RIGHT_BRACKET'''
  p[0] = Node(name = 'DirectAbstractDEclarator2', val = p[1].val, type = p[1].type, lno = p[1].lno, children = [])
  p[0].ast = build_AST(p,[2,3])

def p_initializer(p):
    '''initializer : assignment_expression
                   | openbrace initializer_list closebrace
                   | openbrace initializer_list COMMA closebrace                                   
    '''
    if(len(p) == 2):
      p[0] = p[1]
      p[0].ast = build_AST(p)
    else:
      p[0] = p[2]
      p[0].is_array = True
    
    p[0].name = 'Initializer'
    if(len(p) == 4):
      p[0].maxDepth = p[2].maxDepth + 1
      p[0].ast = build_AST(p,[1,3])
    elif(len(p) == 5):
      p[0].ast = build_AST(p,[1,3,4])

def p_initializer_list(p):
  '''initializer_list : initializer
  | initializer_list COMMA initializer
  '''
  p[0] = Node(name = 'InitializerList', val = '', type = '', children = [p[1]], lno = p.lineno(1), maxDepth = p[1].maxDepth)
  p[0].ast = build_AST(p)
  if(len(p) == 3):
    if(p[1].name != 'InitializerList'):
      p[0].children.append(p[1])
    else:
      p[0].children = p[1].children
    p[0].children.append(p[3])
    p[0].maxDepth = max(p[1].maxDepth, p[3].maxDepth)

def p_statement(p):
    '''statement : labeled_statement
                 | compound_statement
                 | expression_statement
                 | selection_statement
                 | iteration_statement
                 | jump_statement
    '''
    p[0] = Node(name = 'Statement', val = '', type ='', children = [], lno = p.lineno(1))
    p[0].ast = build_AST(p)

def p_labeled_statement(p):
    """labeled_statement : IDENTIFIER COLON statement
    | CASE constant_expression COLON statement
    | DEFAULT COLON statement"""

    name=""
    if p[1]=="case":
        if p[2].type.upper() not in TYPE_INTEGER and p[2].type.upper() not in TYPE_CHAR:
            error=f"{p.lineno(1)} COMPILATION ERROR: Invalid data-type for case"
            ST.c_error.append(error)
        name = 'CaseStatement'
    elif p[1]=="default":
        name = 'DefaultStatement'
    else:
        name = 'LabeledStatement'
    p[0] = Node(name = name, val = '', type ='', children = [], lno = p.lineno(1) )
    p[0].ast = build_AST(p)

def p_compound_statement(p):
    '''compound_statement : openbrace closebrace
                          | openbrace statement_list closebrace
                          | openbrace declaration_list closebrace
                          | openbrace declaration_list statement_list closebrace
    '''  
    #TODO : see what to do in in first case
    if(len(p) == 3):
      p[0] = Node(name = 'CompoundStatement',val = '',type = '', lno = p.lineno(1), children = [])
    elif(len(p) == 4):
      p[0] = p[2]
      p[0].name = 'CompoundStatement'
      p[0].ast = build_AST(p,[1,3])
    elif(len(p) == 4):
      p[0] = Node(name = 'CompoundStatement', val = '', type = '', children = [], lno = p.lineno(1))
      p[0].ast = build_AST(p,[1,4])
    else:
      p[0] = Node(name = 'CompoundStatement', val = '', type = '', children = [], lno = p.lineno(1))
      p[0].ast = build_AST(p,[1,5])

def p_new_compound_statement(p):
    '''new_compound_statement : LEFT_CURLY_BRACKET closebrace
                          | LEFT_CURLY_BRACKET statement_list closebrace
                          | LEFT_CURLY_BRACKET declaration_list closebrace
                          | LEFT_CURLY_BRACKET declaration_list statement_list closebrace
    '''
    if(len(p) == 3):
      p[0] = Node(name = 'CompoundStatement',val = '',type = '', lno = p.lineno(1), children = [])
    elif(len(p) == 4):
      p[0] = p[2]
      p[0].name = 'CompoundStatement'
      p[0].ast = build_AST(p)
    elif(len(p) == 4):
      p[0] = Node(name = 'CompoundStatement', val = '', type = '', children = [], lno = p.lineno(1))
      p[0].ast = build_AST(p,[1,4])
    else:
      p[0] = Node(name = 'CompoundStatement', val = '', type = '', children = [], lno = p.lineno(1))
      p[0].ast = build_AST(p,[1,5])
      
    
def p_function_compound_statement(p):
    '''function_compound_statement : new_compound_statement
    '''  
    p[0]=p[1]
    p[0].ast = build_AST(p)

# def p_function_compound_statement(p):
#     '''function_compound_statement : LEFT_CURLY_BRACKET closebrace
#                           | LEFT_CURLY_BRACKET statement_list closebrace
#                           | LEFT_CURLY_BRACKET declaration_list closebrace
#                           | LEFT_CURLY_BRACKET declaration_list statement_list closebrace
#     '''  
#     if(len(p) == 3):
#       p[0] = Node(name = 'CompoundStatement',val = '',type = '', lno = p.lineno(1), children = [])
#     elif(len(p) == 4):
#       p[0] = p[2]
#       p[0].name = 'CompoundStatement'
#       p[0].ast = build_AST(p)
#     elif(len(p) == 4):
#       p[0] = Node(name = 'CompoundStatement', val = '', type = '', children = [], lno = p.lineno(1))
#       p[0].ast = build_AST(p,[1,4])
#     else:
#       p[0] = Node(name = 'CompoundStatement', val = '', type = '', children = [], lno = p.lineno(1))
#       p[0].ast = build_AST(p,[1,5])


def p_declaration_list(p):
    '''declaration_list : declaration
                        | declaration_list declaration
    '''

    if(len(p) == 2):
      p[0] = p[1]
      p[0].ast = build_AST(p)
    else:
      p[0] = Node(name = 'DeclarationList', val = '', type = '', children = [], lno = p.lineno(1))
      p[0].ast = build_AST(p)
      if(p[1].name != 'DeclarationList'):
        p[0].children.append(p[1])
      else:
        p[0].children = p[1].children
      p[0].children.append(p[2])

def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement
    '''
    if(len(p) == 2):
      p[0] = p[1]
      p[0].ast = build_AST(p)
    else:
      p[0] = Node(name = 'StatementList', val='', type='', children = [], lno = p.lineno(1))
      p[0].ast = build_AST(p)
      if(p[1].name != 'StatmentList'):
        p[0].children.append(p[1])
      else:
        p[0].children = p[1].children
      p[0].children.append(p[2])

def p_expression_statement(p):
    '''expression_statement : SEMICOLON
                            | expression SEMICOLON
    '''
    p[0] = Node(name = 'ExpressionStatement', val='', type='', children = [], lno = p.lineno(1))
    if(len(p) == 3):
      p[0].ast = build_AST(p,[2])
      p[0].val = p[1].val
      p[0].type = p[1].type
      p[0].children = p[1].children
    # TODO : see what to do in case of only semicolon in rhs

def p_selection_statement(p):
    """selection_statement : IF LEFT_BRACKET expression RIGHT_BRACKET compound_statement
    | IF LEFT_BRACKET expression RIGHT_BRACKET compound_statement ELSE compound_statement
    | switch LEFT_BRACKET expression RIGHT_BRACKET compound_statement"""
    #TO_DO scope_name for while and do
    if p[1]=="if":
        if len(p)==6:
          p[0] = Node(name = 'IfStatment', val = '', type = '', children = [], lno = p.lineno(1))
        else:
          p[0] = Node(name = 'IfElseStatement', val = '', type = '', children = [], lno = p.lineno(1))
    else:
        p[0] = Node(name = 'SwitchStatement', val = '', type = '', children = [], lno = p.lineno(1))
    
    p[0].ast = build_AST(p)

def p_switch(p):
    '''switch : SWITCH'''
    p[0] = p[1]
    ST.switchDepth += 1
    p[0] = build_AST(p)

def p_iteration_statement(p):
    '''iteration_statement : while LEFT_BRACKET expression RIGHT_BRACKET compound_statement
    | do compound_statement WHILE LEFT_BRACKET expression RIGHT_BRACKET SEMICOLON
    | for lopenparen for_init_statement expression SEMICOLON expression RIGHT_BRACKET new_compound_statement
    | for lopenparen for_init_statement expression SEMICOLON RIGHT_BRACKET new_compound_statement
    | for lopenparen for_init_statement SEMICOLON expression RIGHT_BRACKET new_compound_statement
    | for lopenparen for_init_statement SEMICOLON RIGHT_BRACKET new_compound_statement
    '''
    #TO_DO scope_name for while and do
    if p[1]=='do':
      p[0] = Node(name = 'DoWhileStatement', val = '', type = '', children = [], lno = p.lineno(1))
      p[0].ast = build_AST(p,[4,6])
    elif p[1]=='while':
      p[0] = Node(name = 'WhileStatement', val = '', type = '', children = [], lno = p.lineno(1))
      p[0].ast = build_AST(p,[2,4])
    else:
      p[0] = Node(name = 'ForStatement', val = '', type = '', children = [], lno = p.lineno(1))
      p[0].ast = build_AST(p,[4,5])
    ST.loopingDepth -= 1


# def p_iteration_statement(p):
#     '''iteration_statement : while LEFT_BRACKET expression RIGHT_BRACKET statement
#     | do statement WHILE LEFT_BRACKET expression RIGHT_BRACKET SEMICOLON
#     | for LEFT_BRACKET expression_statement expression_statement RIGHT_BRACKET statement
#     | for LEFT_BRACKET expression_statement expression_statement expression RIGHT_BRACKET statement'''
    
#     if p[1]=='do':
#       p[0] = Node(name = 'DoWhileStatement', val = '', type = '', children = [], lno = p.lineno(1))
#       p[0].ast = build_AST(p,[4,6])
#     elif p[1]=='while':
#       p[0] = Node(name = 'WhileStatement', val = '', type = '', children = [], lno = p.lineno(1))
#       p[0].ast = build_AST(p,[2,4])
#     else:
#       p[0] = Node(name = 'ForStatement', val = '', type = '', children = [], lno = p.lineno(1))
#       if len(p)==6:
#         p[0].ast = build_AST(p,[4,5])
#       else:
#         p[0].ast = build_AST(p,[4,6])
        
#     ST.loopingDepth -= 1

def p_for_init_statement(p): 
    '''for_init_statement : expression_statement 
                          | declaration 
    ''' 
    p[0] = p[1]
    p[0].ast = build_AST(p)
    ST.scope_to_function[ST.currentScope] = "For"
    
    
def p_while(p):
  '''while : WHILE'''
  ST.loopingDepth += 1
  p[0] = p[1]
  p[0] = build_AST(p)
  
def p_do(p):
  '''do : DO'''
  ST.loopingDepth += 1
  p[0] = p[1]
  p[0] = build_AST(p)
  
def p_for(p):
  '''for : FOR'''
  ST.loopingDepth += 1
  p[0] = p[1]
  p[0] = build_AST(p)

def p_jump_statemen_1(p):
    """jump_statement : GOTO IDENTIFIER SEMICOLON
    | CONTINUE SEMICOLON
    | BREAK SEMICOLON"""
    p[0] = Node(name = 'JumpStatement',val = '',type = '', lno = p.lineno(1), children = [])
    p[0].ast = build_AST(p,[2])

    if p[1]=="continue" and ST.loopingDepth == 0:
      print(p[0].lno, 'continue not inside loop')
    elif p[1]=="break" and ST.loopingDepth == 0 and ST.switchDepth == 0:      
      print(p[0].lno, 'break not inside loop/switch')

def p_jump_statemen_2(p):
    """jump_statement : RETURN SEMICOLON
    | RETURN expression SEMICOLON"""
    p[0] = Node(name = 'JumpStatement',val = '',type = '', lno = p.lineno(1), children = [])   
    p[0].ast = build_AST(p,[2]) 

    if(len(p) == 3):
      if(ST.curFuncReturnType != 'void'):
        error = 'COMPILATION ERROR at line ' + str(p.lineno(1)) + ': function return type is not void'
        ST.c_error.append(error) 
    else:
      if(p[2].type != '' and ST.curFuncReturnType != p[2].type):
        error = 'warning at line ' + str(p.lineno(1)) + ': function return type is not ' + p[2].type
        ST.c_error.append(error)
      
def p_translation_unit(p):
    '''translation_unit : external_declaration
                        | translation_unit external_declaration
    '''
    p[0] = Node(name = 'JumpStatement',val = '',type = '', lno = p.lineno(1), children = [])
    if(len(p) == 2):
      p[0].children.append(p[1])
    else:
      p[0].children.append(p[2])
    p[0].ast = build_AST(p)
    
def p_external_declaration(p):
    '''external_declaration : function_definition
                            | declaration
    '''
    p[0] = p[1]
    p[0].name = 'ExternalDeclaration'
    p[0].ast = build_AST(p)
  
def p_function_definition_1(p):
    '''function_definition : declaration_specifiers declarator declaration_list compound_statement
                           | declarator declaration_list function_compound_statement
                           | declarator function_compound_statement                                                                              
    ''' 
    if(len(p) == 3):
      p[0] = Node(name = 'FuncDeclWithoutType',val = p[1].val,type = 'int', lno = p[1].lno, children = [])
    elif(len(p) == 4):
      p[0] = Node(name = 'FuncDeclWithoutType',val = p[1].val,type = 'int', lno = p[1].lno, children = [])
    else:
      p[0] = Node(name = 'FuncDecl',val = p[2].val,type = p[1].type, lno = p[1].lno, children = [])
    p[0].ast = build_AST(p)


def p_function_definition_2(p):
  '''function_definition : declaration_specifiers declarator function_compound_statement'''

  p[0] = Node(name = 'FuncDecl',val = p[2].val,type = p[1].type, lno = p.lineno(1), children = [])
  p[0].ast = build_AST(p)

def p_openbrace(p):
  '''openbrace : LEFT_CURLY_BRACKET'''
  ST.parent[ST.nextScope] = ST.currentScope
  ST.currentScope = ST.nextScope
  ST.symbol_table.append({})
  ST.nextScope = ST.nextScope + 1
  ST.scope_to_function[ST.currentScope] = ST.scope_to_function[ST.parent[ST.currentScope]]
  p[0] = p[1]

def p_lopenparen(p):
  '''lopenparen : LEFT_BRACKET'''
  ST.parent[ST.nextScope] = ST.currentScope
  ST.currentScope = ST.nextScope
  ST.symbol_table.append({})
  ST.nextScope = ST.nextScope + 1
  #MODIFIED
  ST.scope_to_function[ST.currentScope] = ST.scope_to_function[ST.parent[ST.currentScope]]
  p[0] = p[1]

def p_closebrace(p):
  '''closebrace : RIGHT_CURLY_BRACKET'''
  #global ST.currentScope
  ST.currentScope = ST.parent[ST.currentScope]
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
    if(p):
      print("Syntax error in input at line " + str(p.lineno))
    # p.lineno(1)

def runmain(code):
  open('graph1.dot','w').write("digraph G {")
  parser = yacc.yacc(start = 'translation_unit')
  result = parser.parse(code,debug=False)
  for i in range(len(ST.c_error)):
        print(ST.c_error[i])
  visualize_symbol_table()
  
def visualize_symbol_table():
  #global scopeName
  with open("symbol_table_output.json", "w") as outfile:
    outfile.write('')
  for i in range (ST.nextScope):
    if(len(ST.symbol_table[i]) > 0):
      temp_list = {}
      for key in ST.symbol_table[i].keys():
        if(not key.startswith('struct')):
          temp_list[key] = ST.symbol_table[i][key]
      json_object = json.dumps(temp_list, indent = 4)
      with open("symbol_table_output.json", "a") as outfile:
        outfile.write('In \"' + ST.scope_to_function[i] + "\"")
        outfile.write(json_object+"\n")

file = open(sys.argv[1])
code = file.read()
if __name__ == '__main__':
  runmain(code)



