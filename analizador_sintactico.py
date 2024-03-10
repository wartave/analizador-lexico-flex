#analizador_sintactico.py
import ply.yacc as yacc
import tkinter as tk
from lexer import tokens

global errors_text_area
# Regla de precedencia
precedence = (
    ('left', 'SUMA', 'RESTA'),
    ('left', 'MULTIPLICACION', 'DIVISION'),
    ('nonassoc', 'MENOR_QUE', 'MAYOR_QUE', 'MENOR_IGUAL_QUE', 'MAYOR_IGUAL_QUE', 'DISTINTO_QUE', 'IGUAL_QUE')
)
variables = {}  # Diccionario para mantener un registro de variables declaradas

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
              | llamada_funcion PUNTO_Y_COMA
              | NUEVA_LINEA
    '''
    p[0] = p[1]

def p_declaracion(p):
    '''
    declaracion : VERSA IDENTIFICADOR ASIGNACION expresion
    '''
    variable = p[2]
    expresion = p[4]

    # Verificar si la variable utilizada en la expresión ha sido declarada previamente
    variables_expresion = set()
    recopilar_variables(expresion, variables_expresion)

    variables_sin_declarar = variables_expresion - set(variables.keys())
    if variables_sin_declarar:
        error_message = f"Error: Las siguientes variables no han sido declaradas: {', '.join(variables_sin_declarar)}."
        errors_text_area.insert(tk.END, error_message + '\n')
        return

    if variable in variables:
        error_message = f"Error: La variable '{variable}' ya ha sido declarada."
        errors_text_area.insert(tk.END, error_message + '\n')
    else:
        variables[variable] = True
        p[0] = ('declaracion', p[2], p[4])

def recopilar_variables(expresion, variables):
    if isinstance(expresion, tuple):
        for elemento in expresion[1:]:
            recopilar_variables(elemento, variables)
    elif isinstance(expresion, str):
        variables.add(expresion)

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
              | expresion AND expresion
              | expresion OR expresion
              | TRUE
              | FALSE
              | PARENTESIS_IZQUIERDO expresion PARENTESIS_DERECHO
              | NUMERO
              | IDENTIFICADOR
              | CADENA
              | llamada_funcion
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        if p[1] == '(':
            p[0] = p[2]
        else:
            p[0] = (p[1], p[2], p[3])

def p_llamada_funcion(p):
    '''
    llamada_funcion : IDENTIFICADOR PARENTESIS_IZQUIERDO argumentos_opt PARENTESIS_DERECHO
    '''
    p[0] = ('llamada_funcion', p[1], p[3])

def p_argumentos_opt(p):
    '''
    argumentos_opt : argumentos
                   | empty
    '''
    p[0] = p[1]

def p_argumentos(p):
    '''
    argumentos : argumentos COMA expresion
               | expresion
    '''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_asignacion(p):
    '''
    asignacion : IDENTIFICADOR ASIGNACION expresion
    '''
    p[0] = ('=', p[1], p[3])

def p_estructura_control(p):
    '''
    estructura_control : SI PARENTESIS_IZQUIERDO expresion PARENTESIS_DERECHO LLAVE_IZQUIERDA sentencias LLAVE_DERECHA
                       | SI PARENTESIS_IZQUIERDO expresion PARENTESIS_DERECHO LLAVE_IZQUIERDA sentencias LLAVE_DERECHA SINO LLAVE_IZQUIERDA sentencias LLAVE_DERECHA
                       | MIENTRAS PARENTESIS_IZQUIERDO expresion_booleana PARENTESIS_DERECHO LLAVE_IZQUIERDA sentencias LLAVE_DERECHA
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

def p_expresion_booleana(p):
    '''
    expresion_booleana : TRUE
                       | FALSE
                       | expresion
    '''
    p[0] = p[1]

def p_funcion_definicion(p):
    '''
    funcion_definicion : FUNCION IDENTIFICADOR PARENTESIS_IZQUIERDO parametros_opt  PARENTESIS_DERECHO LLAVE_IZQUIERDA sentencias_opt LLAVE_DERECHA
    '''
    p[0] = ('func_def', p[2], p[4], p[7])

def p_parametros_opt(p):
    '''
    parametros_opt : parametros
                   | empty
    '''
    p[0] = p[1]

def p_sentencias_opt(p):
    '''
    sentencias_opt : sentencias
                   | empty
    '''
    p[0] = p[1]

def p_parametros(p):
    '''
    parametros : parametros COMA IDENTIFICADOR
               | IDENTIFICADOR
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
    global errors_text_area  # Declarar errors_text_area como global
    if p:
        error_message = f"Error de sintaxis en '{p.value}'"
        errors_text_area.insert(tk.END, error_message + '\n')
    else:
        errors_text_area.insert(tk.END, "Error de sintaxis en EOF\n")
    

parser = yacc.yacc()
