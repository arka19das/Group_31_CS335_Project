import code
import csv
from dataclasses import dataclass, field, fields
from pathlib import Path
from typing import Any, List, Union, Dict

offsets = {}
# offsets__with_table_name = {}
code_gen = []
contStack = []
brkStack = []
funcstack = []
table_name_to_num={}
table_name_to_num["#global"]=0


TYPE_FLOAT = ["FLOAT", "DOUBLE"]
TYPE_EASY = {
    "VOID": "VOID",
    "CHAR": "CHAR",
    "SHORT": "SHORT",
    "FLOAT": "FLOAT",
    "INT": "INT",
    "DOUBLE": "DOUBLE",
    "SHORT INT": "SHORT",
    "SIGNED CHAR": "CHAR",
    "SIGNED SHORT": "SHORT",
    "SIGNED SHORT INT": "SHORT",
    "SIGNED": "INT",
    "SIGNED INT": "INT",
    "UNSIGNED CHAR": "UNSIGNED CHAR",
    "UNSIGNED SHORT": "UNSIGNED SHORT",
    "UNSIGNED SHORT INT": "UNSIGNED SHORT",
    "UNSIGNED": "UNSIGNED INT",
    "UNSIGNED INT": "UNSIGNED INT",
}
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
    "SHORT INT": 2,
    "SIGNED CHAR": 1,
    "SIGNED SHORT": 2,
    "SIGNED SHORT INT": 2,
    "SIGNED": 4,
    "SIGNED INT": 4,
    "UNSIGNED CHAR": 1,
    "UNSIGNED SHORT": 2,
    "UNSIGNED SHORT INT": 2,
    "UNSIGNED": 4,
    "UNSIGNED INT": 4,
}

IGNORE_LIST = ["(", ")", "{", "}", "[", "]", ",", ";"]

ops_type = {
    # arithmetic operators
    "+": PRIMITIVE_TYPES,
    "-": PRIMITIVE_TYPES,
    "*": PRIMITIVE_TYPES,
    "/": PRIMITIVE_TYPES,
    "%": TYPE_INTEGER,
    # comparison operators
    ">": PRIMITIVE_TYPES,
    ">=": PRIMITIVE_TYPES,
    "<": PRIMITIVE_TYPES,
    "<=": PRIMITIVE_TYPES,
    "!=": PRIMITIVE_TYPES,
    "==": PRIMITIVE_TYPES,
    # bool operators
    "||": PRIMITIVE_TYPES,
    "&&": PRIMITIVE_TYPES,
    "!": PRIMITIVE_TYPES,
    # bits operators
    "<<": TYPE_INTEGER,
    ">>": TYPE_INTEGER,
    "|": TYPE_INTEGER,
    "&": TYPE_INTEGER,
    "~": TYPE_INTEGER,
    "^": TYPE_INTEGER,
}

TMP_VAR_COUNTER = 0
TMP_LABEL_COUNTER = 0
TMP_CLOSURE_COUNTER = 0


def backpatch():
    return


@dataclass
class Error:
    line_number: int
    rule_name: str = ""
    err_type: str = ""
    message: str = ""

    def __str__(self):
        message = self.err_type.upper()
        if self.line_number != -1:
            message += f" (at line {self.line_number})"
        message += ": " + self.message
        return message


@dataclass
class Node:
    name: str = ""
    val: Any = ""
    type: str = ""
    lno: int = 0
    size: int = 0
    children: List = field(default_factory=list)
    scope: int = 0
    array: List[int] = field(default_factory=list)
    max_depth: int = 0
    is_array: bool = False
    is_func: int = 0
    parentStruct: str = ""
    argument_list: Union[None, List[Any]] = None
    field_list: List = field(default_factory=list)
    level: int = 0
    place: str = ""
    code: str = ""
    # truelist: List = field(default_factory=list)
    # falselist: List = field(default_factory=list)
    continuelist: List = field(default_factory=list)
    breaklist: List = field(default_factory=list)
    # nextlist: List = field(default_factory=list)
    expr: List = field(default_factory=list)
    label: List = field(default_factory=list)
    index: str = ""
    offset: int = -1465465465  # TODO:default value for all nodes 0 or 1?
    lhs: int = 0
    addr: str = ""
    ast: Any = None
    in_whose_scope: str = ""

    def to_dict(self, verbose: bool = False):
        s = {}
        for field in fields(self):
            value = getattr(self, field.name)
            if verbose:
                s[field.name] = value
            else:
                if getattr(self, field.name) != field.default:
                    if field != "argument_list" and value == []:
                        continue
                    s[field.name] = value
        return s

    @property
    def base_type(self):
        if not self.type:
            return self.type
        # return self.type.split()[-1].upper()
        return self.type.upper()


@dataclass
class ScopeTable:
    name: str = ""
    nodes: list = field(default_factory=list)
    subscope_counter: Dict[str, int] = field(default_factory=dict)
    # in_whose_scope: int = 0
    offset_from_original: int = 0

    def find(self, key):
        for node in self.nodes:
            if node.name == key:
                return node
        return None

    def insert(self, node):
        node.in_whose_scope = self.name
        self.nodes.append(node)

    # def assign_in_whose_scope(self):
    # for node in self.nodes:
    # node.in_whose_scope = self.in_whose_scope


class SymbolTable:
    def __init__(self):
        self.curType = []
        self.curFuncReturnType = ""
        self.scope_tables: list[ScopeTable] = []
        self.currentScope = 0
        self.nextScope = 1
        self.parent = {}
        self.looping_depth = 0
        self.switch_depth = 0
        self.errors: list[Error] = []
        self.subscope_name = ""
        self.set()
        self.error_flag = 0

    def set(self):
        self.scope_tables.append(ScopeTable(name="#global"))
        self.parent[0] = 0

    def find(self, key):
        scope = self.currentScope
        node = self.scope_tables[scope].find(key)
        while node is None:
            scope = self.parent[scope]
            node = self.scope_tables[scope].find(key)
            if scope == 0:
                break
        return node

    def push_scope(self):
        self.parent[self.nextScope] = self.currentScope
        self.currentScope = self.nextScope
        self.nextScope = self.nextScope + 1
        value = self.parent_table.subscope_counter.get(self.subscope_name, 1)
        table_name = f"{self.parent_table.name}_{self.subscope_name}{value}"
        table_name_to_num[table_name]=ST.currentScope
        self.parent_table.subscope_counter[self.subscope_name] = value + 1
        self.scope_tables.append(
            ScopeTable(name=table_name)
            # in_whose_scope=self.parent_table.in_whose_scope)
        )

    def pop_scope(self):
        
        self.currentScope = self.parent[self.currentScope]
        
    @property
    def current_table(self):
        return self.scope_tables[self.currentScope]

    @property
    def parent_table(self):
        return self.scope_tables[self.parent[self.currentScope]]

    def error(self, err: Error):
        self.errors.append(err)

    def display_errors(self, verbose: bool = False):
        for err in self.errors:
            if err.err_type == "warning":
                print(err)
                if not verbose:
                    continue
            else:
                self.error_flag = 1
            print(str(err))

    def get_tmp_var(self, vartype=None, value=0) -> str:
        global TMP_VAR_COUNTER
        global offsets
        TMP_VAR_COUNTER += 1
        vname = f"__tmp_var_{TMP_VAR_COUNTER}"
        tmp_offset_string = ""
        if vartype is not None:
            scope = self.currentScope
            scope_table = self.scope_tables[scope]
            node = Node(
                name=vname,
                val=value,
                type=vartype,
                children=[],
                size=get_data_type_size(vartype),
                place=vname,
                offset=offsets[scope],
            )
            scope_table.insert(node)
            tmp_offset_string = f"{-offsets[scope]}($fp)"
            offsets[scope] += get_data_type_size(vartype)
            offsets[scope] += (4 - offsets[scope] % 4) % 4
            # symTab = get_current_symtab()
            # symTab.insert(
            #     {"name": vname, "type": vartype, "is_array": False, "dimensions": []}
            # )
        return vname, tmp_offset_string

    def get_tmp_closure(self, rettype: str, argtypes: list = []) -> str:
        global TMP_CLOSURE_COUNTER
        TMP_CLOSURE_COUNTER += 1
        vname = f"__tmp_closure_{TMP_VAR_COUNTER}"
        # TODO:incomplete and dont know yet where to use
        return vname

    def get_tmp_label(self) -> str:
        global TMP_LABEL_COUNTER
        TMP_LABEL_COUNTER += 1
        # return f"__tmp_label_{TMP_LABEL_COUNTER}"
        return f"__label_{TMP_LABEL_COUNTER}"

    def get_dummy(self) -> Node:
        dummy_var, dummy_offset_string = ST.get_tmp_var("int")
        scope_table = ST.current_table.name
        return Node(
            name="Dummy",
            val=dummy_var,
            place=dummy_var,
            lhs=1,
            in_whose_scope=scope_table,
            offset=-(int(dummy_offset_string[0:-5])),
        )

ST = SymbolTable()


def check_identifier(p, line):
    p_node = ST.find(p.val)
    if (p_node is not None) and ((p.is_func == 1) or ("struct" in p.type.split())):
        ST.error(
            Error(
                line,
                "Check Identifier",
                "compilation error",
                f"Invalid operation on {p.val}",
            )
        )


def type_util(op1: Node, op2: Node, op: str):
    # TODO: code_gen for type_conversion implicit
    rule_name = "type_util"
    dummy_var, dummy_offset_string = ST.get_tmp_var("int")
    scope_table = ST.scope_tables[ST.currentScope].name
    dummy_node = Node(
        name=op + "Operation",
        val=dummy_var,
        lno=op1.lno,
        type="",
        children=[],
        place=dummy_var,
        lhs=1,
        in_whose_scope=scope_table,
        offset=-(int(dummy_offset_string[0:-5])),
    )

    # Where are we using it @Martha ?
    if op1.type == "" or op2.type == "":
        dummy_node.type = "int"
        return dummy_node

    top1 = str(op1.type)
    top2 = str(op2.type)
    tp1 = op1.base_type
    tp2 = op2.base_type

    if op1.level > 0 and op2.level > 0:
        if op == "==" or op == "-" or op == "!=":
            if op1.level != op2.level:
                ST.error(
                    Error(
                        op1.lno,
                        rule_name,
                        "compilation error",
                        f"Invalid operation {op} on pointers of different levels",
                    )
                )
                # return dummy_node

            if op1.base_type != op2.base_type:
                ST.error(
                    Error(
                        op1.lno,
                        rule_name,
                        "compilation error",
                        f"Invalid operation {op} on pointers of different types",
                    )
                )
                # return dummy_node
        else:
            ST.error(
                Error(
                    op1.lno,
                    rule_name,
                    "compilation error",
                    f"Invalid operation {op} on pointers",
                )
            )
            # return dummy_node

        tmp_var, tmp_offset_string = ST.get_tmp_var(op1.type)
        scope_table = ST.scope_tables[ST.currentScope].name
        temp = Node(
            name=op + "Operation",
            val=tmp_var,
            lno=op1.lno,
            type=op1.type,
            level=op1.level,
            children=[],
            place=tmp_var,
            lhs=1,
            in_whose_scope=scope_table,
            offset=-(int(tmp_offset_string[0:-5])),
        )

    elif op1.level > 0 or op2.level > 0:
        if op1.level > 0 and tp2 in TYPE_FLOAT:
            ST.error(
                Error(
                    op1.lno,
                    rule_name,
                    "compilation error",
                    f"Incompatible data type {op} operator",
                )
            )
            return dummy_node
        elif op1.level > 0:
            if op not in ["+", "-"]:
                ST.error(
                    Error(
                        op1.lno,
                        rule_name,
                        "compilation error",
                        f"Invalid operation {op} on pointers",
                    )
                )
                return dummy_node

            tmp_var, tmp_offset_string = ST.get_tmp_var(op1.type)
            scope_table = ST.scope_tables[ST.currentScope].name
            temp = Node(
                name=op + "Operation",
                val=tmp_var,
                lno=op1.lno,
                type=op1.type,
                level=op1.level,
                children=[],
                place=tmp_var,
                lhs=1,
                in_whose_scope=scope_table,
                offset=-(int(tmp_offset_string[0:-5])),
            )

        elif op2.level > 0 and tp1 in TYPE_FLOAT:
            ST.error(
                Error(
                    op1.lno,
                    rule_name,
                    "compilation error",
                    f"Incompatible data type {op} operator",
                )
            )
            return dummy_node

        elif op2.level > 0:
            if op not in ["+", "-"]:
                ST.error(
                    Error(
                        op1.lno,
                        rule_name,
                        "compilation error",
                        f"Invalid operation {op} on pointers",
                    )
                )
                return dummy_node
            tmp_var, tmp_offset_string = ST.get_tmp_var(op2.type)
            scope_table = ST.scope_tables[ST.currentScope].name
            temp = Node(
                name=op + "Operation",
                val=tmp_var,
                lno=op1.lno,
                type=op2.type,
                level=op2.level,
                children=[],
                place=tmp_var,
                lhs=1,
                in_whose_scope=scope_table,
                offset=-(int(tmp_offset_string[0:-5])),
            )

    elif top1.startswith("struct") or top2.startswith("struct"):

        ST.error(
            Error(
                op1.lno,
                rule_name,
                "compilation error",
                f"Incompatible data type {op} operator",
            )
        )

        # typ = op1.type if top1.startswith("struct") else op2.type
        # temp.type = typ
        return dummy_node

    else:
        temp_1 = op1.type.split(" ")
        temp_2 = op2.type.split(" ")
        tp1 = ""
        tp2 = ""
        for i in range(len(temp_1)):
            if temp_1[i] == "*":
                break
            tp1 += temp_1[i].upper()
            tp1 += " "

        for i in range(len(temp_2)):
            if temp_2[i] == "*":
                break
            tp2 += temp_2[i].upper()
            tp2 += " "

        tp1 = tp1[:-1]
        tp2 = tp2[:-1]
        op_type = op1.type
        if tp1 not in ops_type[op] or tp2 not in ops_type[op]:
            ST.error(
                Error(
                    op1.lno,
                    rule_name,
                    "compilation error",
                    f"Incompatible data type {op} operator",
                )
            )
            return dummy_node

        else:
            size1 = SIZE_OF_TYPE[tp1]
            size2 = SIZE_OF_TYPE[tp2]
            if size1 > size2:
                ST.error(
                    Error(
                        op1.lno,
                        rule_name,
                        "warning",
                        f"Implicit type casting of {op2.val}",
                    )
                )

            elif size2 > size1:
                ST.error(
                    Error(
                        op1.lno,
                        rule_name,
                        "warning",
                        f"Implicit type casting of {op1.val}",
                    )
                )
                op_type = op2.type
            else:
                if tp1 == "FLOAT" or tp2 == "FLOAT":
                    op_type = "float"
                elif tp1 == "DOUBLE" or tp2 == "DOUBLE":
                    op_type = "float"
                elif top1.startswith("unsigned"):
                    op_type = op1.type
                else:
                    op_type = op2.type

            if op_type == "char":
                op_type = "int"

            tmp_var, tmp_offset_string = ST.get_tmp_var(op_type)
            scope_table = ST.scope_tables[ST.currentScope].name
            temp = Node(
                name=op + "Operation",
                val=tmp_var,
                lno=op1.lno,
                type=op_type,
                level=0,
                children=[],
                place=tmp_var,
                lhs=1,
                in_whose_scope=scope_table,
                offset=-(int(tmp_offset_string[0:-5])),
            )

    p_node = ST.find(op1.val)
    if (p_node is not None) and (op1.is_func == 1):
        ST.error(
            Error(
                op1.lno,
                "Check Identifier",
                "compilation error",
                f"Invalid operation on {op1.val}",
            )
        )
        return dummy_node
    p_node = ST.find(op2.val)
    if (p_node is not None) and (op2.is_func == 1):
        ST.error(
            Error(
                op2.lno,
                "Check Identifier",
                "compilation error",
                f"Invalid operation on {op2.val}",
            )
        )
        return dummy_node
    return temp


def get_data_type_size(type_1):
    # DONE: error because it is focusing on  the last word only
    if type_1.endswith("*"):
        return 4
    if type_1.startswith("struct"):
        node = ST.find(type_1)
        if node is None:
            return -1
        return ST.find(type_1).size
    # base_type = type_1.split()[-1].upper()
    base_type = type_1.upper().strip(" ")
    return SIZE_OF_TYPE.get(base_type, -1)


def ignore_char(ch):
    return ch in IGNORE_LIST


def remove_redundant_label(code_gen):
    map_label_parent = {}
    for i in range(len(code_gen)):
        if code_gen[i][0] == "label":
            if i == 0 or code_gen[i - 1][0] != "label":
                map_label_parent[code_gen[i][1]] = code_gen[i][1]
            else:
                map_label_parent[code_gen[i][1]] = map_label_parent[code_gen[i - 1][1]]
    for i in range(len(code_gen)):
        for j in range(len(code_gen[i])):
            if code_gen[i][j].startswith("__label"):
                code_gen[i][j] = map_label_parent[code_gen[i][j]]
    return


def write_code(code, file):
    # file = open("3ac.txt", "w")

    # Saving the array in a text file
    for i in range(len(code)):
        # if i > 0 and code[i - 1][0] == "label" and code[i][0] == "label":
        #     continue
        each_line = code[i]
        if each_line[0] != "label":
            file.write("\t")
            for words in each_line:
                file.write(str(words) + "\t")
        else:
            file.write(each_line[1] + "\t" + each_line[2])
        file.write("\n")
    file.close()


def write_mips(code, file):
    for line in code:
        if line[0] != "label":
            file.write(f"\t\t{line[0].lower()}\t")
            args = [arg for arg in line[1:] if arg]
            file.write(",".join(args))
        else:
            file.write(line[1] + line[2]) 
        file.write("\n")
    file.close()


def dump_symbol_table_csv(verbose: bool = False):
    if ST.error_flag:
        return
    node_fields = fields(Node)
    fieldnames = [field.name for field in node_fields]
    filenames = set()

    csv_base_dir = Path("./symbol_table_dump")
    csv_base_dir.mkdir(exist_ok=True)
    for csvfile in csv_base_dir.iterdir():
        csvfile.unlink()

    for scope_table in ST.scope_tables:
        # if not scope_table.nodes:
        #     continue
        name = scope_table.name
        # if not verbose:
        # name = name.split("_")[0]
        with open(csv_base_dir / f"{name}.csv", "a") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if name not in filenames:
                writer.writeheader()
                filenames.add(name)

            for node in scope_table.nodes:
                writer.writerow(node.to_dict(True))


node1 = Node(
    name="printf",
    type="int",
    val="",
    is_func=1,
    argument_list=["int"],
    lno=-1,
    in_whose_scope="#global",
)
node2 = Node(
    name="scanf",
    type="int",
    val="",
    is_func=1,
    argument_list=["int"],
    lno=-1,
    in_whose_scope="#global",
)
node3 = Node(
    name="malloc",
    type="void *",
    val="",
    is_func=1,
    argument_list=["int"],
    lno=-1,
    in_whose_scope="#global",
)
node4 = Node(
    name="sqrt",
    type="float",
    val="",
    is_func=1,
    argument_list=["int"],
    lno=-1,
    in_whose_scope="#global",
)
node5 = Node(
    name="pow",
    type="float",
    val="",
    is_func=1,
    argument_list=["int"],
    lno=-1,
    in_whose_scope="#global",
)
node6 = Node(
    name="abs",
    type="float",
    val="",
    is_func=1,
    argument_list=["int"],
    lno=-1,
    in_whose_scope="#global",
)
node7 = Node(name="NULL", type="void *", val="0", lno=-1, in_whose_scope="#global")


pre_append_array = [node1, node2, node3, node4, node5, node6, node7]


def pre_append_to_table():
    for node in pre_append_array:
        ST.scope_tables[0].insert(node)
