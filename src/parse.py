# Autor: Andrea Catalina Fernández Mena
# Fecha: 20/05/2024
# Descripción: Parser - Consume tokens del lexer y construye AST(Abstract Syntax Tree)

import ply.yacc as yacc
from lexer import *

# Precedencia y asociatividad de los operadores
precedence = (
    ('nonassoc', 'LT', 'LE', 'GT', 'GE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULT', 'DIVIDE', 'MOD'),
    ('right', 'NOT'),
    ('right', 'INCREMENT', 'DECREMENT'),
    ('left', 'AND', 'OR')
)

# Declarar estructura del código
def p_programstart(p):
    'programstart : PROGRAM ID LBRACE code RBRACE'
    p[0] = ('programstart', p[2], p[4])

# Una sola línea de código
def p_code_singleline(p):
    'code : statement'
    p[0] = (p[1],)

# Múltiples líneas de código
def p_code_multiple(p):
    'code : code statement'
    p[0] = p[1] + (p[2],)

#--------------------------------------------------------------
# Declaración y asignación de variables
def p_statement_variables(p):
    '''statement : assignment STMT_TERMINATOR
                 | declaration STMT_TERMINATOR
                 | expression STMT_TERMINATOR
                 | if_statement
                 | while_statement
                 | for_statement
                 | array_declaration STMT_TERMINATOR
                 | array_assignment STMT_TERMINATOR
                 | write_statement
                 | writeln_statement
                 | break_statement
                 | return_statement'''
    p[0] = ('statement', p[1])

# Declarar variables
def p_declaration(p):
    'declaration : datatype declareid'
    p[0] = ('declaration', p[1], p[2])

# Declarar múltiples variables
def p_declareid_single(p):
    'declareid : ID'
    p[0] = ('declareid', p[1])
    
# Variable nombre con data
def p_declareid_singlev(p):
    'declareid : assignment'
    p[0] = ('declareid', p[1])

# Múltiples variables en la misma línea - solo nombre
def p_declareid_multiple(p):
    'declareid : declareid COMMA ID'
    p[0] = ('declareid', p[1], p[3])
    
# Múltiples variables en la misma línea - nombre y data
def p_declareid_multiplev(p):
    'declareid : declareid COMMA assignment'
    p[0] = ('declareid', p[1], p[3])
    
# Asignación números, operaciones, booleanos, strings, chars
def p_assignment(p):
    '''assignment : ID EQUAL expression
                  | ID PLUSEQUAL expression
                  | ID MINUSEQUAL expression'''
    p[0] = ('assignment', p[1], p[2], p[3])

# Datatypes
def p_datatype(p):
    '''datatype : INT
                | FLOAT
                | BOOL
                | CHAR
                | DOUBLE
                | LONG
                | STRING'''
    p[0] = ('datatype', p[1])

def p_expression_plus(p):
    'expression : expression PLUS term'
    p[0] = ('plus', p[1], p[3])

def p_expression_minus(p):
    'expression : expression MINUS term'
    p[0] = ('minus', p[1], p[3])

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_multiplication(p):
    'term : term MULT factor'
    p[0] = ('mult', p[1], p[3])

def p_term_div(p):
    'term : term DIVIDE factor'
    p[0] = ('divide', p[1], p[3])

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_num(p):
    '''factor : ID
              | INTCONST
              | FLOATCONST
              | DOUBLECONST
              | LONGCONST
              | BOOLCONST
              | STRCONST
              | CHARCONST
              | array_access'''
    p[0] = ('factor', p[1])

def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

# Operadores relacionales
def p_expression_relop(p):
    '''expression : expression LT expression
                  | expression GT expression
                  | expression LE expression
                  | expression GE expression
                  | expression NE expression
                  | expression BOOLEQUAL expression'''
    if p[2] == '<':
        p[0] = ('lt', p[1], p[3])
    elif p[2] == '>':
        p[0] = ('gt', p[1], p[3])
    elif p[2] == '<=':
        p[0] = ('le', p[1], p[3])
    elif p[2] == '>=':
        p[0] = ('ge', p[1], p[3])
    elif p[2] == '!=':
        p[0] = ('ne', p[1], p[3])
    elif p[2] == '==':
        p[0] = ('eq', p[1], p[3])

# Operadores lógicos
def p_expression_logical(p):
    '''expression : expression AND expression
                  | expression OR expression'''
    if p[2] == '&&':
        p[0] = ('and', p[1], p[3])
    elif p[2] == '||':
        p[0] = ('or', p[1], p[3])

# Operadores de incremento y decremento
def p_expression_increment(p):
    'expression : ID INCREMENT'
    p[0] = ('increment', p[1])

def p_expression_decrement(p):
    'expression : ID DECREMENT'
    p[0] = ('decrement', p[1])

# Operadores de incremento y decremento
def p_assignment_increment(p):
    'assignment : ID INCREMENT STMT_TERMINATOR'
    p[0] = ('increment', p[1])

def p_assignment_decrement(p):
    'assignment : ID DECREMENT STMT_TERMINATOR'
    p[0] = ('decrement', p[1])

# Operador de flecha
def p_expression_arrow(p):
    'expression : expression ARROW ID'
    p[0] = ('arrow', p[1], p[3])

# Estructuras de control
def p_if_statement(p):
    '''if_statement : IF LPAREN expression RPAREN LBRACE code RBRACE
                    | IF LPAREN expression RPAREN LBRACE code RBRACE ELSE LBRACE code RBRACE'''
    if len(p) == 8:
        p[0] = ('if', p[3], p[6])
    else:
        p[0] = ('if-else', p[3], p[6], p[10])

def p_while_statement(p):
    'while_statement : WHILE LPAREN expression RPAREN LBRACE code RBRACE'
    p[0] = ('while', p[3], p[6])

def p_for_statement(p):
    'for_statement : FOR LPAREN assignment STMT_TERMINATOR expression STMT_TERMINATOR expression RPAREN LBRACE code RBRACE'
    p[0] = ('for', p[3], p[5], p[7], p[10])

def p_arguments(p):
    '''arguments : expression
                 | arguments COMMA expression
                 | empty'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = []

# Declaraciones de arreglos
def p_array_declaration(p):
    'array_declaration : datatype ID LBRACKET INTCONST RBRACKET'
    p[0] = ('array_declaration', p[1], p[2], p[4])

# Asignación a arreglos
def p_array_assignment(p):
    'array_assignment : ID LBRACKET expression RBRACKET EQUAL expression'
    p[0] = ('array_assignment', p[1], p[3], p[6])

# Acceso a elementos de arreglos
def p_array_access(p):
    'array_access : ID LBRACKET expression RBRACKET'
    p[0] = ('array_access', p[1], p[3])

# Declaraciones para write, writeln, break y return
def p_write_statement(p):
    'write_statement : WRITE LPAREN expression RPAREN STMT_TERMINATOR'
    p[0] = ('write', p[3])

def p_writeln_statement(p):
    'writeln_statement : WRITELN LPAREN expression RPAREN STMT_TERMINATOR'
    p[0] = ('writeln', p[3])

def p_break_statement(p):
    'break_statement : BREAK STMT_TERMINATOR'
    p[0] = ('break',)

def p_return_statement(p):
    '''return_statement : RETURN expression STMT_TERMINATOR
                        | RETURN STMT_TERMINATOR'''
    if len(p) == 4:
        p[0] = ('return', p[2])
    else:
        p[0] = ('return',)

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    print(f"Syntax error in input! at '{p.value}', line {p.lineno}")

parser = yacc.yacc()

data_file = open("./test/PruebaParser.txt", "r")
data = data_file.read()

result = parser.parse(data)
print("Parsed expression:")
print(result)
