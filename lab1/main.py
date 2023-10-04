import sys
import scanner

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    lexer = scanner.Scanner()
    for tok in lexer.tokenize(text):
        print('(%r): %s(%s)' % (tok.lineno, tok.type, tok.value))
