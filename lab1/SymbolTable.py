from enum import Enum

class Types(Enum):
    INT = 'int'
    FLOAT = 'float'
    BOOL = 'bool'
    STRING = 'string'
    VECTOR = 'vector'

def type_covertion(elem):
    if isinstance(elem, str):
        return Types.STRING
    if isinstance(elem, int):
        return Types.INT
    if isinstance(elem, float):
        return Types.FLOAT
    if isinstance(elem, VariableSymbol):
        return elem.type


class VariableSymbol:

    def __init__(self, name, type, shape = None):
        if not type in [Types.INT, Types.FLOAT, Types.BOOL, Types.STRING, Types.VECTOR]:
            raise ValueError(f"Invalid type: {type}")
        self.name = name
        self.type = type
        self.shape = None

    # to use hashmaps
    def __hash__(self) -> int:
        return (self.type.__hash__() + self.shape.__hash__() )

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, VariableSymbol):
            return False
        return self.__hash__() == value.__hash__()

class SymbolTable(object):

    def __init__(self, parent, name): # parent scope and symbol table name
        self.parent = parent
        self.name = name
        self.symbols = dict()
    #

    def put(self, name, symbol): # put variable symbol or fundef under <name> entry
        self.symbols[name] = symbol
    #

    def get(self, name): # get variable symbol or fundef from <name> entry
        if self.symbols.get(name, None) != None:
            return self.symbols.get(name)
        elif self.parent != None:
            return self.parent.get(name)
        return None
    #

    def pushScope(self, name):
        return SymbolTable(self, name)
    #

    def popScope(self):
        return self.parent
    #
