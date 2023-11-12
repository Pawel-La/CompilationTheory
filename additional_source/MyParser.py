from sly import Parser
from MyLexer import MyLexer
class MyParser(Parser):
    tokens = MyLexer.tokens
    literals = MyLexer.literals

    precedence = (
        ("nonassoc", ELSE),
        ("nonassoc", "=", INCREMENT, DECREMENT, MULTIPLY_INCITU, DIVIDE_INCITU),
        ("nonassoc", EQUAL, NOT_EQUAL),
        ("nonassoc", "<", ">", LESS_OR_EQUAL, MORE_OR_EQUAL ),
        ('left', "+", "-", MATRIX_PLUS, MATRIX_MINUS),
        ('left', '*', '/', MATRIX_TIMES, MATRIX_DIVIDE),

    )

    def __init__(self):
        self.names = {}

    @_('statements statement')
    def statements(self, p):
        return p.statements + [p.statement]

    @_('statement')
    def statements(self, p):
        return [p.statement]

    @_('"{" statements "}"')
    def statement(self, p):
        return 
    @_('ID "=" expression ";"')
    def statement(self, p):
        self.names[p.ID] = p.expression
        return None

    @_('expression ";"')
    def statement(self, p):
        return None

    @_('expression')
    def statement(self, p):
        return None

    @_('expression "+" expression')
    def expression(self, p):
        return p.expression0 + p.expression1

    @_('expression "-" expression')
    def expression(self, p):
        return p.expression0 - p.expression1

    @_('expression "*" expression')
    def expression(self, p):
        return p.expression0 * p.expression1

    @_('expression "/" expression')
    def expression(self, p):
        return p.expression0 / p.expression1

    @_('INT')
    def expression(self, p):
        return int(p.INT)
    
    @_('FLOAT')
    def expression(self, p):
        return float(p.FLOAT)

    @_('STRING')
    def expression(self, p):
        return p.STRING[1:-1] 

    @_('ID')
    def expression(self, p):
        return self.names.get(p.ID, None)
    
    @_ ('"[" matrix_rows "]" "\'"',
        'ID "\'" ')
    def expression(self, p):
        if p[0] == '[':
            matrix = p[1]
        else:
            matrix = self.names.get(p[0])
        n = len(matrix)
        m = len(matrix[0])
        return [[matrix[i][j] for i in range(n)]for j in range(m)]

    @_('"[" matrix_rows "]" MATRIX_PLUS "[" matrix_rows "]"',
        '"[" matrix_rows "]" MATRIX_PLUS ID',
        'ID MATRIX_PLUS "[" matrix_rows "]"',
        'ID MATRIX_PLUS ID')
    def expression(self, p):
        if self.names.get(p[0],None) != None:
            matrix1 = self.names[p[0]]
        else:
            matrix1 = p.expression0
        if self.names.get(p[2], None) != None or (len(p) > 2 and self.names.get([p[4]], None) != None):
            matrix2 = self.names[p[0]]
        else:
            matrix2 = p.expression1
        if len(matrix1) != len(matrix2) or len(matrix1[0]) != len(matrix2[0]):
            raise ValueError("Matrix dimensions do not match for addition")
        result = [[matrix1[i][j] + matrix2[i][j] for j in range(len(matrix1[0]))] for i in range(len(matrix1))]
        return result

    @_('"[" matrix_rows "]" MATRIX_MINUS "[" matrix_rows "]"',
        '"[" matrix_rows "]" MATRIX_MINUS ID',
        'ID MATRIX_MINUS "[" matrix_rows "]"',
        'ID MATRIX_MINUS ID',
        
        '"[" matrix_rows "]" "-" "[" matrix_rows "]"',
        '"[" matrix_rows "]" "-" ID',
        'ID "-" "[" matrix_rows "]"',
        'ID "-" ID'
        )
    def expression(self, p):
        if self.names.get(p[0],None) != None:
            matrix1 = self.names[p[0]]
        else:
            matrix1 = p.expression0
        if self.names.get(p[2], None) != None or (len(p) > 2 and self.names.get([p[4]], None) != None):
            matrix2 = self.names[p[0]]
        else:
            matrix2 = p.expression1
        if len(matrix1) != len(matrix2) or len(matrix1[0]) != len(matrix2[0]):
            raise ValueError("Matrix dimensions do not match for subtraction")
        result = [[matrix1[i][j] - matrix2[i][j] for j in range(len(matrix1[0]))] for i in range(len(matrix1))]
        return result

    @_('"[" matrix_rows "]" "*" "[" matrix_rows "]"',
        '"[" matrix_rows "]" "*" ID',
        'ID "*" "[" matrix_rows "]"',
        'ID "*" ID')
    def expression(self, p):
        if self.names.get(p[0],None) != None:
            matrix1 = self.names[p[0]]
        else:
            matrix1 = p.expression0
        if self.names.get(p[2], None) != None or (len(p) > 2 and self.names.get([p[4]], None) != None):
            matrix2 = self.names[p[0]]
        else:
            matrix2 = p.expression1
        if len(matrix1[0]) != len(matrix2):
            raise ValueError("Matrix dimensions do not match for multiplication by element")
        result = [[0 for _ in range(len(matrix2[0]))] for _ in range(len(matrix1))]
        for i in range(len(matrix1)):
            for j in range(len(matrix2[0])):
                for k in range(len(matrix2)):
                    result[i][j] += matrix1[i][k] * matrix2[k][j]
        return result
    
    @_('"[" matrix_rows "]" MATRIX_TIMES "[" matrix_rows "]"',
        '"[" matrix_rows "]" MATRIX_TIMES ID',
        'ID MATRIX_TIMES "[" matrix_rows "]"',
        'ID MATRIX_TIMES ID')
    def expression(self, p):
        if self.names.get(p[0],None) != None:
            matrix1 = self.names[p[0]]
        else:
            matrix1 = p.expression0
        if self.names.get(p[2], None) != None or (len(p) > 2 and self.names.get([p[4]], None) != None):
            matrix2 = self.names[p[0]]
        else:
            matrix2 = p.expression1
        if len(matrix1) != len(matrix2) or len(matrix1[0]) != len(matrix2[0]):
            raise ValueError("Matrix dimensions do not match for multiplication by element")
        result = [[matrix1[i][j] * matrix2[i][j] for j in range(len(matrix1[0]))] for i in range(len(matrix1))]
        return result
    
    @_('"[" matrix_rows "]" MATRIX_DIVIDE "[" matrix_rows "]"',
        '"[" matrix_rows "]" MATRIX_DIVIDE ID',
        'ID MATRIX_DIVIDE "[" matrix_rows "]"',
        'ID MATRIX_DIVIDE ID')
    def expression(self, p):
        if self.names.get(p[0],None) != None:
            matrix1 = self.names[p[0]]
        else:
            matrix1 = p.expression0
        if self.names.get(p[2], None) != None or (len(p) > 2 and self.names.get([p[4]], None) != None):
            matrix2 = self.names[p[0]]
        else:
            matrix2 = p.expression1
        if len(matrix1) != len(matrix2) or len(matrix1[0]) != len(matrix2[0]):
            raise ValueError("Matrix dimensions do not match for multiplication by element")
        result = [[matrix1[i][j] / matrix2[i][j] for j in range(len(matrix1[0]))] for i in range(len(matrix1))]
        return result
    
    @_('"[" matrix_rows "]" "[" INT "," INT "]"',
       'ID "[" INT "," INT "]"')
    def expression(self, p):
        if self.names.get(p[0],None) != None:
            matrix1 = self.names[p[0]]
        else:
            raise NameError()
        
        return self.names[p[0]][int(p[-4])][int(p[-2])]
    
    @_('"[" matrix_rows "]" "[" INT "," INT "]" "=" expression',
       'ID "[" INT "," INT "]" "=" expression')
    def expression(self, p):
        if self.names.get(p[0],None) != None:
            matrix1 = self.names[p[0]]
        else:
            raise NameError()
        
        self.names[p[0]][int(p[-6])][int(p[-4])] = p[-1]

    @_('matrix_rows')
    def matrix_rows(self, p):
        return p.matrix_rows

    @_('matrix_row')
    def matrix_rows(self, p):
        return [p.matrix_row]
    
##########################
    @_('"[" matrix_rows "]"')
    def matrix(self, p):
        return p.matrix_rows

    @_(' matrix ')
    def expression(self, p):
        return p.matrix
###########################
    @_('matrix_rows "," matrix_row')
    def matrix_rows(self, p):
        return p.matrix_rows + [p.matrix_row]

    @_('"[" matrix_elements "]"')
    def matrix_row(self, p):
        return p.matrix_elements

    @_('matrix_elements')
    def matrix_row(self, p):
        return p.matrix_elements

    @_('expression')
    def matrix_elements(self, p):
        
        #
        return [p.expression]

    @_('matrix_elements "," expression')
    def matrix_elements(self, p):
        return p.matrix_elements + [p.expression]
    
    @_('PRINT  expression ";"')
    def statement(self, p):
        result = p.expression
        print(result)  # Wyświetlenie wyniku na konsoli
        return None
    
    @_('ZEROS "(" INT ")"')
    def expression(self,p):
        n = int(p[2])
        return [[0 for _ in range(n)] for _ in range(n)]
    
    @_('ONES "(" INT ")"')
    def expression(self,p):
        n = int(p[2])
        return [[1 for _ in range(n)] for _ in range(n)]
    
    @_('EYE "(" INT ")"')
    def expression(self,p):
        n = int(p[2])
        return [[1 if i==j else 0 for i in range(n)] for j in range(n)]

    @_('"-" INT')
    def expression(self, p):
        return -int(p[-1])
    
    @_('"-" FLOAT')
    def expression(self, p):
        return -float(p[-1])
    
    @_('"-" ID')
    def expression(self, p):
        if isinstance(self.names[p[-1]], list):
            matrix = self.names[p[-1]]
            n = len(matrix)
            m = len(matrix[0])
            return [[-1*matrix[i][j] for j in range(m)] for i in range(n)]
        else:
            return -self.names[p[-1]]
    
    @_('ID DECREMENT expression')
    def statement(self, p):
        if self.names.get(p[0],None) == None:
            print(self.names,p[0])
            raise NameError()
        
        self.names[p[0]] -= p[-1]

    @_('ID INCREMENT expression')
    def statement(self, p):
        if self.names.get(p[0],None) == None:
            print(self.names,p[0])
            raise NameError()
        
        self.names[p[0]] += p[-1]

    @_('ID MULTIPLY_INCITU expression')
    def statement(self, p):
        if self.names.get(p[0],None) == None:
            raise NameError()
        var = self.names[p[0]]
        if isinstance(var, list):
            matrix1 = var
            matrix2 = p[-1]
            result = [[0 for _ in range(len(matrix2[0]))] for _ in range(len(matrix1))]
            for i in range(len(matrix1)):
                for j in range(len(matrix2[0])):
                    for k in range(len(matrix2)):
                        result[i][j] += matrix1[i][k] * matrix2[k][j]
            return result
        var *= p[-1]

    @_('ID DIVIDE_INCITU expression')
    def statement(self, p):
        if self.names.get(p[0],None) == None:
            raise NameError()
        
        self.names[p[0]] /= p[-1]
    
    @_('IF "(" expression ")" "{" statements "}"')
    def statement(self, p):
        if p.expression:
            print(p.statements)
            for stmt in p.statements:
                self.parse(stmt)
    
    @_('IF "(" expression ")" statement')
    def statement(self, p):
        if p.expression:
            self.execute(p.statement)

    @_('IF expression "{" statements "}" ELSE "{" statements "}"')
    def statement(self, p):
        if p.expression:
            for stmt in p.statements0:
                self.execute(stmt)
        else:
            for stmt in p.statements1:
                self.execute(stmt)

    @_('WHILE "(" expression ")" "{" statements "}"')
    def statement(self, p):
        while p.expression:
            for stmt in p.statements:
                self.execute(stmt)

    @_('FOR ID "=" expression ":" expression "{" statements "}"')
    def statement(self, p):
        start = p.expression0
        end = p.expression1
        for i in range(start, end + 1):
            self.names[p.ID] = i
            for stmt in p.statements:
                self.parse(stmt)
    
    @_('expression EQUAL expression')
    def expression(self, p):
        return p.expression0 == p.expression1

    @_('expression NOT_EQUAL expression')
    def expression(self, p):
        return p.expression0 != p.expression1

    @_('expression "<" expression')
    def expression(self, p):
        return p.expression0 < p.expression1

    @_('expression LESS_OR_EQUAL expression')
    def expression(self, p):
        return p.expression0 <= p.expression1

    @_('expression ">" expression')
    def expression(self, p):
        return p.expression0 > p.expression1

    @_('expression MORE_OR_EQUAL expression')
    def expression(self, p):
        return p.expression0 >= p.expression1

if __name__ == '__main__':
    lexer = MyLexer()
    parser = MyParser()

    # input_text = """
    # A = [[1 + 1, 2, 3], [4, 5, 6], [7, 8, 9]] + [[9, 8, 7], [6, 5, 4], [3, 2, 1]];
    # B = A;
    # C = A ./ B;
    # """
    print(dir(parser))
    with open("example1.m","r") as f:
        input_text = f.read()
    result = parser.parse(lexer.tokenize(input_text))
    
    for i in parser.names.items():
        print(i)
