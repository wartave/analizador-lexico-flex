import ply.lex as lex

# Definiciones de tokens para el analizador léxico
tokens = (
    'NUMERO',
    'SUMA',
    'RESTA',
    'MULTIPLICACION',
    'DIVISION',
    'PARENTESIS_IZQUIERDO',
    'PARENTESIS_DERECHO',
    'LLAVE_IZQUIERDA',
    'LLAVE_DERECHA',
    'IDENTIFICADOR',
    'CADENA',
    'COMENTARIO',
    'COMENTARIO_MULTILINEA',
    'NUEVA_LINEA',
    'SI',
    'SINO',
    'MIENTRAS',
    'PARA',
    'IMPRIMIR',
    'BREAK',
    'RETORNO',
    'ASIGNACION',
    'COMA',
    'MENOR_QUE',
    'MAYOR_QUE',
    'MENOR_IGUAL_QUE',
    'MAYOR_IGUAL_QUE',
    'DISTINTO_QUE',
    'IGUAL_QUE',
    'PUNTO_Y_COMA',
    'VERSA',
    'FUNCION'
)

# Reglas para tokens
t_SUMA               = r'\+'
t_RESTA              = r'-'
t_MULTIPLICACION     = r'\*'
t_DIVISION           = r'/'
t_PARENTESIS_IZQUIERDO  = r'\('
t_PARENTESIS_DERECHO    = r'\)'
t_LLAVE_IZQUIERDA       = r'\{'
t_LLAVE_DERECHA         = r'\}'
t_ASIGNACION         = r'='
t_COMA               = r','
t_MENOR_QUE          = r'<'
t_MAYOR_QUE          = r'>'
t_MENOR_IGUAL_QUE    = r'<='
t_MAYOR_IGUAL_QUE    = r'>='
t_DISTINTO_QUE       = r'!='
t_IGUAL_QUE          = r'=='
t_PUNTO_Y_COMA       = r';'

# Regla para números
def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t
# Palabras clave
palabras_reservadas = {
    'si': 'SI',
    'sino': 'SINO',
    'mientras': 'MIENTRAS',
    'para': 'PARA',
    'imprimir': 'IMPRIMIR',
    'romper': 'BREAK',
    'retorno': 'RETORNO',
    'funcion': 'FUNCION',
    'versa': 'VERSA'  
}
# Convertir lexemas a minúsculas antes de clasificar
def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = palabras_reservadas.get(t.value.lower(), 'IDENTIFICADOR')
    return t



# Regla para cadenas
def t_CADENA(t):
    r'\"([^\\\n]|(\\.))*?\"'
    return t

# Regla para comentarios multilinea
def t_COMENTARIO_MULTILINEA(t):
    r'\-@(.*?)-'
    pass

# Regla para comentarios (ignorados)
def t_COMENTARIO(t):
    r'\#.*'
    pass

# Regla para nueva línea
def t_NUEVA_LINEA(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    pass

# Ignorar los espacios en blanco y los tabuladores
t_ignore = ' \t'

# Manejar errores de token
def t_error(t):
    print("Carácter ilegal '%s'" % t.value[0])
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()
