import sys
import scanner
import parser
from TypeChecker import TypeChecker 
from Interpreter import Interpreter

EXAMPLES_PATH = "examples"


if __name__ == '__main__':
    try:
        filename = sys.argv[1] \
            if len(sys.argv) > 1 \
            else f"{EXAMPLES_PATH}/example14.txt"
        file = open(filename, "r")
        text = file.read()
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    lexer = scanner.MyLexer()
    parser = parser.MyParser()

    ast = parser.parse(lexer.tokenize(text))
    if ast:
        checker = TypeChecker()
        checker.visit(ast)
        for e in checker.errors:
            print('[ERROR]'+e)
        if len(checker.errors) == 0:
            ast.print()

        print('\nInterpreting...\n')
        interpreter = Interpreter()
        interpreter.visit(ast)
