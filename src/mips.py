
def data_section():
    print(".data")

def text_section():
    print(".text")

def is_int(x):
    try:
        if x== str(int(x)) :
            return True
        else:
            return False
    except: 
     return False
        
#print(is_int("140"))        

LABEL_COUNTER = 0
def get_mips_label() -> str:
        global LABEL_COUNTER
        LABEL_COUNTER += 1
        # return f"__tmp_label_{TMP_LABEL_COUNTER}"
        return f"__labelm_{LABEL_COUNTER}"

TYPE_INTEGER = [
    "char", "unsigned char", "short", "unsigned short", "int", "unsigned int", "long", "unsigned long"
]

TYPE_FLOAT = ["float","double"]

BIN_BIT_OP = ["&","|","<<",">>","^"]

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
    "unsigned long": "SD"
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
    "unsigned long": "LD"
}


Binary_ops = {
    #UNSIGNED INT
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

    #INT
    "int+": ["ADD", 4],
    "int-": ["SUB", 4],
    "int*": ["MULT", 4],

    "int/": ["DIV", 4],
    "int%": ["DIV",4],

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

    #SHORT
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

    #UNSIGNED SHORT
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

    #UNSIGNED CHAR
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

    #CHAR
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
    

    #UNSIGNED LONG
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

    #LONG
    "long+": ["DADD", 8],
    "long-": ["DSUB", 8],
    
    "long*": ["DMULT", 8],
    "long/": ["DDIV", 8],
    "long%": ["DDIV",8],
    
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

    #FLOAT
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

#Handled type_int
#TODO Type_float ,relational operators
def binary_exp_mips(binexp, reg1, a1, reg2, a2, reg3, a3):
    mips = []
    type = ""
    op = ""
    for i in binexp:
        if(i.isalpha() or i == ' '):
            type += i
        else:
            op+= i
    print(type,op)        
    # mips.append(load_reg(reg1, a1, type))
    mips.append(load_reg(reg2, a2, type))
    mips.append(load_reg(reg3, a3, type))        
    if (op =="+" or op == "-") and type in TYPE_INTEGER :        
        op = Binary_ops[binexp][0]
        mips.append([op,reg1,reg2,reg3])
    elif op =="*" and type in TYPE_INTEGER :
        op = Binary_ops[binexp][0]
        mips.append([op,reg2,reg3])
        mips.append(["MFLO  ",reg1])
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
        mips.append([op,reg1,reg2,reg3])
    elif op == "~" and type in TYPE_INTEGER:
        #only 2 regs will be given
        op = Binary_ops[binexp][0]
        mips.append([op,reg1,reg2,"0xffffffffffffffff"])
    elif op == "<" and type in TYPE_INTEGER:
        op = Binary_ops[binexp][0]
        mips.append([op, reg1, reg2, reg3])
    elif op == ">" and type in TYPE_INTEGER:
        op = Binary_ops[binexp][0]
        mips.append([op, reg1, reg3, reg2])
    elif op == "<=" and type in TYPE_INTEGER:
        op = Binary_ops[binexp][0]
        #check greater than and xor with 1
        mips.append([op, reg1, reg3, reg2])
        mips.append(["XORI",reg1,reg1,"0x1"])
    elif op == ">=" and type in TYPE_INTEGER:
        op = Binary_ops[binexp][0]
        #check less than and xor with 1
        mips.append([op, reg1, reg2, reg3])
        mips.append(["XORI", reg1, reg1, "0x1"])
    elif op == "==" and type in TYPE_INTEGER:
        op = Binary_ops[binexp][0]
        mips.append([op, reg1, reg2, reg3])
        mips.append(["SLTUI",reg1,reg1,"1"])
    elif op == "!=" and type in TYPE_INTEGER:
        op = Binary_ops[binexp][0]
        mips.append([op, reg1, reg2, reg3])
        mips.append(["SLTU",reg1,"$0",reg1])   
    elif (op == "&&" or op == "||") and type in TYPE_INTEGER:
        op = Binary_ops[binexp][0]
        mips.append([op, reg1, reg2, reg3])
    elif op == "!" and type in TYPE_INTEGER:
        op = Binary_ops[binexp][0]
        mips.append([op,reg1,reg1,"1"])
    #only 2 registers case, constants case not handled
    elif (op =="+" or op == "-" or op == "/" or op =="*") and type in TYPE_FLOAT :        
        op = Binary_ops[binexp][0]
        mips.append([op,reg1,reg2,reg3])  
    elif op == "<" and type in TYPE_FLOAT:
        op = Binary_ops[binexp][0]
        mips.append([op,"2",reg2,reg3])  
        l0 = get_mips_label()
        mips.append(["BC1F","2",l0])
        mips.append(["ADDI", reg1, "$0", "1"])
        l1 = get_mips_label()
        mips.append(["J",l1])
        mips.append([l0])
        mips.append(["XOR", reg1, reg1, reg1])
        mips.append([l1])
    elif op == ">" and type in TYPE_FLOAT:
        op = Binary_ops[binexp][0]
        mips.append([op, "2", reg3, reg2])
        l0 = get_mips_label()
        mips.append(["BC1F", "2", l0])
        mips.append(["ADDI", reg1, "$0", "1"])
        l1 = get_mips_label()
        mips.append(["J", l1])
        mips.append([l0])
        mips.append(["XOR", reg1, reg1, reg1])
        mips.append([l1])
    elif op == ">=" and type in TYPE_FLOAT:
        op = Binary_ops[binexp][0]
        mips.append([op, "2", reg2, reg3])
        l0 = get_mips_label()
        mips.append(["BC1F", "2", l0])
        mips.append(["XOR", reg1, reg1, reg1])
        l1 = get_mips_label()
        mips.append(["J", l1])
        mips.append([l0])
        mips.append(["ADDI", reg1, "$0", "1"])
        mips.append([l1])
    elif op == "<=" and type in TYPE_FLOAT:
        op = Binary_ops[binexp][0]
        mips.append([op, "2", reg3, reg2])
        l0 = get_mips_label()
        mips.append(["BC1F", "2", l0])
        mips.append(["XOR", reg1, reg1, reg1])
        l1 = get_mips_label()
        mips.append(["J", l1])
        mips.append([l0])
        mips.append(["ADDI", reg1, "$0", "1"])
        mips.append([l1])
    elif op == "!=" and type in TYPE_FLOAT:
        op = Binary_ops[binexp][0]
        mips.append([op, "7", reg2, reg3])
        l0 = get_mips_label()
        mips.append(["BC1F", "7", l0])
        mips.append(["XOR", reg1, reg1, reg1])
        l1 = get_mips_label()
        mips.append(["J", l1])
        mips.append([l0])
        mips.append(["ADDI", reg1, "$0", "1"])
        mips.append([l1])
    elif op == "==" and type in TYPE_FLOAT:
        op = Binary_ops[binexp][0]
        mips.append([op, "7", reg2, reg3])
        l0 = get_mips_label()
        mips.append(["BC1F", "7", l0])
        mips.append(["ADDI", reg1, "$0", "1"])
        l1 = get_mips_label()
        mips.append(["J", l1])
        mips.append([l0])
        mips.append(["XOR", reg1, reg1, reg1])
        mips.append([l1])

    mips.append(store_reg(reg1, a1, type))
    return mips

def LI(reg,const,type):
    if type == "int" or type == "char" or type == "short":
            mips = ["ADDI", reg, "$0", const]
            return mips
    elif type == "long":
            mips = ["DADDI",reg,"$0",const]
            return mips
    elif type == "unsigned int" or type == "unsigned char" or type =="unsigned short":
            mips = ["ADDIU",reg,"$0",const]
            return mips
    elif type == "unsigned long":
            mips = ["DADDIU",reg,"$0",const]
            return mips


def store_reg(reg,addr,type):
    #mips = []
    instr = STORE_INSTRUCTIONS[type]
    mips = [instr,reg,addr]
    return mips

def load_reg(reg,addr,type):
    #mips = []
    instr = LOAD_INSTRUCTIONS[type]
    if(is_int(addr)):
        if type == "int" or type == "char" or type =="short":
            mips = ["ADDI",reg,"$0",addr]
            return mips
        elif type == "long":
            mips = ["DADDI",reg,"$0",addr]
            return mips
        elif type == "unsigned int" or type == "unsigned char" or type =="unsigned short":
            mips = ["ADDIU",reg,"$0",addr]
            return mips
        elif type == "unsigned long":
            mips = ["DADDIU",reg,"$0",addr]
            return mips      
    mips = [instr, reg, addr]
    return mips

#Integer constants and variables only
#int a = 1; int b=a;
def assign_op(atype,reg,laddr,raddr):
    mips = []
    type = atype[:-1]
    if(is_int(raddr)):
        mips.append(LI(reg,raddr,type))
        mips.append(store_reg(reg,laddr,type))
        return mips
    else:
        mips.append(load_reg(reg,raddr,type))
        mips.append(store_reg(reg, laddr, type))
        return mips

#int= a tmp_var *
def assign_op_ptr(atype,reg1,laddr,reg2,raddr):
    mips = []
    type = atype[:-1]
    load_instr = LOAD_INSTRUCTIONS[type]
    mips.append([load_instr,reg2,raddr])
    mips.append(["LD",reg1,laddr])
    mips.append(["SD",reg2,f"0({reg1})"])
    return mips

#TODO int*=



#print(assign_op("unsigned long=","reg1","b_addr","a_addr"))

 
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
