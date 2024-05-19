
# Autor: Andrea Catalina Fernández Mena
# Fecha: 20/05/2024
# Descripción: Intérprete - Traduce cuádruplos a pseudo-código

from codegen import QuadrupleGenerator

class IntermediateCodeInterpreter:
    def __init__(self, quadruples):
        self.quadruples = quadruples
        self.output = []

    def interpret(self):
        for quad in self.quadruples:
            self._process_quadruple(quad)
        return '\n'.join(self.output)

    def _process_quadruple(self, quad):
        op = quad[0]       # La operación a realizar (e.g., '=', '+', 'write')
        arg1 = quad[1]     # Primer argumento/operando (e.g., valor a asignar, primer operando en una suma)
        arg2 = quad[2]     # Segundo argumento/operando (e.g., segundo operando en una suma)
        result = quad[3]   # Resultado de la operación (e.g., variable donde se almacenará el resultado)

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
        elif op == 'gotofalse':
            self.output.append(f"if not {arg1} goto {arg2}")
        elif op == 'goto':
            self.output.append(f"goto {arg1}")
        elif op.endswith(':'):
            self.output.append(f"{op}")
        elif op == 'declare_array':
            self.output.append(f"declare {arg1} array {arg2}[{result}]")
        elif op == 'array_assign':
            self.output.append(f"{arg1}[{arg2}] = {result}")
        elif op == 'array_access':
            self.output.append(f"{result} = {arg1}[{arg2}]")
        else:
            raise ValueError(f"Unknown operation: {op}")

# Ejemplo de uso
ast2 = ('programstart', 'test', (('statement', ('array_declaration', ('datatype', 'int'), 'arr', 10)), 
                                ('statement', ('array_assignment', 'arr', ('factor', 0), ('plus', ('factor', 1), ('factor', 3)))), 
                                ('statement', ('array_assignment', 'arr', ('plus', ('factor', 1), ('factor', 3)), ('mult', ('factor', 5), ('factor', 8)))), 
                                ('statement', ('assignment', 'x', '=', ('plus', ('factor', ('array_access', 'arr', ('factor', 0))), 
                                                                             ('factor', ('array_access', 'arr', ('factor', 1)))))), 
                                ('statement', ('write', ('factor', ('array_access', 'arr', ('plus', ('factor', 0), ('factor', 1))))))))

generator2 = QuadrupleGenerator(ast2)
quadruples2 = generator2.generate()

interpreter = IntermediateCodeInterpreter(quadruples2)
pseudo_code = interpreter.interpret()
print(pseudo_code)