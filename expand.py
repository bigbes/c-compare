from pycparser.c_ast import *

def expand_decl(decl, type_arr):
    typ = type(decl)

    if typ == TypeDecl:
        return expand_decl(decl.type, type_arr)
    elif typ == IdentifierType:
        if decl.names[0] in type_arr:        
            return type_arr[decl.names[0]][1]
        else:
            return decl.names
    elif typ == ID:
        return decl.name
    elif typ in [Struct, Union]:
        decls = [expand_decl(d, type_arr) for d in decl.decls or []]
        return [typ.__name__, decl.name, decls]
    elif typ == Enum:
        if decl.values != None:
            return ['Enum', len(decl.values.enumerators)]
    else:
        nested = expand_decl(decl.type, type_arr)

        if typ == Decl:
            if decl.quals:
                return [decl.quals, nested]
            else:
                return nested
        elif typ == Typename:
            if decl.quals:
                return [decl.quals, nested]
            else:
                return nested
        elif typ == ArrayDecl:
            dimval = decl.dim.value if decl.dim else ''
            return [dimval, nested]
        elif typ == PtrDecl:
            return ['*', nested]
        elif typ == Typedef:
            return [decl.name, nested]
        elif typ == FuncDecl:
            if decl.args:
                params = [expand_decl(param, type_arr) for param in\
				decl.args.params]
            else:
                params = []
            return [params, nested]

def expand_init(init):
    if not init is None:
        typ = type(init)
        if typ == NamedInitializer:
            des = [expand_init(dp) for dp in init.name]
            return (des, expand_init(init.expr))
        elif typ == ExprList:
            return [expand_init(expr) for expr in init.exprs]
        elif typ == Constant:
            return ['Constant', init.type, init.value]

        elif typ == ID:
            return ['ID', init.name]
    else:
        return

#------------------------------------------------------------------------------

if __name__ == "__main__":
    pass
