import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from analizador import analisis_lexico, analisis_sintactico, analisis_semantico

class AnalizadorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("C# Shark - Analizador")
        self.root.geometry("1100x700")
        self.root.configure(bg="#121212")

        # =============== Canvas con Scroll ===============
        canvas = tk.Canvas(self.root, bg="#121212", highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(self.root, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        # Frame dentro del canvas
        self.frame = tk.Frame(canvas, bg="#121212")
        canvas.create_window((0, 0), window=self.frame, anchor="nw")

        self.frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # =============== Logo ===============
        try:
            logo_img = Image.open("resources/cshark_logo.png")
            logo_img = logo_img.resize((120, 120), Image.Resampling.LANCZOS)
            self.logo = ImageTk.PhotoImage(logo_img)
            logo_label = tk.Label(self.frame, image=self.logo, bg="#121212")
            logo_label.pack(pady=10)
        except Exception as e:
            print("Logo no cargado:", e)

        # =============== Secciones ===============
        self.crear_etiqueta("Código C# de entrada:")
        self.codigo_text = self.crear_caja_texto(height=15)

        self.crear_botones()

        self.lexico_text = self.crear_apartado_resultado("Análisis Léxico")
        self.sintactico_text = self.crear_apartado_resultado("Análisis Sintáctico")
        self.semantico_text = self.crear_apartado_resultado("Análisis Semántico")

    def crear_etiqueta(self, texto):
        etiqueta = tk.Label(self.frame, text=texto, fg="#ffffff", bg="#121212", font=("Arial", 12, "bold"))
        etiqueta.pack(pady=(10, 2))

    def crear_caja_texto(self, height=10):
        caja = tk.Text(self.frame, height=height, width=120, bg="#2D033B", fg="#ffffff", insertbackground="white")
        caja.pack(padx=10, pady=5)
        return caja

    def crear_apartado_resultado(self, titulo):
        self.crear_etiqueta(titulo)
        return self.crear_caja_texto(height=10)

    def crear_botones(self):
        btn_frame = tk.Frame(self.frame, bg="#121212")
        btn_frame.pack(pady=15)
        self.boton_personalizado(btn_frame, "Analizar", self.analizar).grid(row=0, column=0, padx=15)
        self.boton_personalizado(btn_frame, "Limpiar", self.limpiar).grid(row=0, column=1, padx=15)

    def boton_personalizado(self, parent, texto, comando):
        return tk.Button(
            parent, text=texto, command=comando,
            bg="#7B2CBF", fg="#ffffff", activebackground="#9D4EDD",
            font=("Arial", 11, "bold"), padx=15, pady=5, bd=0
        )

    def analizar(self):
        codigo = self.codigo_text.get("1.0", tk.END).strip()
        if not codigo:
            messagebox.showwarning("Advertencia", "Por favor ingresa código C#.")
            return

        self.lexico_text.delete("1.0", tk.END)
        self.lexico_text.insert(tk.END, analisis_lexico(codigo))

        self.sintactico_text.delete("1.0", tk.END)
        self.sintactico_text.insert(tk.END, analisis_sintactico(codigo))

        self.semantico_text.delete("1.0", tk.END)
        self.semantico_text.insert(tk.END, analisis_semantico(codigo))

    def limpiar(self):
        self.codigo_text.delete("1.0", tk.END)
        self.lexico_text.delete("1.0", tk.END)
        self.sintactico_text.delete("1.0", tk.END)
        self.semantico_text.delete("1.0", tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = AnalizadorGUI(root)
    root.mainloop()
