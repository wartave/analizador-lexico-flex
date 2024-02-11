import tkinter as tk
from tkinter import scrolledtext
import lexer

# Función para analizar la entrada de texto
def analyze_input():
    input_text = text_area.get("1.0",'end-1c')
    lexer.lexer.input(input_text)
    tokens = []
    while True:
        tok = lexer.lexer.token()
        if not tok:
            break
        tokens.append(tok)
    # Actualizar el contenido del TextArea de tokens
    tokens_text_area.delete('1.0', tk.END)
    for token in tokens:
        tokens_text_area.insert(tk.END, str(token) + '\n')

# Crear la ventana de la aplicación
app = tk.Tk()
app.title("Analizador Léxico")

# Crear un área de texto donde el usuario puede ingresar código
text_area = scrolledtext.ScrolledText(app, width=40, height=10)
text_area.grid(row=0, column=0, padx=10, pady=10)

# Crear un segundo área de texto para mostrar los tokens generados
tokens_text_area = scrolledtext.ScrolledText(app, width=40, height=10)
tokens_text_area.grid(row=0, column=1, padx=10, pady=10)

# Botón para iniciar el análisis léxico
analyze_button = tk.Button(app, text="Analizar", command=analyze_input)
analyze_button.grid(row=1, column=0, columnspan=2, pady=5)

# Ejecutar la aplicación
app.mainloop()
