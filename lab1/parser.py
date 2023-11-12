from sly import Parser
from scanner import MyLexer


class MyParser(Parser):
    debugfile = 'parser.out'
    tokens = MyLexer.tokens

    precedence = (
        ("nonassoc", IF_PREC),
        ("nonassoc", ELSE),
        # ('nonassoc', "=", INC_ASSIGN, DEC_ASSIGN, MUL_ASSIGN, DIV_ASSIGN)
        ('nonassoc', EQ, NOT_EQ),
        ('nonassoc', "<", ">", GREATER_EQ, LESS_EQ),
        ('left', "+", "-", DOT_PLUS, DOT_MINUS),
        ('left', "*", "/", DOT_MUL, DOT_DIV),
        ('right', UMINUS),
        ('left', "\'")
    )

    @_("Statement StatementList")
    def StatementList(self, p):
        return [p[0]] + p[1]

    @_("Statement")
    def StatementList(self, p):
        return [p[0]]

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
        return p[0]

    @_('"{" StatementList "}"')
    def CompoundStatement(self, p):
        return p[1]

    @_('IF "(" Expression ")" Statement %prec IF_PREC')
    def IfStatement(self, p):
        return "IF_TAG", (("IF", p[2]), ("THEN", p[4]))

    @_('IF "(" Expression ")" Statement ELSE Statement')
    def IfStatement(self, p):
        return "IF_ELSE_TAG", (("IF", p[2]), ("THEN", p[4]), ("ELSE", p[6]))

    @_('WHILE "(" Expression ")" Statement')
    def WhileStatement(self, p):
        return 'WHILE', p[2], p[4]

    @_(
        'FOR ID "=" Range Statement',
        'FOR ID "=" List Statement',
    )
    def ForStatement(self, p):
        return 'FOR', p[1], p[3], p[4]

    @_("BREAK", "CONTINUE")
    def JumpStatement(self, p):
        return p[0].upper()

    @_("RETURN Expression")
    def JumpStatement(self, p):
        return p[0], p[1]

    @_("PRINT ListContent")
    def PrintStatement(self, p):
        return 'PRINT', p[1]

    @_(
        'ID_Content "="         Expression',
        "ID_Content INC_ASSIGN  Expression",
        "ID_Content DEC_ASSIGN  Expression",
        "ID_Content DIV_ASSIGN  Expression",
        "ID_Content MUL_ASSIGN  Expression",
    )
    def AssignmentStatement(self, p):
        return (p[1], p[0], p[2])

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
    )
    def Expression(self, p):
        return (p[1], p[0], p[2])

    @_('"(" Expression ")"')
    def Expression(self, p):
        return p[1]

    @_('"-" Expression %prec UMINUS')
    def Expression(self, p):
        return ('-', p[1])

    @_('Expression "\'"')
    def Expression(self, p):
        return ('TRANSPOSE', p[0])

    @_(
        "List",
        "Number",
        "STRING",
        "ID_Content",
        "MatrixSpecialFunction",
    )
    def Expression(self, p):
        return p[0]

    @_('RangeElement ":" RangeElement')
    def Range(self, p):
        return ("RANGE", p[0], p[2])

    @_(
        "Number",
        "ID"
    )
    def RangeElement(self, p):
        return p[0]

    @_('"[" ListContent "]"')
    def List(self, p):
        return 'LIST', p[1]

    @_('Expression "," ListContent')
    def ListContent(self, p):
        return [p[0]] + p[2]

    @_("Expression")
    def ListContent(self, p):
        return [p[0]]

    @_("ID")
    def ID_Content(self, p):
        return p[0]

    @_("ID ListAccess")
    def ID_Content(self, p):
        return 'ACCESS', p[0], p[1]

    @_('"[" ListAccessElement "]"')
    def ListAccess(self, p):
        return ([p[1]])

    @_('"[" ListAccessElement "," ListAccessElement "]"')
    def ListAccess(self, p):
        return ([p[1]] + [p[3]])

    @_('DECIMAL', 'ID')
    def ListAccessElement(self, p):
        return p[0]

    @_(
        'EYE "(" Expression ")"',
        'ZEROS "(" Expression ")"',
        'ONES "(" Expression ")"',
    )
    def MatrixSpecialFunction(self, p):
        return (p[0].upper(), p[2])

    @_(
        "DECIMAL",
        "FLOAT"
    )
    def Number(self, p):
        return p[0]

    def error(self, p):
        if p:
            print("Syntax error at line {0}: LexToken({1}, '{2}')".format(
                p.lineno, p.type, p.value)
            )
        else:
            print("End of File!")
