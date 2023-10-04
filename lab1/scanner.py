from sly import Lexer


class Scanner(Lexer):

    tokens = {
        DOT_PLUS, DOT_MINUS, DOT_MUL, DOT_DIV, INC_ASSIGN, DEC_ASSIGN, MUL_ASSIGN,
        DIV_ASSIGN, BE, SE, NE, EQ, ID, IF, ELSE, FOR, WHILE, BREAK, CONTINUE,
        RETURN, EYE, ZEROS, ONES, PRINT, DECIMAL, FLOAT, STRING
    }

    literals = {
        '+', '-', '*', '/', '>', '<', '=', ',', ';', '(', ')', '[', ']', '{',
        '}', ':', '\''
    }

    DOT_PLUS = r'\.\+'
    DOT_MINUS = r'\.-'
    DOT_MUL = r'\.\*'
    DOT_DIV = r'\./'

    INC_ASSIGN = r'\+='
    DEC_ASSIGN = r'-='
    MUL_ASSIGN = r'\*='
    DIV_ASSIGN = r'/='

    BE = r'>='
    SE = r'<='
    NE = r'!='
    EQ = r'=='

    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['if']        = IF
    ID['else']      = ELSE
    ID['while']     = WHILE
    ID['for']       = FOR
    ID['break']     = BREAK
    ID['continue']  = CONTINUE
    ID['return']    = RETURN
    ID['eye']       = EYE
    ID['zeros']     = ZEROS
    ID['ones']      = ONES
    ID['print']     = PRINT

    FLOAT   = r'(\d*\.\d+[eE]?\d+)|(\d+\.\d*[eE]?\d+)|(\d*\.\d+)|(\d+\.\d*)'
    DECIMAL = r'\d+'
    STRING  = r'(\".*\")|(\'.*\')'

    ignore = ' \t'
    ignore_comment = r'\#.*'

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    def error(self, t):
        print('Line %d, Bad character %r' % (self.lineno, t.value[0]))
        self.index += 1
