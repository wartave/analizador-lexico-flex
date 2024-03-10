#main.py

import tkinter as tk
from tkinter import scrolledtext
import lexer
from collections import defaultdict
import ply.yacc as yacc
import analizador_sintactico
import analizador_semantico



errores_semanticos=[]

def analyze_input():
    analizador_sintactico.variables={}
    analizador_semantico.variables_declaradas={}
    analizador_semantico.funciones_definidas=set();
    analizador_sintactico.errors_text_area.delete('1.0', tk.END)
    if  analizador_sintactico.errors_text_area is not None:
        analizador_sintactico.errors_text_area.delete('1.0', tk.END)
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
         if  analizador_sintactico.errors_text_area is not None:
            analizador_sintactico.errors_text_area.delete('1.0', tk.END)
            analizador_sintactico.errors_text_area.insert(tk.END, "Error de sintaxis en la entrada.")
    else:
            result = analizador_sintactico.parser.parse(input_text)
            output_text_area.delete('1.0', tk.END)
            output_text_area.insert(tk.END, "Resultado del análisis sintáctico: " + str(result))

            if result is not None:
                # Analizar semánticamente
                errores_semanticos = analizador_semantico.analizar_semanticamente(result)
                 #analizador_sintactico.errors_text_area.delete('1.0', tk.END)
                if errores_semanticos is not None:
                    error_text = "Errores semánticos encontrados:\n" + "\n".join(errores_semanticos)
                    if  analizador_sintactico.errors_text_area is not None:
                        analizador_sintactico.errors_text_area.insert(tk.END, error_text)
            else:
                if  analizador_sintactico.errors_text_area is not None:
                    analizador_sintactico.errors_text_area.insert(tk.END, "No se encontraron errores semánticos.")
        

app = tk.Tk()
app.title("Analizador Léxico, Sintáctico y Semántico")

text_area = scrolledtext.ScrolledText(app, width=40, height=10)
text_area.grid(row=0, column=0, padx=10, pady=10)

output_text_area = scrolledtext.ScrolledText(app, width=40, height=10)
output_text_area.grid(row=0, column=1, padx=10, pady=10)


analizador_sintactico.errors_text_area = scrolledtext.ScrolledText(app, width=40, height=10)
analizador_sintactico.errors_text_area.grid(row=0, column=2, padx=10, pady=10)
analyze_button = tk.Button(app, text="Analizar", command=analyze_input)
analyze_button.grid(row=1, column=0, columnspan=3, pady=5)


app.mainloop()