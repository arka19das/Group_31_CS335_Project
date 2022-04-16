
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
        
#print(is_int("$(fp)"))        

TYPE_INT = [
    "char", "unsigned char", "short", "unsigned short", "int", "unsigned int", "long", "unsigned long"
]

#TYPE_LONG = []

BIN_BIT_OP = ["&","|","<<",">>","^"]

STORE_INSTRUCTIONS = {
    "char": "SW",
    "int": "SW",
    "short": "SH",
    "void": "SW",
    "long": "SW",
    "float": "SD",
    "double": "SDC1",
    "unsigned char": "SW",
    "unsigned int": "SW",
    "unsigned short": "SW",
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
    "unsigned int+": ["ADDU", 4],
    "unsigned int-": ["SUBU", 4],
    "unsigned int*": ["MULTU", 4],

    "unsigned int/": ["DIVU", 4],
    "unsigned int%": ["DIVU", 4],
   
    #"unsigned int<=": ["SLTU","XORI $2 $2 0x1" 4],
    #SLE not there in edumips  
    "unsigned int<=": ["SLTU", 4],
    "unsigned int<": ["SLTU", 4],
    #SGE and SGT not there in edumips, have to use SLTU changing the seq of registers
    "unsigned int>=": ["SLTU", 4],
    "unsigned int>": ["SLTU", 4],
    #SEQU, SNEU not there in edumips
    #"unsigned int==": ["XOR","SLTU $2 $2 1" 4],
    "unsigned int==": ["XOR", 4],
    #"unsigned int!=": ["XOR","SLTU $2 $0 $2" 4],
    "unsigned int!=": ["XOR", 4],
    
    "unsigned int&": ["AND", 4],
    "unsigned int^": ["XOR", 4],
    "unsigned int|": ["OR", 4],
    "unsigned int~": ["NOT", 4],
    "unsigned int<<": ["SLL", 4],
    "unsigned int>>": ["SRL", 4],

    # "unsigned int!": ["NOR", 4],
    # "unsigned int&&": ["NOR", 4],
    # "unsigned int||": ["NOR", 4],

    #Changes similar to unsigned int
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
    "int~": ["NOT", 4],
    "int<<": ["SLL", 4],
    "int>>": ["SRL", 4],
    # Not handled
    # "int!": ["NOT", 4],
    # "int||": ["NOT", 4],
    # "int&&": ["NOT", 4],

    

    #Changes similar to unsigned int
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
    "short~": ["NOT", 2],
    "short<<": ["SLL", 2],
    "short>>": ["SRL", 2],

    # "short!": ["NOR", 2],
    # "short&&": ["NOR", 2],
    # "short||": ["NOR", 2],

    "unsigned short+": ["ADDU", 2],
    "unsigned short-": ["SUBU", 2],
    "unsigned short*": ["MULTU", 2],
   
    "unsigned short/": ["DIVU", 2],
    "unsigned short%": ["DIVU", 2],
    
    #"unsigned int<=": ["SLTU","XORI $2 $2 0x1" 4],
    #SLE not there in edumips
    "unsigned short<=": ["SLTU", 2],
    "unsigned short<": ["SLTU", 2],
    #SGE and SGT not there in edumips, have to use SLTU changing the seq of registers
    "unsigned short>=": ["SLTU", 2],
    "unsigned short>": ["SLTU", 2],
    #SEQU, SNEU not there in edumips
    #"unsigned int==": ["XOR","SLTU $2 $2 1" 4],
    "unsigned short==": ["XOR", 2],
    #"unsigned int!=": ["XOR","SLTU $2 $0 $2" 4],
    "unsigned short!=": ["XOR", 2],
    
    "unsigned short&": ["AND", 2],
    "unsigned short^": ["XOR", 2],
    "unsigned short|": ["OR", 2],
    "unsigned short~": ["NOT", 2],
    "unsigned short<<": ["SLL", 2],
    "unsigned short>>": ["SRL", 2],

    #"unsigned short!": ["NOR", 2],
    #"unsigned short||": ["NOR", 2],
    #"unsigned short&&": ["NOR", 2],

    "unsigned char+": ["ADDU", 4],
    "unsigned char-": ["SUBU", 4],
    "unsigned char*": ["MULTU", 4],
    
    "unsigned char/": ["DIVU", 4],
    "unsigned char%": ["DIVU", 4],
    
    #"unsigned int<=": ["SLTU","XORI $2 $2 0x1" 4],
    #SLE not there in edumips
    "unsigned char<=": ["SLTU", 4],
    "unsigned char<": ["SLTU", 4],
    #SGE and SGT not there in edumips, have to use SLTU changing the seq of registers
    "unsigned char>=": ["SLTU", 4],
    "unsigned char>": ["SLTU", 4],
    #SEQU, SNEU not there in edumips
    #"unsigned int==": ["XOR","SLTU $2 $2 1" 4],
    "unsigned char==": ["XOR", 4],
    #"unsigned int!=": ["XOR","SLTU $2 $0 $2" 4],
    "unsigned char!=": ["XOR", 4],
    
    "unsigned char&": ["AND", 4],
    "unsigned char^": ["XOR", 4],
    "unsigned char|": ["OR", 4],
    "unsigned char~": ["NOT", 4],
    "unsigned char<<": ["SLL", 4],
    "unsigned char>>": ["SRL", 4],

    # "unsigned char!": ["NOR", 4],
    # "unsigned char||": ["NOR", 4],
    # "unsigned char&&": ["NOR", 4],

    #changes similar to unsigned_int
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
    "char~": ["NOT", 4],
    "char>>": ["SRL", 4],
    "char<<": ["SLL", 4],

    # "char!": ["NOR", 4], 
    # "char&&": ["NOR", 4],
    # "char||": ["NOR", 4],
    

    #Changes similar to unsigned int
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
    "unsigned long~": ["NOT", 8],
    "unsigned long>>": ["DSRL", 8],
    "unsigned long<<": ["DSLL", 8],

    # "unsigned long!": ["NOR", 8],
    # "unsigned long&&": ["NOR", 8],
    # "unsigned long||": ["NOR", 8],

    #Changes similar to unsigned int
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
    "long<<": ["DSLL", 8],
    "long>>": ["DSRL", 8],
    "long~": ["NOT", 8],

    # "long!": ["NOR", 8],
    # "long||": ["NOR", 8],
    # "long&&": ["NOR", 8],



    # DOUBLE, FLOAT, NOT HANDLED WITH NEW OPERATORS
    #<=, >, >=,!= pata nahi kya karenge
    "double+": ["ADD.D", 8],
    "double-": ["SUB.D", 8],
    "double*": ["MUL.D", 8],
    "double/": ["DIV.D", 8],
    "double<=": ["SLE", 8],
    "double<": ["C.LT.D", 8],
    "double>=": ["SGE", 8],
    "double>": ["SLT", 8],
    "double==": ["C.EQ.D", 8],
    "double!=": ["SNE", 8],

    #<=, >, >=,!= pata nahi kya karenge
    "float+": ["ADD.D", 4],
    "float-": ["SUB.D", 4],
    "float*": ["MUL.D", 4],
    "float/": ["DIV.D", 4],
    "float<=": ["SLE", 4],
    "float<": ["C.LT.D", 4],
    "float>=": ["SGE", 4],
    "float>": ["SLT", 4],
    "float==": ["C.EQ.D", 4],
    "float!=": ["SNE", 4],
    

    "+": ["ADD", 4],
}

#Handled type_int with [+,-,%,&,|,>>,<<,^,~,>,>=,<=,<,==,!=]
def binary_exp_mips(binexp, reg1, a1, reg2, a2, reg3, a3):
    mips = []
    type = ""
    op = ""
    for i in binexp:
        if(i.isalpha() or i == ' '):
            type += i
        else:
            op+= i
    mips.append(load_reg(reg1, a1, type))
    mips.append(load_reg(reg2, a2, type))
    mips.append(load_reg(reg3, a3, type))        
    if (op =="+" or op == "-") and type in TYPE_INT :        
        op = Binary_ops[binexp][0]
        mips.append([op,reg1,reg2,reg3])
    elif op =="%" and type in TYPE_INT :
        op = Binary_ops[binexp][0]
        mips.append([op,reg2,reg3])
        mips.append(["MFHI",reg1])
    elif op in BIN_BIT_OP and type in TYPE_INT:
        op = Binary_ops[binexp][0]
        mips.append([op,reg1,reg2,reg3])
    elif op == "~" and type in TYPE_INT:
        #only 2 regs will be given
        op = Binary_ops[binexp][0]
        mips.append([op,reg1,"$0",reg2])
    elif op == "<" and type in TYPE_INT:
        op = Binary_ops[binexp][0]
        mips.append([op, reg1, reg2, reg3])
    elif op == ">" and type in TYPE_INT:
        op = Binary_ops[binexp][0]
        mips.append([op, reg1, reg3, reg2])
    elif op == "<=" and type in TYPE_INT:
        op = Binary_ops[binexp][0]
        #check greater than and xor with 1
        mips.append([op, reg1, reg3, reg2])
        mips.append(["XORI",reg1,reg1,"0x1"])
    elif op == ">=" and type in TYPE_INT:
        op = Binary_ops[binexp][0]
        #check less than and xor with 1
        mips.append([op, reg1, reg2, reg3])
        mips.append(["XORI", reg1, reg1, "0x1"])
    elif op == "==" and type in TYPE_INT:
        op = Binary_ops[binexp][0]
        mips.append([op, reg1, reg2, reg3])
        mips.append(["SLTUI",reg1,reg1,"1"])
    elif op == "!=" and type in TYPE_INT:
        op = Binary_ops[binexp][0]
        mips.append([op, reg1, reg2, reg3])
        mips.append(["SLTUI",reg1,"$0",reg1])    

    mips.append(store_reg(reg1, a1, type))
    return mips
         


def store_reg(reg,addr,type):
    #mips = []
    instr = LOAD_INSTRUCTIONS[type]
    mips = [instr,reg,addr]
    return mips

def load_reg(reg,addr,type):
    #mips = []
    instr = STORE_INSTRUCTIONS[type]
    if(is_int(addr)):
        if type == "int" or type == "char" or type =="short":
            mips = ["ADDI",reg,"$0",addr]
        elif type == "long":
            mips = ["DADDI",reg,"$0",addr]
        elif type == "unsigned int" or type == "unsigned char" or type =="unsigned short":
            mips = ["ADDIU",reg,"$0",addr]
        elif type == "unsigned long":
            mips = ["DADDIU",reg,"$0",addr]      
    mips = [instr, reg, addr]
    return mips
