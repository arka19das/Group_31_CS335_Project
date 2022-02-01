#!/bin/bash

FILENO=$1
# shift
[ -d "output" ] || mkdir output
touch ./output/out_lexer_$FILENO.txt
python ./src/scanner.py ./tests/lexer/test_lexer_$FILENO.c >./output/out_lexer_$FILENO.txt
