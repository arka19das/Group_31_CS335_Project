from dis import code_info
from utils import *

comment_variable = ";"
error_variable = "----------error----------\n"


def data_section():
    print(".data")


def text_section():
    print(".text")


def is_int(x):
    try:
        if x == str(int(x)):
            return True
        else:
            return False
    except:
        return False


def is_char(x):
    if x[0] == "'" and x[-1] == "'":
        return True
    return False


def is_num(x):
    #TODO Has to modify
    return x.isdigit() or '.' in x
    # try:
    #     if s.isnumeric():
    #         return True
    # except:
    #     return False


# print(is_int("140"))

LABEL_COUNTER = 0


def get_mips_label() -> str:
    global LABEL_COUNTER
    LABEL_COUNTER += 1
    # return f"__tmp_label_{TMP_LABEL_COUNTER}"
    return f".__labelm_{LABEL_COUNTER}"


TYPE_INTEGER = [
    "char",
    "unsigned char",
    "short",
    "unsigned short",
    "int",
    "unsigned int",
    "long",
    "unsigned long",
]

TYPE_FLOAT = ["float", "double"]

BIN_BIT_OP = ["&", "|", "<<", ">>", "^"]

STORE_INSTRUCTIONS = {
    "char": "SW",
    "int": "SW",
    "short": "SH",
    "void": "SW",
    "long": "SD",
    "float": "SWC1",
    "double": "SDC1",
    "unsigned char": "SW",
    "unsigned int": "SW",
    "unsigned short": "SH",
    "unsigned long": "SD",
}

LOAD_INSTRUCTIONS = {
    "char": "LW",
    "int": "LW",
    "short": "LH",
    "void": "LW",
    "long": "LD",
    "float": "LWC1",
    "double": "LDC1",
    "unsigned char": "LWU",
    "unsigned int": "LWU",
    "unsigned short": "LHU",
    "unsigned long": "LD",
}


Binary_ops = {
    # UNSIGNED INT
    "unsigned int+": ["ADDU", 4],
    "unsigned int-": ["SUBU", 4],
    "unsigned int*": ["MULTU", 4],
    "unsigned int/": ["DIVU", 4],
    "unsigned int%": ["DIVU", 4],
    "unsigned int<=": ["SLTU", 4],
    "unsigned int<": ["SLTU", 4],
    "unsigned int>=": ["SLTU", 4],
    "unsigned int>": ["SLTU", 4],
    "unsigned int==": ["XOR", 4],
    "unsigned int!=": ["XOR", 4],
    "unsigned int&": ["AND", 4],
    "unsigned int^": ["XOR", 4],
    "unsigned int|": ["OR", 4],
    "unsigned int~": ["XORI", 4],
    "unsigned int<<": ["SLLV", 4],
    "unsigned int>>": ["SRLV", 4],
    "unsigned int!": ["SLTUI", 4],
    "unsigned int&&": ["AND", 4],
    "unsigned int||": ["OR", 4],
    # INT
    "int+": ["ADD", 4],
    "int-": ["SUB", 4],
    "int*": ["MULT", 4],
    "int/": ["DIV", 4],
    "int%": ["DIV", 4],
    "int<=": ["SLT", 4],
    "int<": ["SLT", 4],
    "int>=": ["SLT", 4],
    "int>": ["SLT", 4],
    "int==": ["XOR", 4],
    "int!=": ["XOR", 4],
    "int&": ["AND", 4],
    "int^": ["XOR", 4],
    "int|": ["OR", 4],
    "int~": ["XORI", 4],
    "int<<": ["SLLV", 4],
    "int>>": ["SRLV", 4],
    "int!": ["SLTUI", 4],
    "int||": ["OR", 4],
    "int&&": ["AND", 4],
    # SHORT
    "short+": ["ADD", 2],
    "short-": ["SUB", 2],
    "short*": ["MULT", 2],
    "short/": ["DIV", 2],
    "short%": ["DIV", 2],
    "short<=": ["SLT", 2],
    "short<": ["SLT", 2],
    "short>=": ["SLT", 2],
    "short>": ["SLT", 2],
    "short==": ["XOR", 2],
    "short!=": ["XOR", 4],
    "short&": ["AND", 2],
    "short^": ["XOR", 2],
    "short|": ["OR", 2],
    "short~": ["XORI", 2],
    "short<<": ["SLLV", 2],
    "short>>": ["SRLV", 2],
    "short!": ["SLTI", 2],
    "short&&": ["AND", 2],
    "short||": ["OR", 2],
    # UNSIGNED SHORT
    "unsigned short+": ["ADDU", 2],
    "unsigned short-": ["SUBU", 2],
    "unsigned short*": ["MULTU", 2],
    "unsigned short/": ["DIVU", 2],
    "unsigned short%": ["DIVU", 2],
    "unsigned short<=": ["SLTU", 2],
    "unsigned short<": ["SLTU", 2],
    "unsigned short>=": ["SLTU", 2],
    "unsigned short>": ["SLTU", 2],
    "unsigned short==": ["XOR", 2],
    "unsigned short!=": ["XOR", 2],
    "unsigned short&": ["AND", 2],
    "unsigned short^": ["XOR", 2],
    "unsigned short|": ["OR", 2],
    "unsigned short~": ["XOR", 2],
    "unsigned short<<": ["SLLV", 2],
    "unsigned short>>": ["SRLV", 2],
    "unsigned short!": ["SLTUI", 2],
    "unsigned short||": ["OR", 2],
    "unsigned short&&": ["AND", 2],
    # UNSIGNED CHAR
    "unsigned char+": ["ADDU", 4],
    "unsigned char-": ["SUBU", 4],
    "unsigned char*": ["MULTU", 4],
    "unsigned char/": ["DIVU", 4],
    "unsigned char%": ["DIVU", 4],
    "unsigned char<=": ["SLTU", 4],
    "unsigned char<": ["SLTU", 4],
    "unsigned char>=": ["SLTU", 4],
    "unsigned char>": ["SLTU", 4],
    "unsigned char==": ["XOR", 4],
    "unsigned char!=": ["XOR", 4],
    "unsigned char&": ["AND", 4],
    "unsigned char^": ["XOR", 4],
    "unsigned char|": ["OR", 4],
    "unsigned char~": ["XOR", 4],
    "unsigned char<<": ["SLLV", 4],
    "unsigned char>>": ["SRLV", 4],
    "unsigned char!": ["SLTUI", 4],
    "unsigned char||": ["OR", 4],
    "unsigned char&&": ["AND", 4],
    # CHAR
    "char+": ["ADD", 4],
    "char-": ["SUB", 4],
    "char*": ["MULT", 4],
    "char/": ["DIV", 4],
    "char%": ["DIV", 4],
    "char<=": ["SLT", 4],
    "char<": ["SLT", 4],
    "char>=": ["SLT", 4],
    "char>": ["SLT", 4],
    "char==": ["XOR", 4],
    "char!=": ["XOR", 4],
    "char&": ["AND", 4],
    "char^": ["XOR", 4],
    "char|": ["OR", 4],
    "char~": ["XORI", 4],
    "char>>": ["SRLV", 4],
    "char<<": ["SLLV", 4],
    "char!": ["SLTUI", 4],
    "char&&": ["AND", 4],
    "char||": ["OR", 4],
    # UNSIGNED LONG
    "unsigned long+": ["DADDU", 8],
    "unsigned long-": ["DSUBU", 8],
    "unsigned long*": ["DMULTU", 8],
    "unsigned long/": ["DDIVU", 8],
    "unsigned long%": ["DDIVU", 8],
    "unsigned long<=": ["SLTU", 8],
    "unsigned long<": ["SLTU", 8],
    "unsigned long>=": ["SLTU", 8],
    "unsigned long>": ["SLTU", 8],
    "unsigned long==": ["XOR", 8],
    "unsigned long!=": ["XOR", 8],
    "unsigned long&": ["AND", 8],
    "unsigned long^": ["XOR", 8],
    "unsigned long|": ["OR", 8],
    "unsigned long~": ["XORI", 8],
    "unsigned long>>": ["DSRLV", 8],
    "unsigned long<<": ["DSLLV", 8],
    "unsigned long!": ["SLTUI", 8],
    "unsigned long&&": ["AND", 8],
    "unsigned long||": ["OR", 8],
    # LONG
    "long+": ["DADD", 8],
    "long-": ["DSUB", 8],
    "long*": ["DMULT", 8],
    "long/": ["DDIV", 8],
    "long%": ["DDIV", 8],
    "long<=": ["SLT", 8],
    "long<": ["SLT", 8],
    "long>=": ["SLT", 8],
    "long>": ["SLT", 8],
    "long==": ["XOR", 8],
    "long!=": ["XOR", 8],
    "long&": ["AND", 8],
    "long^": ["XOR", 8],
    "long|": ["OR", 8],
    "long<<": ["DSLLV", 8],
    "long>>": ["DSRLV", 8],
    "long~": ["XORI", 8],
    "long!": ["SLTUI", 8],
    "long||": ["OR", 8],
    "long&&": ["AND", 8],
    "double+": ["ADD.D", 8],
    "double-": ["SUB.D", 8],
    "double*": ["MUL.D", 8],
    "double/": ["DIV.D", 8],
    "double<=": ["C.LT.D", 8],
    "double<": ["C.LT.D", 8],
    "double>=": ["C.LT.D", 8],
    "double>": ["C.LT.D", 8],
    "double==": ["C.EQ.D", 8],
    "double!=": ["C.EQ.D", 8],
    # FLOAT
    "float+": ["ADD.D", 4],
    "float-": ["SUB.D", 4],
    "float*": ["MUL.D", 4],
    "float/": ["DIV.D", 4],
    "float<=": ["C.LT.D", 4],
    "float<": ["C.LT.D", 4],
    "float>=": ["C.LT.D", 4],
    "float>": ["C.LT.D", 4],
    "float==": ["C.EQ.D", 4],
    "float!=": ["C.EQ.D", 4],
}

# Handled type_int
# TODO Type_float ,relational operators
def binary_exp_mips(binexp, reg1, a1, reg2, a2, reg3, a3):
    mips = []
    type = ""
    op = ""
    for i in binexp:
        if i.isalpha() or i == " ":
            type += i
        else:
            op += i
    print(type, op)
    # mips.append(load_reg(reg1, a1, type))
    mips.append(load_reg(reg2, a2, type))
    mips.append(load_reg(reg3, a3, type))
    if (op == "+" or op == "-") and type in TYPE_INTEGER:
        op = Binary_ops[binexp][0]
        mips.append([op, reg1, reg2, reg3])
    elif op == "*" and type in TYPE_INTEGER:
        op = Binary_ops[binexp][0]
        mips.append([op, reg2, reg3])
        mips.append(["MFLO  ", reg1])
    elif op == "/" and type in TYPE_INTEGER:
        op = Binary_ops[binexp][0]
        mips.append([op, reg2, reg3])
        mips.append(["MFLO", reg1])
    elif op == "%" and type in TYPE_INTEGER:
        op = Binary_ops[binexp][0]
        mips.append([op, reg2, reg3])
        mips.append(["MFHI", reg1])
    elif op in BIN_BIT_OP and type in TYPE_INTEGER:
        op = Binary_ops[binexp][0]
        mips.append([op, reg1, reg2, reg3])
    elif op == "~" and type in TYPE_INTEGER:
        # only 2 regs will be given
        op = Binary_ops[binexp][0]
        mips.append([op, reg1, reg2, "0xffffffffffffffff"])
    elif op == "<" and type in TYPE_INTEGER:
        op = Binary_ops[binexp][0]
        mips.append([op, reg1, reg2, reg3])
    elif op == ">" and type in TYPE_INTEGER:
        op = Binary_ops[binexp][0]
        mips.append([op, reg1, reg3, reg2])
    elif op == "<=" and type in TYPE_INTEGER:
        op = Binary_ops[binexp][0]
        # check greater than and xor with 1
        mips.append([op, reg1, reg3, reg2])
        mips.append(["XORI", reg1, reg1, "0x1"])
    elif op == ">=" and type in TYPE_INTEGER:
        op = Binary_ops[binexp][0]
        # check less than and xor with 1
        mips.append([op, reg1, reg2, reg3])
        mips.append(["XORI", reg1, reg1, "0x1"])
    elif op == "==" and type in TYPE_INTEGER:
        op = Binary_ops[binexp][0]
        mips.append([op, reg1, reg2, reg3])
        mips.append(["SLTUI", reg1, reg1, "1"])
    elif op == "!=" and type in TYPE_INTEGER:
        op = Binary_ops[binexp][0]
        mips.append([op, reg1, reg2, reg3])
        mips.append(["SLTU", reg1, "$0", reg1])
    elif (op == "&&" or op == "||") and type in TYPE_INTEGER:
        op = Binary_ops[binexp][0]
        mips.append([op, reg1, reg2, reg3])
    elif op == "!" and type in TYPE_INTEGER:
        op = Binary_ops[binexp][0]
        mips.append([op, reg1, reg1, "1"])
    # only 2 registers case, constants case not handled
    elif (op == "+" or op == "-" or op == "/" or op == "*") and type in TYPE_FLOAT:
        op = Binary_ops[binexp][0]
        mips.append([op, reg1, reg2, reg3])
    elif op == "<" and type in TYPE_FLOAT:
        op = Binary_ops[binexp][0]
        mips.append([op, "2", reg2, reg3])
        l0 = get_mips_label()
        mips.append(["BC1F", "2", l0])
        mips.append(["ADDI", reg1, "$0", "1"])
        l1 = get_mips_label()
        mips.append(["J", l1])
        mips.append([f"{l0}:"])
        mips.append(["XOR", reg1, reg1, reg1])
        mips.append([f"{l1}:"])
    elif op == ">" and type in TYPE_FLOAT:
        op = Binary_ops[binexp][0]
        mips.append([op, "2", reg3, reg2])
        l0 = get_mips_label()
        mips.append(["BC1F", "2", l0])
        mips.append(["ADDI", reg1, "$0", "1"])
        l1 = get_mips_label()
        mips.append(["J", l1])
        mips.append([f"{l0}:"])
        mips.append(["XOR", reg1, reg1, reg1])
        mips.append([f"{l1}:"])
    elif op == ">=" and type in TYPE_FLOAT:
        op = Binary_ops[binexp][0]
        mips.append([op, "2", reg2, reg3])
        l0 = get_mips_label()
        mips.append(["BC1F", "2", l0])
        mips.append(["XOR", reg1, reg1, reg1])
        l1 = get_mips_label()
        mips.append(["J", l1])
        mips.append([f"{l0}:"])
        mips.append(["ADDI", reg1, "$0", "1"])
        mips.append([f"{l1}:"])
    elif op == "<=" and type in TYPE_FLOAT:
        op = Binary_ops[binexp][0]
        mips.append([op, "2", reg3, reg2])
        l0 = get_mips_label()
        mips.append(["BC1F", "2", l0])
        mips.append(["XOR", reg1, reg1, reg1])
        l1 = get_mips_label()
        mips.append(["J", l1])
        mips.append([f"{l0}:"])
        mips.append(["ADDI", reg1, "$0", "1"])
        mips.append([f"{l1}:"])
    elif op == "!=" and type in TYPE_FLOAT:
        op = Binary_ops[binexp][0]
        mips.append([op, "7", reg2, reg3])
        l0 = get_mips_label()
        mips.append(["BC1F", "7", l0])
        mips.append(["XOR", reg1, reg1, reg1])
        l1 = get_mips_label()
        mips.append(["J", l1])
        mips.append([f"{l0}:"])
        mips.append(["ADDI", reg1, "$0", "1"])
        mips.append([f"{l1}:"])
    elif op == "==" and type in TYPE_FLOAT:
        op = Binary_ops[binexp][0]
        mips.append([op, "7", reg2, reg3])
        l0 = get_mips_label()
        mips.append(["BC1F", "7", l0])
        mips.append(["ADDI", reg1, "$0", "1"])
        l1 = get_mips_label()
        mips.append(["J", l1])
        mips.append([f"{l0}:"])
        mips.append(["XOR", reg1, reg1, reg1])
        mips.append([f"{l1}:"])
    # elif op == "*=" and type in TYPE_INTEGER:

    mips.append(store_reg(reg1, a1, type))
    return mips


def LI(reg, const, type):
    if type == "int" or type == "char" or type == "short":
        mips = ["ADDI", reg, "$0", const]
        return mips
    elif type == "long":
        mips = ["DADDI", reg, "$0", const]
        return mips
    elif type == "unsigned int" or type == "unsigned char" or type == "unsigned short":
        mips = ["ADDIU", reg, "$0", const]
        return mips
    elif type == "unsigned long":
        mips = ["DADDIU", reg, "$0", const]
        return mips


def store_reg(reg, addr, type):
    # mips = []
    instr = STORE_INSTRUCTIONS.get(type, f"{error_variable} {type}_store not found")
    mips = [instr, reg, addr]
    return mips


def load_reg(reg, addr, type):
    # mips = []
    instr = LOAD_INSTRUCTIONS.get(type, f"{error_variable} {type}not found")
    if is_int(addr):
        if type == "int" or type == "char" or type == "short":
            mips = ["ADDI", reg, "$0", addr]
            return mips
        elif type == "long":
            mips = ["DADDI", reg, "$0", addr]
            return mips
        elif (
            type == "unsigned int"
            or type == "unsigned char"
            or type == "unsigned short"
        ):
            mips = ["ADDIU", reg, "$0", addr]
            return mips
        elif type == "unsigned long":
            mips = ["DADDIU", reg, "$0", addr]
            return mips
    mips = [instr, reg, addr]
    return mips


# Integer constants and variables only
# int a = 1; int b=a;
def assign_op(atype, reg, laddr, raddr):
    mips = []
    type = atype[:-1]
    if is_int(raddr):
        mips.append(LI(reg, raddr, type))
        mips.append(store_reg(reg, laddr, type))
        return mips
    else:
        mips.append(load_reg(reg, raddr, type))
        mips.append(store_reg(reg, laddr, type))
        return mips


# int= a tmp_var *
def assign_op_ptr(atype, reg1, laddr, reg2, raddr):
    mips = []
    type = atype[:-1]
    load_instr = LOAD_INSTRUCTIONS.get(type, f"{error_variable} {atype} not found")
    mips.append([load_instr, reg2, raddr])
    mips.append(["LD", reg1, laddr])
    mips.append(["SD", reg2, f"0({reg1})"])
    return mips


# int*=  var tmp_var
def addr_str(reg1, laddr, raddr):
    mips = []
    mips.append(["LD", reg1, raddr])
    mips.append(["SD", reg1, laddr])
    return mips


# addr tmp_var var
def addr_load(reg1, addr1, offset_var):
    mips = []
    mips.append(["DADDI", reg1, "$fp", offset_var])
    mips.append(["SD", reg1, addr1])
    return mips


# beq	__tmp_var_3	0	__label_1
def beq_mips(type, reg, addr, label):
    mips = []
    load_instr = LOAD_INSTRUCTIONS[type]
    mips.append([load_instr, reg, addr])
    mips.append(["BEQ", reg, "$0", label])
    return mips


def conversion(type1, addr1, type2, addr2):
    mips = []
    size = -0.2
    if type1 in TYPE_INTEGER and type2.endswith("*"):
        if type2[0:-2].endswith("*"):
            size = -8
        elif type2[0:-2] in TYPE_INTEGER + TYPE_FLOAT:
            size = -4
            if (
                type2[0:-2] == "long"
                or type2[0:-2] == "unsigned long"
                or type2[0:-2] == "double"
            ):
                size = -8
            elif type2[0:-2] == "short" or type2[0:-2] == "unsigned short":
                size = -2
        else:
            size = ST.find(type2[0:-2])

    if type1.endswith("*"):
        type1 = "long"
    if type2.endswith("*"):
        type2 = "long"
    if type1 in TYPE_INTEGER:
        mips.append(load_reg("t0", addr1, type1))
        if size != -0.2:
            op = "DMULTI"
            mips.append([op, "t0", str(size)])
            mips.append(["MFLO  ", "t0"])
    elif type1 in TYPE_FLOAT:
        mips.append(load_reg("f2", addr1, type1))

    if (
        type1
        in ("int", "short", "unsigned short", "unsigned int", "char", "unsigned char")
        and type2 in TYPE_FLOAT
    ):
        mips.append(["MTC1", "t0", "f2"])
        mips.append(["CVT.D.W", "f2", "f2"])

    elif type1 in ("long", "unsigned long") and type2 in TYPE_FLOAT:
        mips.append(["DMTC1", "t0", "f2"])
        mips.append(["CVT.D.L", "f2", "f2"])

    elif (
        type2
        in ("int", "short", "unsigned short", "unsigned int", "char", "unsigned char")
        and type1 in TYPE_FLOAT
    ):
        mips.append(["CVT.W.D", "f2", "f2"])
        mips.append(["MFC1", "t0", "f2"])
    elif type2 in ("long", "unsigned long") and type1 in TYPE_FLOAT:
        mips.append(["CVT.L.D", "f2", "f2"])
        mips.append(["DMFC1", "t0", "f2"])
    elif (type1 in TYPE_FLOAT and type2 in TYPE_FLOAT) or (
        type1 in TYPE_INTEGER and type2 in TYPE_INTEGER
    ):
        pass

    else:
        print(f"TYPECASTING NOT POSSIBLE {type1},{type2}")

    if type2 in TYPE_INTEGER:
        mips.append(store_reg("t0", addr2, type2))
    elif type2 in TYPE_FLOAT:
        mips.append(store_reg("f2", addr2, type2))

    return mips

def nload(type,reg1,reg2,laddr,raddr):
    mips = []
    size  = int(type[0])
    mips.append(["LD",reg2,raddr])
    if(size == 4):
       mips.append(["LW",reg1,f"0({reg2})"])
       mips.append(["SW",reg1,laddr])
    else:
       mips.append(["LD",reg1,f"0({reg2})"])
       mips.append(["SD",reg1,laddr])
    return mips   

def non_prim_load(type,reg1,reg2,laddr,raddr):
    mips = []
    x=""
    l_offset=int(laddr[0:-5])
    for i in type:
        if i.isnumeric():
            x+=i
    size = int(x)
    # mips.append(["LD",reg2,laddr])
    mips.append(["LD",reg2,raddr])
    for i in range(0,size,8):
        if i == 0:
            mips.append(["LD",reg1,f"0({reg2})"])
            mips.append(["SD",reg1,f"{l_offset}($fp)"])
        else:
            mips.append(["DADDI",reg2,reg2,"-8"])
            mips.append(["LD",reg1,f"0({reg2})"])
            l_offset = l_offset-8
            mips.append(["SD",reg1,f"{l_offset}($fp)"])
    return mips        


#print(non_prim_load("t0","t1","-160($fp)","-152($fp)","104non_primitive_load"))


def mips_generation(full_code_gen):
    mips_set = []
    params = []

    for code_gen in full_code_gen:
        mips_set.append([comment_variable] + code_gen)
        s = code_gen[0]
        operators = (
            "<",
            ">",
            "+",
            "-",
            "*",
            "/",
            "%",
            "!",
            "&",
            "|",
            "^",
            "<=",
            ">=",
            "!=",
            "==",
            "&&",
            "||",
            "<<",
            ">>",
        )
        if "2" in s and "_" not in s:
            conversion_type = s.split("2")
            if "float" in conversion_type:
                print("ERROR: float  conversion not supported")
            else:
                print(code_gen)
                mips_set += conversion(
                    conversion_type[0], code_gen[2], conversion_type[1], code_gen[1]
                )

        elif s.endswith(operators):

            if s.endswith(("<=", ">=", "!=", "==", "&&", "||", "<<", ">>",)):
                if s[0:-2].endswith("*"):
                    s = "long" + s[-2:]
            else:
                if s[0:-1].endswith("*"):
                    s = "long" + s[-1:]

            # TODO:for pointers and arrays convert to long instead of float *
            mips_set += binary_exp_mips(
                s, "t0", code_gen[1], "t1", code_gen[2], "t2", code_gen[3]
            )

        elif s.endswith("=") and code_gen[3]=="":
            mips_set.extend(assign_op(s, "t0", code_gen[1], code_gen[2]))
        elif s.endswith("=") and code_gen[3]=="*":
            mips_set.extend(assign_op_ptr(s, "t0", code_gen[1],"$t1", code_gen[2])
        elif s == "4load" or s == "8load":
            mips_set.extend(nload(s,"t0","t1",code_gen[1],code_gen[2]))
        elif s.endswith("non_primitive_load"):
            mips_set.extend(non_prim_load(s,"t0","t1",code_gen[1],code_gen[2]))    
        elif s == "funcstart":
            mips_set.append(["label",code_gen[1],":",""])
            pass
        elif s == "addr":
            mips_set.extend(addr_load("t0",code_gen[1],code_gen[2]))    
        elif s == "endfunc":
            pass
        
        elif "return" in s:

            if s[-1]=="0":
                mips_set.append(["ADDI", "-16($fp)", "$0", "$0"])
            elif is_char(code_gen[1]):
                mips_set.append(["ADDI", "-16($fp)", "$0", code_gen[3]])
            elif is_num(code_gen[1]):
                if "." in s:
                    #instruction nahi pata float ke liye
                    mips_set.append(["ADDI", "-16($fp)", "$0", code_gen[3]])
                else:
                    mips_set.append(["ADDI", "-16($fp)", "$0", code_gen[3]])
            else:
                #TO_DO
                _type = _type = s.split("_")[1]
            
            # load_registers_on_function_return("sp")
            # mips_set.append(["LA", "$sp", "0($fp)"])
            # mips_set.append(["LW", "$ra", "-8($sp)"])
            # mips_set.append(["LA", "$fp", "-4($sp)"])
            # mips_set.append(["JR", "$ra", ""])

        elif "call" in s:
            node_type = s.split("_")
            
            mips_set.append(["SW", "$fp", "-4($sp)"])
            mips_set.append(["SW", "$ra", "-8($sp)"])
            sz = get_data_type_size(node_type[1])
            
            if node_type[1] in ["float", "double"]:
                mips_set.append([LOAD_INSTRUCTIONS[node_type[1]], f"{-8-sz}($sp)", "$f0"])
            elif node_type[1] in ["int", "long", "doublchar"]:
                mips_set.append([LOAD_INSTRUCTIONS[node_type[1]], f"{-8-sz}($sp)", "$v0"])
            elif node_type[1] != "void":
                # non_primitive_load jaisa
                pass
            
            for p in params:
                mips_set.append(p)
            params = []
            mips_set.append(["LA","$fp",f"{-int(node_type[2])}($sp)"])
            mips_set.append(["JAL", code_gen[1], ""])
     
        elif "param" in s:
            if is_char(code_gen[1]):
                mips_set.append(["ADDI", code_gen[2], "$0", code_gen[3]])
            elif is_num(code_gen[1]):
                if "." in s:
                    #instruction nahi pata float ke liye
                    mips_set.append(["ADDI", code_gen[2], "$0", code_gen[3]])
                else:
                    mips_set.append(["ADDI", code_gen[2], "$0", code_gen[3]])
            else:
                _type = _type = s.split("_")[1]
                params.append(load_reg("$t0",code_gen[3],_type))
                params.append(store_reg("$t0", code_gen[2], _type))
        
        elif s == ";":
            pass
        else:
            mips_set.append([comment_variable] + code_gen)

    return mips_set


# print(assign_op("unsigned long=","reg1","b_addr","a_addr"))

# arr=binary_exp_mips("double<" ,'reg1',	'__tmp_var_3_sp',	'reg2', 'a_sp'	, 'reg3', 'b_sp')
# print(arr)
# for i in Binary_ops.keys():
#     if i.startswith("float") or i.startswith('double'):
#         continue
#     arr=binary_exp_mips(i ,'reg1',	'__tmp_var_3_sp',	'reg2', '140'	, 'reg3', 'b_sp')
#     print('#',i, 'reg1',	'__tmp_var_3_sp',	'reg2', '140', 'reg3', 'b_sp')
#     for a in arr:
#         for x in a:
#             print(x,end='\t')
#         print("\n")
# code_gen = [["param", "foo", "__tmp_var_1", ""], ["call_4", "foo", "", ""]]
# print(mips_generation(code_gen))
