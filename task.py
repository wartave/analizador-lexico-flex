import tkinter as tk
import sys

class TaskWindow:
    def __init__(self, title):
        self.title = title
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry("400x300")

        self.label = tk.Label(self.root, text="Esta es la ventana de la tarea: " + title)
        self.label.pack()

        self.root.mainloop()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python task.py <title>")
        sys.exit(1)

    title = sys.argv[1]
    task_window = TaskWindow(title)
