import sys

filename = sys.argv[1]
reserved = { 'print' : 'PRINT' }
tokens = [
    'NAME','NUMBER',
    ] + list(reserved.values())
 
# Each literal must be a single character
literals = ['=','+','-','*','/', '(',')']
 
# Tokens definitions
def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'NAME')    # Check for reserved words 
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t
 
t_ignore = " \t"
 
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
 
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
 
# Build the lexer, and enable debugging
import ply.lex as lex
lex.lex(debug=1) 
 
# Parsing rules
precedence = (
    ('left','+','-'),
    ('left','*','/')
    )
 
# dictionary of names
names = { }
 
def p_statement_assign(p):
    'statement : NAME "=" expression'
    names[p[1]] = p[3]
 
#def p_statement_expr(p):
#    'statement : expression'
#    print(p[1])

def p_statement_print(p):
    'statement : PRINT expression'
    print p[2]

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_expression_exp_plsterm(p):
    'expression : expression "+" term'
    p[0] = p[1] + p[3]

def p_expression_exp_minterm(p):
    'expression : expression "-" term'
    p[0] = p[1] - p[3]

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_term_mulfactor(p):
    'term : term "*" factor'
    p[0] = p[1] * p[3]

def p_term_divfactor(p):
    'term : term "/" factor'
    p[0] = p[1] / p[3]

def p_expression_group(p):
    "expression : '(' expression ')'"
    p[0] = p[2]
 
def p_factor_number(p):
    "factor : NUMBER"
    p[0] = p[1]
 
def p_factor_name(p):
    "factor : NAME"
    try:
        p[0] = names[p[1]]
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0
 
def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")
 
import ply.yacc as yacc
yacc.yacc()

code_file = open(filename,"r")
stream = code_file.readlines() 
for line in stream:
    yacc.parse(line)
