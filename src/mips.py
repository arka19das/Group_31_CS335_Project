
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
        
print(is_int("$(fp)"))        

def plus(reg1,a1,reg2,a2,reg3,a3):
    mips=[]
    mips.append(["LW",      {reg1},    {a1}])
    mips.append(["LW",      {reg2},    {a2}])
    mips.append(["LW",      {reg3},    {a3}])
    mips.append(["ADD",     {reg1},    {reg2},    {reg3}])
    mips.append(["SW",      {reg1},    {a1}])
    return mips


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

def store_reg(reg,addr,type):
    mips = []
    instr = LOAD_INSTRUCTIONS[type]
    mips.append[(instr,reg,addr)]
    return mips

def load_reg(reg,addr,type):
    mips = []
    instr = STORE_INSTRUCTIONS[type]
    mips.append[(instr, reg, addr)]
    return mips
