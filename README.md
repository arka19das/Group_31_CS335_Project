# CS335 Course Project

Building a Compiler from C to MIPS, implemented in Python

## Group Members: 
* A. Kedarnath: 190002
* Akshay Gupta: 190093 
* Arka Das: 190175
* Bisweswar Martha: 190239 


## Milestone 1
We created a specification of language for which compiler will be developed. For more details, check [here](./docs/manual.pdf) 

## Milestone 2
We developed a lexical scanner using lex and yacc, which takes a C program with specifications mentioned above and generates a table of tokens with the corresponding lexeme, line number and column number of the token as output. To test an example, we use the testing script. To add your own test cases, name the file as, eg:- test_lexer_1, and then place it within the tests/lexer folder. To run the test case, use the testing script as mentiond below :-

### Using the testing script

```
# to test test_lexer_1 
./testing_script.sh 1
```
# Things to do
Illegal character, directly stop lexing and exit.  
New and delete keyword 
