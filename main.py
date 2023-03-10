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


def get_def_use_chains(cursor):
    chains = {}
    for node in cursor.walk_preorder():
        if node.kind == clang.cindex.CursorKind.VAR_DECL:
            var_name = node.displayname
            def_pos = node.extent.start.offset
            if var_name not in chains:
                chains[var_name] = []
            chains[var_name].append((def_pos, "def"))
        elif node.kind == clang.cindex.CursorKind.DECL_REF_EXPR:
            var_name = node.displayname
            use_pos = node.extent.start.offset
            if var_name not in chains:
                chains[var_name] = []
            chains[var_name].append((use_pos, "use"))
    for var_name, chain in chains.items():
        chains[var_name] = sorted(chain)
    du_chains = {}
    for var_name, chain in chains.items():
        du_chain = []
        for i in range(len(chain)):
            if chain[i][1] == "def":
                if len(du_chain) > 0:
                    du_chains[var_name] = du_chain
                du_chain = [(chain[i][0], "def")]
            elif chain[i][1] == "use":
                if len(du_chain) > 0:
                    du_chain.append((chain[i][0], "use"))
        if len(du_chain) > 0:
            du_chains[var_name] = du_chain
    return du_chains
        

clang.cindex.Config.set_library_file('/usr/lib/llvm-8/lib/libclang-8.so.1')
file_path = "benchmark/bzip2-1.0.5/merged/bzip2-1.0.5.c.origin.c"
script_path = "benchmark/bzip2-1.0.5/merged/test.sh"

with open(file_path, 'r') as f:
    source = f.readlines()

ast = get_ast(file_path)
print_ast(ast)
