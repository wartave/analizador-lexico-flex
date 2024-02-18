import ply.yacc as yacc
from lexer import tokens

# Regla de precedencia
precedence = (
    ('left', 'SUMA', 'RESTA'),
    ('left', 'MULTIPLICACION', 'DIVISION'),
    ('nonassoc', 'MENOR_QUE', 'MAYOR_QUE', 'MENOR_IGUAL_QUE', 'MAYOR_IGUAL_QUE', 'DISTINTO_QUE', 'IGUAL_QUE')
)
variables_declaradas = set()  # Conjunto para mantener un registro de variables declaradas

# Definición de la gramática
def p_programa(p):
    '''
    programa : sentencias
    '''
    p[0] = p[1]

def p_sentencias(p):
    '''
    sentencias : sentencias sentencia
               | sentencia
    '''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_sentencia(p):
    '''
    sentencia : expresion PUNTO_Y_COMA
              | asignacion PUNTO_Y_COMA
              | declaracion PUNTO_Y_COMA
              | estructura_control
              | funcion_definicion
              | retorno PUNTO_Y_COMA
              | BREAK PUNTO_Y_COMA
              | imprimir_expresion PUNTO_Y_COMA
              | VERSA expresion PUNTO_Y_COMA
              | NUEVA_LINEA
    '''
    p[0] = p[1]

def p_declaracion(p):
    '''
    declaracion : VERSA IDENTIFICADOR ASIGNACION expresion
    '''
    variable = p[2]
    if variable in variables_declaradas:
        print(f"Error: La variable '{variable}' ya ha sido declarada.")
    else:
        variables_declaradas.add(variable)
        p[0] = ('declaracion', p[2], p[4])
    
def p_expresion(p):
    '''
    expresion : expresion SUMA expresion
              | expresion RESTA expresion
              | expresion MULTIPLICACION expresion
              | expresion DIVISION expresion
              | expresion MENOR_QUE expresion
              | expresion MAYOR_QUE expresion
              | expresion MENOR_IGUAL_QUE expresion
              | expresion MAYOR_IGUAL_QUE expresion
              | expresion DISTINTO_QUE expresion
              | expresion IGUAL_QUE expresion
              | PARENTESIS_IZQUIERDO expresion PARENTESIS_DERECHO
              | NUMERO
              | IDENTIFICADOR
              | CADENA
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        if p[1] == '(':
            p[0] = p[2]
        else:
            p[0] = (p[1], p[2], p[3])

def p_asignacion(p):
    '''
    asignacion : IDENTIFICADOR ASIGNACION expresion
    '''
    p[0] = ('=', p[1], p[3])

def p_estructura_control(p):
    '''
    estructura_control : SI PARENTESIS_IZQUIERDO expresion PARENTESIS_DERECHO LLAVE_IZQUIERDA sentencias LLAVE_DERECHA
                       | SI PARENTESIS_IZQUIERDO expresion PARENTESIS_DERECHO LLAVE_IZQUIERDA sentencias LLAVE_DERECHA SINO LLAVE_IZQUIERDA sentencias LLAVE_DERECHA
                       | MIENTRAS PARENTESIS_IZQUIERDO expresion PARENTESIS_DERECHO LLAVE_IZQUIERDA sentencias LLAVE_DERECHA
                       | PARA PARENTESIS_IZQUIERDO asignacion PUNTO_Y_COMA expresion PUNTO_Y_COMA asignacion PARENTESIS_DERECHO LLAVE_IZQUIERDA sentencias LLAVE_DERECHA
    '''
    if p[1] == 'si':
        if len(p) == 8:
            p[0] = ('if', p[3], p[6], [])
        else:
            p[0] = ('if-else', p[3], p[6], p[10])
    elif p[1] == 'mientras':
        p[0] = ('while', p[3], p[6])
    elif p[1] == 'para':
        p[0] = ('for', p[3], p[5], p[7], p[10])

def p_funcion_definicion(p):
    '''
    funcion_definicion : FUNCION IDENTIFICADOR PARENTESIS_IZQUIERDO parametros PARENTESIS_DERECHO LLAVE_IZQUIERDA sentencias LLAVE_DERECHA
    '''
    p[0] = ('func_def', p[2], p[4], p[7])

def p_parametros(p):
    '''
    parametros : parametros COMA IDENTIFICADOR
               | IDENTIFICADOR
               | empty
    '''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    elif len(p) == 2:
        if p[1] is None:
            p[0] = []
        else:
            p[0] = [p[1]]

def p_retorno(p):
    '''
    retorno : RETORNO expresion
    '''
    p[0] = ('return', p[2])

def p_empty(p):
    '''
    empty :
    '''
    pass

def p_imprimir_expresion(p):
    '''
    imprimir_expresion : IMPRIMIR PARENTESIS_IZQUIERDO expresion PARENTESIS_DERECHO
                       | IMPRIMIR PARENTESIS_IZQUIERDO CADENA PARENTESIS_DERECHO
    '''
    p[0] = ('imprimir', p[3])

def p_error(p):
    if p:
        print("Error de sintaxis en '%s'" % p.value)
    else:
        print("Error de sintaxis en EOF")

parser = yacc.yacc()