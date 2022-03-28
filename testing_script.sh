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

semantic() {
    [ -d "output/semantic" ] || mkdir -p output/semantic
    [ -f "src/parsetab.py" ] && rm src/parsetab.py
    python ./src/parser.py -input ./tests/semantics/test_semantics_"$1".c -w
    [ -d "output/semantic/symbol_table_dump_$1" ] && rm -rf output/semantic/symbol_table_dump_"$1"
    [ -d "symbol_table_dump" ] && mv symbol_table_dump ./output/semantic/symbol_table_dump_"$1" || echo "CSV Dump Failed"
    [ -f "ast.dot" ] && mv ast.dot ./output/semantic/semantic_"$1".dot || echo "AST Not Formed"
}

usage="./testing_script.sh <lex|parse|semantic> <test_number>"

[ -d "output" ] || mkdir output

if [[ $# -ne 2 ]]; 
    then echo "$usage" && exit
fi

case $1 in 
    "lex") lex "$2" ;;
    "parse") parse "$2" ;;
    "semantic") semantic "$2" ;;
    *) echo "$usage";;
esac
