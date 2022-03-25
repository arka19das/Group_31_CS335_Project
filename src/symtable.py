import copy

c_error = list()

# bool not required since already converted to TYPE_INTEGER
TYPE_FLOAT = ["FLOAT", "DOUBLE", "LONG DOUBLE"]
TYPE_CHAR = [
    "CHAR",
    "SIGNED CHAR",
    "UNSIGNED CHAR",
]
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

PRIMITIVE_TYPES = TYPE_CHAR + TYPE_FLOAT + TYPE_INTEGER

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


cast_type = {
    'int'     : ['int', 'float', 'char'],
    'float'   : ['int', 'float', 'char'],
    'char'    : ['int', 'char'],
    'pointer' : ['int', 'float', 'char'],
}

class ScopeTable:
    def __init__(self, scope_depth=0, parent=None, scope_id=0, scope_type='Other'):
        self.scope_id = scope_id        
        self.scope_depth = scope_depth  
        self.parent = parent            
        self.classes = dict()
        self.functions = dict()
        self.structs = dict()               
        self.typedef = dict()               
        self.variables = dict()             
        self.type = scope_type    

    def lookup_class(self, c_name):
        return True if c_name in self.classes else False
    
    def lookup_function(self, f_name):
        return True if f_name in self.functions else False
    
    def lookup_struct(self, s_name):
        return True if s_name in self.structs else False
    
    def lookup_typedef(self, t_name):
        return True if t_name in self.typedef else False
        # return self.aliases.get(name, None)
    
    def lookup_var(self, v_name):
        return True if v_name in self.variables else False

class SymbolTable():
    def __init__(self):
        self.global_scope = ScopeTable()
        self.global_scope.type = 'Global_Table'
        self.scope_list = [self.global_scope]
        self.scope_stack = [self.global_scope]
        
    def table_depth(self):
        return len(self.scope_stack)

    def table_scope(self):
        assert len(self.scope_stack) >= 1
        return self.scope_stack[-1]
    
    def push_scope(self, scope_type='Other') :
        new_scope = ScopeTable(self.table_depth(), self.scope_stack[-1], len(self.scope_list), scope_type)
        self.scope_list.append(new_scope)
        self.scope_stack.append(new_scope)

    def pop_scope(self) :
        self.scope_stack.pop()

    def lookup_component(self, component, name):
        scope = self.table_scope()
        
        if component == 'class':
            _component_to_function = [scope.lookup_class, scope.functions]
        elif component == 'function':
            _component_to_function = [scope.lookup_function, scope.classes]
        elif component == 'struct':
            _component_to_function = [scope.lookup_struct, scope.structs]
        elif component == 'typedef':
            _component_to_function = [scope.lookup_typedef, scope.typedef]
        elif component == 'var':
            _component_to_function = [scope.lookup_var, scope.variables]
        else:
            raise Exception(f"{component} is not a valid kind of identifier")    
            
        _lookup = _component_to_function[0]
        _dict = _component_to_function[1]
        while scope:
            if _lookup(name):
                return _dict[name]
            scope = scope.parent
        return None

    # def lookup_var(self, name):
    #     scope = self.cur_scope()
    #     while scope:
    #         if scope.lookup_var(name):
    #             return scope.variables[name]
    #         scope = scope.parent
    #     return None

    # def lookup_struct(self, name):
    #     scope = self.cur_scope()
    #     while scope:
    #         if scope.lookup_struct(name):
    #             return scope.structs[name]
    #         scope = scope.parent
    #     return None

    # def lookup_alias(self, name):
    #     scope = self.cur_scope()
    #     while scope:
    #         if scope.lookup_alias(name):
    #             return scope.aliases[name]
    #         scope = scope.parent
    #     return None
    #     # return self.cur_scope().lookup_alias(id)

    # def lookup_func(self, name):
    #     if name in self.function:
    #         return self.function[name]
    #     return None

    def get_size(self, dtype):
        raise Exception('TODO')

    def add_var(self, name, mdata):
        scope =  self.table_scope()
        if scope.lookup_var(name):
            c_error.append('Redeclaration of variable named {}'.format(name))
            # #parser.error = c_error[-1]
            # #parser_error()
            return

        scope.variables[name] = mdata

    def add_struct(self, name, mdata):
        scope = self.table_scope()
        if scope.lookup_struct(name):
            c_error.append('Redeclaration of struct named {}'.format(name))
            # #parser.error = c_error[-1]
            # #parser_error()
            return

        scope.structs[name] = mdata

    def add_typedef(self, alias, actual):
        scope = self.table_scope()
        lookup_alias = scope.lookup_alias(alias)
        if lookup_alias is None:
            scope.typedef[alias] = actual
        elif lookup_alias != actual:
            c_error.append('Redeclaration of type/alias named {}'.format(alias))
            # #parser.error = c_error[-1]
            # #parser_error()
        return
        
    def add_function(self, name, mdata):
        scope = self.table_scope()
        if name in scope.functions:
            _func = scope.functions[name]
            if _func.ret_type == mdata.ret_type and _func.args == mdata.args:
                return
            c_error.append('Redeclaration of function named {}'.format(name))
            # #parser.error = c_error[-1]
            # #parser_error()
            return
                
        scope.functions[name] = mdata
    
    def add_class(self, name, mdata):
        scope = self.table_scope()
        if name in scope.classes:
            _class = scope.classes[name]
            ##TO_DO
            ##CHECK CLASS REDECLARATION

        scope.classes[name] = mdata
        
    def check_type(self, type):
        scope = self.table_scope()
        while scope:
            if scope.type in type:
                return True
            scope = scope.parent
        return False
    
    #Checking if scope is Loop or Switch for allowing break 
    def check_break_scope(self):
        return self.check_type(["Switch","Loop"])

    #Checking if scope is Loop for allowing continue 
    def check_continue_scope(self): 
        return self.check_type(["Loop"])

    def dump_csv(self, filename):
        Exception("TO_DO")    

# if __name__ == '__main__':
#     sym = SymbolTable()
#     sym.push_scope()
#     sym.add_var('a',{'type':1})
#     print(sym.lookup_component('var','a'))

class StructType():
    def __init__(self, name=None, variables=None):
        super().__init__()
        
        self.name = name
        self.variables = variables
        self.size = 0
        if self.variables:
            self.set_size()

    def is_defined(self):
        if self.variables is not None:
            return True
        
        sym_type = symtable.lookup_component('struct', self.name)
        if sym_type is not None:
            self.variables = sym_type.variables
            self.set_size()
            
        return self.variables is not None

    def set_size(self):
        self.offsets = {}
        for key, value in self.variables.items():
            self.offsets[key] = self.size
            self.size += value.get_size()
    
    def get_size(self):
        return self.size
    
    def get_offset(self, name):
        return self.offsets[name]
    
    def get_first_element_type(self):
        # returns type of first element in struct
        name, vartype = next(iter(self.variables.items()))
        return vartype
    
    def get_element_type(self, name):
        return self.variables[name]

    def __eq__(self, other):
        if not isinstance(other, StructType) or self.name != other.name :
            return False

        return True    

class Function:
    def __init__(self, mdata):
        super().__init__()
        self.mdata = mdata              
        #IS Always global
        self.scope_id = 0               
    
    def param_size(self):
        size = 0
        for name, vtype in self.mdata.args:
            size += vtype.get_size()
        return size
        
    def __eq__(self, other):
        # is_declared is not checked
        if not isinstance(other, Function):
            return False
        
        args_same = True
        if len(self.args) != len(other.args):
            return False
        for (name1, type1), (name2, type2) in zip(self.mdata.args, other.mdata.args):
            args_same = args_same and (type1 == type2)
        return args_same and self.name == other.name and self.ret_type == other.ret_type

class VarType:
    def __init__(self, mdata, arr_offset=None):
        super().__init__()
        self.mdata = mdata
        self.arr_offset = arr_offset
        self.is_tmp = False
        self.is_param = False

    def get_size(self):
        if self.ref_count > 0:
            if self.arr_offset is None or self.arr_offset == []:
                return ADDR_SIZE
            else:
                if self.is_tmp:
                    return ADDR_SIZE
                size = self.get_ref_size() * int(self.arr_offset[0].const)

                return size
        else:
            if isinstance(self._type, StructType):
                if self.is_tmp:
                    return ADDR_SIZE
                return self._type.get_size()
            else:
                try:
                    return SIZE_OF_TYPE[self._type]
                except:
                    raise Exception(f'Invalid type {self._type}')    
        
    def get_ref_size(self):
        return self.get_ref_type().get_size()

    def get_ref_type(self):
        if not self.is_array():
            return VarType(self.ref_count - 1, self._type)
        else:
            return self.get_array_element_type()

    def get_pointer_type(self):
        return VarType(self.ref_count + 1, self._type, self.arr_offset)

    def is_array(self):
        return len(self.arr_offset) > 0 and self.arr_offset is not None
    
    def get_array_len(self):
        assert(self.is_array())
        return int(self.arr_offset[0].const)

    def get_array_element_type(self):
        assert(self.is_array())
        # return type of element after applying array access operator
        if len(self.arr_offset) > 1:
            return VarType(self.ref_count, self._type, self.arr_offset[1:])
        else:
            return VarType(self.ref_count-1, self._type, self.arr_offset[1:])

    def is_struct_type(self):
        return (not self.mdata.ref_count>0) and isinstance(self._type, StructType)

    def castable_to(self, other):
        if self.mdata.ref_count>0:
            return other.mdata.ref_count>0 or other.mdata._type in ['int', 'char']
        elif self.mdata._type in ['int', 'char']:
            return other.mdata.ref_count>0 or other.mdata._type in ['int', 'char', 'float']
        elif self.mdata._type in ['float']:
            return (not other.mdata.ref_count>0) and other.mdata._type in ['int', 'char', 'float']
        else:
            return self == other

    def get_caste_type(self, other):
        
        if self == other:
            return copy.deepcopy(self)
        
        # if it is pointer => other must be same
        if self.mdata.ref_count>0:
            if self == other:
                return copy.deepcopy(self)
            else:
                return None
    
        # if not pointer => handle on scale of basic_type
        elif self.mdata._type in ['int', 'char']:
            if other.mdata.ref_count>0:
                return None
            elif other.mdata._type in ['int', 'float']:
                return copy.deepcopy(other)
            elif other.mdata._type == 'char':
                return copy.deepcopy(self)
            else:
                return None
        
        elif self.mdata._type == 'float':
            if other.mdata.ref_count>0:
                return None
            elif other.mdata._type in ['int', 'char', 'float']:
                return copy.deepcopy(self)
            else:
                return None
        else:
            return None

    def __eq__(self, other):
        if not isinstance(other, VarType):
            return False
        return self.ref_count == other.ref_count and self._type == other._type

class ScopeName:
    def __init__(self, name):
        super().__init__()
        self.name = name
            
class BaseExpr:
       
    def __init__(self, t_name):
        super().__init__()
        self.t_name = t_name
        self.bool = False
        self.expr_type = VarType(0, 'int')

    def op_allowed(self, op, _type):
        if op not in ops_type.keys():
            return True
        return _type in ops_type.keys[op]
    
    def has_lvalue(self, ):
        # if current expression has address (if current expression can be lhs in assignment op)
        # checks if address exists for this expression
        if isinstance(self, Const):
            return False
        elif isinstance(self, Identifier):
            return True
        elif isinstance(self, UnaryExpr):
            return True if self.ops == '*' else False 
        elif isinstance(self, PostfixExpr):
            return True if self.ops in ['[', '.', '->'] else False
        else:
            return False
        
class Const(BaseExpr):
    def __init__(self, const, dvalue):
        super().__init__("Constant")
        self.const = const
        self.dvalue = dvalue
        self.get_type()

    def get_type(self):
        if self.dvalue == 'int':
            self.expr_type = VarType(0, 'int')
        elif self.dvalue == 'float':
            self.expr_type = VarType(0, 'float')
        elif self.dvalue == 'char':
            self.const = str(ord(self.const[1:-1].encode('utf-8').decode('unicode_escape')))
            self.dvalue = 'int'
            self.expr_type = VarType(0, 'int')
        elif self.dvalue == 'STRING_LITERAL':
            self.expr_type = VarType(1, 'char', [Const(str(len(self.const.encode('utf-8').decode('unicode_escape'))-1), 'int')])
        # else:
        #     parser_error('Unknown Constant type')

class Identifier(BaseExpr):
    def __init__(self, name: str):
        super().__init__("Identifier")
        self.name = name
        self.get_type()
    
    def get_type(self):
        _var = symtable.lookup_var(self.name)
        if _var is None:
            raise SyntaxError(f'Undeclared Variable {self.name}')
        else:
            self.expr_type = _var

class CastExpr(BaseExpr):
    def __init__(self, _type, Expr):
        super().__init__("Cast Expression")
        self.type = _type
        self.expr = Expr
        self.get_type()

    def get_type(self):
        if self.expr.expr_type.mdata.ref_count>0:
            # source is pointer
            if self.type.mdata.ref_count>0:
                # target is pointer
                self.expr_type = self.type
            else:
                # target is not pointer
                if self.type._type in ['int']:
                    # target is int / char
                    self.expr_type = self.type
                else:
                    # target is float
                    raise SyntaxError(f'Cannot convert pointer to {self.expr.expr_type._type}')
        else:
            # source is not pointer
            if self.type.mdata.ref_count>0:
                # target is pointer
                if self.expr.expr_type._type in ['int']:
                    # source is int / char
                    self.expr_type = self.type
                else:
                    # source is float
                    raise SyntaxError(f'Cannot convert {self.expr.expr_type._type} to pointer')
            else:
                # target is int/char/float, and source is also int/char/float
                self.expr_type = self.type
    
    @staticmethod
    def get_cast(target_type,expr):
        if target_type == expr.expr_type:
            return expr
        return CastExpr(target_type, expr)

class OpExpr(BaseExpr):
    """
    binary operators : +, -, *, /, %, >, >=, <, <=, ==, !=, ||, &&, <<, >>, |, &, ^
    """
    def __init__(  self,  lhs, ops, rhs ):
        
        self.ops_type['=='] = ['int', 'char', 'float']
        self.ops_type['!='] = ['int', 'char', 'float']
        super().__init__("Expression")
        self.lhs = lhs
        self.ops = ops
        self.rhs = rhs
        self.get_type()
       
    def get_type(self):
        
        ref_count = 0
        inferred_type = 'int'
        # if any of the operand is char than cast it to `int` for ops
        if isinstance(self.lhs, BaseExpr) and self.lhs.expr_type == VarType(0,'char'):
            self.lhs = CastExpr.get_cast(VarType(0, 'int'), self.lhs)

        if isinstance(self.rhs, BaseExpr) and self.rhs.expr_type == VarType(0,'char'):
            self.rhs = CastExpr.get_cast(VarType(0, 'int'), self.rhs)

        # will be error when (void *) + int 
        # if (
        #     self.lhs.expr_type._type not in self.ops_type[self.ops] and
        #     self.rhs.expr_type._type not in self.ops_type[self.ops]
        # ):
        #     raise SyntaxError(f'Invalid operands to ops {self.ops} (have `{self.lhs.expr_type}` and `{self.rhs.expr_type}`)')

        if self.ops in ['>', '>=', '<', '<=']:
            if self.lhs.expr_type.get_caste_type(self.rhs.expr_type):
                self.expr_type = VarType(0, 'int')
                return
            else:
                raise SyntaxError(f'Type not compatible with ops {self.ops}')
                return
        elif self.ops in ['||', '&&']:
            if self.lhs.expr_type.is_struct_type() or self.rhs.expr_type.is_struct_type():
                raise SyntaxError(f'Type not compatible with ops {self.ops}')
                return
            else:
                self.expr_type = VarType(0, 'int')
                return

        # if lhs is pointer
        if self.lhs.expr_type.ref_count > 0:
            # if rhs is pointer -> only '-' works
            if self.rhs.expr_type.ref_count > 0:
                if self.ops in ['-'] and self.rhs.expr_type.ref_count == self.lhs.expr_type.ref_count:
                    inferred_type = 'int'
                    ref_count = 0
                else:
                    raise SyntaxError('Type not compatible with ops {}'.format(self.ops))
                    # compilation_err.append('Type not compatible with ops {}'.format(self.ops))
                    # parser.error = compilation_err[-1]
                    # raise SyntaxError()
            # lhs is pointer and rhs is int => pointer add and sub
            else:
                if self.rhs.expr_type._type == 'int' or self.rhs.expr_type._type == 'char':
                    inferred_type = self.lhs.expr_type._type
                    ref_count = self.lhs.expr_type.ref_count
                else:
                    raise SyntaxError('Type not compatible with ops {}'.format(self.ops))
                    
        # if lhs is not pointer
        else:
            # lhs is int and rhs is pointer
            if self.rhs.expr_type.ref_count > 0:
                if self.ops in ['+']:
                    if self.lhs.expr_type._type == 'int':
                        inferred_type = self.rhs.expr_type._type
                        ref_count = self.rhs.expr_type.ref_count
                    else:
                        raise SyntaxError('Type not compatible with ops {}'.format(self.ops))
                        
                else:
                    raise SyntaxError('Type not compatible with ops {}'.format(self.ops))
                    
            # if lhs and rhs are both NOT pointer
            else:
                if self.rhs.expr_type._type == self.lhs.expr_type._type:
                    if self.rhs.expr_type._type in self.ops_type[self.ops]:
                        inferred_type = self.lhs.expr_type._type
                        ref_count = self.lhs.expr_type.ref_count
                    else:
                        raise SyntaxError('Type not compatible with ops {}'.format(self.ops))
                        
                else:
                    if self.rhs.expr_type._type in self.ops_type[self.ops]:
                        if self.lhs.expr_type._type in self.ops_type[self.ops]:
                            if self.rhs.expr_type._type == 'float' or self.lhs.expr_type._type == 'float':
                                inferred_type = 'float'
                                ref_count = 0
                            else:
                                inferred_type = 'int'
                                ref_count = 0
                            self.lhs = CastExpr.get_cast(VarType(ref_count, inferred_type), self.lhs)
                            self.rhs = CastExpr.get_cast(VarType(ref_count, inferred_type), self.rhs)
                        else:
                            raise SyntaxError('Type not compatible with ops {}'.format(self.ops))
                    else:
                        raise SyntaxError('Type not compatible with ops {}'.format(self.ops))

        self.expr_type = VarType(ref_count, inferred_type)

class UnaryExpr(OpExpr):
    """
    unary/prefix operators : +, -, * , &, ++, --, !, ~, sizeof
    """
    def __init__(self, ops, rhs):
        self.ops_type['++'] = ['int', 'char', 'float']
        self.ops_type['--'] = ['int', 'char', 'float']
        super().__init__(None, ops, rhs)
        self.get_type()

    def get_type(self):

        ref_count = 0
        inferred_type = 'int'

        # if any of the operand is char than cast it to `int` for ops
        if isinstance(self.rhs, BaseExpr) and self.rhs.expr_type == VarType(0,'char'):
            self.rhs = CastExpr.get_cast(VarType(0, 'int'), self.rhs)

        # sizeof ops
        if self.ops == 'sizeof':
            inferred_type = 'int'
            ref_count = 0
        # arithmetic ops
        if self.ops in ['--', '++']:
            if not self.rhs.has_lvalue():
                raise SyntaxError("lvalue required as increment/decrement operand")
                self.expr_type = self.rhs.expr_type
                return
            else:
                self.expr_type = self.rhs.expr_type
                return

        elif self.ops in ['+', '-']:
            if self.rhs.expr_type.ref_count == 0:
                if self.rhs.expr_type._type not in self.ops_type[self.ops]:
                    raise SyntaxError('Type not compatible with ops {}'.format(self.ops))
                    self.expr_type = self.rhs.expr_type
                    return
                
                inferred_type = self.rhs.expr_type._type
                ref_count = 0

            else:
                if self.ops in ['-', '+']:
                    raise SyntaxError('wrong type argument to unary minus')
                inferred_type = self.rhs.expr_type._type
                ref_count = self.rhs.expr_type.ref_count
        # bool ops
        elif self.ops in ['!', '~']:
            if self.rhs.expr_type._type not in self.ops_type[self.ops]:
                raise SyntaxError('Type not compatible with ops {}'.format(self.ops))
            
            inferred_type = 'int'
            ref_count = 0
        # error reporting
        elif self.ops == '*':
            if self.rhs.expr_type.ref_count > 0:
                inferred_type = self.rhs.expr_type._type
                ref_count = self.rhs.expr_type.ref_count - 1
            else:
                raise SyntaxError('Can not dereference a non pointer')
        elif self.ops == '&':
            # if not isinstance(self.rhs, Identifier) and \
            #     (not (isinstance(self.rhs, PostfixExpr) and self.rhs.ops in ['.', '->'])) and \
            #     (not (isinstance(self.rhs, UnaryExpr) and self.rhs.ops in ['*'])):
            if not self.rhs.has_lvalue():
                raise SyntaxError(f'lvalue required as unary `{self.ops}` operand')
            else:
                ref_count = self.rhs.expr_type.ref_count + 1
                inferred_type = self.rhs.expr_type._type
        
        self.expr_type = VarType(ref_count, inferred_type)

class PostfixExpr(OpExpr):
    """
    postfix operators : ++, --, array access `[`, function call `(`, `.` , `->`
    """
    def __init__(self, lhs, ops, rhs=None):
        self.ops_type['++'] = ['int', 'char', 'float']
        self.ops_type['--'] = ['int', 'char', 'float']
        super().__init__(lhs, ops, rhs)

    def get_type(self):
        
        ref_count = 0
        inferred_type = 'int'
        arr_offset = []

        # if any of the operand is char than cast it to `int` for ops
        if isinstance(self.lhs, BaseExpr) and self.lhs.expr_type == VarType(0,'char'):
            self.lhs = CastExpr.get_cast(VarType(0, 'int'), self.lhs)

        # arithmetic ops
        if self.ops in ['--', '++']:
            if not self.lhs.has_lvalue():
                raise SyntaxError("lvalue required as increment/decrement operand")
                self.expr_type = self.lhs.expr_type # for error recovery
                return
            else:
                self.expr_type = self.lhs.expr_type
                return

        # struct child accessing 
        elif self.ops == '.':
            if isinstance(self.lhs.expr_type._type, StructType) and self.lhs.expr_type.ref_count == 0:
                if self.lhs.expr_type._type.is_defined():
                    struct_var = self.lhs.expr_type._type.variables.get(self.rhs, None)
                    if struct_var is None:
                        raise SyntaxError('{} has no member named {}'.format(self.lhs.expr_type._type.name, self.rhs))
                    inferred_type = struct_var._type
                    ref_count = struct_var.ref_count
                else:
                    raise SyntaxError('Incomplete struct {}'.format(self.lhs.expr_type._type.name))
            else:
                raise SyntaxError('Dereferencing invalid struct type')

        # struct deferencing child
        elif self.ops == '->':
            if self.lhs.expr_type.ref_count == 1 and isinstance(self.lhs.expr_type._type, StructType):
                if self.lhs.expr_type._type.is_defined():
                    # print(self.lhs.expr_type)
                    struct_var = self.lhs.expr_type._type.variables.get(self.rhs, None)
                    if struct_var is None:
                        raise SyntaxError('{} has no member named {}'.format(self.lhs.expr_type._type.name, self.rhs))
                    inferred_type = struct_var._type
                    ref_count = struct_var.ref_count
                else:
                    raise SyntaxError('Incomplete struct {}'.format(self.lhs.expr_type._type.name))
            else:
                raise SyntaxError('Dereferencing invalid struct type')
        # function calling
        elif self.ops == '(':
            arg_list = [] if self.rhs is None else self.rhs

            _var = symtable.lookup_func(self.lhs)
            if isinstance(_var, Function):
                func = self.lhs = _var
                if func is None:
                    raise SyntaxError('{} is not callable'.format(self.lhs))

                if func.name in ['printf', 'scanf']:
                    if len(arg_list) < 1:
                        raise SyntaxError('too few/many arguments to function {}'.format(func.name))
                    # check if first arg is list
                    elif isinstance(arg_list[0], Const) and arg_list[0].expr_type == VarType(1, 'char'):
                        inferred_type = func.ret_type._type
                        ref_count = func.ret_type.ref_count
                    else:
                        raise SyntaxError(f'expected string as first arguments to function {func.name}')
                elif len(arg_list) == len(func.args):
                    inferred_type = func.ret_type._type
                    ref_count = func.ret_type.ref_count
    
                    # sanity checking of function args and casting them
                    if self.rhs:
                        casted_args = []
                        for i, (arg, (_,expected)) in enumerate(zip(arg_list, func.args)):
                            given = arg.expr_type
                            # if expected.get_caste_type(given) is None:
                            if not given.castable_to(expected):
                                # print(expected, given)
                                raise SyntaxError(f'incompatible type for argument {i+1} of `{func.name}`')
                            else:
                                casted_args.append(CastExpr.get_cast(expected, arg))
                        self.rhs = casted_args
                else:
                    raise SyntaxError('too few/many arguments to function {}'.format(func.name))
            else:
                raise SyntaxError(f'called object {self.lhs} is not a function')

        # array reference
        elif self.ops == '[':
            if self.rhs.expr_type == VarType(0, 'int'):
                # print(self.lhs.expr_type, self.rhs.expr_type)
                if self.lhs.expr_type.ref_count > 0:
                    inferred_type = self.lhs.expr_type._type
                    if len(self.lhs.expr_type.arr_offset) > 1:
                        ref_count = self.lhs.expr_type.ref_count
                        arr_offset = self.lhs.expr_type.arr_offset[1:]
                    elif len(self.lhs.expr_type.arr_offset) == 1:
                        ref_count = self.lhs.expr_type.ref_count - 1
                        arr_offset = self.lhs.expr_type.arr_offset[1:]
                    else:
                        ref_count = self.lhs.expr_type.ref_count - 1
                else:
                    raise SyntaxError('Subscripted value is neither array nor pointer')
            else:
                raise SyntaxError('Array subscript is not an integer')
        
        self.expr_type = VarType(ref_count, inferred_type, arr_offset)

class AssignExpr(OpExpr):
    def __init__(self, lhs, ops, rhs):
        super().__init__(lhs, ops, rhs)

    def get_type(self):
        
        if self.lhs.expr_type.is_array():
            raise SyntaxError("assignment to expression with array type")
            return

        if not self.lhs.has_lvalue():
            raise SyntaxError("lvalue required as left operand of assignment")
            self.expr_type = self.lhs.expr_type
            return
        
        if self.ops in ['*=','/=','%=','+=','-=', '<<=', '>>=', '&=', '|=', '^=']:
            self.rhs = OpExpr(copy.deepcopy(self.lhs), self.ops[:-1], self.rhs)

        # compatability is checked in CastExpr
        self.rhs = CastExpr.get_cast(self.lhs.expr_type, self.rhs)
        self.expr_type = self.lhs.expr_type

class CondExpr(BaseExpr):
    def __init__(self, cond, if_expr, else_expr):
        super().__init__("Conditional Expr")
        self.cond = cond
        self.if_expr = if_expr
        self.else_expr = else_expr
    
    def get_type(self, ):
        # check type mismatch between if_expr and else_expr
        self.expr_type = self.if_expr.expr_type.get_caste_type(self.else_expr)
        if self.expr_type is None:
            raise SyntaxError("Types not compatible with ternary operator")

class CommaExpr(BaseExpr):
    def __init__(self, *expr):
        super().__init__("Comma Expression")
        self.expr_list = expr
        self.get_type()

    def add_expr(self, expr):
        self.expr_list.append(expr)

    def get_type(self):
        self.expr_type = self.expr_list[-1].expr_type
