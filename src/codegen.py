# Autor: Andrea Catalina Fernández Mena
# Fecha: 20/05/2024
# Descripción: Codegen - Generador de cuadruplos/codigo intermedio a partir de AST proveniente del parser


class QuadrupleGenerator:
    def __init__(self, ast):
        self.ast = ast
        self.quadruples = []
        self.temp_counter = 1 
        self.label_counter = 1  

    def new_temp(self):
        temp = f"T{self.temp_counter}"
        self.temp_counter += 1
        return temp

    def new_label(self):
        label = f"L{self.label_counter}"
        self.label_counter += 1
        return label

    def generate(self):
        self._process_node(self.ast)
        return self.quadruples

    def _process_node(self, node):
        if not node:
            return None

        nodetype = node[0]

        if nodetype == 'programstart':
            for stmt in node[2]:
                self._process_node(stmt)

        elif nodetype == 'statement':
            self._process_node(node[1])

        elif nodetype == 'write':
            value = self._process_node(node[1])
            self.quadruples.append(('write', value, None, None))

        elif nodetype == 'writeln':
            value = self._process_node(node[1])
            self.quadruples.append(('writeln', value, None, None))

        elif nodetype == 'assignment':
            target = node[1]
            value = self._process_node(node[3])
            self.quadruples.append(('=', value, None, target))

        elif nodetype == 'array_declaration':
            datatype = node[1][1]
            array_name = node[2]
            array_size = node[3]
            self.quadruples.append(('declare_array', datatype, array_name, array_size))

        elif nodetype == 'array_assignment':
            array_name = node[1]
            index = self._process_node(node[2])
            value = self._process_node(node[3])
            self.quadruples.append(('array_assign', array_name, index, value))

        elif nodetype == 'array_access':
            array_name = node[1]
            index = self._process_node(node[2])
            temp = self.new_temp()
            self.quadruples.append(('array_access', array_name, index, temp))
            return temp

        elif nodetype == 'if-else':
            condition = self._process_node(node[1])
            true_label = self.new_label()
            false_label = self.new_label()
            end_label = self.new_label()

            self.quadruples.append(('gotofalse', condition, false_label, None))
            self.quadruples.append(('goto', true_label, None, None))

            self.quadruples.append((true_label + ':', None, None, None))
            for stmt in node[2]:
                self._process_node(stmt)

            self.quadruples.append(('goto', end_label, None, None))

            self.quadruples.append((false_label + ':', None, None, None))
            for stmt in node[3]:
                self._process_node(stmt)

            self.quadruples.append((end_label + ':', None, None, None))

        elif nodetype == 'while':
            condition = node[1]
            body = node[2]

            start_label = self.new_label()
            true_label = self.new_label()
            false_label = self.new_label()

            self.quadruples.append((start_label + ':', None, None, None))

            # Condition check
            condition_result = self._process_node(condition)
            self.quadruples.append(('gotofalse', condition_result, false_label, None))
            self.quadruples.append(('goto', true_label, None, None))

            self.quadruples.append((true_label + ':', None, None, None))

            # Loop body
            for stmt in body:
                self._process_node(stmt)

            # Jump back to the start of the loop
            self.quadruples.append(('goto', start_label, None, None))
            self.quadruples.append((false_label + ':', None, None, None))

        elif nodetype == 'plus':
            left = self._process_node(node[1])
            right = self._process_node(node[2])
            temp = self.new_temp()
            self.quadruples.append(('+', left, right, temp))
            return temp

        elif nodetype == 'minus':
            left = self._process_node(node[1])
            right = self._process_node(node[2])
            temp = self.new_temp()
            self.quadruples.append(('-', left, right, temp))
            return temp

        elif nodetype == 'mult':
            left = self._process_node(node[1])
            right = self._process_node(node[2])
            temp = self.new_temp()
            self.quadruples.append(('*', left, right, temp))
            return temp

        elif nodetype == 'lt':
            left = self._process_node(node[1])
            right = self._process_node(node[2])
            temp = self.new_temp()
            self.quadruples.append(('<', left, right, temp))
            return temp

        elif nodetype == 'gt':
            left = self._process_node(node[1])
            right = self._process_node(node[2])
            temp = self.new_temp()
            self.quadruples.append(('>', left, right, temp))
            return temp

        elif nodetype == 'decrement':
            target = node[1]
            temp = self.new_temp()
            self.quadruples.append(('-', target, 1, temp))
            self.quadruples.append(('=', temp, None, target))

        elif nodetype == 'factor':
            if isinstance(node[1], tuple) and node[1][0] == 'array_access':
                return self._process_node(node[1])
            return node[1]

    def _process_declaration(self, node, datatype):
        pass  # No generar cuadruplos para declaraciones

# Ejemplo de uso
ast2 = ('programstart', 'test', (('statement', ('array_declaration', ('datatype', 'int'), 'arr', 10)), ('statement', ('array_assignment', 'arr', ('factor', 0), ('plus', ('factor', 1), ('factor', 3)))), ('statement', ('array_assignment', 'arr', ('plus', ('factor', 1), ('factor', 3)), ('mult', ('factor', 5), ('factor', 8)))), ('statement', ('assignment', 'x', '=', ('plus', ('factor', ('array_access', 'arr', ('factor', 0))), ('factor', ('array_access', 'arr', ('factor', 1)))))), ('statement', ('write', ('factor', ('array_access', 'arr', ('plus', ('factor', 0), ('factor', 1))))))))
generator2 = QuadrupleGenerator(ast2)
quadruples2 = generator2.generate()

for quad in quadruples2:
    print(quad)
