
import AST
from SymbolTable import *
from SymbolTable import Types as T




binary_correlations = {
    "+": {T.INT: 
                {T.INT: T.INT, 
                 T.FLOAT: T.FLOAT},
          T.FLOAT: 
                {T.INT: T.FLOAT, 
                 T.FLOAT: T.FLOAT},
          T.STRING: 
                {T.STRING: T.STRING}},
    
    "-": {T.INT: 
                {T.INT: T.INT, 
                 T.FLOAT: T.FLOAT},
          T.FLOAT: 
                {T.INT: T.FLOAT, 
                 T.FLOAT: T.FLOAT}},
    
    "*": {T.INT: 
                {T.INT: T.INT, 
                 T.FLOAT: T.FLOAT},
          T.FLOAT: 
                {T.INT: T.FLOAT, 
                 T.FLOAT: T.FLOAT}},
    
    "/": {T.INT: 
                {T.INT: T.INT,
                 T.FLOAT: T.FLOAT},
          T.FLOAT: 
                {T.INT: T.FLOAT, 
                 T.FLOAT: T.FLOAT}},
    
    "<": {T.INT: 
                {T.INT: T.BOOL, 
                 T.FLOAT: T.BOOL},
          T.FLOAT: 
                {T.INT: T.BOOL, 
                 T.FLOAT: T.BOOL}},
    
    ">": {T.INT: 
                {T.INT: T.BOOL, 
                 T.FLOAT: T.BOOL},
          T.FLOAT: 
                {T.INT: T.BOOL, 
                 T.FLOAT: T.BOOL}},
    
    "<=": {T.INT: 
                {T.INT: T.BOOL, 
                 T.FLOAT: T.BOOL},
           T.FLOAT: 
                {T.INT: T.BOOL, 
                 T.FLOAT: T.BOOL}},
    
    ">=": {T.INT: 
                {T.INT: T.BOOL, 
                 T.FLOAT: T.BOOL},
           T.FLOAT: 
                {T.INT: T.BOOL, 
                 T.FLOAT: T.BOOL}},
    
    "==": {T.INT: 
                {T.INT: T.BOOL, 
                 T.FLOAT: T.BOOL},
           T.FLOAT: 
                {T.INT: T.BOOL, 
                 T.FLOAT: T.BOOL},
           T.BOOL: 
                {T.BOOL: T.BOOL},
           T.STRING: 
                {T.STRING: T.BOOL}},
    
    "!=": {T.INT:  
                {T.INT: T.BOOL, 
                 T.FLOAT: T.BOOL},
           T.FLOAT: 
                {T.INT: T.BOOL,
                  T.FLOAT: T.BOOL},
           T.BOOL: 
                {T.BOOL: T.BOOL},
           T.STRING: 
                {T.STRING: T.BOOL}},
    
    ".+": {T.VECTOR: 
                {T.VECTOR: T.VECTOR}},
    
    ".-": {T.VECTOR: 
                {T.VECTOR: T.VECTOR}},
    
    ".*": {T.VECTOR: 
                {T.VECTOR: T.VECTOR, 
                 T.INT: T.VECTOR, 
                 T.FLOAT: T.VECTOR},
           T.INT: 
                {T.VECTOR: T.VECTOR},
           T.FLOAT: 
                {T.VECTOR: T.VECTOR}},
    
    "./": {T.VECTOR: 
                {T.VECTOR: T.VECTOR, 
                 T.INT: T.VECTOR, 
                 T.FLOAT: T.VECTOR}}
}











class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)


    def generic_visit(self, node):        # Called if no explicit visitor function exists for a node.
        print(node)
        print( "generic_visit", node.__class__.__name__)



class TypeChecker(NodeVisitor):
    def __init__(self):
        super().__init__()
        self.symbol_table = SymbolTable(None, "main")
        self.loopcount = 0
        self.errors = []

    def visit_BinaryOperation(self, node : AST.BinaryOperation):

        sym1 = self.visit(node.left_expression)     
        sym2 = self.visit(node.right_expression)

        if sym1 is None or sym2 is None:
            return 

        try:
            new_type = binary_correlations[node.op][sym1.type][sym2.type]
        except KeyError:
            self.errors.append(f"Operation {node.op} not supported between types {sym1.type} and {sym2.type} in line {node.line_number}")
            return

        if sym1.type == sym2.type == T.VECTOR:
            if sym1.shape == sym2.shape:
                return VariableSymbol(None, T.VECTOR, sym1)
            else:
                self.errors.append(f"Vectors different shape on line {node.line_number}")
        return VariableSymbol(None, new_type)

    def visit_StatementList(self, node :AST.StatementList):
        for statement in node.statements:
            self.visit(statement)

    def visit_IfStatement(self, node : AST.IfStatement):
        self.visit(node.expression)
        self.visit(node.statement_if)

        if node.statement_else is not None:
            self.visit(node.statement_else)
    
    def visit_WhileStatement(self, node : AST.WhileStatement):
        self.loopcount += 1

        self.symbol_table = self.symbol_table.pushScope("While")
        self.visit(node.expression)
        self.visit(node.statement)

        self.loopcount -= 1
        self.symbol_table = self.symbol_table.popScope()

    def visit_ForStatement(self, node : AST.ForStatement):
        self.loopcount += 1

        self.symbol_table = self.symbol_table.pushScope("For")
        self.visit(node.range_or_list)

        if isinstance(node.range_or_list, AST.Range):
            symbol = self.visit(node.range_or_list)
        elif isinstance(node.range_or_list, AST.List):
            symbol = self.visit(node.range_or_list.content[0])

        self.symbol_table.symbols[node.identifier] = symbol
        self.visit(node.statement)

        self.loopcount -= 1
        self.symbol_table = self.symbol_table.popScope()

    def visit_TransposeOperation(self, node : AST.TransposeOperation):
        if not (isinstance(node.expression, AST.IdContent) or isinstance(node.expression, AST.List)):
            self.errors.append(f"Only Vectors can be transposed [{node.line_number}]")
            return
        symbol : VariableSymbol = self.visit(node.expression)
        return VariableSymbol(None, symbol.type, symbol.shape[::-1])

    def visit_UnaryMinusOperation(self, node : AST.UnaryMinusOperation):
        if node in [AST.List, AST.IdContent, AST.Number]:
            return self.visit(node.expression)
        self.errors.append(f"Wrong type after minus in line {node.line_number}")
        return

    def visit_Range(self, node: AST.Range):
        from_exp = self.visit(node.left_range_element)
        to_exp = self.visit(node.right_range_element)

        if from_exp.type == T.FLOAT or to_exp.type == T.FLOAT:
            return VariableSymbol(None,T.FLOAT)
        return VariableSymbol(None,T.INT)

    def visit_JumpStatement(self, node: AST.JumpStatement):
        if node.name == "BREAK" or node.name == "CONTINUE":
            if self.loopcount == 0:
                self.errors.append(
                    f"Break/Continue outside of loop in line {node.line_number}"
                )

    def visit_RangeElement(self, node: AST.RangeElement):
        if isinstance(node.value, str):
            symbol = self.symbol_table.get(node.value)
            if symbol is None:
                self.errors.append(
                    f"Variable {node.value} not declared in line {node.line_number}"
                )
            return symbol
            
        return self.visit(node.value)

    def visit_PrintStatement(self, node : AST.PrintStatement):
        for elem in node.list_content:
            self.visit(elem)

    def visit_AssignmentStatement(self, node: AST.AssignmentStatement):
        symbol = self.visit(node.expression)
        if symbol == None:
            return None
        self.symbol_table.put(node.id_content.identifier, symbol)

    def visit_List(self, node : AST.List):
        elements = node.list_content
        types = []
        for element in elements:
            if isinstance(element, AST.List):
                element_type = self.visit(element)
            else:
                element_type = VariableSymbol(None, type_covertion(element))
            types += [element_type]
    

        if all(x == types[0] for x in types):
            if types[0].type == T.VECTOR:
                return VariableSymbol(None, T.VECTOR, (len(elements),types[0].shape[0]))
            else:
                return VariableSymbol(None, T.VECTOR, (len(elements),))
        else:
            self.errors.append(
                f"Vector elements have different types in line {node.line_number}"
            )
            return None
  
    def visit_IdContent(self, node : AST.IdContent):
        symbol = self.symbol_table.get(node.identifier)
        if symbol is None:
            self.errors.append(
                f"Variable {node.identifier} not declared in line {node.line_number}"
            )
            return None
        else:
            return symbol



    def visit_MatrixSpecialFunction(self, node : AST.MatrixSpecialFunction):
        symbol = self.visit(node.expression)
        return VariableSymbol(None, T.VECTOR, "Unknown")

    def visit_Number(self, node : AST.Number):
        return VariableSymbol(None,type_covertion(node.value))
    

if __name__ == "__main__":
    print(binary_correlations["./"][Types.VECTOR][Types.VECTOR])