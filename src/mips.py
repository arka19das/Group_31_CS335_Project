
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
    "char","unsigned char", "short","unsigned short", "int", "unsigned int", "long", "unsigned long"
]

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
    "unsigned int<=": ["SLEU", 4],
    "unsigned int<": ["SLTU", 4],
    #SGE and SGT not there in edumips, have to use SLTU changing the seq of registers
    "unsigned int>=": ["SGEU", 4],
    "unsigned int>": ["SGTU", 4],
    #SEQU, SNEU not there in edumips
    #"unsigned int==": ["XOR","SLTU $2 $2 1" 4],
    "unsigned int==": ["SEQU", 4],
    #"unsigned int!=": ["XOR","SLTU $2 $0 $2" 4],
    "unsigned int!=": ["SNEU", 4],
    
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

    "int<=": ["SLE", 4],
    "int<": ["SLT", 4],
    "int>=": ["SGE", 4],
    "int>": ["SGT", 4],
    "int==": ["SEQ", 4],
    "int!=": ["SNE", 4],

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

    "short<=": ["SLE", 2],
    "short<": ["SLT", 2],
    "short>=": ["SGE", 2],
    "short>": ["SGT", 2],
    "short==": ["SEQ", 2],
    "short!=": ["SNE", 4],
   
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
    "unsigned short<=": ["SLEU", 2],
    "unsigned short<": ["SLTU", 2],
    #SGE and SGT not there in edumips, have to use SLTU changing the seq of registers
    "unsigned short>=": ["SGEU", 2],
    "unsigned short>": ["SGTU", 2],
    #SEQU, SNEU not there in edumips
    #"unsigned int==": ["XOR","SLTU $2 $2 1" 4],
    "unsigned short==": ["SEQU", 2],
    #"unsigned int!=": ["XOR","SLTU $2 $0 $2" 4],
    "unsigned short!=": ["SNEU", 2],
    
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
    "unsigned char<=": ["SLEU", 4],
    "unsigned char<": ["SLTU", 4],
    #SGE and SGT not there in edumips, have to use SLTU changing the seq of registers
    "unsigned char>=": ["SGEU", 4],
    "unsigned char>": ["SGTU", 4],
    #SEQU, SNEU not there in edumips
    #"unsigned int==": ["XOR","SLTU $2 $2 1" 4],
    "unsigned char==": ["SEQU", 4],
    #"unsigned int!=": ["XOR","SLTU $2 $0 $2" 4],
    "unsigned char!=": ["SNEU", 4],
    
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
    
    "char<=": ["SLE", 4],
    "char<": ["SLT", 4],
    "char>=": ["SGE", 4],
    "char>": ["SGT", 4],
    "char==": ["SEQ", 4],
    "char!=": ["SNE", 4],
    
    "char&": ["AND", 4],
    "char^": ["XOR", 4],
    "char|": ["OR", 4],
    "char~": ["NOT", 4],
    "char>>": ["SRL", 4],
    "char<<": ["SLL", 4],

    # "char!": ["NOR", 4], 
    # "char&&": ["NOR", 4],
    # "char||": ["NOR", 4],
    

    #LONG, DOUBLE, FLOAT, UNSIGNED LONG NOT HANDLED WITH NEW OPERATORS
    #Changes similar to unsigned int
    "unsigned long+": ["DADDU", 8],
    "unsigned long-": ["DSUBU", 8],
    "unsigned long*": ["DMULTU", 8],
    "unsigned long/": ["DDIVU", 8],
    "unsigned long<=": ["SLEU", 8],
    "unsigned long<": ["SLTU", 8],
    "unsigned long>=": ["SGEU", 8],
    "unsigned long>": ["SGTU", 8],
    "unsigned long==": ["SEQU", 8],
    "unsigned long!=": ["SNEU", 8],
    "unsigned long&": ["AND", 8],
    "unsigned long^": ["XOR", 8],
    "unsigned long|": ["OR", 8],
    "unsigned long!": ["NOR", 8],
    "unsigned long~": ["NOT", 8],

    #Changes similar to unsigned int
    "long+": ["DADD", 8],
    "long-": ["DSUB", 8],
    "long*": ["DMULT", 8],
    "long/": ["DDIV", 8],
    "long<=": ["SLE", 8],
    "long<": ["SLT", 8],
    "long>=": ["SGE", 8],
    "long>": ["SGT", 8],
    "long==": ["SEQ", 8],
    "long!=": ["SNE", 8],
    "long&": ["AND", 8],
    "long^": ["XOR", 8],
    "long|": ["OR", 8],
    "long!": ["NOR", 8],
    "long~": ["NOT", 8],

    #<=, >, >=,!= pata nahi kya karenge
    "double+": ["ADD.D", 8],
    "double-": ["SUB.D", 8],
    "double*": ["MUL.D", 8],
    "double/": ["DIV.D", 8],
    "double<=": ["SLE", 8],
    "double<": ["C.LT.D", 8],
    "double>=": ["SGE", 8],
    "double>": ["SGT", 8],
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
    "float>": ["SGT", 4],
    "float==": ["C.EQ.D", 4],
    "float!=": ["SNE", 4],
    

    "+": ["ADD", 4],
}


def binary_exp_mips(binexp, reg1, a1, reg2, a2, reg3, a3):
    mips = []
    type = ""
    op = ""
    for i in binexp:
        if(i.isalpha() or i == ' '):
            type += i
        else:
            op+= i
    if (op =="+" or op == "-") and type in TYPE_INT :        
        #mips.append(["LW",      {reg1},    {a1}])
        mips.append(load_reg(reg1, a1, type))
        #mips.append(["LW",      {reg2},    {a2}])
        mips.append(load_reg(reg2, a2, type))
        #mips.append(["LW",      {reg3},    {a3}])
        mips.append(load_reg(reg3, a3, type))
        #mips.append(["ADD",     {reg1},    {reg2},    {reg3}])
        op = Binary_ops[binexp]
        mips.append([op,reg1,reg2,reg3])
        #mips.append(["SW",      {reg1},    {a1}])
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
        instr = "LI"
    mips = [instr, reg, addr]
    return mips
