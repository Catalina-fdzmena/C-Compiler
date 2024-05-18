# Autor: Andrea Catalina Fernández Mena
# Fecha: 20/05/2024
# Descripción: Lexer - responsable de leer el código fuente y producir los tokens.

import ply.lex as lex

#Lista de palabras reservadas
reserved = {
   'program' : 'PROGRAM',
   'if' : 'IF',
   'then' : 'THEN',
   'else' : 'ELSE',
   'do' : 'DO',
   'while' : 'WHILE',
   'for' : 'FOR',
   'foreach' : 'FOREACH',
   'write' : 'WRITE',
   'writeln' : 'WRITELN',
   'program' : 'PROGRAM',
   
   'string' : 'STRING',
   'int' : 'INT',
   'float' : 'FLOAT',
   'bool' : 'BOOL',
   'char' : 'CHAR',
   'double' : 'DOUBLE',
   'long' : 'LONG',

    'break' : 'BREAK',
    'void' : 'VOID',
    'new' : 'NEW',
    'private' : 'PRIVATE',
    'return' : 'RETURN',
    'true' : 'TRUE',
    'false' : 'FALSE',
    'const' : 'CONST',
    'public' : 'PUBLIC',
}

#Lista de tokens
tokens = [
    # // /**/ ... 
	'COMMENT', 'MULTILINECOMMENT', 'PREPROCESSOR',
	# Literales: IDs, Int-Constants, Char-Constant, String-Constant 
	'ID', 'INTCONST', 'CHARCONST', 'STRCONST',
    #Literales - num data s
   'FLOATCONST','BOOLCONST','DOUBLECONST','LONGCONST',
	#Operadores primarios . ?. ++ -- ->
	'MEMBERACCESS', 'CONDMEMBACCESS', 'INCREMENT', 'DECREMENT', 'ARROW',
	# Op. unarios ! 
	'LNOT',
	# * / %
	'MULT', 'DIVIDE', 'MOD',
	# + -
	'PLUS', 'MINUS',
	# < > <= >=
	'LT', 'GT', 'LE', 'GE',
	#  == !=
	'EQ', 'NE',
    #AND ,OR
    'AND', 'OR',
	# Op. lambda y de asignacion = == += -= *= /= %= &= |= ^= 
	'EQUAL', 'BOOLEQUAL', 'PLUSEQUAL', 'MINUSEQUAL', 'TIMESEQUAL', 'DIVEQUAL', 'MODEQUAL',
	'ANDEQUAL', 'OREQUAL', 'XOREQUAL', 
	# ( ) { } [ ] , . ; :
	'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET', 'COMMA', 'STMT_TERMINATOR', 'COLON'
] + list(reserved.values())

#Expresiones regulares en tokens
t_ignore_SINGLELINE_COMMENT = r'//.*'
t_ignore_MULTILINE_COMMENT = r'/\*(.|\n)*?\*/'
#Ignorar espacios, tabulaciones y caracteres form feed
t_ignore = ' \t\x0c'

# Operadores
t_MEMBERACCESS		= r'\.'
t_CONDMEMBACCESS	= r'\?\.'
t_INCREMENT			= r'\+\+'
t_DECREMENT			= r'--'
t_ARROW				= r'->'
t_LNOT				= r'!'
t_MULT				= r'\*'
t_DIVIDE 			= r'/'
t_MOD   			= r'%'
t_PLUS  			= r'\+'
t_MINUS 			= r'-'
t_LT				= r'<'
t_GT				= r'>'
t_LE 				= r'<='
t_GE  				= r'>='
t_EQ   				= r'=='
t_NE   				= r'!='
t_AND  			    = r'&&'
t_OR    			= r'\|\|'
t_EQUAL     		= r'='
t_BOOLEQUAL         = r'=='
t_PLUSEQUAL   		= r'\+='
t_MINUSEQUAL  		= r'-='
t_TIMESEQUAL 		= r'\*='
t_DIVEQUAL  		= r'/='
t_MODEQUAL 			= r'%='
t_ANDEQUAL   		= r'&='
t_OREQUAL    		= r'\|='
t_XOREQUAL    		= r'\^='

# Delimitadores
t_LPAREN           = r'\('
t_RPAREN           = r'\)'
t_LBRACKET         = r'\['
t_RBRACKET         = r'\]'
t_LBRACE           = r'\{'
t_RBRACE           = r'\}'
t_COMMA            = r','
t_STMT_TERMINATOR  = r';'
t_COLON            = r':'

# IDs and Keywords
def t_ID(t):
	r'[a-zA-Z_@][a-zA-Z_0-9]*'
	t.type = reserved.get(t.value,'ID')    #  Check for reserved words
	return t

# Literales INT
t_INTCONST = r'\d+([uU]|[lL]|[uU][lL]|[lL][uU])?'

# Literales STR
t_STRCONST = r'\"([^\\\n]|(\\.))*?\"'


# Literales CHAR
t_CHARCONST = r'(L)?\'([^\\\n]|(\\.))*?\''

# Literales FLOAT
def t_FLOATCONST(t):
    r'(\d+\.\d+)[fF]'
    t.value = float(t.value[:-1])  # Remove 'f' or 'F' suffix
    return t

# Literales BOOL
def t_BOOLCONST(t):
    r'true|false'
    t.value = True if t.value == 'true' else False
    return t

# Literales DOUBLE
def t_DOUBLECONST(t):
    r'\d+\.\d+[dD]|\d*\.\d+E [+-]?\d'
    t.value = float(t.value[:-1])  #Quita sufijo 'd','D'
    return t

# Literales LONG
def t_LONGCONST(t):
    r'\d+[lL]'
    t.value = int(t.value[:-1])  #Quita sufijo 'l','L' 
    return t

#String ignorar quotes
def t_STRING(t):
    r'\"([^"\\]|\\.)*\"'
    t.value = t.value[1:-1]  # Remove quotes
    return t

#Single line comment (ignored)
def t_SINGLELINE_COMMENT(t):
    r'//.*'
    pass

#Multiple line comment (ignored)
def t_MULTILINE_COMMENT(t):
    r'/\*(.|\n)*?\*/'
    t.lineno += t.value.count('\n')
    pass

#------------------------------------------------------------------
#Reglas

# Define a rule so we can track line numbers
def t_NEWLINE(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

# Preprocessor directive (ignored)
def t_PREPROCESSOR(t):
	r'\#(.)*?\n'
	t.lineno += 1

#Regla de manejo de errores
def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)
	
#--------------------------------------------------------------------
#Lectura de lexer para pruebas

data_file = open("./test/test_case1.txt", "r")
data = data_file.read()

lexer = lex.lex()
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok)
