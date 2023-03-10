import clang.cindex


def get_ast(file_path):
    # Initialize the Clang Index
    index = clang.cindex.Index.create()

    # Parse the source file and get the AST
    tu = index.parse(file_path)
    return tu.cursor


def print_ast(cursor, depth=0):
    # Print information about the current node
    if cursor.kind == clang.cindex.CursorKind.BINARY_OPERATOR:
        if '>=' not in source[cursor.location.line - 1] and '<=' not in source[cursor.location.line - 1] and \
                '==' not in source[cursor.location.line - 1] and '-=' not in source[cursor.location.line - 1] and \
                '+=' not in source[cursor.location.line - 1] and '*=' not in source[cursor.location.line - 1] and \
                '/=' not in source[cursor.location.line - 1] and '=' in source[cursor.location.line - 1]:
            print('  ' * depth + str(cursor.kind) + ': =')
    else:
        print('  ' * depth + str(cursor.kind) + ': ' + cursor.spelling)

    # Recursively print the children nodes
    for child in cursor.get_children():
        print_ast(child, depth=depth + 1)


clang.cindex.Config.set_library_file('/usr/lib/llvm-8/lib/libclang-8.so.1')
file_path = "benchmark/bzip2-1.0.5/merged/bzip2-1.0.5.c.origin.c"
script_path = "benchmark/bzip2-1.0.5/merged/test.sh"

with open(file_path, 'r') as f:
    source = f.readlines()

ast = get_ast(file_path)
print_ast(ast)
