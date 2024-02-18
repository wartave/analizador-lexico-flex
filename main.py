import tkinter as tk
from tkinter import scrolledtext
import lexer
import ply.yacc as yacc
from analizador_sintactico import parser
# Definir la gramática del analizador sintáctico
# (las mismas reglas y acciones que mencioné anteriormente)
# ...

# Crear el analizador sintáctico


def analyze_input():
    input_text = text_area.get("1.0", 'end-1c')
    lexer.lexer.input(input_text)
    tokens = []
    while True:
        tok = lexer.lexer.token()
        if not tok:
            break
        tokens.append(tok)
    
    # Tokenización completada, ahora analizar sintácticamente
    syntax_errors = False
    for token in tokens:
        if token.type == 'ERROR':
            syntax_errors = True
            break
    
    if syntax_errors:
        tokens_text_area.delete('1.0', tk.END)
        tokens_text_area.insert(tk.END, "Error de sintaxis en la entrada.")
    else:
        # Analizar sintácticamente
        try:
            result = parser.parse(input_text)
            tokens_text_area.delete('1.0', tk.END)
            tokens_text_area.insert(tk.END, "Resultado del análisis sintáctico: " + str(result))
        except Exception as e:
            tokens_text_area.delete('1.0', tk.END)
            tokens_text_area.insert(tk.END, "Error durante el análisis sintáctico: " + str(e))


app = tk.Tk()
app.title("Analizador Léxico y Sintáctico")

text_area = scrolledtext.ScrolledText(app, width=40, height=10)
text_area.grid(row=0, column=0, padx=10, pady=10)

tokens_text_area = scrolledtext.ScrolledText(app, width=40, height=10)
tokens_text_area.grid(row=0, column=1, padx=10, pady=10)

analyze_button = tk.Button(app, text="Analizar", command=analyze_input)
analyze_button.grid(row=1, column=0, columnspan=2, pady=5)

app.mainloop()
