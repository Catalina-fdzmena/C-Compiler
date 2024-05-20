# Autor: Andrea Catalina Fernández Mena A01197705
# Fecha: 20/05/2024
# Descripción: SemanticExecuter - El siguiente codigo es un ejecutor y analizador semantico
#Recorre y evalua  todas las entradas del codigo intermedio

class SemanticError(Exception):
    pass

class SemanticExecuter:
    def __init__(self):
        self.memory_var_data = {}

    def get_value(self, arg):
        if isinstance(arg, str) and arg in self.memory_var_data:
            return self.memory_var_data[arg]
        return arg
    
    #Devuelve los tipos de datos
    def get_type(self, value):
        if isinstance(value, int):
            return 'int'
        elif isinstance(value, float):
            return 'float'
        #Pendiente de añadir el resto de tipos 
        return None

    #Evaluación semantica basica de tipos en operaciones
    def _check_operation(self, type1, type2, op):
        rules = {
            ('int', 'int'): 'int',
            ('int', 'float'): 'float',
            ('int', 'double'): 'double',
            ('float', 'int'): 'float',
            ('float', 'float'): 'float',
            ('float', 'double'): 'double',
            ('double', 'int'): 'double',
            ('double', 'float'): 'double',
            ('double', 'double'): 'double',
        }

        if (type1, type2) in rules:
            return rules[(type1, type2)]
        else:
            raise SemanticError(f"Invalid operation {type1} {op} {type2}")

    def interpret(self, quadruple_table):
        quad_table_size = len(quadruple_table)
        quad_id = 0

        #Evaluación y generación de operaciones
        while quad_id < quad_table_size:
            quad = quadruple_table[quad_id]

            arg1_value = self.get_value(quad.arg1)
            arg2_value = self.get_value(quad.arg2)

            arg1_type = self.get_type(arg1_value)
            arg2_type = self.get_type(arg2_value)

            if quad.operator == '=':
                self.memory_var_data[quad.result] = arg1_value
            elif quad.operator in ('+', '-', '*', '/', '%'):
                if arg1_value is None or arg2_value is None:
                    raise ValueError(f"Null value encountered in operation {quad.operator} with args {arg1_value} and {arg2_value}")

                result_type = self._check_operation(arg1_type, arg2_type, quad.operator)

                if quad.operator == '+':
                    self.memory_var_data[quad.result] = arg1_value + arg2_value
                elif quad.operator == '-':
                    self.memory_var_data[quad.result] = arg1_value - arg2_value
                elif quad.operator == '*':
                    self.memory_var_data[quad.result] = arg1_value * arg2_value
                elif quad.operator == '/':
                    self.memory_var_data[quad.result] = arg1_value / arg2_value
                elif quad.operator == '%':
                    self.memory_var_data[quad.result] = arg1_value % arg2_value
            
            elif quad.operator == '==':
                self.memory_var_data[quad.result] = arg1_value == arg2_value
            elif quad.operator == '!=':
                self.memory_var_data[quad.result] = arg1_value != arg2_value
            elif quad.operator == '<':
                self.memory_var_data[quad.result] = arg1_value < arg2_value
            elif quad.operator == '<=':
                self.memory_var_data[quad.result] = arg1_value <= arg2_value
            elif quad.operator == '>':
                self.memory_var_data[quad.result] = arg1_value > arg2_value
            elif quad.operator == '>=':
                self.memory_var_data[quad.result] = arg1_value >= arg2_value
            
            #lectura y diferencia entre write y writeln
            elif quad.operator == 'write':
                print(arg1_value, end='')
            elif quad.operator == 'writeln':
                print(arg1_value)

            #Lectura y evaluación de saltos    
            elif quad.operator == 'goto':     #salta si se indica
                quad_id = quad.result - 1
            elif quad.operator == 'gototrue': #salta si la cond es verdadera
                if arg1_value:
                    quad_id = quad.result - 1
            elif quad.operator == 'gotofalse': #salta si la cond es falsa
                if not arg1_value:
                    quad_id = quad.result - 1
            
            #Evaluaciones de arreglos
            elif quad.operator == 'declare_array':
                array_name = quad.arg2
                array_size = self.get_value(quad.result)
                self.memory_var_data[array_name] = [0] * array_size
            
            elif quad.operator == 'array_assign':
                array_name = quad.arg1
                index = self.get_value(quad.arg2)
                value = self.get_value(quad.result)
                self.memory_var_data[array_name][index] = value
            
            elif quad.operator == 'array_access':
                array_name = quad.arg1
                index = self.get_value(quad.arg2)
                self.memory_var_data[quad.result] = self.memory_var_data[array_name][index]
                
            quad_id += 1

# Ejemplo de uso con uso con el AST
"""
ast2 = ('programstart', 'test', (('statement', ('array_declaration', ('datatype', 'int'), 'arr', 10)), ('statement', ('array_assignment', 'arr', ('factor', 0), ('plus', ('factor', 1), ('factor', 3)))), ('statement', ('array_assignment', 'arr', ('plus', ('factor', 1), ('factor', 3)), ('mult', ('factor', 5), ('factor', 8)))), ('statement', ('assignment', 'x', '=', ('plus', ('factor', ('array_access', 'arr', ('factor', 0))), ('factor', ('array_access', 'arr', ('factor', 1)))))), ('statement', ('write', ('factor', ('array_access', 'arr', ('plus', ('factor', 0), ('factor', 1))))))))
generator2 = CodeGen(ast2)
quadruples2 = generator2.generate()

semantic_analyzer = SemanticExecuter()
semantic_analyzer.interpret(quadruples2)
"""
