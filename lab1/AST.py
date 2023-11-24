from abc import ABC, abstractmethod


class Node(ABC):
    count = 0

    def __init__(self):
        self.id = str(Node.count)
        Node.count += 1

    @abstractmethod
    def print(self, indent=0):
        pass


class StatementList(
    Node,
):
    def __init__(self, statements, line_number=None):
        super().__init__()
        self.line_number = line_number

        self.statements = statements

    def print(self, indent=0):
        for statement in self.statements:
            statement.print(indent)


class IfStatement(Node):
    def __init__(
        self, expression, statement_if, statement_else=None, line_number=None
    ):
        super().__init__()
        self.line_number = line_number

        self.expression = expression
        self.statement_if = statement_if
        self.statement_else = statement_else

    def print(self, indent=0):
        print("| " * indent + "if")
        self.expression.print(indent + 1)
        print("| " * indent + "then")
        self.statement_if.print(indent + 1)
        if self.statement_else:
            print("| " * indent + "else")
            self.statement_else.print(indent + 1)


class WhileStatement(Node):
    def __init__(
        self, expression, statement, line_number=None
    ):
        super().__init__()
        self.line_number = line_number

        self.expression = expression
        self.statement = statement

    def print(self, indent=0):
        print("| " * indent + "while")
        self.expression.print(indent + 1)
        self.statement.print(indent + 1)


class ForStatement(Node):
    def __init__(
        self, identifier, range_or_list, statement, line_number=None
    ):
        super().__init__()
        self.line_number = line_number

        self.identifier = identifier
        self.range_or_list = range_or_list
        self.statement = statement

    def print(self, indent=0):
        print("| " * indent + "for")
        print("| " * (indent + 1) + self.identifier)
        self.range_or_list.print(indent + 1)
        self.statement.print(indent + 1)


class JumpStatement(Node):
    def __init__(
        self, name, expression=None, line_number=None
    ):
        super().__init__()
        self.line_number = line_number

        self.name = name
        self.expression = expression

    def print(self, indent=0):
        print("| " * indent + self.name)
        if self.expression:
            self.expression.print(indent + 1)


class PrintStatement(Node):
    def __init__(
        self, list_content, line_number=None
    ):
        super().__init__()
        self.line_number = line_number

        self.list_content = list_content

    def print(self, indent=0):
        print("| " * indent + "print")

        for elem in self.list_content:
            if type(elem) == str:
                print("| " * (indent + 1) + elem)
            else:
                elem.print(indent + 1)


class AssignmentStatement(Node):
    def __init__(
        self, id_content, assign_op, expression, line_number=None
    ):
        super().__init__()
        self.line_number = line_number

        self.id_content = id_content
        self.assign_op = assign_op
        self.expression = expression

    def __str__(self):
        return f"{self.id_content}={self.expression}"

    def print(self, indent=0):
        print("| " * indent + str(self.assign_op))
        self.id_content.print(indent + 1)
        if type(self.expression) == str:
            print("| " * indent + self.expression)
        else:
            self.expression.print(indent + 1)


class BinaryOperation(Node):
    def __init__(
        self, left_expression, op, right_expression, line_number=None
    ):
        super().__init__()
        self.line_number = line_number

        self.left_expression = left_expression
        self.op = op
        self.right_expression = right_expression

    def print(self, indent=0):
        print("| " * indent + self.op)
        self.left_expression.print(indent + 1)
        self.right_expression.print(indent + 1)


class UnaryMinusOperation(Node):
    def __init__(
        self, expression, line_number=None
    ):
        super().__init__()
        self.line_number = line_number

        self.expression = expression

    def print(self, indent=0):
        print("| " * indent + "-")
        self.expression.print(indent + 1)


class TransposeOperation(Node):
    def __init__(
        self, expression, line_number=None
    ):
        super().__init__()
        self.line_number = line_number

        self.expression = expression

    def print(self, indent=0):
        print("| " * indent + "transpose")
        self.expression.print(indent + 1)


class Range(Node):
    def __init__(
        self, left_range_element, right_range_element, line_number=None
    ):
        super().__init__()
        self.line_number = line_number

        self.left_range_element = left_range_element
        self.right_range_element = right_range_element

    def print(self, indent=0):
        print("| " * indent + "range")
        self.left_range_element.print(indent + 1)
        self.right_range_element.print(indent + 1)


class RangeElement(Node):
    def __init__(
        self, value, line_number=None
    ):
        super().__init__()
        self.line_number = line_number

        self.value = value

    def print(self, indent=0):
        if type(self.value) == str:
            print("| " * indent + self.value)
        else:
            self.value.print(indent)


class List(Node):
    def __init__(self, list_content, line_number=None):
        super().__init__()
        self.line_number = line_number

        self.list_content = list_content

    def print(self, indent=0):
        print("| " * indent + "vector")
        for elem in self.list_content:
            if isinstance(elem, Node):
                elem.print(indent + 1)
            else:
                print("| " * (indent + 1) + str(elem))


class IdContent(Node):
    def __init__(self, identifier, list_access=None, line_number=None):
        super().__init__()
        self.line_number = line_number

        self.identifier = identifier
        self.list_access = list_access

    def print(self, indent=0):
        if self.list_access:
            print("| " * indent + "ref")
            print("| " * (indent + 1) + self.identifier)
            self.list_access.print(indent + 1)
        else:
            print("| " * indent + self.identifier)


class ListAccess(Node):
    def __init__(self, list_access_element_left, list_access_element_right=None,
                 line_number=None):
        super().__init__()
        self.line_number = line_number

        self.list_access_element_left = list_access_element_left
        self.list_access_element_right = list_access_element_right

    def print(self, indent=0):
        self.list_access_element_left.print(indent)
        if self.list_access_element_right:
            self.list_access_element_right.print(indent)


class ListAccessElement(Node):
    def __init__(self, value, line_number=None):
        super().__init__()
        self.line_number = line_number

        self.value = value

    def print(self, indent=0):
        print("| " * indent + str(self.value))


class MatrixSpecialFunction(Node):
    def __init__(self, function, expression, line_number=None):
        super().__init__()
        self.line_number = line_number

        self.function = function
        self.expression = expression

    def print(self, indent=0):
        print("| " * indent + f"{self.function}")
        self.expression.print(indent + 1)


class Number(Node):
    def __init__(self, value, line_number=None):
        super().__init__()
        self.line_number = line_number

        self.value = value

    def print(self, indent=0):
        print("| " * indent + str(self.value))
