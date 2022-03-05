from typing import List, Union, Tuple

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
    "CHAR": 4,  # Char is not 4 bytes, but this allows us to support all
    # unicode characters and also prevents potential alignment
    # issues
    "SIGNED CHAR": 4,
    "UNSIGNED CHAR": 4,
    "SHORT": 2,
    "SHORT INT": 2,
    "SIGNED SHORT": 2,
    "SIGNED SHORT INT": 2,
    "UNSIGNED SHORT": 2,
    "UNSIGNED SHORT INT": 2,
    "INT": 4,
    "SIGNED INT": 4,
    "UNSIGNED INT": 4,
    "SIGNED": 4,
    "UNSIGNED": 4,
    "LONG": 8,
    "LONG INT": 8,
    "SIGNED LONG INT": 8,
    "SIGNED LONG": 8,
    "UNSIGNED LONG": 8,
    "UNSIGNED LONG INT": 8,
    "LONG LONG": 8,
    "LONG LONG INT": 8,
    "SIGNED LONG LONG": 8,
    "SIGNED LONG LONG INT": 8,
    "UNSIGNED LONG LONG": 8,
    "UNSIGNED LONG LONG INT": 8,
    "FLOAT": 4,
    "DOUBLE": 8,
    "LONG DOUBLE": 16,
}

#pointer not being handled 
# Variables (0-V) -> {"name", "type", "datatype", "value", "is_array", "dims", "pointer_lvl"}
# Functions (1-F) -> {"name", "type", "ret_type", "param_types"}
# Structs (2-S)   -> {"name", "type", "alt name" (via typedef), "field names", "field types"}
# Classes (3-C)   -> {"name", "type",... TBD}
# Labels (4-L)    -> {"name"}
class SymbolTableBase:
    def __init__(self, parent=None, function_scope=None) -> None:
        # self.table = {}
        
        self._custom_types = dict()
        self._parameters=[]
        self._table = dict()
        self.function_scope = function_scope
        if self.parent is not None:
            self.parent.children.append(self)
        self.children = []
        if parent is None:
            self.table_name = "GLOBAL"
        else:
            self.table_name = f"BLOCK_{self.table_number}"  ### error since i wanna try something different than other
    def _get_proper_name(entry: dict, type: int = 0):
        if type == 1:
            return entry["name"] + "(" + ",".join(entry["param_types"]) + ")"
        else:
            return entry["name"]
    def _lookUpCurrtable(self, name: str, paramtab_check: bool, type: int = 0) -> Union[None, list, dict]:
        if name in self.table.keys():
            return self.table["name"]
        elif paramtab_check and (name in self._parameters):
            return self._parameters["name"]
        return None
    def lookUptables(self, name: str, paramtab_check: bool, type: int = 0)-> Union[None, list, dict]:
        ans=self._lookUpCurrtable(name,paramtab_check, type)
        if ans:
            return ans 
        elif self.parent:
            ans=self.parent._lookUptables(name,paramtab_check, type)
        else:
            return None
    def update(self, name: str, value) -> bool:
        res=lookUpTables(name,paramtab_check)
        if res:
            #TODO: check if value conforms to datatype
            #TODO: not done yet
            res["value"] = value
            return True
        else:
            raise Exception(f"{name} is not defined in SymbolTables")
    def insert(self, entry, type: int,is_param_tab_check=False ):
        name=self._get_proper_name(entry,type)
        res=self.lookUptables(name,paramtab_check=is_param_tab_check)
        if res:
            print(f"already present {name}")
            return false,res
        entry["type"]=type
        # entry["pointr_lvl"]=entry.get("pointer_lvl",0)
        if type>4:
            raise Exception("{name} is of {type} which is unidentified")
        if type==0:
            if not self.check_type(entry["datatype"]):
                raise Exception(f"{entry['datatype']} is not valid datatype")
            if entry["is_array"]:
                pass
            entry["table_name"]=self.table_name
            self._table[name]=entry
            if param:
                self._param_tab
        elif type==1:
            pass
        elif type==2:
            pass
        elif type==3:
            pass
        elif type==4:
            pass
        
        
        

class Parser:
    def __init__(self):
        self.ERROR_MESSAGES = []
        self.WARNING_MESSAGES = []

        self.SYMBOL_TABLES = []
        self.globalsymbol_table = SymbolTableBase()
        self.SYMBOL_TABLES.append(self.globalsymbol_table)
        currentscope_table = 0

    def pop_scope(self) -> None:
        # global currentsymbol_table

        self.SYMBOL_TABLES.pop()
        # currentscope_table -= 1
        return

    def push_scope(self, parent=None, function_scope=None) -> None:
        # global currentscope_table
        symtab = SymbolTableBase(parent, function_scope)

        self.SYMBOL_TABLES.push(symtab)
        return

    def getCurrSymbolTable(self) -> Union[None, SymbolTableBase]:
        return self.SYMBOL_TABLES[-1]

    def error(self, err):
        self.ERROR_MESSAGES.append(err)
        return err

    def warn(self, err):
        self.WARNING_MESSAGES.append(err)
        return err

    def type_conversion(self, converted_from, converted_to):
        if converted_from == converted_to:
            return converted_from
        if (converted_from not in PRIMITIVE_TYPES) or (
            converted_to not in PRIMITIVE_TYPES
        ):
            self.error(
                f"ERROR not in primitive types {converted_from}  or {converted_to}"
            )
            return None
        if (
            converted_from in TYPE_FLOAT and converted_to not in TYPE_FLOAT
        ) or SIZE_OF_TYPE(converted_from) > SIZE_OF_TYPE(converted_from):
            self.warn(f"EXPLICIT type conversion posssible loss in data")
        return converted_to

    def final_type(var1, var2):
        type1 = var1["type"]
        type2 = var2["type"]
        if type1 == type2:
            return type2
        if (type1 not in PRIMITIVE_TYPES) or (type2 not in PRIMITIVE_TYPES):
            self.error(f"ERROR not in primitive types {type1}  or {type2}")
            return None
        if type1.count("*") != type2.count("*"):
            self.err()
 
