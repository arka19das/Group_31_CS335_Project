#!/bin/bash


FILENO=$1
# shift
mkdir output
touch ./output/out_lexer_$FILENO.txt
python ./src/scanner.py.py ./tests/test_lexer_$FILENO.c  > ./output/out_lexer_$FILENO.txt
