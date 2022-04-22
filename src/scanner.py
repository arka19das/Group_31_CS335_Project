# line 101 warning
import ply.lex as lex
import sys
import argparse


class Lexer(object):
    error_flag = False
    reserved = {
        "auto": "AUTO",
        "break": "BREAK",
        "bool": "BOOL",
        "case": "CASE",
        "char": "CHAR",
        "const": "CONST",
        "continue": "CONTINUE",
        "default": "DEFAULT",
        "do": "DO",
        # "double": "DOUBLE",
        "else": "ELSE",
        "float": "FLOAT",
        "for": "FOR",
        "goto": "GOTO",
        "if": "IF",
        "int": "INT",
        # "long": "LONG",
        "return": "RETURN",
        "short": "SHORT",
        "signed": "SIGNED",
        "sizeof": "SIZEOF",
        "struct": "STRUCT",
        "switch": "SWITCH",
        "typedef": "TYPEDEF",  # "union": "UNION",  # temporarily having union
        "unsigned": "UNSIGNED",
        "void": "VOID",
        "while": "WHILE",
        # "bool": "BOOLEAN",  # newly added
        # "true": "TRUE",  # newly added might be removed
        # "false": "FALSE",  # newly added might be removed
    }

    tokens = list(reserved.values()) + [
        "IDENTIFIER",
        "FLOAT_CONSTANT",
        "HEX_CONSTANT",
        "OCT_CONSTANT",
        "INT_CONSTANT",
        "CHAR_CONSTANT",
        "STRING_LITERAL",
        "RIGHT_ASSIGN",
        "LEFT_ASSIGN",
        "ADD_ASSIGN",
        "SUB_ASSIGN",
        "MUL_ASSIGN",
        "DIV_ASSIGN",
        "MOD_ASSIGN",
        "AND_ASSIGN",
        "XOR_ASSIGN",
        "OR_ASSIGN",
        "RIGHT_OP",
        "LEFT_OP",
        "INC_OP",
        "DEC_OP",
        "INHERITANCE_OP",  # maybe remove later
        "PTR_OP",
        "LOGICAL_AND_OP",
        "LOGICAL_OR_OP",
        "LE_OP",
        "GE_OP",
        "EQ_OP",
        "NE_OP",
        "SEMICOLON",
        "LEFT_CURLY_BRACKET",
        "RIGHT_CURLY_BRACKET",
        "COMMA",
        "COLON",
        "EQ",
        "LEFT_BRACKET",
        "RIGHT_BRACKET",
        "LEFT_THIRD_BRACKET",
        "RIGHT_THIRD_BRACKET",
        "DOT",
        "BITWISE_AND",
        "BITWISE_XOR",
        "BITWISE_NOT",
        "LOGICAL_NOT",
        "MINUS",
        "PLUS",
        "MULTIPLY",
        "DIVIDE",
        "MOD",
        "LESS",
        "GREATER",
        #'EXPONENT',
        "BITWISE_OR",
        "QUESTION",
        "TYPE_NAME",  ##############NOT SURE of implications############
    ]

    TYPE_NAMES = []
    data = ""
    def t_TRUE(self, t):
        r"true"
        t.type = "INT_CONSTANT"
        t.value = "1"
        return t

    def t_FALSE(self, t):
        r"false"
        t.type = "INT_CONSTANT"
        t.value = "0"
        return t

    def t_BOOLEAN(self, t):
        r"bool"
        t.type = "INT"
        t.value = "int"
        return t

    def t_IDENTIFIER(self, t):
        r"[a-zA-Z_][a-zA-Z0-9_]*"
        t.type = self.reserved.get(t.value, "IDENTIFIER")
        if t.type == "IDENTIFIER":
            if t.value in self.TYPE_NAMES:
                t.type = "TYPE_NAME"
        # incomplete
        return t

    def t_NEWLINE(self, t):
        r"\n+"
        t.lexer.lineno += t.value.count("\n")

    def t_comment(self, t):
        r"/\*(.|\n)*?\*/ | //(.)*?(\n|\Z)"
        t.lexer.lineno += t.value.count("\n")

    def t_preprocessor(self, t):
        r"\#(.)*?\n"
        t.lexer.lineno += 1

    t_INT_CONSTANT = r"[0-9]+([uU][lL][lL]|[uU][lL]|[lL][lL]|[uU]|[lL])?"  # u,l,U,L,ul,ull,ll,Ul,Ull,ULL,UL
    t_HEX_CONSTANT = r"0[xX][0-9a-fA-F]+([uU][lL][lL]|[uU][lL]|[lL][lL]|[uU]|[lL])?"
    t_OCT_CONSTANT = r"0[0-7]+([uU][lL][lL]|[uU][lL]|[lL][lL]|[uU]|[lL])?"
    t_FLOAT_CONSTANT = r"((\d+)(\.\d+)(e(\+|-)?(\d+))? | (\d+)\.?e(\+|-)?(\d+)| (\.\d+)(e(\+|-)?(\d+))?)([lL]|[fF])?"
    t_STRING_LITERAL = r"\"([^\"\\\n]|(\\.))*\""
    t_CHAR_CONSTANT = r"(L)?\'([^\\\n]|(\\.))*?\'"
    t_RIGHT_ASSIGN = r">>="
    t_LEFT_ASSIGN = r"<<="
    t_ADD_ASSIGN = r"\+="
    t_SUB_ASSIGN = r"-="
    t_MUL_ASSIGN = r"\*="
    t_DIV_ASSIGN = r"/="
    t_MOD_ASSIGN = r"%="
    t_AND_ASSIGN = r"&="
    t_XOR_ASSIGN = r"\^="
    t_OR_ASSIGN = r"\|="
    t_RIGHT_OP = r">>"
    t_LEFT_OP = r"<<"
    t_INC_OP = r"\+\+"
    t_DEC_OP = r"--"
    t_INHERITANCE_OP = r"<-"
    t_PTR_OP = r"->"
    t_LOGICAL_AND_OP = r"&&"
    t_LOGICAL_OR_OP = r"\|\|"
    t_LE_OP = r"<="
    t_GE_OP = r">="
    t_EQ_OP = r"=="
    t_NE_OP = r"!="
    t_BITWISE_XOR = r"\^"
    t_SEMICOLON = r";"
    t_LEFT_CURLY_BRACKET = r"({)"  # |<%
    t_RIGHT_CURLY_BRACKET = r"(})"  # |%>
    t_COMMA = r","
    t_COLON = r":"
    t_EQ = r"="
    t_LEFT_BRACKET = r"\("
    t_RIGHT_BRACKET = r"\)"
    t_LEFT_THIRD_BRACKET = r"(\[)"  # |<:
    t_RIGHT_THIRD_BRACKET = r"(\])"  # |:>
    t_DOT = r"\."
    t_BITWISE_AND = r"&"
    t_BITWISE_NOT = r"~"
    t_LOGICAL_NOT = r"!"
    t_MINUS = r"-"
    t_PLUS = r"\+"
    t_MULTIPLY = r"\*"
    t_DIVIDE = r"/"
    t_MOD = r"%"
    t_LESS = r"<"
    t_GREATER = r">"
    # t_EXPONENT = r"\^"
    t_BITWISE_OR = r"\|"
    t_QUESTION = r"\?"

    t_ignore = " \t"

    def t_error(self, t):
        print("Illegal character '%s' at %d" % (t.value[0], self.find_column( t)))
        self.error_flag = True
        t.lexer.skip(1)

    def find_column(self, token):
        line_start = self.data.rfind("\n", 0, token.lexpos) + 1
        return (token.lexpos - line_start) + 1

    # Build the lexer
    def build(self, **kwargs):
        # lex.lex(debug=1)
        # lexer=lex.lex(optimize=1)
        self.lexer = lex.lex(module=self, **kwargs)

    def test(self, data):
        self.lexer.input(data)
        self.data=data
        while self.error_flag == False:
            tok = self.lexer.token()
            if self.error_flag == True or not tok:
                break

            print(
                "|{: <20} |{: <20} |{: >20} |{:>20}|".format(
                    tok.type, tok.value, tok.lineno, self.find_column(data, tok)
                )
            )


if __name__ == "__main__":
    with open(str(sys.argv[1]), "r+") as file:
        data = file.read()

        print("Reading..." + str(sys.argv[1]))
        print(
            "----------------------------------------------------------------------------------------"
        )
        print(data)
        file.close()
        print(
            "----------------------------------------------------------------------------------------"
        )
        print(
            "----------------------------------------------------------------------------------------"
        )
        print(
            "|{: <20} |{: <20} |{: >20} |{:>20}|".format(
                "Token Type", "Token Name", "Line Nunmber", "Column Number"
            )
        )
        print(
            "|{: <20} |{: <20} |{: >20} |{:>20}|".format(
                "==========", "==========", "============", "============="
            )
        )

        myobj = Lexer()
        myobj.build()
        myobj.test(data)
        print(
            "----------------------------------------------------------------------------------------"
        )
        # lex.runmain(lexer, data)
        # print(TYPE_NAMES)
