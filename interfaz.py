import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import sys
import os

class AnalizadorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Analizador C# - LP")
        self.geometry("700x500")

        # Variables
        self.usuario_key = tk.StringVar(value="medardomoran")
        self.archivo_path = None

        # Widgets
        self.crear_widgets()

    def crear_widgets(self):
        # Selección de usuario
        frame_usuario = ttk.LabelFrame(self, text="Seleccionar Usuario")
        frame_usuario.pack(fill="x", padx=10, pady=5)

        usuarios = [("Medardo Moran", "medardomoran"),
                    ("Mario Alvarado", "marioalvarado"),
                    ("Andres Layedra", "andreslayedra")]

        for text, val in usuarios:
            ttk.Radiobutton(frame_usuario, text=text, variable=self.usuario_key, value=val).pack(side="left", padx=10, pady=5)

        # Selección archivo
        frame_archivo = ttk.Frame(self)
        frame_archivo.pack(fill="x", padx=10, pady=5)

        ttk.Button(frame_archivo, text="Seleccionar archivo .cs", command=self.seleccionar_archivo).pack(side="left")
        self.label_archivo = ttk.Label(frame_archivo, text="Ningún archivo seleccionado", width=60)
        self.label_archivo.pack(side="left", padx=10)

        # Botones para análisis
        frame_botones = ttk.Frame(self)
        frame_botones.pack(fill="x", padx=10, pady=10)

        ttk.Button(frame_botones, text="Ejecutar Análisis Léxico", command=self.ejecutar_lexico).pack(side="left", padx=5)
        ttk.Button(frame_botones, text="Ejecutar Análisis Sintáctico", command=self.ejecutar_sintactico).pack(side="left", padx=5)
        ttk.Button(frame_botones, text="Ejecutar Análisis Semántico", command=self.ejecutar_semantico).pack(side="left", padx=5)

        # Textbox para resultados
        frame_resultado = ttk.LabelFrame(self, text="Resultado")
        frame_resultado.pack(fill="both", expand=True, padx=10, pady=5)

        self.text_resultado = tk.Text(frame_resultado, wrap="word", state="normal")
        self.text_resultado.pack(fill="both", expand=True)

    def seleccionar_archivo(self):
        path = filedialog.askopenfilename(filetypes=[("C# Files", "*.cs")])
        if path:
            self.archivo_path = path
            nombre = os.path.basename(path)
            self.label_archivo.config(text=nombre)

    def ejecutar_analizador(self, script_name):
        if not self.archivo_path:
            messagebox.showwarning("Archivo no seleccionado", "Por favor, seleccione un archivo .cs para analizar.")
            return

        usuario = self.usuario_key.get()
        python_executable = sys.executable
        try:
            # Ejecutar el script con argumentos
            proceso = subprocess.run([python_executable, script_name, usuario],
                                    capture_output=True, text=True, timeout=15)

            salida = proceso.stdout
            error = proceso.stderr

            resultado = ""
            if salida:
                resultado += f"Salida estándar:\n{salida}\n"
            if error:
                resultado += f"Errores:\n{error}\n"
            if not salida and not error:
                resultado = "No se obtuvo salida ni error."

            self.text_resultado.delete("1.0", tk.END)
            self.text_resultado.insert(tk.END, resultado)

        except subprocess.TimeoutExpired:
            messagebox.showerror("Error", f"El análisis con {script_name} tardó demasiado y fue cancelado.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo ejecutar {script_name}:\n{e}")

    def ejecutar_lexico(self):
        self.ejecutar_analizador("lex.py")

    def ejecutar_sintactico(self):
        self.ejecutar_analizador("yacc.py")

    def ejecutar_semantico(self):
        self.ejecutar_analizador("semantico.py")


if __name__ == "__main__":
    app = AnalizadorApp()
    app.mainloop()