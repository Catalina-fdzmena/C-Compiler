# Autor: Andrea Catalina Fernández Mena A01197705
# Fecha: 20/05/2024
# Descripción: Intérprete - Traduce cuádruplos a pseudo-código

from codegen import CodeGen

class IR_Interpret:
    def __init__(self, quadruples):
        self.quadruples = quadruples
        self.output = []

    #Recorre la lista de cuadruplos y procesa a pseudocodigo
    def interpret(self):
        for quad in self.quadruples:
            self._process_quadruple(quad)
        return '\n'.join(self.output)

    #Genera pseudocodigo con base en la posición del cuadruplo y lo interpreta añadiendo los espacios o simbolos legibles
    def _process_quadruple(self, quad):
        op = quad.operator
        arg1 = quad.arg1
        arg2 = quad.arg2
        result = quad.result

        if op == '=':
            self.output.append(f"{result} = {arg1}")
        elif op == 'write':
            self.output.append(f"write({arg1})")
        elif op == 'writeln':
            self.output.append(f"writeln({arg1})")
        elif op in ('+', '-', '*', '/', '%'):
            self.output.append(f"{result} = {arg1} {op} {arg2}")
        elif op == '<':
            self.output.append(f"{result} = {arg1} < {arg2}")
        elif op == '>':
            self.output.append(f"{result} = {arg1} > {arg2}")
        elif op == '>=':
            self.output.append(f"{result} = {arg1} > {arg2}")
        elif op == 'gotofalse':
            self.output.append(f"if not {arg1} goto {result}")
        elif op == 'gototrue':
            self.output.append(f"if {arg1} goto {result}")
        elif op == 'goto':
            self.output.append(f"goto {result}")
        elif op == 'declare_array':
            self.output.append(f"declare {arg1} array {arg2}[{result}]")
        elif op == 'array_assign':
            self.output.append(f"{arg1}[{arg2}] = {result}")
        elif op == 'array_access':
            self.output.append(f"{result} = {arg1}[{arg2}]")
        else:
            raise ValueError(f"Unknown operation: {op}")


# Ejemplo de uso con el AST y el generador de cuádruplos definidos previamente
"""
ast2 = ('programstart', 'main', (('statement', ('declaration', ('datatype', 'int'), ('declareid_multiple', ('declareid_multiple', ('declareid_multiple', ('declareid_single', 'i'), 'n'), 'f'), 'x'))), ('statement', ('writeln', ('factor', 'texto dump'))), ('statement', ('assignment', 'f', '=', ('factor', 5))), ('statement', ('for', ('assignment', 'x', '=', ('factor', 0)), ('lt', ('factor', 'x'), ('factor', 'f')), ('increment', 'x'), (('statement', ('assignment', 'n', '=', ('plus', ('factor', 'x'), ('factor', 'f')))),))), ('statement', ('writeln', ('factor', 'n')))))
quad_gen = CodeGen(ast2)
quadruples = quad_gen.generate()

# Intérprete de cuádruplos a pseudocódigo
interpreter = IR_Interpret(quadruples)
pseudo_code = interpreter.interpret()
print(pseudo_code)
"""