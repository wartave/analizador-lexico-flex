import tkinter as tk
from tkinter import ttk

class TaskWindow:
    def __init__(self, master, title):
        self.master = master
        self.title = title
        self.window = tk.Toplevel(master)
        self.window.title(title)
        self.window.geometry("400x300")

        self.label = tk.Label(self.window, text="Esta es la ventana de la tarea: " + title)
        self.label.pack()

class TextEditor:
    def __init__(self, master, simulator):
        self.master = master
        self.simulator = simulator

        # Crear el marco para el editor de texto
        self.editor_frame = tk.Frame(self.simulator.desktop, bg="white", width=600, height=400)
        self.editor_frame.place(x=100, y=100)

        # Crear el widget Text dentro del marco
        self.text_widget = tk.Text(self.editor_frame)
        self.text_widget.pack(expand=True, fill="both")

        # Botones para cerrar, minimizar y expandir (simulados)
        self.close_button = tk.Button(self.editor_frame, text="Cerrar", command=self.close_text_editor)
        self.close_button.place(x=550, y=0)

        self.minimize_button = tk.Button(self.editor_frame, text="Minimizar", command=self.minimize_text_editor)
        self.minimize_button.place(x=500, y=0)

        self.expand_button = tk.Button(self.editor_frame, text="Expandir", command=self.expanded_text_editor)
        self.expand_button.place(x=450, y=0)

        # Configurar eventos para permitir arrastrar la ventana
        self.editor_frame.bind("<ButtonPress-1>", self.start_drag)
        self.editor_frame.bind("<B1-Motion>", self.on_drag)

        # Estado del editor de texto (normal, minimizado, maximizado)
        self.state = "normal"

    def close_text_editor(self):
        self.editor_frame.destroy()
        self.simulator.remove_from_taskbar("Editor de Texto")

    def minimize_text_editor(self):
        if self.state != "minimized":
            self.editor_frame.place_forget()
            self.state = "minimized"

    def expanded_text_editor(self):
        if self.state == "normal":
        # Guardar las dimensiones y posición actuales antes de expandir
            self.editor_frame.previous_dimensions = (self.editor_frame.winfo_width(), self.editor_frame.winfo_height())
            self.editor_frame.previous_position = (self.editor_frame.winfo_x(), self.editor_frame.winfo_y())
            # Expandir al tamaño completo del escritorio
            self.editor_frame.place(x=0, y=0, relwidth=1, relheight=1)
            self.state = "expanded"
        elif self.state == "expanded":
            # Restaurar las dimensiones y posición anteriores
            width, height = self.editor_frame.previous_dimensions
            x, y = self.editor_frame.previous_position
            self.editor_frame.place(x=x, y=y, width=width, height=height)
            self.state = "normal"
    def expand_text_editor(self):
        if self.state == "minimized":
            self.editor_frame.place(x=0, y=0, relwidth=1, relheight=1)  # Ocupar todo el espacio disponible
            self.state = "expanded"
        elif self.state == "expanded":
            self.editor_frame.place(x=100, y=100, width=600, height=400)  # Volver al tamaño original
            self.state = "normal"
        elif self.state == "maximized":
            self.editor_frame.place(x=100, y=100)
            self.state = "normal"

    def start_drag(self, event):
        # Guardar la posición inicial del cursor
        self.x = event.x
        self.y = event.y

    def on_drag(self, event):
        # Calcular el desplazamiento del cursor
        dx = event.x - self.x
        dy = event.y - self.y

        # Mover la ventana del editor de texto
        x = self.editor_frame.winfo_x() + dx
        y = self.editor_frame.winfo_y() + dy
        self.editor_frame.place(x=x, y=y)

        # Actualizar las coordenadas del cursor
        self.x = event.x
        self.y = event.y

class Simulator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Simulador de Sistema Operativo")
        self.root.geometry("800x600")

        self.desktop = tk.Frame(self.root, bg="light blue", width=800, height=400)
        self.desktop.pack(fill=tk.BOTH, expand=True)

        self.taskbar = tk.Frame(self.root, bg="gray", width=800, height=50)
        self.taskbar.pack(fill=tk.X)

        self.task_button = tk.Button(self.taskbar, text="Abrir nueva tarea", command=self.open_task_window)
        self.task_button.pack(side=tk.LEFT)

        self.opened_programs = []

        # Crear un widget Label para el icono y hacerlo arrastrable
        self.icon_label = tk.Label(self.desktop, text="Icono", bg="white")
        self.icon_label.bind("<ButtonPress-1>", self.start_drag)
        self.icon_label.bind("<B1-Motion>", self.on_drag)
        self.icon_label.bind("<ButtonRelease-1>", self.release_drag)  # Cuando se suelta el botón del mouse
        self.icon_label.bind("<Button-3>", self.show_context_menu)  # Menú contextual con clic derecho
        self.icon_label.pack()

        self.is_dragging = False  # Bandera para indicar si se está arrastrando el icono

    def open_task_window(self):
        title = "Tarea " + str(len(self.root.children) + 1)
        TaskWindow(self.root, title)
        self.update_taskbar(title)

    def start_drag(self, event):
        # Establecer la bandera de arrastre en Verdadero al iniciar el arrastre
        self.is_dragging = True
        
        # Obtener la posición inicial del widget
        self.drag_data = {"x": event.x, "y": event.y}

    def on_drag(self, event):
        # Si se está arrastrando el icono, moverlo
        if self.is_dragging:
            # Definir el tamaño de la cuadrícula
            grid_size = 50
            
            # Calcular la cantidad de movimiento
            delta_x = event.x - self.drag_data["x"]
            delta_y = event.y - self.drag_data["y"]

            # Calcular la nueva posición del icono en la cuadrícula
            x_grid = round((self.icon_label.winfo_x() + delta_x) / grid_size) * grid_size
            y_grid = round((self.icon_label.winfo_y() + delta_y) / grid_size) * grid_size

            # Mover el icono a la nueva posición en la cuadrícula
            self.icon_label.place(x=x_grid, y=y_grid)

    def release_drag(self, event):
        # Restablecer la bandera de arrastre a Falso cuando se suelta el botón del mouse
        self.is_dragging = False
        
        # Solo abrir el editor de texto si no se está arrastrando el icono
        text_editor = TextEditor(self.root, self)
        self.update_taskbar("Editor de Texto")

    def update_taskbar(self, program_name):
        if program_name not in self.opened_programs:
            program_button = tk.Button(self.taskbar, text=program_name)
            program_button.pack(side=tk.LEFT)
            self.opened_programs.append(program_name)

    def remove_from_taskbar(self, program_name):
        if program_name in self.opened_programs:
            for widget in self.taskbar.winfo_children():
                if widget.cget("text") == program_name:
                    widget.destroy()
                    self.opened_programs.remove(program_name)

    def show_context_menu(self, event):
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Abrir", command=self.open_text_editor)
        menu.add_command(label="Borrar", command=self.delete_icon)
        menu.add_command(label="Cambiar nombre", command=self.change_name)
        menu.post(event.x_root, event.y_root)

    def open_text_editor(self):
        text_editor = TextEditor(self.root, self)
        self.update_taskbar("Editor de Texto")

    def delete_icon(self):
        self.icon_label.destroy()

    def change_name(self):
        new_name = tk.simpledialog.askstring("Cambiar nombre", "Ingrese el nuevo nombre:")
        if new_name:
            self.icon_label.config(text=new_name)

if __name__ == "__main__":
    simulator = Simulator()
    simulator.root.mainloop()

