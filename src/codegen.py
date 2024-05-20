# Autor: Andrea Catalina Fernández Mena A01197705
# Fecha: 20/05/2024
# Descripción: Codegen - Generador de cuadruplos/codigo intermedio a partir de AST proveniente del parser

#Declaracion de estructura de cuadruplos
class Quadruple:
    def __init__(self, operator, arg1, arg2, result):
        self.operator = operator
        self.arg1 = arg1
        self.arg2 = arg2
        self.result = result

    def __repr__(self):
        return f"({self.operator}, {self.arg1}, {self.arg2}, {self.result})"

#Generación de cuadruplos
class CodeGen:
    def __init__(self, ast):
        self.ast = ast
        self.quadruples = []
        self.symbol_table = {}
        self.temp_counter = 0

    def temp_gen(self):
        temp = f"T{self.temp_counter}"
        self.temp_counter += 1
        return temp

    def generate(self):
        self._process_node(self.ast)
        return self.quadruples
    
    #nodos para producir cuadruplos, nodos con indice representan los saltos condicionales y no condicionales
    def _process_node(self, node):
        if not node:
            return None
        nodetype = node[0]

        if nodetype == 'programstart':
            for stmt in node[2]:
                self._process_node(stmt)

        elif nodetype == 'statement':
            self._process_node(node[1])

        #Metodos para imprimir
        elif nodetype == 'write':
            value = self._process_node(node[1])
            self.quadruples.append(Quadruple('write', value, None, None))

        elif nodetype == 'writeln':
            value = self._process_node(node[1])
            self.quadruples.append(Quadruple('writeln', value, None, None))

        #Asignacion (=) en cuadruplos
        elif nodetype == 'assignment':
            target = node[1]
            value = self._process_node(node[3])
            self.quadruples.append(Quadruple('=', value, None, target))

        #Metodos para declaracion, asignación y acceso de arreglos
        elif nodetype == 'array_declaration':
            datatype = node[1][1]
            array_name = node[2]
            array_size = node[3]
            self.symbol_table[array_name] = {'type': datatype, 'size': array_size}
            self.quadruples.append(Quadruple('declare_array', datatype, array_name, array_size))

        elif nodetype == 'array_assignment':
            array_name = node[1]
            index = self._process_node(node[2])
            value = self._process_node(node[3])
            self.quadruples.append(Quadruple('array_assign', array_name, index, value))

        elif nodetype == 'array_access':
            array_name = node[1]
            index = self._process_node(node[2])
            temp = self.temp_gen()
            self.quadruples.append(Quadruple('array_access', array_name, index, temp))
            return temp

        #Acomodo de saltos en condicional if-else
        elif nodetype == 'if-else':
            condition = self._process_node(node[1])
            temp_condition = self.temp_gen()
            self.quadruples.append(Quadruple('=', condition, None, temp_condition))
            false_jump = len(self.quadruples)
            self.quadruples.append(Quadruple('gotofalse', temp_condition, None, None))

            for stmt in node[2]:
                self._process_node(stmt)
            end_jump = len(self.quadruples)
            self.quadruples.append(Quadruple('goto', None, None, None))

            self.quadruples[false_jump].result = len(self.quadruples)

            for stmt in node[3]:
                self._process_node(stmt)

            self.quadruples[end_jump].result = len(self.quadruples)

        #Acomodo de saltos en ciclo while
        elif nodetype == 'while':
            start_jump = len(self.quadruples)
            condition = node[1]
            body = node[2]

            condition_result = self._process_node(condition)
            temp_condition = self.temp_gen()
            self.quadruples.append(Quadruple('=', condition_result, None, temp_condition))
            false_jump = len(self.quadruples)
            self.quadruples.append(Quadruple('gotofalse', temp_condition, None, None))

            for stmt in body:
                self._process_node(stmt)

            self.quadruples.append(Quadruple('goto', None, None, start_jump))
            self.quadruples[false_jump].result = len(self.quadruples)

        #Acomodo de saltos en ciclo for 
        elif nodetype == 'for':
            self._process_node(node[1])  # init 
            start_jump = len(self.quadruples)
            condition = self._process_node(node[2])  # condicional
            temp_condition = self.temp_gen()
            self.quadruples.append(Quadruple('=', condition, None, temp_condition))
            false_jump = len(self.quadruples)
            self.quadruples.append(Quadruple('gotofalse', temp_condition, None, None))
            self.quadruples.append(Quadruple('gototrue', temp_condition, None, None))
            true_jump = len(self.quadruples)-1
            increment_jump = len(self.quadruples)
            self._process_node(node[3])  # incremento
            self.quadruples.append(Quadruple('goto', None, None, start_jump))
            self.quadruples[true_jump].result = len(self.quadruples)
            for stmt in node[4]:  # body
                self._process_node(stmt)


            self.quadruples.append(Quadruple('goto', None, None, increment_jump))
            self.quadruples[false_jump].result = len(self.quadruples)

        #Acomodo de operadores
        elif nodetype == 'plus':
            left = self._process_node(node[1])
            right = self._process_node(node[2])
            temp = self.temp_gen()
            self.quadruples.append(Quadruple('+', left, right, temp))
            return temp

        elif nodetype == 'minus':
            left = self._process_node(node[1])
            right = self._process_node(node[2])
            temp = self.temp_gen()
            self.quadruples.append(Quadruple('-', left, right, temp))
            return temp

        elif nodetype == 'mult':
            left = self._process_node(node[1])
            right = self._process_node(node[2])
            temp = self.temp_gen()
            self.quadruples.append(Quadruple('*', left, right, temp))
            return temp

        elif nodetype == 'divide':
            left = self._process_node(node[1])
            right = self._process_node(node[2])
            temp = self.temp_gen()
            self.quadruples.append(Quadruple('/', left, right, temp))
            return temp

        elif nodetype == 'mod':
            left = self._process_node(node[1])
            right = self._process_node(node[2])
            temp = self.temp_gen()
            self.quadruples.append(Quadruple('%', left, right, temp))
            return temp

        elif nodetype == 'lt':
            left = self._process_node(node[1])
            right = self._process_node(node[2])
            temp = self.temp_gen()
            self.quadruples.append(Quadruple('<', left, right, temp))
            return temp

        elif nodetype == 'gt':
            left = self._process_node(node[1])
            right = self._process_node(node[2])
            temp = self.temp_gen()
            self.quadruples.append(Quadruple('>', left, right, temp))
            return temp

        elif nodetype == 'le':
            left = self._process_node(node[1])
            right = self._process_node(node[2])
            temp = self.temp_gen()
            self.quadruples.append(Quadruple('<=', left, right, temp))
            return temp

        elif nodetype == 'ge':
            left = self._process_node(node[1])
            right = self._process_node(node[2])
            temp = self.temp_gen()
            self.quadruples.append(Quadruple('>=', left, right, temp))
            return temp

        elif nodetype == 'ne':
            left = self._process_node(node[1])
            right = self._process_node(node[2])
            temp = self.temp_gen()
            self.quadruples.append(Quadruple('!=', left, right, temp))
            return temp

        elif nodetype == 'booleq':
            left = self._process_node(node[1])
            right = self._process_node(node[2])
            temp = self.temp_gen()
            self.quadruples.append(Quadruple('==', left, right, temp))
            return temp

        elif nodetype == 'and':
            left = self._process_node(node[1])
            right = self._process_node(node[2])
            temp = self.temp_gen()
            self.quadruples.append(Quadruple('&&', left, right, temp))
            return temp

        elif nodetype == 'or':
            left = self._process_node(node[1])
            right = self._process_node(node[2])
            temp = self.temp_gen()
            self.quadruples.append(Quadruple('||', left, right, temp))
            return temp

        elif nodetype == 'increment':
            variable = node[1]
            self.quadruples.append(Quadruple('=', variable, None, variable))
            self.quadruples.append(Quadruple('+', variable, 1, variable))

        elif nodetype == 'decrement':
            target = node[1]
            self.quadruples.append(Quadruple('-', target, 1, target))

        elif nodetype == 'factor':
            if isinstance(node[1], tuple) and node[1][0] == 'array_access':
                return self._process_node(node[1])
            return node[1]

        elif nodetype == 'declaration':
            self._process_declaration(node[2], node[1][1])

#Declaración de variables 
    def _process_declaration(self, node, datatype):
        if node[0] == 'declareid_single':
            self.symbol_table[node[1]] = datatype
            self.quadruples.append(Quadruple('=', None, None, node[1]))
        elif node[0] == 'declareid_multiple':
            self._process_declaration(node[1], datatype)
            self.symbol_table[node[-1]] = datatype
            self.quadruples.append(Quadruple('=', None, None, node[-1]))
        elif node[0] == 'declareid_single_d':
            var_id = node[1][1]
            expression = node[1][3]
            self._process_assignment(var_id, expression)
        elif node[0] == 'declareid_multiple_d':
            self._process_declaration(node[1], datatype)
            var_id = node[-1][1]
            expression = node[-1][3]
            self._process_assignment(var_id, expression)

#Genera cuadruplos para asignar valores a variables 
    def _process_assignment(self, var_id, expression):
        if expression[0] == 'expression_typedata':
            self.quadruples.append(Quadruple('=', expression[1], None, var_id))
        elif expression[0] == 'expression_operations':
            operator = expression[2]
            left = expression[1][1]
            right = expression[3][1]
            if expression[1][0] != 'expression_typedata':
                left = self.temp_gen()
                self._process_assignment(left, expression[1])
            if expression[3][0] != 'expression_typedata':
                right = self.temp_gen()
                self._process_assignment(right, expression[3])
            temp = self.temp_gen()
            self.quadruples.append(Quadruple(operator, left, right, temp))
            self.quadruples.append(Quadruple('=', temp, None, var_id))
        elif expression[0] == 'expression_parenthesis':
            self._process_assignment(var_id, expression[1])


# Pruebas para uso de cuádruplos
"""
ast2 = ('programstart', 'test', (('statement', ('array_declaration', ('datatype', 'int'), 'arr', 10)), ('statement', ('array_assignment', 'arr', ('factor', 0), ('plus', ('factor', 1), ('factor', 3)))), ('statement', ('array_assignment', 'arr', ('plus', ('factor', 1), ('factor', 3)), ('mult', ('factor', 5), ('factor', 8)))), ('statement', ('assignment', 'x', '=', ('plus', ('factor', ('array_access', 'arr', ('factor', 0))), ('factor', ('array_access', 'arr', ('factor', 1)))))), ('statement', ('write', ('factor', ('array_access', 'arr', ('plus', ('factor', 0), ('factor', 1))))))))
quad_gen = CodeGen(ast2)
quadruples = quad_gen.generate()

counter = 0
for quad in quadruples:
    print(f"L{counter}", quad)
    counter += 1
"""
