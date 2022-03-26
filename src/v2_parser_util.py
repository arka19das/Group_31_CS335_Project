from dataclasses import dataclass, field, fields
from typing import List, Any

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

@dataclass
class Node:
    name: str = ''
    val: Any = ''
    type: str = ''
    lno: int = 0
    size: int = 0
    children: list = field(default_factory=list)
    scope: int = 0
    array: list = field(default_factory=list)
    maxDepth: int = 0
    isFunc: int = 0
    parentStruct: str = ''
    argumentList: List[Any] = None
    #argumentList  = None
    field_list: list = field(default_factory=list)
    level: int = 0
    ast: Any = None

    def to_dict(self):
        s = {}
        for field in fields(self):
          value = getattr(self, field.name)
          if getattr(self, field.name) != field.default and value != []: 
              s[field.name] = value
        return s

@dataclass
class ScopeTable:
    nodes: list = field(default_factory=list)

    def find(self, key):
        for node in self.nodes:
            if node.name == key:
                return node 
        return None

    def insert(self, node):
        self.nodes.append(node)

class SymbolTable:
    def __init__(self):
        self.curType = []
        self.curFuncReturnType = ''
        self.symbol_table: list[ScopeTable] = []
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
        self.symbol_table.append(ScopeTable())
        self.parent[0]=0
        self.scope_to_function[0] = '#global'

    def find_scope(self, key):
        curscp = self.currentScope
        while(self.parent[curscp] != curscp):
            if self.symbol_table[curscp].find(key) is not None:
                break
            curscp = self.parent[curscp]
        if (curscp == 0 and self.symbol_table[curscp].find(key) is None):
            return -1 
        else :
            return curscp

    def find(self, key):
        scope = self.currentScope
        node = self.symbol_table[scope].find(key)
        while node is None:
            scope = self.parent[scope]
            node = self.symbol_table[scope].find(key)
            if scope == 0:
                break
        return node

    def scope_table(self, scope):
        return self.symbol_table[scope]

    @property
    def current_table(self):
        return self.symbol_table[self.currentScope]

    @property
    def parent_table(self):
        return self.symbol_table[self.parent[self.currentScope]]

    @property
    def global_table(self):
        return self.symbol_table[0]

ST = SymbolTable()

def is_iden(p):
  p_node = ST.find(p.val)
  
  if (p_node is not None) and ((p.isFunc == 1) or ('struct' in p.type.split())):
      error = "Compilation Error at line " +str(p.lno)+ " :Invalid operation on" + p.val
      ST.c_error.append(error)   

def type_util(op1, op2, op):
  temp = Node(name = op+'Operation' ,val = '',lno = op1.lno,type = 'int',children = [])
  if(op1.type == '' or op2.type == ''):
    temp.type = 'int' #default
    return temp
  top1 = str(op1.type)
  top2 = str(op2.type)
  tp1 = op1.type.split()[-1].upper()
  tp2 = op2.type.split()[-1].upper()
  
  if top1.endswith("*") >0 and top2.endswith("*")>0:
      error = "Can not cast pointer to pointer"
      ST.c_error.append(error)
      temp.type = op1.type
  elif top1.endswith("*") >0 or top2.endswith("*")>0:
      if top1.endswith("*") >0 and tp2 in TYPE_FLOAT:
        error = str(op1.lno) +  ' COMPILATION ERROR : Incompatible data type with ' + op +  ' operator'  
        ST.c_error.append(error)
        temp.type = op1.type
      if top2.endswith("*") >0 and tp1 in TYPE_FLOAT:
        error = str(op1.lno) +  ' COMPILATION ERROR : Incompatible data type with ' + op +  ' operator'  
        ST.c_error.append(error)
        temp.type = op2.type
  else:
    if tp1 not in ops_type[op] or tp2 not in  ops_type[op]:
        error = str(op1.lno) + ' COMPILATION ERROR : Incompatible data type with ' + op +  ' operator' 
        ST.c_error.append(error)
        
    size1 = SIZE_OF_TYPE[tp1]
    size2 = SIZE_OF_TYPE[tp2]
    if size1>size2:
      error = str(op1.lno) + ' WARNING : Implicit Type casting of ' + op2.val 
      ST.c_error.append(error)
      temp.type = op1.type
    elif size2>size1:
      error = str(op1.lno) + ' WARNING : Implicit Type casting of ' + op1.val 
      ST.c_error.append(error)
      temp.type = op2.type
    else:
      if tp1=="FLOAT" or tp2=="FLOAT":
        temp.type = "float"
      elif tp1=="DOUBLE" or tp2=="DOUBLE":
            temp.type = "float"
      elif top1.startswith("unsigned"):
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
    node = ST.find(type_1)
    if node is None:
        return -1
    return ST.find(type_1).size    
  
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