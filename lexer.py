import ply.lex as lex


def lexer(data):
    # List of token names.
    tokens = [
        '_TYPE',
        '_NUMBER',
        '_PLUSEQU',
        '_PLUSPLUS',
        '_PLUS',
        '_MINUSEQU',
        '_MINUSMINUS',
        '_SELECT',
        '_MINUS',
        '_TIMES',
        '_DIVIDE',
        '_DOT',
        '_LPAREN',
        '_RPAREN',
        '_LSQUAREBRA',
        '_RSQUAREBRA',
        '_LBRACE',
        '_RBRACE',
        '_EQUAL',
        '_ASSIGN',
        '_SEMI',
        '_COMMA',
        '_NOTEQU',
        '_NOT',
        '_POUND',
        '_REVERSE',
        '_ANDLOGIC',
        '_AND',
        '_ORLOGIC',
        '_OR',
        '_REMAIN',
        '_LESSEQU',
        '_LESSLESS',
        '_LESS',
        '_GREATEQU',
        '_GREATGREAT',
        '_GREAT',
        '_INCLUDE',
        '_DEFINE',
        '_STRING',
        '_ID'
    ]

    reserved = {
        'if': '_IF',
        'while': '_WHILE',
        'else': '_ELSE',
        'return': '_RETURN',
        'auto':'_AUTO',
        'struct': '_STRUCT',
        'break': '_BREAK',
        'long': '_LONG',
        'switch': '_SWITCH',
        'case': '_CASE',
        'enum': "_ENUM",
        'const': "_CONST",
        'register': '_REGISTER',
        'typedef': '_TYPEDEF',
        'extern': '_EXTERN',
        'union': '_UNION',
        'continue': '_CONTINUE',
        'for': '_FOR',
        'default': '_DEFAULT',
        'goto': '_GOTO',
        'sizeof': '_SIZEOF',
        'volatile': '_VOLATILE',
        'do': '_DO',
        'static': '_STATIC',

    }

    tokens += reserved.values()

    # Regular expression rules
    t__PLUSEQU = r'\+='
    t__PLUSPLUS = r'\+\+'
    t__PLUS = r'\+'
    t__MINUSEQU = r'-='
    t__MINUSMINUS = r'--'
    t__SELECT = r'-\>'
    t__MINUS = r'-'
    t__TIMES = r'\*'
    t__DIVIDE = r'/'
    t__DOT = r'\.'
    t__LPAREN = r'\('
    t__RPAREN = r'\)'
    t__LSQUAREBRA = r'\['
    t__RSQUAREBRA = r'\]'
    t__LBRACE = r'{'
    t__RBRACE = r'}'
    t__EQUAL = r'=='
    t__ASSIGN = r'='
    t__SEMI = r';'
    t__COMMA = r','
    t__NOTEQU = r'!='
    t__NOT = r'!'
    t__REVERSE = r'\~'
    t__ANDLOGIC = r'\&\&'
    t__AND = r'\&'
    t__ORLOGIC = r'\|\|'
    r__OR = r'\|'
    t__REMAIN = r'\%'
    t__LESSEQU = r'<='
    t__LESSLESS = r'<<'
    t__LESS = r'<'
    t__GREATEQU = r'>='
    t__GREATGREAT = r'>>'
    t__GREAT = r'>'
    t__INCLUDE = r'\#include'
    t__DEFINE = r'\#define'

    def t__TYPE(t):
        r'int|float|double|char|short|unsigned|void|signed'
        return t

    def t__NUMBER(t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t__ID(t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        # t.value = (t.value, symbol_lookup(t.value))
        t.type = reserved.get(t.value, '_ID')  # Check for reserved words
        return t

    def t__STRING(t):
        r'"[a-zA-Z_0-9]*"'
        return t

    # track line numbers
    def t_newline(t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # ignored characters (spaces and tabs)
    t_ignore = ' \t'

    # Error handling rule
    def t_error(t):
        #print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Build the lexer
    lexer = lex.lex()
    lexer.input(data)

    # Tokenize
    prev_line = 1
    codelist = [[]]
    while True:
        tok = lexer.token()
        if not tok:
            break      # No more input
        elif prev_line != tok.lineno:
            # print('')
            codelist.append([])
            prev_line = tok.lineno
        #print(tok.type, end=' ')
        codelist[len(codelist)-1].append(tok)
    return codelist
