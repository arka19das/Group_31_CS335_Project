import csv
from dataclasses import dataclass, field, fields
from pathlib import Path
from typing import Any, List, Union, Dict

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
    is_func: int = 0
    parentStruct: str = ""
    argument_list: Union[None, List[Any]] = None
    field_list: List = field(default_factory=list)
    level: int = 0
    ast: Any = None

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
        return self.type.split()[-1].upper()


@dataclass
class ScopeTable:
    name: str = ""
    nodes: list = field(default_factory=list)
    subscope_counter: Dict[str, int] = field(default_factory=dict)

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
        self.curFuncReturnType = ""
        self.scope_tables: list[ScopeTable] = []
        self.currentScope = 0
        self.nextScope = 1
        self.parent = {}
        self.looping_depth = 0
        self.switch_depth = 0
        self.errors: list[Error] = []
        self.subscope_name = ''
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

        value = self.parent_table.subscope_counter.get(
            self.subscope_name, 1)
        table_name = f"{self.parent_table.name}_{self.subscope_name}{value}"
        self.parent_table.subscope_counter[self.subscope_name] = value + 1
        self.scope_tables.append(ScopeTable(name=table_name))

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
            if err.err_type == "warning" and not verbose:
                continue
            self.error_flag = 1
            print(str(err))


ST = SymbolTable()


def check_identifier(p):
    p_node = ST.find(p.val)
    if (p_node is not None) and (
        (p.is_func == 1) or ("struct" in p.type.split())
    ):
        ST.error(
            Error(
                p[1].lno,
                'Check Identifier',
                "compilation error",
                f"Invalid operation on {p.val}",
            )
        )


def type_util(op1: Node, op2: Node, op: str):
    rule_name = "type_util"
    temp = Node(
        name=op + "Operation",
        val=op1.val + op + op2.val,
        lno=op1.lno,
        type="int",
        children=[],
    )
    if op1.type == "" or op2.type == "":
        temp.type = "int"  # default
        return temp
    top1 = str(op1.type)
    top2 = str(op2.type)
    tp1 = op1.base_type
    tp2 = op2.base_type

    if top1.endswith("*") and top2.endswith("*"):
        ST.error(
            Error(
                -1,
                rule_name,
                "compilation error",
                "Cannot cast pointer to pointer",
            )
        )
        temp.type = op1.type
        # temp.level = op1.level
    elif top1.endswith("*") or top2.endswith("*"):
        # MODIFIED
        if top1.endswith("*") and tp2 in TYPE_FLOAT:
            ST.error(
                Error(
                    -1,
                    rule_name,
                    "compilation error",
                    f"Incompatible data type {op} operator",
                )
            )
            temp.type = op1.type
            temp.level = op1.level
        elif top1.endswith("*"):
            temp.type = op1.type
            temp.level = op1.level
        elif top2.endswith("*") and tp1 in TYPE_FLOAT:
            ST.error(
                Error(
                    -1,
                    rule_name,
                    "compilation error",
                    f"Incompatible data type {op} operator",
                )
            )
            temp.type = op2.type
            temp.level = op2.level
        elif top2.endswith("*"):
            temp.type = op2.type
            temp.level = op2.level

    else:
        if tp1 not in ops_type[op] or tp2 not in ops_type[op]:
            ST.error(
                Error(
                    -1,
                    rule_name,
                    "compilation error",
                    f"Incompatible data type {op} operator",
                )
            )

        size1 = SIZE_OF_TYPE[tp1]
        size2 = SIZE_OF_TYPE[tp2]
        if size1 > size2:
            ST.error(
                Error(
                    -1,
                    rule_name,
                    "warning",
                    f"Implicit type casting of {op2.val}",
                )
            )
            temp.type = op1.type
        elif size2 > size1:
            ST.error(
                Error(
                    -1,
                    rule_name,
                    "warning",
                    f"Implicit type casting of {op1.val}",
                )
            )
            temp.type = op2.type
        else:
            if tp1 == "FLOAT" or tp2 == "FLOAT":
                temp.type = "float"
            elif tp1 == "DOUBLE" or tp2 == "DOUBLE":
                temp.type = "float"
            elif top1.startswith("unsigned"):
                temp.type = op1.type
            else:
                temp.type = op2.type

    if temp.type == "char":
        temp.type = "int"

    if op in ["*", "-", "%"]:
        temp.val = op1.val

    check_identifier(op1)
    check_identifier(op2)
    return temp


def get_data_type_size(type_1):

    if type_1.endswith("*"):
        return 8
    if type_1.startswith("struct"):
        node = ST.find(type_1)
        if node is None:
            return -1
        return ST.find(type_1).size

    base_type = type_1.split()[-1].upper()
    return SIZE_OF_TYPE.get(base_type, -1)


def ignore_char(ch):
    return ch in IGNORE_LIST


def dump_symbol_table_csv(verbose: bool = False):
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
        if not verbose:
            name = name.split("_")[0]
        with open(csv_base_dir / f"{name}.csv", "a") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if name not in filenames:
                writer.writeheader()
                filenames.add(name)

            for node in scope_table.nodes:
                writer.writerow(node.to_dict(True))
