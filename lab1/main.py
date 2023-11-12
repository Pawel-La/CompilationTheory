import sys
import scanner
import parser
from ast_draw import draw_ast

EXAMPLES_PATH = "examples"


if __name__ == '__main__':

    try:
        filename = sys.argv[1] \
            if len(sys.argv) > 1 \
            else f"{EXAMPLES_PATH}//example4.txt"
        file = open(filename, "r")
        text = file.read()
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    lexer = scanner.MyLexer()
    parser = parser.MyParser()

    result = parser.parse(lexer.tokenize(text))
    if result:
        draw_ast(result)

