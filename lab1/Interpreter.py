import AST
from Memory import MemoryStack
from Exceptions import *
from VisitDecorators import when, on
import sys
import numpy as np

sys.setrecursionlimit(10000)


class Interpreter(object):
    def __init__(self):
        self.memory = MemoryStack()

    @on("node")
    def visit(self, node):
        pass

    @when(AST.StatementList)
    def visit(self, node: AST.StatementList):
        for statement in node.statements:
            self.visit(statement)

    @when(AST.IfStatement)
    def visit(self, node: AST.IfStatement):
        self.memory.push_memory_to_stack()

        if self.visit(node.expression):
            self.visit(node.statement_if)
        elif node.statement_else is not None:
            self.visit(node.statement_else)

        self.memory.pop_memory_from_stack()

    @when(AST.WhileStatement)
    def visit(self, node: AST.WhileStatement):
        self.memory.push_memory_to_stack()

        while self.visit(node.expression):
            try:
                self.visit(node.statement)
            except ContinueException:
                continue
            except BreakException:
                break

        self.memory.pop_memory_from_stack()

    @when(AST.ForStatement)
    def visit(self, node: AST.ForStatement):
        self.memory.push_memory_to_stack()

        list_to_iterate = self.visit(node.range_or_list)
        try:
            for el in list_to_iterate:
                try:
                    self.memory.set_variable(node.identifier, el)
                    self.visit(node.statement)
                except ContinueException:
                    continue
                except BreakException:
                    break
        finally:
            self.memory.pop_memory_from_stack()

    @when(AST.PrintStatement)
    def visit(self, node: AST.PrintStatement):
        visits = [self.visit(el) for el in node.expression]
        for i in range(len(visits) - 1):
            print(visits[i], end=", ")
        print(visits[-1])

    @when(AST.AssignmentStatement)
    def visit(self, node: AST.AssignmentStatement):
        right = self.visit(node.expression)

        if node.assign_op == "=":
            if node.id_content.list_access is None:
                self.memory.set_variable(node.id_content.identifier, right)
            else:
                variable = self.memory.get_variable(node.id_content.identifier)
                list_access = self.visit(node.id_content.list_access)

                if type(list_access) == int:
                    variable[list_access] = right
                else:
                    if type(list_access[0]) == int:
                        x1 = list_access[0]
                        x2 = x1 + 1
                    else:
                        x1 = list_access[0][0]
                        x2 = list_access[0][1]

                    if type(list_access[1]) == int:
                        y1 = list_access[1]
                        y2 = y1 + 1
                    else:
                        y1 = list_access[1][0]
                        y2 = list_access[1][1]
                    variable[x1: x2, y1: y2] = right

        else:
            variable = self.memory.get_variable(node.id_content.identifier)
            if node.assign_op == "+=":
                self.memory.set_variable(node.id_content.identifier,
                                         variable + right)
            elif node.assign_op == "-=":
                self.memory.set_variable(node.id_content.identifier,
                                         variable - right)
            elif node.assign_op == "*=":
                self.memory.set_variable(node.id_content.identifier,
                                         variable * right)
            elif node.assign_op == "/=":
                self.memory.set_variable(node.id_content.identifier,
                                         variable / right)

    @when(AST.BinaryOperation)
    def visit(self, node: AST.BinaryOperation):
        left = self.visit(node.left_expression)
        right = self.visit(node.right_expression)

        ops = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': lambda x, y: x / y,
            '.+': lambda x, y: x + y,
            '.-': lambda x, y: x - y,
            '.*': np.multiply,
            './': np.divide,
            '==': lambda x, y: x == y,
            '!=': lambda x, y: x != y,
            '>=': lambda x, y: x >= y,
            '<=': lambda x, y: x <= y,
            '<': lambda x, y: x < y,
            '>': lambda x, y: x > y
        }

        return ops[node.op](left, right)
    
    @when(AST.JumpStatement)
    def visit(self, node: AST.JumpStatement):
        print(node.name)
        if node.name == "BREAK":
            raise BreakException()
        
        if node.name == "CONTINUE":
            raise ContinueException()

    @when(AST.Range)
    def visit(self, node: AST.Range):
        result = np.arange(
            self.visit(node.left_range_element),
            self.visit(node.right_range_element)
        )
        return result

    @when(AST.RangeElement)
    def visit(self, node: AST.RangeElement):
        if isinstance(node.value, str):
            return self.memory.get_variable(node.value)

        return self.visit(node.value)

    @when(AST.List)
    def visit(self, node: AST.List):
        return list(map(lambda el: self.visit(el), node.list_content))

    @when(AST.IdContent)
    def visit(self, node: AST.IdContent):
        if node.list_access is None:
            return self.memory.get_variable(node.identifier)
        else:
            variable = self.memory.get_variable(node.identifier)
            list_access = self.visit(node.list_access)

            for access in list_access:
                variable = variable[access]

            return variable

    @when(AST.ListAccess)
    def visit(self, node: AST.ListAccess):
        left_element = self.visit(node.list_access_element_left)
        right_element = None

        if node.list_access_element_right:
            right_element = self.visit(node.list_access_element_right)

        return left_element, right_element

    @when(AST.ListAccessElement)
    def visit(self, node: AST.ListAccessElement):
        if type(node.value) == int:
            return node.value
        if type(node.value) == str:
            return self.memory.get_variable(node.value)
        return self.visit(node.value)

    @when(AST.ListAccessElementRange)
    def visit(self, node: AST.ListAccessElementRange):
        return node.from_value, node.to_value

    @when(AST.MatrixSpecialFunction)
    def visit(self, node: AST.MatrixSpecialFunction):
        size = self.visit(node.expression)
        if node.function == 'zeros':
            return np.zeros((size, size))
        elif node.function == 'ones':
            return np.ones((size, size))
        elif node.function == 'eye':
            return np.eye(size)

    @when(AST.Number)
    def visit(self, node: AST.Number):
        return node.value

    @when(AST.String)
    def visit(self, node: AST.String):
        return node.value
