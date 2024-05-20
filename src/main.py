# Autor: Andrea Catalina Fernández Mena A01197705
# Fecha: 20/05/2024
# Descripción: Main - Manda a llamar todos los pasos anteriores del compilador y ejecuta

from parse import run_parse
from codegen import CodeGen
from interpreter import IR_Interpret
from semantic import SemanticExecuter,SemanticError

data_file = open("./test/test_case5.txt", "r")
data = data_file.read()

result = run_parse(data)

#Imprimir AST
print("Parsed expression as AST(Abstract Syntax Tree): ")
print(result , '\n')

#CodeGen - Cuadruplos
print("From the AST we generate the following IR/Quadruples: ")
quad_gen = CodeGen(result)
quadruples = quad_gen.generate()

counter = 0
for quad in quadruples:
    print(f"L{counter}", quad)
    counter += 1

print('\n')

print("Which are represented on pseucode as: ")
interpreter = IR_Interpret(quadruples)
pseudo_code = interpreter.interpret()
print(pseudo_code)

print('\n')

print('-----------------------------------------------------------------------------')
print('Program Execution and Evaluation:')
semantic_analyzer = SemanticExecuter()
semantic_analyzer.interpret(quadruples)
