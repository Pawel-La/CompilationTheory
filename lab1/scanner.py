from sly import Lexer
#komentarz

class MyLexer(Lexer):

    tokens = {
        DOT_PLUS, DOT_MINUS, DOT_MUL, DOT_DIV,
        INC_ASSIGN, DEC_ASSIGN, MUL_ASSIGN, DIV_ASSIGN,
        GREATER_EQ, LESS_EQ, NOT_EQ, EQ,
        ID, IF, ELSE, FOR, WHILE, BREAK, CONTINUE, RETURN, PRINT,
        EYE, ZEROS, ONES,
        DECIMAL, FLOAT, STRING
    }

    literals = {
        '+', '-', '*', '/', '>', '<', '=', ',', ';', '(', ')', '[', ']', '{',
        '}', ':', '\''
    }

    DOT_PLUS    = r'\.\+'
    DOT_MINUS   = r'\.-'
    DOT_MUL     = r'\.\*'
    DOT_DIV     = r'\./'

    INC_ASSIGN = r'\+='
    DEC_ASSIGN = r'-='
    MUL_ASSIGN = r'\*='
    DIV_ASSIGN = r'/='

    GREATER_EQ  = r'>='
    LESS_EQ     = r'<='
    NOT_EQ      = r'!='
    EQ          = r'=='

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

    FLOAT   = r'((\d*\.\d+)|(\d+\.))([eE]?\d+)?'
    DECIMAL = r'\d+'
    STRING  = r'(\".*?\")|(\'.*?\')'

    ignore = ' \t'
    ignore_comment = r'\#.*'

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    def error(self, t):
        print('Line %d, Bad character %r' % (self.lineno, t.value[0]))
        self.index += 1
