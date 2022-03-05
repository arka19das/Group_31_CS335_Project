
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
            # parser.error = c_error[-1]
            # parser_error()
            return

        scope.variables[name] = mdata

    def add_struct(self, name, mdata):
        scope = self.table_scope()
        if scope.lookup_struct(name):
            c_error.append('Redeclaration of struct named {}'.format(name))
            # parser.error = c_error[-1]
            # parser_error()
            return

        scope.structs[name] = mdata

    def add_typedef(self, alias, actual):
        scope = self.table_scope()
        lookup_alias = scope.lookup_alias(alias)
        if lookup_alias is None:
            scope.typedef[alias] = actual
        elif lookup_alias != actual:
            c_error.append('Redeclaration of type/alias named {}'.format(alias))
            # parser.error = c_error[-1]
            # parser_error()
        return
        
    def add_function(self, name, mdata):
        scope = self.table_scope()
        if name in scope.functions:
            _func = scope.functions[name]
            if _func.ret_type == mdata.ret_type and _func.args == mdata.args:
                return
            c_error.append('Redeclaration of function named {}'.format(name))
            # parser.error = c_error[-1]
            # parser_error()
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