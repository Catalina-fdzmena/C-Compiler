# C# Compiler
This repository aims to develop a compiler for the C# programming language using Python and the PLY (Python Lex-Yacc) library. The project focuses on leveraging Python's capabilities and PLY's tools to parse and execute C# code efficiently.

**Features**

    Array Support: Efficiently parse and execute array declarations and operations.
    Control Structures: Full support for while, for, and if-else statements.
    Comprehensive Token Handling: Recognizes a wide range of tokens and reserved words for C#.

**Supported Tokens**

    Keywords: program, if, then, else, do, while, for, foreach, write, writeln, string, int, float, bool, char, double, long, break, void, new, private, return, true, false, const, public
    Operators: Increment (++), Decrement (--), Arrow (->), Not (!), Multiplication (*), Division (/), Modulus (%), Addition (+), Subtraction (-), Less than (<), Greater than (>), Less than or equal to (<=), Greater than or equal to (>=), Not equal (!=), And (&&), Or (||), Assignment (=), Equality (==), Plus-equal (+=), Minus-equal (-=), Multiplication-equal (*=), Division-equal (/=), Modulus-equal (%=), And-equal (&=), Or-equal (|=), Xor-equal (^=)
    Delimiters: Parentheses (()), Braces ({}), Brackets ([]), Comma (,), Statement terminator (;), Colon (:)
    Literals: Identifiers, Integer constants, Character constants, String constants, Float constants, Boolean constants, Double constants, Long constants
    Comments: Single-line (//), Multi-line (/**/)