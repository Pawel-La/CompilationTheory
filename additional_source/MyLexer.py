from sly import Lexer

class MyLexer(Lexer):
    # Set of token names.   This is always required
    tokens = {
            MATRIX_PLUS, MATRIX_MINUS, MATRIX_TIMES, MATRIX_DIVIDE,
            
            EQUAL, LESS_OR_EQUAL, MORE_OR_EQUAL, NOT_EQUAL,

            INCREMENT, DECREMENT, MULTIPLY_INCITU, DIVIDE_INCITU,

    
            IF, ELSE, FOR, WHILE,
    
            BREAK, CONTINUE, RETURN,

            EYE, ONES, ZEROS,

            PRINT,
    
            ID,
            
            INT, FLOAT, STRING,
            }

    literals = {'+','-','*','/', "{", "[", "(", ")", "]", "}", ":", ",", ";", "'", "=", "<", ">"}
    # String containing ignored characters between tokens
    ignore = ' \t'

    ignore_comment = r'\#.*'

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)
    FLOAT = r'[1-9][0-9]*\.[0-9]+([eE][-]?[0-9]+)?'
    INT  = r'[0-9]+'


    # operatory macierzowe    
    MATRIX_PLUS    = r'\.\+'
    MATRIX_MINUS   = r'\.-'
    MATRIX_TIMES   = r'\.\*'
    MATRIX_DIVIDE  = r'\./'

    # operatory relacyjne
    EQUAL = r'=='
    LESS_OR_EQUAL = r'<=' 
    MORE_OR_EQUAL = r'>='
    NOT_EQUAL = r'!='

    # operatory przypisania
    INCREMENT = r'\+='
    DECREMENT = r'-='
    MULTIPLY_INCITU = r'\*='
    DIVIDE_INCITU = r'/='

    
    STRING = r'\'[^\']*\'|\"[^\"]*\"'



    
    # # identyfikatory
    ID      = r'[a-zA-Z_][a-zA-Z0-9_]*'

    # słowa kluczowe
    ID['if'] = IF
    ID['else'] = ELSE
    ID['while'] = WHILE
    ID['print'] = PRINT
    
    ID['break'] = BREAK
    ID['continue'] = CONTINUE
    ID['return'] = RETURN

    ID['eye'] = EYE
    ID['ones'] = ONES
    ID['zeros'] = ZEROS

    ID['print'] = PRINT
    


    # 
    
    

if __name__ == '__main__':
    data = """I =\n eye(10);\nones(5);\n b = 4 -2.2\n c = 2<=3 'if' {else}"""
    lexer = MyLexer()
    for tok in lexer.tokenize(data):
        print('type=%r, value=%r' % (tok.type, tok.value))