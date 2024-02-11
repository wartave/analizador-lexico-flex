import tkinter as tk
from tkinter import scrolledtext
import lexer


def analyze_input():
    input_text = text_area.get("1.0",'end-1c')
    lexer.lexer.input(input_text)
    tokens = []
    while True:
        tok = lexer.lexer.token()
        if not tok:
            break
        tokens.append(tok)
        
    tokens_text_area.delete('1.0', tk.END)
    for token in tokens:
        tokens_text_area.insert(tk.END, str(token) + '\n')


app = tk.Tk()
app.title("Analizador Léxico")


text_area = scrolledtext.ScrolledText(app, width=40, height=10)
text_area.grid(row=0, column=0, padx=10, pady=10)


tokens_text_area = scrolledtext.ScrolledText(app, width=40, height=10)
tokens_text_area.grid(row=0, column=1, padx=10, pady=10)


analyze_button = tk.Button(app, text="Analizar", command=analyze_input)
analyze_button.grid(row=1, column=0, columnspan=2, pady=5)


app.mainloop()
