### Group 31
### Author: Bisweswar Martha, A Kedarnath, Akshay Gupta, Arka Das


# The subset C Reference Manual {#the-gnu-c-reference-manual .settitle align="center"}

[]{#SEC_Contents}

This is a reference manual containing the features for the subset of C programming language(GNU C99) for which we are developing our compiler for which we are going to develop a compiler using the implementation language Python to convert it to MIPS language.

This shall contain a subset of all the features of C99 along with slight extensions to the base language. All details have been elaborated below.

------------------------------------------------------------------------



[]{#Lexical-Elements}

## 1 Lexical Elements {#lexical-elements .chapter}

[]{#index-lexical-elements}

This chapter describes the lexical elements that make up C source code after preprocessing.
These elements are called *tokens*.
There are five types of tokens: keywords, identifiers, constants, operators, and separators.
White space, sometimes required to separate tokens, is also described in this chapter.

[]{#Identifiers}


[]{#Identifiers-1}

### 1.1 Identifiers {#identifiers .section}

[]{#index-identifiers}

Identifiers are sequences of characters used for naming variables, functions, new data types, and preprocessor macros.
You can include letters and decimal digits in identifiers. The first character of an identifier cannot be a digit. Identifiers are case sensitive.
Unlike C99, we do not allow underscores in a variable

------------------------------------------------------------------------

[]{#Keywords}


[]{#Keywords-1}

### 1.2 Keywords {#keywords .section}

[]{#index-keywords}

Keywords are special identifiers reserved for use as part of the programming language itself.
You cannot use them for any other purpose.

Here is a list of keywords recognized by C:

```example
break case char continue default do else
float for goto if intreturn signed sizeof
struct switch unsigned void while
```


------------------------------------------------------------------------

[]{#Constants}


[]{#Constants-1}

### 1.3 Constants {#constants .section}

[]{#index-constants}

A constant is a literal numeric or character value, such as `5` or `'m'`.
All constants are of a particular data type; you can use type casting to explicitly specify the type of a constant.

------------------------------------------------------------------------

[]{#Integer-Constants}


[]{#Integer-Constants-1}

#### 1.3.1 Integer Constants {#integer-constants .subsection}

[]{#index-integer-constants} []{#index-constants_002c-integer}

An integer constant is a sequence of digits, with an optional prefix to denote a number base.

If the sequence of digits is preceded by `0x` or `0X`, then the constant is considered to be hexadecimal. Hexadecimal values may use the digits from 0 to 9, as well as the letters `a` to `f` and `A` to `F`.

If the first digit is 0 (zero), and the next character is not '`x`{.sample}' or '`X`{.sample}', then the constant is considered to be octal (base 8).
Octal values may only use the digits from 0 to 7; 8 and 9 are not allowed.

In all other cases, the sequence of digits is assumed to be decimal.

There are various integer data types, for short integers, long integers, signed integers, and unsigned integers.
You can force an integer constant to be of a long and/or unsigned integer type by appending a sequence of one or more letters to the end of the constant:

`u` \ `U` :   Unsigned integer type.

Float Constants are currently not allowed.

------------------------------------------------------------------------

[]{#Character-Constants}


[]{#Character-Constants-1}

#### 1.3.2 Character Constants {#character-constants .subsection}

[]{#index-character-constants} []{#index-constants_002c-character}

A character constant is usually a single character enclosed within single quotation marks, such as `'Q'`.
A character constant is of type `int` by default.

Some characters, such as the single quotation mark character itself, cannot be represented using only one character.
To represent such characters, there are several "escape sequences" that you can use:

`\\` :   Backslash character.

`\?` :   Question mark character.

`\'` :   Single quotation mark.

`\"` :   Double quotation mark.

`\n` :   Newline character.

`\t` :   Horizontal tab.

`\o, \oo, \ooo` :   Octal number.

`\xh, \xhh, \xhhh, …` :   Hexadecimal number.

To use any of these escape sequences, enclose the sequence in single quotes, and treat it as if it were any other character.

The octal number escape sequence is the backslash character followed by one, two, or three octal digits.

The hexadecimal escape sequence is the backslash character, followed by `x` and an unlimited number of hexadecimal digits. While the length of possible hexadecimal digit strings is unlimited, the number of character constants in any given character set is not.


------------------------------------------------------------------------

[]{#String-Constants}
[]{#String-Constants-1}

#### 1.3.3 String Constants {#string-constants .subsection}

[]{#index-string-constants} []{#index-string-literals}

A string constant is a sequence of zero or more characters, digits, and escape sequences enclosed within double quotation marks.
A string constant is of type "array of characters".
All string constants contain a null termination character (`\0`) as their last character.
Strings are stored as arrays of characters, with no inherent size attribute.
The null termination character lets string-processing functions know where the string ends.

Adjacent string constants are concatenated (combined) into one string, with the null termination character added to the end of the final concatenated string.

A string cannot contain double quotation marks, as double quotation marks are used to enclose the string.
To include the double quotation mark character in a string, use the `\"` escape sequence.
You can use any of the escape sequences that can be used as character constants in strings.

If a string is too long to fit on one line, you can use a backslash `\` to break it up onto separate lines.

To insert a newline character into the string, so that when the string is printed it will be printed on two different lines, you can use the newline escape sequence '`\n`{.sample}'.

------------------------------------------------------------------------

[]{#Operators}


[]{#Operators-1}

### 1.4 Operators {#operators .section}

[]{#index-operators-as-lexical-elements}

An operator is a special token that performs an operation, such as addition or subtraction, on either one, two, or three operands.
Full coverage of operators can be found in a later chapter.

------------------------------------------------------------------------

[]{#Separators}


[]{#Separators-1}

### 1.5 Separators {#separators .section}

[]{#index-separators}

A separator separates tokens.
White space (see next section) is a separator, but it is not a token.
The other separators are all single-character tokens themselves:
```example
( ) [ ] { } ; , . :
```

------------------------------------------------------------------------

[]{#White-Space}


[]{#White-Space-1}

### 1.6 White Space {#white-space .section}

[]{#index-white-space}

White space is the collective term used for several characters: the space character, the tab character, the newline character, the vertical tab character, and the form-feed character.
White space is ignored, and is therefore optional, except when it is used to separate tokens.

Although you must use white space to separate many tokens, no white space is required between operators and operands, nor is it required between other separators and that which they separate.
Furthermore, wherever one space is allowed, any amount of white space is allowed.
In string constants, spaces and tabs are not ignored; rather, they are part of the string.

------------------------------------------------------------------------

[]{#Data-Types}


[]{#Data-Types-1}

## 2 Data Types {#data-types .chapter}

[]{#index-data-types} []{#index-types}
------------------------------------------------------------------------

[]{#Primitive-Types}


[]{#Primitive-Data-Types}

### 2.1 Primitive Data Types {#primitive-data-types .section}

[]{#index-primitive-data-types} []{#index-data-types_002c-primitive}
[]{#index-types_002c-primitive}
------------------------------------------------------------------------

[]{#Integer-Types}


[]{#Integer-Types-1}

#### 2.1.1 Integer Types {#integer-types .subsection}

[]{#index-integer-types} []{#index-data-types_002c-integer}
[]{#index-types_002c-integer}

The integer data types range in size from at least 8 bits to at least 64 bits.
You should use integer types for storing whole number values (and the `char` data type for storing characters).
The sizes and ranges listed for these types are minimums; depending on your computer platform, these sizes and ranges may be larger.

While these ranges provide a natural ordering, the standard does not require that any two types have a different range.
For example, it is common for `int` to have the same range.
The standard even allows `signed char` to have the same range, though such platforms are very unusual.

- `signed char` []{#index-signed-char-data-type}\
  The 8-bit `signed char` data type can hold integer values in the range of -128 to 127.
- `unsigned char` []{#index-unsigned-char-data-type}\
  The 8-bit `unsigned char` data type can hold integer values in the range of 0 to 255.
- `char` []{#index-char-data-type}\
  Depending on your system, the `char` data type is defined as having
  the same range as either the `signed char` or the `unsigned char`
  data type (they are three distinct types, however). By convention,
  you should use the `char` data type specifically for storing ASCII
  characters (such as `` `m' ``), including escape sequences (such as
  `` `\n' ``).
- `int` []{#index-int-data-type}\
  The 32-bit `int` data type can hold integer values in the range of
  -2,147,483,648 to 2,147,483,647.
- `unsigned int` []{#index-unsigned-int-data-type}\
  The 32-bit `unsigned int` data type can hold integer values in the
  range of 0 to 4,2.2.967,295. 

------------------------------------------------------------------------

[]{#Real-Number-Types}


[]{#Real-Number-Types-1}

#### 2.1.2 Real Number Types {#real-number-types .subsection}

[]{#index-real-number-types} []{#index-floating-point-types}
[]{#index-data-types_002c-real-number}
[]{#index-data-types_002c-floating-point}
[]{#index-types_002c-real-number} []{#index-types_002c-floating-point}

There are three data types that represent fractional numbers.

-   `float` []{#index-float-data-type}\
    The `float` data type is the smallest of the three floating point
    types. Its minimum value is no greater than `1e-37`. Its maximum
    value is no less than `1e37`.

All floating point data types are signed; trying to use
`unsigned float`, for example, will cause a compile-time error.

------------------------------------------------------------------------

[]{#Structures}
[]{#Structures-1}

### 2.2.Structures {#structures .section}

[]{#index-structures} []{#index-types_002c-structure}
[]{#index-data-types_002c-structure}

A structure is a programmer-defined data type made up of variables of other data types (possibly including other structure types).

------------------------------------------------------------------------

[]{#Defining-Structures}


[]{#Defining-Structures-1}

#### 2.2.1 Defining Structures {#defining-structures .subsection}

[]{#index-defining-structures} []{#index-structures_002c-defining}

You define a structure using the `struct` keyword followed by the declarations of the structure's members, enclosed in braces.
You declare each member of a structure just as you would normally declare a variable---using the data type followed by one or more variable names separated by commas, and optionally ending with a semicolon.
Then end the structure definition with a semicolon after the closing brace.

You should also include a name for the structure in between the `struct` keyword and the opening brace.
This is optional, but if you leave it out, you can't refer to that structure data type later on.

It is possible for a structure type to contain a field which is a pointer to the same type.

A struct can not contain other structs as fields

------------------------------------------------------------------------

[]{#Declaring-Structure-Variables}

[]{#Declaring-Structure-Variables-1}

#### 2.2.2 Declaring Structure Variables {#declaring-structure-variables .subsection}

[]{#index-declaring-structure-variables}
[]{#index-structure-variables_002c-declaring}

You can declare variables of a structure type when both you initially
define the structure and after the definition, provided you gave the
structure type a name.

------------------------------------------------------------------------

[]{#Declaring-Structure-Variables-at-Definition}


[]{#Declaring-Structure-Variables-at-Definition-1}

#### 2.2.2.1 Declaring Structure Variables at Definition {#declaring-structure-variables-at-definition .subsubsection}

[]{#index-declaring-structure-variables-at-definition}
[]{#index-structure-variables_002c-declaring-at-definition}

You can declare variables of a structure type when you define the
structure type by putting the variable names after the closing brace of
the structure definition, but before the final semicolon. You can
declare more than one such variable by separating the names with commas.

------------------------------------------------------------------------

[]{#Declaring-Structure-Variables-After-Definition}


[]{#Declaring-Structure-Variables-After-Definition-1}

#### 2.2.2.2 Declaring Structure Variables After Definition {#declaring-structure-variables-after-definition .subsubsection}

[]{#index-declaring-structure-variables-after-definition}
[]{#index-structure-variables_002c-declaring-after-definition}

You can declare variables of a structure type after defining the
structure by using the `struct` keyword and the name you gave the
structure type, followed by variable names separated by commas.

------------------------------------------------------------------------

[]{#Accessing-Structure-Members}
[]{#Accessing-Structure-Members-1}

#### 2.2.3 Accessing Structure Members {#accessing-structure-members .subsection}

[]{#index-accessing-structure-members}
[]{#index-structure-members_002c-accessing}

You can access the members of a structure variable using the member
access operator (`.`) You put the name of the structure variable on the left side of the operator, and the name of the member on the right side.

------------------------------------------------------------------------

[]{#Size-of-Structures}


[]{#Size-of-Structures-1}

#### 2.2.4 Size of Structures {#size-of-structures .subsection}

[]{#index-size-of-structures} []{#index-structures_002c-size-of}

The size of a structure type is equal to the sum of the size of all of its members

------------------------------------------------------------------------

[]{#Arrays}


[]{#Arrays-1}

### 2.3 Arrays {#arrays .section}

[]{#index-arrays} []{#index-types_002c-array}
[]{#index-data-types_002c-array}

An array is a data structure that lets you store one or more elements consecutively in memory.
In C, array elements are indexed beginning at position zero, not one.

------------------------------------------------------------------------

[]{#Declaring-Arrays}


[]{#Declaring-Arrays-1}

#### 2.3.1 Declaring Arrays {#declaring-arrays .subsection}

[]{#index-declaring-arrays} []{#index-arrays_002c-declaring}

You declare an array by specifying the data type for its elements, its name, and the number of elements it can store.

For standard C code, the number of elements in an array must be positive.

The number of elements can be as small as zero.
Zero-length arrays are useful as the last element of a structure which is really a header for a variable-length object:

------------------------------------------------------------------------

[]{#Accessing-Array-Elements}


[]{#Accessing-Array-Elements-1}

#### 2.3.3 Accessing Array Elements {#accessing-array-elements .subsection}

[]{#index-accessing-array-elements}
[]{#index-array-elements_002c-accessing}

You can access the elements of an array by specifying the array name,
followed by the element index, enclosed in brackets. Remember that the
array elements are numbered starting with zero.

------------------------------------------------------------------------

[]{#Arrays-of-Structures}


[]{#Arrays-of-Structures-1}

#### 2.3.5 Arrays of Structures {#arrays-of-structures .subsection}

[]{#index-arrays-of-structures} []{#index-structures_002c-arrays-of}

You can create an array of a structure type just as you can an array of
a primitive data type.

As with initializing structures which contain structure members, the
additional inner grouping braces are optional. But, if you use the
additional braces, then you can partially initialize some of the
structures in the array, and fully initialize others:

After initialization, you can still access the structure members in the
array using the member access operator. You put the array name and
element number (enclosed in brackets) to the left of the operator, and
the member name to the right.


------------------------------------------------------------------------

[]{#Pointers}


[]{#Pointers-1}

### 2.4 Pointers {#pointers .section}

[]{#index-pointers} []{#index-types_002c-pointer}
[]{#index-data-types_002c-pointer}

Pointers hold memory addresses of stored constants or variables. For any
data type, including both primitive types and custom types, you can
create a pointer that holds the memory address of an instance of that
type.

------------------------------------------------------------------------

[]{#Declaring-Pointers}


[]{#Declaring-Pointers-1}

#### 2.4.1 Declaring Pointers {#declaring-pointers .subsection}

[]{#index-declaring-pointers} []{#index-pointers_002c-declaring}

You declare a pointer by specifying a name for it and a data type. The
data type indicates of what type of variable the pointer will hold
memory addresses.

To declare a pointer, include the indirection operator (`*`)
before the identifier. Here is the
general form of a pointer declaration:

```example
data-type * name;
```

White space is not significant around the indirection operator. When declaring multiple pointers in the same statement, you must explicitly declare each as a pointer, using the indirection operator:

------------------------------------------------------------------------

[]{#Initializing-Pointers}
[]{#Initializing-Pointers-1}

#### 2.4.2 Initializing Pointers {#initializing-pointers .subsection}

[]{#index-initializing-pointers} []{#index-pointers_002c-initializing}

You can initialize a pointer when you first declare it by specifying a
variable address to store in it.

Note the use of the address operator, used to get the memory address of a variable.
After you declare a pointer, you do *not* use the indirection operator with the pointer's name when assigning it a new address to point to.
On the contrary, that would change the value of the variable that the points to, not the value of the pointer itself.

The value stored in a pointer is an integral number: a location within the computer's memory space.
If you are so inclined, you can assign pointer values explicitly using literal integers, casting them to the appropriate pointer type.
However, we do not recommend this practice unless you need to have extremely fine-tuned control over what is stored in memory, and you know exactly what you are doing.
It would be all too easy to accidentally overwrite something that you did not intend to.
Most uses of this technique are also non-portable.

It is important to note that if you do not initialize a pointer with the address of some other existing object, it points nowhere in particular and will likely make your program crash if you use it (formally, this kind of thing is called *undefined behavior*).

------------------------------------------------------------------------

[]{#Pointers-to-Structures}


[]{#Pointers-to-Structures-1}

#### 2.4.4 Pointers to Structures {#pointers-to-structures .subsection}

[]{#index-pointers-to-structures} []{#index-structures_002c-pointers-to}

You can create a pointer to a structure type just as you can a pointer
to a primitive data type.

You can access the members of a structure variable through a pointer,
but you can't use the regular member access operator anymore. Instead,
you have to use the indirect member access operator (`->`)


------------------------------------------------------------------------
------------------------------------------------------------------------

[]{#Expressions-and-Operators-1}

## 3 Expressions and Operators {#expressions-and-operators .chapter}

------------------------------------------------------------------------

[]{#Expressions}

[]{#Expressions-1}

### 3.1 Expressions {#expressions .section}

[]{#index-expressions}

An *expression* consists of at least one operand and zero or more
operators. Operands are typed objects such as constants, variables, and
function calls that return values. 

[]{#index-operators}

An *operator* specifies an operation to be performed on its operand(s).
Operators may have one, two, or three operands, depending on the
operator.

------------------------------------------------------------------------

[]{#Assignment-Operators}
[]{#Assignment-Operators-1}

### 3.2 Assignment Operators {#assignment-operators .section}

Assignment operators store values in variables. C provides several
variations of assignment operators. The standard assignment operator `=` simply stores the value of its right operand in the variable specified by its left operand. As with all assignment operators, the left operand cannot be a literal or constant value.

------------------------------------------------------------------------

[]{#Incrementing-and-Decrementing}
[]{#Incrementing-and-Decrementing-1}

### 3.3 Incrementing and Decrementing {#incrementing-and-decrementing .section}

[]{#index-increment-operator} []{#index-decrement-operator}
[]{#index-operator_002c-increment} []{#index-operator_002c-decrement}

The increment operator `++` adds 1 to its operand. The operand must be a
either a variable of one of the primitive data types or a pointer. You can apply the increment operator either before or after the operand.  A prefix increment adds 1 before the operand is evaluated. A postfix increment adds 1 after the operand is evaluated. 

Likewise, you can subtract 1 from an operand using the decrement
operator `--`. The concepts of prefix and postfix application apply here as with the increment operator.

------------------------------------------------------------------------

[]{#Arithmetic-Operators}


[]{#Arithmetic-Operators-1}

### 3.4 Arithmetic Operators {#arithmetic-operators .section}

[]{#index-arithmetic-operators} []{#index-operators_002c-arithmetic}

C provides operators for standard arithmetic operations: addition,
subtraction, multiplication, and division, along with modular division
and negation. (Note that you can add and subtract memory pointers, but you cannot multiply or divide them)

Integer division of positive values truncates towards zero, so 5/3 is 1.
However, if either operand is negative, the direction of rounding is
implementation-defined.

You use the modulus operator `%` to obtain the remainder produced by
dividing its two operands. The operands must be
expressions of a primitive data type.

Modular division returns the remainder produced after performing integer
division on the two operands. The operands must be of a primitive
integer type.


If the operand you use with the negative operator is of an unsigned data
type, then the result cannot negative, but rather is the maximum value
of the unsigned data type, minus the value of the operand.

Numeric values are assumed to be positive unless explicitly made
negative.

------------------------------------------------------------------------

[]{#Comparison-Operators}

[]{#Comparison-Operators-1}

### 3.5 Comparison Operators {#comparison-operators .section}

[]{#index-comparison-operators} []{#index-operators_002c-comparison}

You use the comparison operators to determine how two operands relate to
each other: are they equal to each other, is one larger than the other,
is one smaller than the other, and so on. When you use any of the
comparison operators, the result is either 1 or 0, meaning true or
false, respectively.

(In the following code examples, the variables `x` and `y` stand for any
two expressions of arithmetic types, or pointers.)

The equal-to operator `==` tests its two operands for equality. The
result is 1 if the operands are equal, and 0 if the operands are not
equal.

The not-equal-to operator `!=` tests its two operands for inequality.
The result is 1 if the operands are not equal, and 0 if the operands
*are* equal.

------------------------------------------------------------------------

[]{#Logical-Operators}


[]{#Logical-Operators-1}

### 3.6 Logical Operators {#logical-operators .section}

[]{#index-logical-operators}

Logical operators test the truth value of a pair of operands. Any
nonzero expression is considered true in C, while an expression that
evaluates to zero is considered false.

The logical conjunction operator `&&` tests if two expressions are both
true. If the first expression is false, then the second expression is
not evaluated.


The logical disjunction operator `||` tests if at least one of two
expressions it true. If the first expression is true, then the second
expression is not evaluated.


You can prepend a logical expression with a negation operator `!` to
flip the truth value.



------------------------------------------------------------------------

[]{#Bit-Shifting}


[]{#Bit-Shifting-1}

### 3.7 Bit Shifting {#bit-shifting .section}

[]{#index-bit-shifting} []{#index-shifting}

You use the left-shift operator `<<` to shift its first operand's bits
to the left. The second operand denotes the number of bit places to
shift. Bits shifted off the left side of the value are discarded; new
bits added on the right side will all be 0.


Similarly, you use the right-shift operator `>>` to shift its first
operand's bits to the right. Bits shifted off the right side are
discarded; new bits added on the left side are *usually* 0, but if the
first operand is a signed negative value, then the added bits will be
either 0 *or* whatever value was previously in the leftmost bit
position.


For both `<<` and `>>`, if the second operand is greater than the
bit-width of the first operand, or the second operand is negative, the
behavior is undefined.

------------------------------------------------------------------------

[]{#Bitwise-Logical-Operators}


[]{#Bitwise-Logical-Operators-1}

### 3.8 Bitwise Logical Operators {#bitwise-logical-operators .section}

[]{#index-bitwise-logical-operators}
[]{#index-logical-operators_002c-bitwise}

C provides operators for performing bitwise conjunction, inclusive
disjunction, exclusive disjunction, and negation (complement).

Bitwise conjunction examines each bit in its two operands, and when two
corresponding bits are both 1, the resulting bit is 1. All other
resulting bits are 0.

Bitwise inclusive disjunction examines each bit in its two operands, and
when two corresponding bits are both 0, the resulting bit is 0. All
other resulting bits are 1.

Bitwise exclusive disjunction examines each bit in its two operands, and
when two corresponding bits are different, the resulting bit is 1. All
other resulting bits are 0.

Bitwise negation reverses each bit in its operand.

------------------------------------------------------------------------

[]{#Pointer-Operators}

[]{#Pointer-Operators-1}

### 3.9 Pointer Operators {#pointer-operators .section} (Optional)

[]{#index-pointer-operators}

You can use the address operator `&` to obtain the memory address of an
identifier only.

Function pointers and data pointers are not compatible, in the sense
that you cannot expect to store the address of a function into a data
pointer, and then copy that into a function pointer and call it
successfully.

Given a memory address stored in a pointer, you can use the indirection
operator `*` to obtain the value stored at the address. (This is called
*dereferencing* the pointer.)

Avoid using dereferencing pointers that have not been initialized to a
known memory location.

------------------------------------------------------------------------

[]{#The-sizeof-Operator}
[]{#The-sizeof-Operator-1}

### 3.10 The sizeof Operator {#the-sizeof-operator .section}

[]{#index-sizeof-operator}

You can use the `sizeof` operator to obtain the size (in bytes) of the
data type of its operand. The operand may be an actual type specifier
(such as `int` or `float`), as well as any valid expression. When the
operand is a type name, it must be enclosed in parentheses.

The result of the `sizeof` operator is perhaps identical to `unsigned int`; it varies from system to system.

------------------------------------------------------------------------

[]{#Type-Casts}
[]{#Type-Casts-1}

### 3.11 Type Casts {#type-casts .section}

[]{#index-type-casts} []{#index-casts}

You can use a type cast to explicitly cause an expression to be of a
specified data type. A type cast consists of a type specifier enclosed
in parentheses, followed by an expression. To ensure proper casting, you
should also enclose the expression that follows the type specifier in
parentheses.

------------------------------------------------------------------------

[]{#Array-Subscripts}
[]{#Array-Subscripts-1}

### 3.12 Array Subscripts {#array-subscripts .section}

[]{#index-array-subscripts}

You can access array elements by specifying the name of the array, and
the array subscript (or index, or element number) enclosed in brackets.

------------------------------------------------------------------------

[]{#Function-Calls-as-Expressions}


[]{#Function-Calls-as-Expressions-1}

### 3.13 Function Calls as Expressions {#function-calls-as-expressions .section}

[]{#index-function-calls_002c-as-expressions}

A call to any function which returns a value is an expression.


------------------------------------------------------------------------

[]{#The-Comma-Operator}


[]{#The-Comma-Operator-1}

### 3.14 The Comma Operator {#the-comma-operator .section}

[]{#index-comma-operator}

You use the comma operator `,` to separate two
expressions. For instance, the first expression might produce a value
that is used by the second expression.

A comma is also used to separate function parameters; however, this is
*not* the comma operator in action. In fact, if the comma operator is
used as we have discussed here in a function call, then the compiler
will interpret that as calling the function with an extra parameter.

------------------------------------------------------------------------

[]{#Member-Access-Expressions}
[]{#Member-Access-Expressions-1}

### 3.15 Member Access Expressions {#member-access-expressions .section}

[]{#index-member-access-expressions}

You can use the member access operator `.` to access the members of a
structure. You put the name of the structure variable
on the left side of the operator, and the name of the member on the
right side.


[]{#index-indirect-member-access-operator}

You can also access the members of a structure or union variable via a
pointer by using the indirect member access operator `->`. `x->y` is
equivalent to `(*x).y`.

------------------------------------------------------------------------

[]{#Conditional-Expressions}
[]{#Conditional-Expressions-1}

### 3.16 Conditional Expressions {#conditional-expressions .section}

[]{#index-conditional-expressions}
[]{#index-expressions_002c-conditional} []{#index-ternary-operator}

You use the conditional operator to cause the entire conditional
expression to evaluate to either its second or its third operand, based
on the truth value of its first operand.

------------------------------------------------------------------------

[]{#Operator-Precedence}


[]{#Operator-Precedence-1}

### 3.18 Operator Precedence {#operator-precedence .section}

[]{#index-operator-precedence} []{#index-precedence_002c-operator}

When an expression contains multiple operators, such as `a + b * f()`,
the operators are grouped based on rules of *precedence*. For instance,
the meaning of that expression is to call the function `f` with no
arguments, multiply the result by `b`, then add that result to `a`.
That's what the C rules of operator precedence determine for this
expression.

The following is a list of types of expressions, presented in order of
highest precedence first. Sometimes two or more operators have equal
precedence; all those operators are applied from left to right unless
stated otherwise.

1.  Function calls, array subscripting, and membership access operator
    expressions.
2.  Unary operators, including logical negation, bitwise complement,
    increment, decrement, unary positive, unary negative, indirection
    operator, address operator, type casting, and `sizeof` expressions.
    When several unary operators are consecutive, the later ones are
    nested within the earlier ones: `!-x` means `!(-x)`.
3.  Multiplication, division, and modular division expressions.
4.  Addition and subtraction expressions.
5.  Bitwise shifting expressions.
6.  Greater-than, less-than, greater-than-or-equal-to, and
    less-than-or-equal-to expressions.
7.  Equal-to and not-equal-to expressions.
8.  Bitwise AND expressions.
9.  Bitwise exclusive OR expressions.
10. Bitwise inclusive OR expressions.
11. Logical AND expressions.
12. Logical OR expressions.
13. Conditional expressions. When used as subexpressions,
    these are evaluated right to left.
14. All assignment expressions. When
    multiple assignment statements appear as subexpressions in a single
    larger expression, they are evaluated right to left.
15. Comma operator expressions.

------------------------------------------------------------------------

[]{#Statements-1}

[]{#Statements-1}

## 4 Statements {#statements .chapter}

[]{#index-statements}

You write statements to cause actions and to control flow within your
programs. You can also write statements that do not do anything at all,
or do things that are uselessly trivial.
**The declarations must be completed before beginning with the statements in any scope. In any other cases it will return an error**
------------------------------------------------------------------------

[]{#Labels}


[]{#Labels-1}

### 4.1 Labels {#labels .section}

[]{#index-labels} []{#index-labeled-statements}
[]{#index-statements_002c-labeled}

Labels are allowed  to  be used identify a section of source code for use with a
later `goto` (see [The goto Statement](#The-goto-Statement)). A label
consists of an identifier
followed by a colon.

Label names should not interfere with other identifier names. The ISO C standard mandates that a label must be followed by at least
one statement, possibly a null statement otherwise undefined behavior shall occur in the compiler.

------------------------------------------------------------------------

[]{#Expression-Statements}


[]{#Expression-Statements-1}

### 4.2 Expression Statements {#expression-statements .section}

[]{#index-expression-statements} []{#index-statements_002c-expression}

Any expression can be turned into a statement by adding a semicolon to
the end of the expression.

------------------------------------------------------------------------

[]{#The-if-Statement}


[]{#The-if-Statement-1}

### 4.3 The `if` Statement {#the-if-statement .section}

[]{#index-if-statements} []{#index-else-statements}

`if` statement is used to conditionally execute part of your
program, based on the truth value of a given expression. 

If `test`{.variable} evaluates to true, then `then-statement`{.variable}
is executed and `else-statement`{.variable} is not. If `test`{.variable}
evaluates to false, then `else-statement`{.variable} is executed and
`then-statement`{.variable} is not. The `else` clause is optional.

You can use a series of `if` statements to test for multiple conditions.

**Unlike GNU C99, for our subset of c the statement(s) compulsorily  have to be necessarily in blocks using braces '{' at the beginning and '}' at the end for correct evaluation by our compiler.**


------------------------------------------------------------------------

[]{#The-switch-Statement}


[]{#The-switch-Statement-1}

### 4.4 The `switch` Statement {#the-switch-statement .section}

[]{#index-switch-statement}

The `switch` statement is used to compare one expression with
others, and then execute a series of sub-statements based on the result
of the comparisons. Here is the general form of a `switch` statement:

``` example
switch (test)
  {
    case compare-1:
      if-equal-statement-1
    case compare-2:
      if-equal-statement-2
    …
    default:
      default-statement
  }
```

The `switch` statement compares `test`{.variable} to each of the
`compare`{.variable} expressions, until it finds one that is equal to
`test`{.variable}. Then, the statements following the successful case
are executed. All of the expressions compared must be of either character or integer
type, and the `compare-N`{.variable} expressions must similarly be of a constant
character or integer type (e.g., a literal character/integer or an expression built of literal
characters/integers). 
You cannot use both integer and character labels simultaneously

Optionally, you can specify a default case. If `test`{.variable} doesn't
match any of the specific cases listed prior to the default case, then
the statements for the default case are executed. Traditionally, the
default case is put after the specific cases, but that isn't required.

------------------------------------------------------------------------

[]{#The-while-Statement}


[]{#The-while-Statement-1}

### 4.5 The `while` Statement {#the-while-statement .section}

[]{#index-while-statement}

The `while` statement is a loop statement with an exit test at the
beginning of the loop. Here is the general form of the `while`
statement:

``` example
while (test)
  {statement(s)}
```

**Unlike GNU C99, for our subset of c, the statement(s) following `while(test)`{.variable}  compulsorily have to be nexessarily in blocks using braces '{' at the beginning and '}' at the end for correct evaluation by our compiler, just as we did above for if.**

The `while` statement first evaluates `test`{.variable}. If
`test`{.variable} evaluates to true, `statement`{.variable} is executed,
and then `test`{.variable} is evaluated again. `statement`{.variable}
continues to execute repeatedly as long as `test`{.variable} is true
after each execution of `statement`{.variable}.

A `break` statement can also cause a `while` loop to exit.

------------------------------------------------------------------------

[]{#The-do-Statement}


[]{#The-do-Statement-1}

### 4.6 The `do` Statement {#the-do-statement .section}

[]{#index-do-statement}

The `do` statement is a loop statement with an exit test at the end of
the loop. Here is the general form of the `do` statement:

``` example
do
  {statement(s)}
while (test);
```

**Unlike GNU C99, for our subset of c, the statement(s) following `do`{.variable}  compulsorily have to be nexessarily in blocks using braces '{' at the beginning and '}' at the end for correct evaluation by our compiler, just as we did above for while.**



The `do` statement first executes `statement`{.variable}. After that, it
evaluates `test`{.variable}. If `test`{.variable} is true, then
`statement`{.variable} is executed again. `statement`{.variable}
continues to execute repeatedly as long as `test`{.variable} is true
after each execution of `statement`{.variable}.

A `break` statement can also cause a `do` loop to exit.

------------------------------------------------------------------------

[]{#The-for-Statement}


[]{#The-for-Statement-1}

### 4.7 The `for` Statement {#the-for-statement .section}

[]{#index-for-statement}

The `for` statement is a loop statement whose structure allows easy
variable initialization, expression testing, and variable modification.
It is very convenient for making counter-controlled loops. Here is the
general form of the `for` statement:

::: example
``` example
for (initialize; test; step)
  {statement}
```
:::


**Unlike GNU C99, for our subset of c, the statement(s) following `for (initialize; test; step)`{.variable} compulsorily have to be necessarily in blocks using braces '{' at the beginning and '}' at the end for correct evaluation by our compiler, just as we did above for if.**


The `for` statement first evaluates the expression
`initialize`{.variable}. Then it evaluates the expression
`test`{.variable}. If `test`{.variable} is false, then the loop ends and
program control resumes after `statement`{.variable}. Otherwise, if
`test`{.variable} is true, then `statement`{.variable} is executed.
Finally, `step`{.variable} is evaluated, and the next iteration of the
loop begins with evaluating `test`{.variable} again.

Most often, `initialize`{.variable} assigns values to one or more
variables, which are generally used as counters, `test`{.variable}
compares those variables to a predefined expression, and
`step`{.variable} modifies those variables' values.

All three of the expressions in a `for` statement are optional, and any
combination of the three is valid. Since the first expression is
evaluated only once, it is perhaps the most commonly omitted expression.

If you leave out the `test`{.variable} expression, then the `for`
statement is an infinite loop (unless you put a `break` or `goto`
statement somewhere in `statement`{.variable}). This is like using `1`
as `test`{.variable}; it is never false.

Usage of  the comma operator confusingly is not allowed (see [The Comma
Operator](#The-Comma-Operator)) for monitoring multiple variables in a
`for` statement, because as usual the comma operator discards the result
of its left operand. 

If you need to test two conditions, you will need to use the `&&`
operator.

A `break` statement can also cause a `for` loop to exit.

------------------------------------------------------------------------

[]{#Blocks}


[]{#Blocks-1}

### 4.8 Blocks {#blocks .section}

[]{#index-blocks} []{#index-compound-statements}

A *block* is a set of zero or more statements enclosed in braces. Blocks
are also known as *compound statements*. A block is used as the
body of an `if` statement or a loop statement, to group statements
together. You can also put blocks inside other blocks.

Declarations of variables are allowed inside a block; such variables are local to
that block (details described in scope of a variable). In C89, declarations must occur before other statements, and
so sometimes it is useful to introduce a block simply for this purpose:


------------------------------------------------------------------------

[]{#The-Null-Statement}


[]{#The-Null-Statement-1}

### 4.9 The Null Statement {#the-null-statement .section}

[]{#index-null-statement} []{#index-statement_002c-null}

The *null statement* is merely a semicolon alone.

A null statement does not do anything. It does not store a value
anywhere. It does not cause time to pass during the execution of your
program.
Most often, a null statement is used as the body of a loop statement, or
as one or more of the expressions in a `for` statement.
A null statement is also sometimes used to follow a label that would
otherwise be the last thing in a block.

------------------------------------------------------------------------

[]{#The-goto-Statement}


[]{#The-goto-Statement-1}

### 4.10 The `goto` Statement {#the-goto-statement .section}

[]{#index-goto-statement}

Use the `goto` statement to unconditionally jump to a different
place in the program.

Specifying  a label to jump to is necessary; when the `goto` statement is
executed, program control jumps to that label. See [Labels](#Labels).

The label can be anywhere in the same function as the `goto` statement
that jumps to it, but a `goto` statement cannot jump to a label in a
different function.
<!---Important error--->
**Usage of goto is not recommended in case of loops as this can cause program to not execute properly. If possible usage of for, while and do while loop constructs are recommended.**

------------------------------------------------------------------------

[]{#The-break-Statement}


[]{#The-break-Statement-1}

### 4.11 The `break` Statement {#the-break-statement .section}

[]{#index-break-statement}

You can use the `break` statement to terminate a `while`, `do`, `for`,
or `switch` statement. 
If you put a `break` statement inside of a loop or `switch` statement
which itself is inside of a loop or `switch` statement, the `break` only
terminates the innermost loop or `switch` statement.

------------------------------------------------------------------------

[]{#The-continue-Statement}
[]{#The-continue-Statement-1}

### 4.12 The `continue` Statement {#the-continue-statement .section}

[]{#index-continue-statement}

Use the `continue` statement in loops to terminate an iteration
of the loop and begin the next iteration.
If you put a `continue` statement inside a loop which itself is inside a
loop, then it affects only the innermost loop.

------------------------------------------------------------------------

[]{#The-return-Statement}


[]{#The-return-Statement-1}

### 4.13 The `return` Statement {#the-return-statement .section}

[]{#index-return-statement}

You can use the `return` statement to end the execution of a function
and return program control to the function that called it.

`return-value`{.variable} is an optional expression to return. If the
function's return type is `void`, then it is invalid to return an
expression. You can, however, use the `return` statement without a
return value.

If the function's return type is not the same as the type of
`return-value`{.variable}, and automatic type conversion cannot be
performed, then returning `return-value`{.variable} is invalid.

If the function's return type is not `void` then return value *must* be specified at the end of the body of the function.

------------------------------------------------------------------------

[]{#Functions}

## 5 Functions {#functions .chapter}

You can write functions to separate parts of your program into distinct
subprocedures. To write a function, you must at least create a function
definition. Every program requires at least one function, called `main`. That is where the program's execution begins.

-----------------------------------------------------------------

[]{#Function-Declarations}

### 5.1 Function Declarations and Definitions

You write a function declaration **followed** by function definition to specify the name of a function, a list of parameters, the function's return type, and to specify what a function actually
does.

Here is the general form of a function:

``` example
return-type function-name (parameter-list){
  function-body
}
```

`return-type` indicates the data type of the value returned
by the function. You can declare a function that doesn't return anything
by using the return type `void`.

`function-name` can be any valid identifier (see [Identifiers](#Identifiers)).

`parameter-list` consists of zero or more parameters, separated by commas. A parameter consists of a data type and an name for the parameter.

The parameter names can be any identifier, and if you have more than one parameter, you can't use the same name more than once within a single declaration. You can put it in a header file and use the `#include`
directive to include that function declaration in any source code files
that use the function.

`The function body` is a series of statements (*at least one*) enclosed in braces.

Functions with empty bodies are not allowed.

-------------------------- ---- ---------------------------- ---- --

[]{#Calling-Functions}

### 5.2 Calling Functions

You can call a function by using its name and supplying any needed
parameters. A function call can make up an entire statement, or it can be used as a subexpression. If a parameter takes more than one argument, you separate parameters with commas.

---------------------------------------------------------------------------

[]{#Function-Parameters}

### 5.3 Function Parameters

Function parameters can be any expression, a literal value, a value
stored in variable, an address in memory, or a more complex expression
built by combining these.

Within the function body, the parameter is a local copy of the value passed into the function; you cannot change the value passed in by changing the local copy. If the value that you pass to a function is a memory address, then you can access (and change) the data stored at the memory address. This achieves an effect similar to pass-by-reference, but the memory address itself cannot be changed.

**Currently we only support 1D type of array as parameter**.

------------------------------------------------------------------------

[]{#The-main-Function}

### 5.4 The `main` Function

Every program requires at least one function, called '`main`'.
This is where the program begins executing. The return type for `main` is always `int`. Reaching the `}` at the end of `main` without a return, or executing a `return` statement with no value (that is, `return;`) are both
equivalent. The effect of this is equivalent to `return 0;`.

------------------------------------------------------------------------

[]{#Recursive-Functions}

### 5.5 Recursive Functions

You can write a function that is recursive --- a function that calls
itself.

------------------------------------------------------------------------

[]{#Program-Structure-and-Scope}

## 6 Program Structure and Scope {#program-structure-and-scope .chapter}

------------------------------------------------------------------------

[]{#Program-Structure}

### 6.1 Program Structure (#program-structure .section)

A C program may exist entirely within a single source file, but more
commonly, will consist of several custom header files and source files, and will also include and link with files from existing libraries. By convention, header files contain variable and function declarations, and source files contain the corresponding definitions.

------------------------------------------------------------------------

[]{#Scope}

### 6.2 Scope

A declared object can be visible only within a particular function, or within a particular file. Unless explicitly stated otherwise, declarations made at the top-level of a file (i.e., not within a function) are visible to the entire file, but are not visible outside of the file.

------------------------------------------------------------------------

[]{#Advanced-Features}


[]{#Advanced-Features-1}

## 7 Implementation of Advanced Features

[]{#index-advanced-features}

This section shall contain details of various advanced features apart from the above mentioned basic features we are going to implement through our compiler along with some of the code optimizations
**We are gonna implement this only if time permits**.


------------------------------------------------------------------------

[]{#File-Handling}

[]{#File-Handling-1}

### 7.1 File Handling{#filehandling .section}

We extend the basic C99 to include file IO using functions such as `fopen, fclose, fseek, fwrite, fread` for opening, closing, pointing at a specific location in the file, writing to a file, reading from a file respectively.

------------------------------------------------------------------------

[]{#Library-Functions}

[]{#Library-Functions-1}

### 7.2 Library Functions{#libraryfunctions .section}

We implement various library functions to provide additional mathematical functions, string manipulation functions such as `strchr(),strlwr(),strupr()` to provide additional functionalities.

**This list is not exhaustive and further addition or elimination shall be made based on the time remaining as we go along with this project.**

--------------------------------------------------------------------------------

[]{#Multidimensional Arrays}

[]{#Multidimensional Arrays-1}

### 7.3 Multidimensional Arrays{#multidimensionalarrays .section}
We plan to implement multidimensional arrays, in simple words as an array of arrays. Data in multidimensional arrays are stored in tabular form.

Currently, we only allow pointers of level 1 to refer to rows of the multidimensional arrays. 
Pointers of higher levels cannot be initialized to rows of multidimensional arrays 

**We have started to implement this, work in progress**.

### 7.4 Compile Time Evaluation 

Constant expressions are evaluated at compile time

### 7.5 Return non-primitive types 

We can return non-primitive types such as struct from a function, as well simple types like int, float, etc.

----------------------------------------------------------------
--------------------------------------------------------------------------
## References
https://www.gnu.org/software/gnu-c-manual/gnu-c-manual.html
