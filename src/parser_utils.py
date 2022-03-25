import sys

TYPE_FLOAT = ["FLOAT", "DOUBLE", "LONG DOUBLE"]
TYPE_INTEGER = [
    "SHORT",
    "SHORT INT",
    "SIGNED SHORT",
    "SIGNED SHORT INT",
    "UNSIGNED SHORT",
    "UNSIGNED SHORT INT",
    "INT",
    "SIGNED INT",
    "UNSIGNED INT",
    "SIGNED",
    "UNSIGNED",
    "LONG",
    "LONG INT",
    "SIGNED LONG INT",
    "SIGNED LONG",
    "UNSIGNED LONG",
    "UNSIGNED LONG INT",
    "LONG LONG",
    "LONG LONG INT",
    "SIGNED LONG LONG",
    "SIGNED LONG LONG INT",
    "UNSIGNED LONG LONG",
    "UNSIGNED LONG LONG INT",
]

TYPE_CHAR = [
    "CHAR",
    "SIGNED CHAR",
    "UNSIGNED CHAR",
]

PRIMITIVE_TYPES = TYPE_CHAR + TYPE_FLOAT + TYPE_INTEGER

SIZE_OF_TYPE = {
    "VOID": 0,
    "CHAR": 1,  
    "SHORT": 2,
    "FLOAT": 4,
    "INT": 4,
    "DOUBLE": 8,
    "LONG": 8,
    
    "SHORT INT": 2,
    "LONG INT": 8,
    "LONG LONG": 8,
    "LONG LONG INT": 8,
    "LONG DOUBLE": 16,
    
    "SIGNED CHAR": 1,
    "SIGNED SHORT": 2,
    "SIGNED SHORT INT": 2,
    "SIGNED": 4,
    "SIGNED INT": 4,
    "SIGNED LONG": 8,
    "SIGNED LONG INT": 8,
    "SIGNED LONG LONG": 8,
    "SIGNED LONG LONG INT": 8,
    
    "UNSIGNED CHAR": 1,
    "UNSIGNED SHORT": 2,
    "UNSIGNED SHORT INT": 2,
    "UNSIGNED": 4,
    "UNSIGNED INT": 4,
    "UNSIGNED LONG": 8,
    "UNSIGNED LONG INT": 8,
    "UNSIGNED LONG LONG": 8,
    "UNSIGNED LONG LONG INT": 8,    
}

ops_type = {
    # arithmetic operators
    '+' : PRIMITIVE_TYPES,
    '-' : PRIMITIVE_TYPES,
    '*' : PRIMITIVE_TYPES,
    '/' : PRIMITIVE_TYPES,
    '%' : TYPE_INTEGER,

    # comparsion operators
    '>' : PRIMITIVE_TYPES,
    '>=' : PRIMITIVE_TYPES,
    '<' : PRIMITIVE_TYPES,
    '<=' : PRIMITIVE_TYPES,
    '!=' : PRIMITIVE_TYPES,
    '==' : PRIMITIVE_TYPES,
    
    
    # bool operators
    '||' : PRIMITIVE_TYPES,
    '&&' : PRIMITIVE_TYPES,
    '!' : PRIMITIVE_TYPES,
    
    # bits operators
    '<<' : TYPE_INTEGER,
    '>>' : TYPE_INTEGER,
    '|' : TYPE_INTEGER,
    '&' : TYPE_INTEGER,
    '~' : TYPE_INTEGER,
    '^' : TYPE_INTEGER,
}

class SymbolTable:
    def __init__(self):
        self.curType = []
        self.curFuncReturnType = ''
        self.symbol_table = []
        # typedef_list = {}
        # all_typedef = []
        self.scope_to_function = {}
        self.currentScope = 0
        self.nextScope = 1
        self.parent = {}
        self.loopingDepth = 0
        self.switchDepth = 0
        self.c_error = []
        self.set()
        
    def set(self):
        self.symbol_table.append({})
        self.parent[0]=0
        self.scope_to_function[0] = '#global'

    def find_scope(self, key):
        curscp = self.currentScope
        while(self.parent[curscp] != curscp):
            if(key in self.symbol_table[curscp].keys()):
                break
            curscp = self.parent[curscp]
        if (curscp == 0 and key not in self.symbol_table[curscp].keys()):
            return -1 
        else :
            return curscp

class Node:
  def __init__(self, name = '',val = '',lno = 0,type = '',children = '',scope = 0, array = [], is_array=0, maxDepth = 0,isFunc = 0, isarray=0, parentStruct = '', level = 0,ast = None):
    
    self.name = name
    self.val = val
    self.type = type
    self.lno = lno
    self.scope = scope
    self.array = array
    self.is_array = is_array
    self.maxDepth = maxDepth
    self.isFunc = isFunc
    self.isarray = isarray
    self.parentStruct = parentStruct
    self.ast = ast
    self.level = level
    if children:
      self.children = children
    else:
      self.children = []

ST = SymbolTable()

def is_iden(p):
  found_scope = ST.find_scope(p.val)
  
  if (found_scope != -1) and ((p.isFunc == 1) or ('struct' in p.type.split())):
      error = "Compilation Error at line " +str(p.lno)+ " :Invalid operation on" + p.val
      ST.c_error.append(error)   

def type_util(op1, op2, op):
  temp = Node(name = op+'Operation' ,val = '',lno = op1.lno,type = 'int',children = [])
  if(op1.type == '' or op2.type == ''):
    temp.type = 'int' #default
    return temp
  
  top1 = str(op1.type)
  top2 = str(op2.type)
  if top1.endswith("*") >0 and top2.endswith("*")>0:
      error = "Can not cast pointer to pointer"
      ST.c_error.append(error)
      temp.type = op1.type
  elif top1.endswith("*") >0 or top2.endswith("*")>0:
      if top1.endswith("*") >0 and op2.type.split()[-1].upper() in TYPE_FLOAT:
        error = str(op1.lno) +  ' COMPILATION ERROR : Incompatible data type with ' + op +  ' operator'  
        ST.c_error.append(error)
        temp.type = op1.type
      if top2.endswith("*") >0 and op1.type.split()[-1].upper() in TYPE_FLOAT:
        error = str(op1.lno) +  ' COMPILATION ERROR : Incompatible data type with ' + op +  ' operator'  
        ST.c_error.append(error)
        temp.type = op2.type
      
  else:
    print(op1.type, op2.type)
    if op1.type.split()[-1].upper() not in ops_type[op] or op2.type.split()[-1].upper() not in  ops_type[op]:
      error = str(op1.lno) + ' COMPILATION ERROR : Incompatible data type with ' + op +  ' operator' 
      ST.c_error.append(error)

    size1 = SIZE_OF_TYPE[op1.type.split()[-1].upper()]
    size2 = SIZE_OF_TYPE[op2.type.split()[-1].upper()]

    if size1>size2:
      error = str(op1.lno) + ' WARNING : Implicit Type casting of ' + op2.val 
      ST.c_error.append(error)
      temp.type = op1.type
    elif size2>size1:
      error = str(op1.lno) + ' WARNING : Implicit Type casting of ' + op1.val 
      ST.c_error.append(error)
      temp.type = op2.type
    else:
          if str(op1.type).startswith("unsigned"):
            temp.type = op1.type
          else:
            temp.type = op2.type
  if temp.type == 'char':
    temp.type = 'int'
  
  if op in ['*', '-', '%']:
    temp.val = op1.val
  
  is_iden(op1)
  is_iden(op2)
  return temp

def get_data_type_size(type_1):
  
  if type_1.endswith('*'):
    return 8
  if type_1.startswith('struct'):
    scope = ST.find_scope(type_1)
    if scope==-1:
        return -1
    return ST.symbol_table[scope][type_1]['size']    
  
  type_1 = type_1.split()[-1]
  if type_1.upper() not in SIZE_OF_TYPE.keys():
    return -1
  return SIZE_OF_TYPE[type_1.upper()]
  
def ignore_1(s):
  if(s == "}"):
    return True
  elif(s == "{"):
    return True
  elif(s == ")"):
    return True
  elif(s == "("):
    return True
  elif(s == ";"):
    return True
  elif(s == '['):
    return True
  elif(s == ']'):
    return True
  elif(s == ','):
    return True
  return False
