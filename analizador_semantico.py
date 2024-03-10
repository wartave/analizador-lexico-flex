#analizador_semantico.py
from collections import defaultdict

variables_declaradas = {}
funciones_definidas = set()

def analizar_semanticamente(arbol):
    global variables_declaradas, funciones_definidas
    variables_declaradas = {}
    funciones_definidas = set()
    errores_semanticos = []
    recorrer_arbol(arbol, errores_semanticos, None)
    if errores_semanticos is None:
        errores_semanticos = []
    return errores_semanticos

def recorrer_arbol(nodo, errores_semanticos, funcion_actual):
    if isinstance(nodo, tuple):
        if nodo[0] == 'llamada_funcion':
            nombre_funcion = nodo[1]
            if nombre_funcion not in funciones_definidas:
                errores_semanticos.append(f"Error: La función '{nombre_funcion}' no ha sido definida.")
        elif nodo[0] == 'declaracion':
            variable = nodo[1]
            if variable in variables_declaradas and variables_declaradas[variable]:
                errores_semanticos.append(f"Error: La variable '{variable}' ya ha sido declarada.")
            else:
                variables_declaradas[variable] = 0  # Inicializar la variable con 0
        elif nodo[0] == '=':
            variable = nodo[1]
            if variable not in variables_declaradas:
                errores_semanticos.append(f"Error: La variable '{variable}' no ha sido declarada.")
            else:
                variables_declaradas[variable] = evaluar_expresion(nodo[2], variables_declaradas)
        elif nodo[0] == 'if' or nodo[0] == 'if-else':
            if isinstance(nodo[1], tuple) and isinstance(nodo[1][0], str):
                variable_condicion = nodo[1][0]
                if variable_condicion not in variables_declaradas:
                    errores_semanticos.append(f"Error: La variable '{variable_condicion}' en la condición del if no ha sido declarada.")
            recorrer_arbol(nodo[2], errores_semanticos, funcion_actual)
            recorrer_arbol(nodo[3], errores_semanticos, funcion_actual)
            if len(nodo) == 5:
                recorrer_arbol(nodo[4], errores_semanticos, funcion_actual)
        elif nodo[0] == 'while':
            resultado_condicion = evaluar_expresion(nodo[1], variables_declaradas)
            if resultado_condicion is None:
                errores_semanticos.append("Error: La expresión en la condición del bucle 'mientras' no es válida.")
            elif not isinstance(resultado_condicion, bool):
                errores_semanticos.append("Error: La expresión en la condición del bucle 'mientras' debe ser de tipo booleano.")
            recorrer_arbol(nodo[2], errores_semanticos, funcion_actual)
        elif nodo[0] == 'for':
            recorrer_arbol(nodo[2], errores_semanticos, funcion_actual)
            recorrer_arbol(nodo[4], errores_semanticos, funcion_actual)
        elif nodo[0] == 'func_def':
            nombre_funcion = nodo[1]
            if nombre_funcion in funciones_definidas:
                errores_semanticos.append(f"Error: La función '{nombre_funcion}' ya ha sido definida.")
            else:
                funciones_definidas.add(nombre_funcion)
                if nodo[2] is not None:
                    for parametro in nodo[2]:
                        variables_declaradas[parametro] = 0
                if not nodo[3]:
                    errores_semanticos.append(f"Error: La función '{nombre_funcion}' no tiene sentencias.")
                recorrer_arbol(nodo[3], errores_semanticos, nombre_funcion)
                if nodo[2] is not None:
                    for parametro in nodo[2]:
                        del variables_declaradas[parametro]
        elif nodo[0] == 'return':
            if funcion_actual is None:
                errores_semanticos.append("Error: La sentencia 'retorno' no está dentro de una función.")
            else:
                recorrer_arbol(nodo[1], errores_semanticos, funcion_actual)
        else:
            for hijo in nodo[1:]:
                recorrer_arbol(hijo, errores_semanticos, funcion_actual)
    elif isinstance(nodo, list):
        for elemento in nodo:
            recorrer_arbol(elemento, errores_semanticos, funcion_actual)

def evaluar_expresion(expresion, variables_declaradas):
    if isinstance(expresion, tuple):
        operador = expresion[0]
        if operador in ['+', '-', '*', '/']:
            izquierda = evaluar_expresion(expresion[1], variables_declaradas)
            derecha = evaluar_expresion(expresion[2], variables_declaradas)
            if izquierda is None or derecha is None:
                return None
            if operador == '+':
                return izquierda + derecha
            elif operador == '-':
                return izquierda - derecha
            elif operador == '*':
                return izquierda * derecha
            elif operador == '/':
                return izquierda / derecha
        elif operador in ['<', '>', '<=', '>=', '==', '!=']:
            izquierda = evaluar_expresion(expresion[1], variables_declaradas)
            derecha = evaluar_expresion(expresion[2], variables_declaradas)
            if izquierda is None or derecha is None:
                return None
            if operador == '<':
                return izquierda < derecha
            elif operador == '>':
                return izquierda > derecha
            elif operador == '<=':
                return izquierda <= derecha
            elif operador == '>=':
                return izquierda >= derecha
            elif operador == '==':
                return izquierda == derecha
            elif operador == '!=':
                return izquierda != derecha
        elif operador in ['and', 'or']:
            izquierda = evaluar_expresion(expresion[1], variables_declaradas)
            derecha = evaluar_expresion(expresion[2], variables_declaradas)
            if izquierda is None or derecha is None:
                return None
            if operador == 'and':
                return izquierda and derecha
            elif operador == 'or':
                return izquierda or derecha
        else:
            return None  # Expresión no válida
    elif isinstance(expresion, str):
        if expresion in variables_declaradas:
            return variables_declaradas[expresion]
        elif expresion.lower() == 'true':
            return True
        elif expresion.lower() == 'false':
            return False
        else:
            return None  # Expresión no válida
    elif isinstance(expresion, int):
        return expresion
    elif isinstance(expresion, bool):
        return expresion
    return None
