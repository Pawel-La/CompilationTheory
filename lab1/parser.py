from sly import Parser
from scanner import MyLexer


class MyParser(Parser):
    debugfile = 'parser.out'
    tokens = MyLexer.tokens

    precedence = (
        ("nonassoc", IF_PREC),
        ("nonassoc", ELSE),
        ('nonassoc', "=", INC_ASSIGN, DEC_ASSIGN, MUL_ASSIGN, DIV_ASSIGN),
        ('nonassoc', EQ, NOT_EQ),
        ('nonassoc', "<", ">", GREATER_EQ, LESS_EQ),
        ('left', "+", "-", DOT_PLUS, DOT_MINUS),
        ('left', "*", "/", DOT_MUL, DOT_DIV),
        ('right', UMINUS),
        ('left', "\'")
    )

    @_(
        "Statement StatementList",
        "Statement"
    )
    def StatementList(self, p):
        pass

    @_(
        "CompoundStatement",
        "IfStatement",
        "WhileStatement",
        "ForStatement",
        'JumpStatement ";"',
        'PrintStatement ";"',
        'AssignmentStatement ";"',
        'Expression ";"',
    )
    def Statement(self, p):
        pass

    @_('"{" StatementList "}"')
    def CompoundStatement(self, p):
        pass

    # had to defined IF_PREC here because it didn't define itself automatically
    @_(
        'IF "(" Expression ")" Statement %prec IF_PREC',
        'IF "(" Expression ")" Statement ELSE Statement',
    )
    def IfStatement(self, p):
        pass

    @_('WHILE "(" Expression ")" Statement')
    def WhileStatement(self, p):
        pass

    @_(
        'FOR ID "=" Range Statement',
        'FOR ID "=" List Statement',
    )
    def ForStatement(self, p):
        pass

    @_(
        "BREAK",
        "CONTINUE",
        "RETURN Expression",
    )
    def JumpStatement(self, p):
        pass

    @_("PRINT ListContent")
    def PrintStatement(self, p):
        pass

    @_(
        'LeftValue "="         Expression',
        "LeftValue INC_ASSIGN  Expression",
        "LeftValue DEC_ASSIGN  Expression",
        "LeftValue DIV_ASSIGN  Expression",
        "LeftValue MUL_ASSIGN  Expression",
    )
    def AssignmentStatement(self, p):
        pass

    @_(
        'Expression "+"         Expression',
        'Expression "-"         Expression',
        'Expression "*"         Expression',
        'Expression "/"         Expression',
        'Expression DOT_PLUS    Expression',
        'Expression DOT_MINUS   Expression',
        'Expression DOT_MUL     Expression',
        'Expression DOT_DIV     Expression',
        'Expression EQ          Expression',
        'Expression NOT_EQ      Expression',
        'Expression GREATER_EQ  Expression',
        'Expression LESS_EQ     Expression',
        'Expression ">"         Expression',
        'Expression "<"         Expression',
        '"(" Expression ")"',
        '"-" Expression %prec UMINUS',
        'Expression "\'"',
        "List",
        "Number",
        "STRING",
        "LeftValue",
        "MatrixFunction",
    )
    def Expression(self, p):
        pass

    @_('RangeElement ":" RangeElement')
    def Range(self, p):
        pass

    @_(
        "Number",
        "ID"
    )
    def RangeElement(self, p):
        pass

    @_('"[" ListContent "]"')
    def List(self, p):
        pass

    @_(
        'Expression "," ListContent',
        "Expression",
    )
    def ListContent(self, p):
        pass

    @_(
        "ID",
        "ID List",
    )
    def LeftValue(self, p):
        pass

    @_(
        'EYE "(" Expression ")"',
        'ZEROS "(" Expression ")"',
        'ONES "(" Expression ")"',
    )
    def MatrixFunction(self, p):
        pass

    @_(
        "DECIMAL",
        "FLOAT"
    )
    def Number(self, p):
        pass

    def error(self, p):
        if not p:
            print("End of File!")
        else:
            print("Syntax error at line {0}: LexToken({1}, '{2}')".format(
                p.lineno, p.type, p.value)
            )
