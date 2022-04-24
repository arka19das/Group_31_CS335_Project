﻿# CS335 Course Project

Building a Compiler from C to MIPS, implemented in Python

## Group Members:


| Name             | Roll No | Contribution % |
|------------------|---------|----------------|
| A. Kedarnath     | 190002  | 25%            |
| Akshay Gupta     | 190093  | 25%            |
| Arka Das         | 190175  | 25%            |
| Bisweswar Martha | 190239  | 25%            |

## Milestone 1

We created a specification of language for which compiler will be developed. For more details, check [here](./docs/manual.pdf)

## Milestone 2

We developed a lexical scanner using lex and yacc, which takes a C program with specifications mentioned above and generates a table of tokens with the corresponding lexeme, line number and column number of the token as output. To test an example, we use the testing script. To add your own test cases, name the file as, eg:- test_lexer_1, and then place it within the tests/lexer folder. To run the test case, use the testing script as mentioned below :-

## Milestone 3

We developed a parser. Description koi likhdo pls

## Milestone 2

Parser += Semantics + AST

## Using the testing script

### Lexer

```
# to test nth lexer testcase
./testing_script.sh lex <n>
```

### Parser

```
# to test nth parser testcase
./testing_script.sh parse <n>
```

### Semantics

```
# to test nth semantic testcase
./testing_script.sh semantic <n>
```
### Intermediate code_gen and activation record

```
python ./src/parser.py <testing_file_path> #command for testing
```
 The output ```3ac.txt``` shall have the 3ac.txt of the input file and ```activation_record.txt``` shall have the 3ac along with the offset with respect to the frame pointer or stack pointer when the final code would be generated. The __label_<number> denotes the labels, and __tmp_var_<number> are registers used by us to do various computations hence they will not have any offsets. 

### tag folder consists of the tests for this tag


# Rules for our grammar 

1. Declaration only at beginning of scope
2. `short`, `long`, `double`, `typedef` and `auto` removed
3. Global Constants are not allowed.
