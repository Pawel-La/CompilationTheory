from sly import Parser
from scanner import MyLexer
import AST


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
        p[1].statements.insert(0, p[0])
        return p[1]

    @_("Statement")
    def StatementList(self, p):
        return AST.StatementList(statements=[p[0]])

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
        return AST.IfStatement(
            expression=p[2],
            statement_if=p[4],
            line_number=p.lineno
        )

    @_('IF "(" Expression ")" Statement ELSE Statement')
    def IfStatement(self, p):
        return AST.IfStatement(
            expression=p[2],
            statement_if=p[4],
            statement_else=p[6],
            line_number=p.lineno
        )

    @_('WHILE "(" Expression ")" Statement')
    def WhileStatement(self, p):
        return AST.WhileStatement(
            expression=p[2],
            statement=p[4],
            line_number=p.lineno
        )

    @_(
        'FOR ID "=" Range Statement',
        'FOR ID "=" List Statement',
    )
    def ForStatement(self, p):
        return AST.ForStatement(
            identifier=p[1],
            range_or_list=p[3],
            statement=p[4],
            line_number=p.lineno
        )

    @_("BREAK", "CONTINUE")
    def JumpStatement(self, p):
        return AST.JumpStatement(
            name=p[0].upper(),
            line_number=p.lineno
        )

    @_("RETURN Expression")
    def JumpStatement(self, p):
        return AST.JumpStatement(
            name=p[0],
            expression=p[1],
            line_number=p.lineno
        )

    @_("PRINT ListContent")
    def PrintStatement(self, p):
        return AST.PrintStatement(
            list_content=p[1],
            line_number=p.lineno
        )

    @_(
        'ID_Content "="         Expression',
        "ID_Content INC_ASSIGN  Expression",
        "ID_Content DEC_ASSIGN  Expression",
        "ID_Content DIV_ASSIGN  Expression",
        "ID_Content MUL_ASSIGN  Expression",
    )
    def AssignmentStatement(self, p):
        return AST.AssignmentStatement(
            id_content=p[0],
            assign_op=p[1],
            expression=p[2],
            line_number=p.lineno
        )

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
        return AST.BinaryOperation(
            left_expression=p[0],
            op=p[1],
            right_expression=p[2],
            line_number=p.lineno
        )

    @_('"(" Expression ")"')
    def Expression(self, p):
        return p[1]

    @_('"-" Expression %prec UMINUS')
    def Expression(self, p):
        return AST.UnaryMinusOperation(
            expression=p[1],
            line_number=p.lineno
        )

    @_('Expression "\'"')
    def Expression(self, p):
        return AST.TransposeOperation(
            expression=p[0],
            line_number=p.lineno
        )

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
        return AST.Range(
            left_range_element=p[0],
            right_range_element=p[2],
            line_number=p.lineno
        )

    @_(
        "Number",
        "ID"
    )
    def RangeElement(self, p):
        return AST.RangeElement(
            value=p[0],
            line_number=p.lineno
        )

    @_('"[" ListContent "]"')
    def List(self, p):
        return AST.List(
            list_content=p[1],
            line_number=p.lineno
        )

    @_('Expression "," ListContent')
    def ListContent(self, p):
        return [p[0]] + p[2]

    @_("Expression")
    def ListContent(self, p):
        return [p[0]]

    @_("ID")
    def ID_Content(self, p):
        return AST.IdContent(
            identifier=p[0],
            line_number=p.lineno
        )

    @_("ID ListAccess")
    def ID_Content(self, p):
        return AST.IdContent(
            identifier=p[0],
            list_access=p[1],
            line_number=p.lineno
        )

    @_('"[" ListAccessElement "]"')
    def ListAccess(self, p):
        return AST.ListAccess(
            list_access_element_left=p[1],
            line_number=p.lineno
        )

    @_('"[" ListAccessElement "," ListAccessElement "]"')
    def ListAccess(self, p):
        return AST.ListAccess(
            list_access_element_left=p[1],
            list_access_element_right=p[3],
            line_number=p.lineno
        )

    @_('DECIMAL', 'ID')
    def ListAccessElement(self, p):
        return AST.ListAccessElement(
            value=p[0],
            line_number=p.lineno
        )

    @_(
        'EYE "(" Expression ")"',
        'ZEROS "(" Expression ")"',
        'ONES "(" Expression ")"',
    )
    def MatrixSpecialFunction(self, p):
        return AST.MatrixSpecialFunction(
            function=p[0],
            expression=p[2],
            line_number=p.lineno
        )

    @_(
        "DECIMAL",
        "FLOAT"
    )
    def Number(self, p):
        return AST.Number(
            value=p[0],
            line_number=p.lineno
        )

    def error(self, p):
        if p:
            print("Syntax error at line {0}: LexToken({1}, '{2}')".format(
                p.lineno, p.type, p.value)
            )
        else:
            print("End of File!")
