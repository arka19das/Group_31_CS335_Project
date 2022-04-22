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
]

TYPE_FLOAT = ["float"]

BIN_BIT_OP = ["&", "|", "<<", ">>", "^"]
COMP_OP = ["<=","<",">",">","=="]

STORE_INSTRUCTIONS = {
    "char": "sw",
    "int": "sw",
    "short": "sh",
    "void": "sw",
    "float": "s.s",
    "unsigned char": "sw",
    "unsigned int": "sw",
    "unsigned short": "sh",
}

LOAD_INSTRUCTIONS = {
    "char": "lw",
    "int": "lw",
    "short": "lh",
    "void": "lw",
    "float": "l.s",
    "unsigned char": "lw",
    "unsigned int": "lw",
    "unsigned short": "lhu",
}


Binary_ops = {
    # UNSIGNED INT
    "unsigned int+": ["addu", 4],
    "unsigned int-": ["subu", 4],

    "unsigned int*": ["multu", 4],
    "unsigned int/": ["divu", 4],
    "unsigned int%": ["divu", 4],

    "unsigned int<=": ["sleu", 4],
    "unsigned int<": ["sltu", 4],
    "unsigned int>=": ["sgeu", 4],
    "unsigned int>": ["sgtu", 4],
    "unsigned int==": ["seq", 4],
    "unsigned int!=": ["xor", 4],
    
    "unsigned int&": ["and", 4],
    "unsigned int^": ["xor", 4],
    "unsigned int|": ["or", 4],
    "unsigned int~": ["nor", 4],
    "unsigned int<<": ["sll", 4],
    "unsigned int>>": ["srl", 4],
    
    "unsigned int!": ["sltiu", 4],
    "unsigned int&&": ["and", 4],
    "unsigned int||": ["or", 4],
    # INT
    "int+": ["add", 4],
    "int-": ["sub", 4],

    "int*": ["mult", 4],
    "int/": ["div", 4],
    "int%": ["div", 4],

    "int<=": ["sle", 4],
    "int<": ["slt", 4],
    "int>=": ["sge", 4],
    "int>": ["sgt", 4],
    "int==": ["seq", 4],
    "int!=": ["xor", 4],
    
    "int&": ["and", 4],
    "int^": ["xor", 4],
    "int|": ["or", 4],
    "int~": ["nor", 4],
    "int<<": ["sll", 4],
    "int>>": ["srl", 4],
   
    "int!": ["sltiu", 4],
    "int||": ["or", 4],
    "int&&": ["and", 4],
    # SHORT
    "short+": ["add", 2],
    "short-": ["sub", 2],

    "short*": ["mult", 2],
    "short/": ["div", 2],
    "short%": ["div", 2],

    "short<=": ["sle", 2],
    "short<": ["slt", 2],
    "short>=": ["sge", 2],
    "short>": ["sgt", 2],
    "short==": ["seq", 2],
    "short!=": ["xor", 4],
    
    "short&": ["and", 2],
    "short^": ["xor", 2],
    "short|": ["or", 2],
    "short~": ["nor", 2],
    "short<<": ["sll", 2],
    "short>>": ["srl", 2],
    
    "short!": ["sltiu", 2],
    "short&&": ["and", 2],
    "short||": ["or", 2],
    # UNSIGNED SHORT
    "unsigned short+": ["addu", 2],
    "unsigned short-": ["subu", 2],
    
    "unsigned short*": ["multu", 2],
    "unsigned short/": ["divu", 2],
    "unsigned short%": ["divu", 2],
    
    "unsigned short<=": ["sleu", 2],
    "unsigned short<": ["sltu", 2],
    "unsigned short>=": ["sgeu", 2],
    "unsigned short>": ["sgtu", 2],
    "unsigned short==": ["seq", 2],
    "unsigned short!=": ["xor", 2],
    
    "unsigned short&": ["and", 2],
    "unsigned short^": ["xor", 2],
    "unsigned short|": ["or", 2],
    "unsigned short~": ["nor", 2],
    "unsigned short<<": ["sll", 2],
    "unsigned short>>": ["srl", 2],
    
    "unsigned short!": ["sltiu", 2],
    "unsigned short||": ["or", 2],
    "unsigned short&&": ["and", 2],
    
    # UNSIGNED CHAR
    "unsigned char+": ["addu", 4],
    "unsigned char-": ["subu", 4],
    
    "unsigned char*": ["multu", 4],
    "unsigned char/": ["divu", 4],
    "unsigned char%": ["divu", 4],
    
    "unsigned char<=": ["sleu", 4],
    "unsigned char<": ["slt", 4],
    "unsigned char>=": ["sgeu", 4],
    "unsigned char>": ["sgtu", 4],
    "unsigned char==": ["seq", 4],
    "unsigned char!=": ["xor", 4],
    
    "unsigned char&": ["and", 4],
    "unsigned char^": ["xor", 4],
    "unsigned char|": ["or", 4],
    "unsigned char~": ["nor", 4],
    "unsigned char<<": ["sll", 4],
    "unsigned char>>": ["srl", 4],
    
    "unsigned char!": ["sltiu", 4],
    "unsigned char||": ["or", 4],
    "unsigned char&&": ["and", 4],
    # CHAR
    "char+": ["add", 4],
    "char-": ["sub", 4],
    
    "char*": ["mult", 4],
    "char/": ["div", 4],
    "char%": ["div", 4],
    
    "char<=": ["sle", 4],
    "char<": ["slt", 4],
    "char>=": ["sge", 4],
    "char>": ["sgt", 4],
    "char==": ["seq", 4],
    "char!=": ["xor", 4],
    
    "char&": ["and", 4],
    "char^": ["xor", 4],
    "char|": ["or", 4],
    "char~": ["nor", 4],
    "char>>": ["srl", 4],
    "char<<": ["sll", 4],
    
    "char!": ["sltiu", 4],
    "char&&": ["and", 4],
    "char||": ["or", 4],
    # FLOAT
    "float+": ["add.s", 4],
    "float-": ["sub.s", 4],
    
    "float*": ["mul.s", 4],
    "float/": ["div.s", 4],
    
    "float<=": ["c.le.s", 4],
    "float<": ["c.lt.s", 4],
    "float>=": ["c.le.s", 4],
    "float>": ["c.lt.s", 4],
    "float==": ["c.eq.s", 4],
    "float!=": ["c.eq.s", 4],
}

# Handled type_int
# TODO Type_float ,relational operators
def load_reg(reg, addr, type):
    # mips = []
    instr = LOAD_INSTRUCTIONS.get(type, f"{error_variable} {type}not found")
    if is_int(addr) and type in TYPE_INTEGER:
        mips = ["li",reg,addr]
        return mips
        # if type == "int" or type == "char" or type == "short":
        #     mips = ["ADDI", reg, "$0", addr]
        #     return mips
        # elif type == "long":
        #     mips = ["DADDI", reg, "$0", addr]
        #     return mips
        # elif (
        #     type == "unsigned int"
        #     or type == "unsigned char"
        #     or type == "unsigned short"
        # ):
        #     mips = ["ADDIU", reg, "$0", addr]
        #     return mips
        # elif type == "unsigned long":
        #     mips = ["DADDIU", reg, "$0", addr]
        #     return mips
    mips = [instr, reg, addr]
    return mips

def store_reg(reg, addr, type):
    # mips = []
    instr = STORE_INSTRUCTIONS.get(type, f"{error_variable} {type}_store not found")
    mips = [instr, reg, addr]
    return mips



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
    if (op == "+" or op == "-") and type in TYPE_INTEGER:
        mips.append(load_reg(reg3, a3, type))
        op = Binary_ops[binexp][0]
        mips.append([op, reg1, reg2, reg3])
    elif (op == "*" or op =="/") and type in TYPE_INTEGER:
        mips.append(load_reg(reg3, a3, type))
        op = Binary_ops[binexp][0]
        mips.append([op, reg2, reg3])
        mips.append(["mflo", reg1])
    elif op == "%" and type in TYPE_INTEGER:
        mips.append(load_reg(reg3, a3, type))
        op = Binary_ops[binexp][0]
        mips.append([op, reg2, reg3])
        mips.append(["mfhi", reg1])
    elif op in BIN_BIT_OP and type in TYPE_INTEGER:
        mips.append(load_reg(reg3, a3, type))
        op = Binary_ops[binexp][0]
        mips.append([op, reg1, reg2, reg3])
    elif op == "~" and type in TYPE_INTEGER:
        # only 2 regs will be given
        op = Binary_ops[binexp][0]
        mips.append([op, reg1, "$0" ,reg2 ])
    elif op in COMP_OP and type in TYPE_INTEGER:
        op = Binary_ops[binexp][0]
        mips.append([op, reg1, reg2, reg3])
    # elif op == ">" and type in TYPE_INTEGER:
    #     mips.append(load_reg(reg3, a3, type))
    #     op = Binary_ops[binexp][0]
    #     mips.append([op, reg1, reg3, reg2])
    # elif op == "<=" and type in TYPE_INTEGER:
    #     mips.append(load_reg(reg3, a3, type))
    #     op = Binary_ops[binexp][0]
    #     # check greater than and xor with 1
    #     mips.append([op, reg1, reg3, reg2])
    # elif op == ">=" and type in TYPE_INTEGER:
    #     mips.append(load_reg(reg3, a3, type))
    #     op = Binary_ops[binexp][0]
    #     # check less than and xor with 1
    #     mips.append([op, reg1, reg2, reg3])
    #     mips.append(["XORI", reg1, reg1, "0x1"])
    # elif op == "==" and type in TYPE_INTEGER:
    #     mips.append(load_reg(reg3, a3, type))
    #     op = Binary_ops[binexp][0]
    #     mips.append([op, reg1, reg2, reg3])
    #     mips.append(["SLTUI", reg1, reg1, "1"])
    elif op == "!=" and type in TYPE_INTEGER:
        mips.append(load_reg(reg3, a3, type))
        op = Binary_ops[binexp][0]
        mips.append([op, reg1, reg2, reg3])
        mips.append(["sltu", reg1, "$0", reg1])
    elif (op == "&&" or op == "||") and type in TYPE_INTEGER:
        mips.append(load_reg(reg3, a3, type))
        op = Binary_ops[binexp][0]
        mips.append([op, reg1, reg2, reg3])
    elif op == "!" and type in TYPE_INTEGER:
        op = Binary_ops[binexp][0]
        mips.append([op, reg1, reg1, "1"])
    # only 2 registers case, constants case not handled
    elif (op == "+" or op == "-" or op == "/" or op == "*") and type in TYPE_FLOAT:
        op = Binary_ops[binexp][0]
        mips.append([op, reg1, reg2, reg3])
    elif (op == "<" or op == "<=") and type in TYPE_FLOAT:
        mips.append(load_reg(reg3, a3, type))
        op = Binary_ops[binexp][0]
        mips.append([op,reg2,reg3])
        # mips.append([op, "2", reg2, reg3])
        l0 = get_mips_label()
        mips.append(["bc1f", l0])
        mips.append(["addi", reg1, "$0", "1"])
        l1 = get_mips_label()
        mips.append(["j", l1])
        mips.append([f"{l0}:"])
        mips.append(["xor", reg1, reg1, reg1])
        mips.append([f"{l1}:"])
    elif (op == ">" or op ==">=") and type in TYPE_FLOAT:
        mips.append(load_reg(reg3, a3, type))
        op = Binary_ops[binexp][0]
        mips.append([op,reg3,reg2])
    #     mips.append([op, "2", reg3, reg2])
        l0 = get_mips_label()
        mips.append(["bc1f", l0])
        mips.append(["addi", reg1, "$0", "1"])
        l1 = get_mips_label()
        mips.append(["j", l1])
        mips.append([f"{l0}:"])
        mips.append(["xor", reg1, reg1, reg1])
        mips.append([f"{l1}:"])
    # elif op == ">=" and type in TYPE_FLOAT:
    #     mips.append(load_reg(reg3, a3, type))
    #     op = Binary_ops[binexp][0]
    #     mips.append([op, "2", reg2, reg3])
    #     l0 = get_mips_label()
    #     mips.append(["BC1F", "2", l0])
    #     mips.append(["XOR", reg1, reg1, reg1])
    #     l1 = get_mips_label()
    #     mips.append(["J", l1])
    #     mips.append([f"{l0}:"])
    #     mips.append(["ADDI", reg1, "$0", "1"])
    #     mips.append([f"{l1}:"])
    # elif op == "<=" and type in TYPE_FLOAT:
    #     mips.append(load_reg(reg3, a3, type))
    #     op = Binary_ops[binexp][0]
    #     mips.append([op, "2", reg3, reg2])
    #     l0 = get_mips_label()
    #     mips.append(["BC1F", "2", l0])
    #     mips.append(["XOR", reg1, reg1, reg1])
    #     l1 = get_mips_label()
    #     mips.append(["J", l1])
    #     mips.append([f"{l0}:"])
    #     mips.append(["ADDI", reg1, "$0", "1"])
    #     mips.append([f"{l1}:"])
    elif op == "!=" and type in TYPE_FLOAT:
        mips.append(load_reg(reg3, a3, type))
        op = Binary_ops[binexp][0]
        mips.append([op, reg2, reg3])
        l0 = get_mips_label()
        mips.append(["bc1f", l0])
        mips.append(["xor", reg1, reg1, reg1])
        l1 = get_mips_label()
        mips.append(["j", l1])
        mips.append([f"{l0}:"])
        mips.append(["addi", reg1, "$0", "1"])
        mips.append([f"{l1}:"])
    elif op == "==" and type in TYPE_FLOAT:
        mips.append(load_reg(reg3, a3, type))
        op = Binary_ops[binexp][0]
        mips.append([op,reg2,reg3])
    #     mips.append([op, "7", reg2, reg3])
        l0 = get_mips_label()
        mips.append(["bc1f", l0])
        mips.append(["addi", reg1, "$0", "1"])
        l1 = get_mips_label()
        mips.append(["j", l1])
        mips.append([f"{l0}:"])
        mips.append(["xor", reg1, reg1, reg1])
        mips.append([f"{l1}:"])
    # # elif op == "*=" and type in TYPE_INTEGER:

    mips.append(store_reg(reg1, a1, type))
    return mips

print(binary_exp_mips("int~","t1","a1","t2","a2","t3","a3"))

# def LI(reg, const, type):
#     if type == "int" or type == "char" or type == "short":
#         mips = ["ADDI", reg, "$0", const]
#         return mips
#     elif type == "long":
#         mips = ["DADDI", reg, "$0", const]
#         return mips
#     elif type == "unsigned int" or type == "unsigned char" or type == "unsigned short":
#         mips = ["ADDIU", reg, "$0", const]
#         return mips
#     elif type == "unsigned long":
#         mips = ["DADDIU", reg, "$0", const]
#         return mips





# Integer constants and variables only
# int a = 1; int b=a;
def assign_op(atype, reg, laddr, raddr):
    mips = []
    type = atype[:-1]
    if is_int(raddr):
        mips.append(["li",reg,raddr])
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
    mips.append(["lw", reg1, laddr])
    mips.append(["sw", reg2, f"0({reg1})"])
    return mips


# int*=  var tmp_var
def addr_str(reg1, laddr, raddr):
    mips = []
    mips.append(["lw", reg1, raddr])
    mips.append(["sw", reg1, laddr])
    return mips


# addr tmp_var var
def addr_load(reg1, laddr, raddr):
    mips = []
    #mips.append(["DADDI", reg1, "$fp", offset_var])
    mips.append(["la",reg1,raddr])
    mips.append(["sw", reg1, laddr])
    return mips


# beq	__tmp_var_3	0	__label_1
def beq_mips(type, reg, addr, label):
    mips = []
    load_instr = LOAD_INSTRUCTIONS[type]
    mips.append([load_instr, reg, addr])
    mips.append(["beq", reg, "$0", label])
    return mips

def nload(type,reg1,reg2,laddr,raddr):
    mips = []
    size  = int(type[0])
    mips.append(["lw",reg2,raddr])
    if(size == 4):
       mips.append(["lw",reg1,f"0({reg2})"])
       mips.append(["sw",reg1,laddr])
    else:
       mips.append(["lh",reg1,f"0({reg2})"])
       mips.append(["sh",reg1,laddr])
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
    mips.append(["lw",reg2,raddr])
    for i in range(0,size,4):
        if i == 0:
            mips.append(["lw",reg1,f"0({reg2})"])
            mips.append(["sw",reg1,f"{l_offset}($fp)"])
        else:
            mips.append(["addi",reg2,reg2,"-4"])
            mips.append(["lw",reg1,f"0({reg2})"])
            l_offset = l_offset-4
            mips.append(["sw",reg1,f"{l_offset}($fp)"])
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
        mips.append(load_reg("$t0", addr1, type1))
        if size != -0.2:
            op = "DMULTI"
            mips.append([op, "$t0", str(size)])
            mips.append(["MFLO  ", "$t0"])
    elif type1 in TYPE_FLOAT:
        mips.append(load_reg("f2", addr1, type1))

    if (
        type1
        in ("int", "short", "unsigned short", "unsigned int", "char", "unsigned char")
        and type2 in TYPE_FLOAT
    ):
        mips.append(["MTC1", "$t0", "f2"])
        mips.append(["CVT.D.W", "f2", "f2"])

    elif type1 in ("long", "unsigned long") and type2 in TYPE_FLOAT:
        mips.append(["DMTC1", "$t0", "f2"])
        mips.append(["CVT.D.L", "f2", "f2"])

    elif (
        type2
        in ("int", "short", "unsigned short", "unsigned int", "char", "unsigned char")
        and type1 in TYPE_FLOAT
    ):
        mips.append(["CVT.W.D", "f2", "f2"])
        mips.append(["MFC1", "$t0", "f2"])
    elif type2 in ("long", "unsigned long") and type1 in TYPE_FLOAT:
        mips.append(["CVT.L.D", "f2", "f2"])
        mips.append(["DMFC1", "$t0", "f2"])
    elif (type1 in TYPE_FLOAT and type2 in TYPE_FLOAT) or (
        type1 in TYPE_INTEGER and type2 in TYPE_INTEGER
    ):
        pass

    else:
        print(f"TYPECASTING NOT POSSIBLE {type1},{type2}")

    if type2 in TYPE_INTEGER:
        mips.append(store_reg("$t0", addr2, type2))
    elif type2 in TYPE_FLOAT:
        mips.append(store_reg("f2", addr2, type2))

    return mips




#print(non_prim_load("$t0","$t1","-160($fp)","-152($fp)","104non_primitive_load"))


def mips_generation(full_code_gen):
    mips_set = []
    params = []
    return_offset = 0
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
                    s = "int" + s[-2:]
            else:
                if s[0:-1].endswith("*"):
                    s = "int" + s[-1:]

            # TODO:for pointers and arrays convert to long instead of float *
            mips_set += binary_exp_mips(
                s, "$t0", code_gen[1], "$t1", code_gen[2], "$t2", code_gen[3]
            )

        elif s.endswith("=") and code_gen[3]=="":
            mips_set.extend(assign_op(s, "$t0", code_gen[1], code_gen[2]))
        elif s.endswith("=") and code_gen[3]=="*":
            mips_set.extend(assign_op_ptr(s, "$t0", code_gen[1], code_gen[2]))
        elif s == "2load" or s == "4load":
            mips_set.extend(nload(s,"$t0","$t1",code_gen[1],code_gen[2]))
        elif s.endswith("non_primitive_load"):
            mips_set.extend(non_prim_load(s,"$t0","$t1",code_gen[1],code_gen[2]))    
        elif s == "funcstart":
            mips_set.append(["label",code_gen[1],":",""])
            pass
        elif s == "addr":
            mips_set.extend(addr_load("$t0",code_gen[1],code_gen[2]))    
        elif s == "endfunc":
            pass
        
        elif "return" in s:
            
            node_split =s.split("_")
            return_offset = int(node_split[-1])-16
            if s[-1]=="0":
                mips_set.append(["ADDI", f"{return_offset}($fp)", "$0", "$0"])
            elif is_char(code_gen[1]):
                mips_set.append(["ADDI", f"{return_offset}($fp)", "$0", code_gen[3]])
            elif is_num(code_gen[1]):
                if "." in s:
                    #instruction nahi pata float ke liye
                    mips_set.append(["ADDI", "0($v0)", "$0", code_gen[3]])
                else:
                    mips_set.append(["ADDI", f"{return_offset}($fp)", "$0", code_gen[3]])
            else:
                # node_split = s.split("_")
                offset = int(code_gen[1].split('(')[0])
                sz = int(node_split[1])
                # sz+=(8-sz%8)%8
                for i in range(0,sz,8):
                    # mips_set.append(load_reg("$t0",f"{offset-i}($fp)",node_split[2]))
                    # mips_set.append(store_reg("$t0", f"{return_offset-i}($fp)", node_split[2]))
                    mips_set.append(store_reg(f"{offset-i}($fp)", f"{return_offset-i-8}($fp)", node_split[2]))
            
            return_offset+=16
            return_size=-return_offset
            # load_registers_on_function_return("sp")
            mips_set.append(["ADDIU","$t0","$fp",f"{return_size}"])
            mips_set.append(["MOVZ","$fp","$t0","$0"])
            mips_set.append(["LW", "$ra", "-16($fp)"])
            mips_set.append(["MOVZ","$sp","$fp","$0"])
            mips_set.append(["LA", "$fp", "-8($fp)"])
            mips_set.append(["JR", "$ra", ""])

        elif "call" in s:
            node_type = s.split("_")
            
            mips_set.append(["DADDI","$t0","$0",f"{int(node_type[2])-int(node_type[3])}"])
            mips_set.append(["SUB","$sp","$sp","$t0"])
            mips_set.append(["SW", "$fp", "-8($sp)"])
            mips_set.append(["SW", "$ra", "-16($sp)"])
            
            for p in params:
                mips_set.append(p)
            params = []
            # mips_set.append(["ADDI","$t7","$0",int(node_type[-1])])
            mips_set.append(["LA","$fp",f"{-int(node_type[2])}($sp)"])
            mips_set.append(["MOVZ","$sp","$fp","$0"])
            mips_set.append(["jal", code_gen[1], ""])
            # return_offset = node_type[3]

        elif "param" in s:
            if is_char(code_gen[1]):
                params.append(["addi", code_gen[2], "$0", code_gen[3]])
            elif is_num(code_gen[1]):
                if "." in s:
                    #instruction nahi pata float ke liye
                    params.append(["addi", code_gen[2], "$0", code_gen[3]])
                else:
                    params.append(["addi", code_gen[2], "$0", code_gen[3]])
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
