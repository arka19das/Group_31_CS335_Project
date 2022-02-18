#!/bin/bash

lex() {
    [ -d "output/lexer" ] || mkdir -p output/lexer
    python ./src/scanner.py ./tests/lexer/test_lexer_"$1".c > ./output/lexer/out_lexer_"$1".txt 
}

parse() {
    [ -d "output/parser" ] || mkdir -p output/parser
    [ -f "src/parsetab.py" ] && rm src/parsetab.py
    python ./src/parser.py -input ./tests/parser/test_parser_"$1".c
    mv ./src/parser.out ./output/parser/out_parser_"$1".out
    python ./src/graph.py ./output/parser/out_parser_"$1".out \
        ./output/parser/out_parser_"$1".dot
    sfdp -x -Goverlap=scale -Tsvg ./output/parser/out_parser_"$1".dot\
        -o ./output/parser/out_graph_"$1".svg
}

usage="./testing_script.sh <lex|parse> <test_number>"

[ -d "output" ] || mkdir output

if [[ $# -ne 2 ]]; 
    then echo "$usage" && exit
fi

case $1 in 
    "lex") lex "$2" ;;
    "parse") parse "$2" ;;
    *) echo "$usage";;
esac
