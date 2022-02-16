ERROR: parser_incomplete.py:287: Symbol 'BOOL' used, but not defined as a token or a rule
ERROR: parser_incomplete.py:290: Symbol 'TYPE_NAME' used, but not defined as a token or a rule
ERROR: parser_incomplete.py:580: Symbol 'declaration_list' used, but not defined as a token or a rule
ERROR: parser_incomplete.py:582: Symbol 'declaration_list' used, but not defined as a token or a rule
WARNING: Token 'BOOLEAN' defined, but not used
WARNING: Token 'FALSE' defined, but not used
WARNING: Token 'TRUE' defined, but not used
WARNING: Token 'UNION' defined, but not used
WARNING: There are 4 unused tokens
WARNING: Symbol 'translation_unit' is unreachable
WARNING: Symbol 'external_declaration' is unreachable
Traceback (most recent call last):
  File "parser_incomplete.py", line 644, in <module>
    parser = yacc.yacc()
  File "/home/arkadas/anaconda3/lib/python3.7/site-packages/ply/yacc.py", line 3432, in yacc
    raise YaccError('Unable to build parser')
ply.yacc.YaccError: Unable to build parser
