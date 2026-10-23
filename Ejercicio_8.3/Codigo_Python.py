import math
import tkinter as tk
from abc import ABC, abstractmethod
from tkinter import messagebox


# ---------------- Modelo ----------------
class FiguraGeometrica(ABC):
    @abstractmethod
    def volumen(self): ...

    @abstractmethod
    def superficie(self): ...


class Cilindro(FiguraGeometrica):
    def __init__(self, radio, altura):
        self.radio, self.altura = radio, altura

    def volumen(self):
        return math.pi * self.radio ** 2 * self.altura

    def superficie(self):
        return 2 * math.pi * self.radio * (self.radio + self.altura)


class Esfera(FiguraGeometrica):
    def __init__(self, radio):
        self.radio = radio

    def volumen(self):
        return 4 / 3 * math.pi * self.radio ** 3

    def superficie(self):
        return 4 * math.pi * self.radio ** 2


class Piramide(FiguraGeometrica):
    """Pirámide de base cuadrada: apotema = altura de cada cara lateral."""

    def __init__(self, base, altura, apotema):
        self.base, self.altura, self.apotema = base, altura, apotema

    def volumen(self):
        return self.base ** 2 * self.altura / 3

    def superficie(self):
        return self.base ** 2 + 2 * self.base * self.apotema


class Cubo(FiguraGeometrica):
    def __init__(self, lado):
        self.lado = lado

    def volumen(self):
        return self.lado ** 3

    def superficie(self):
        return 6 * self.lado ** 2


class Prisma(FiguraGeometrica):
    def __init__(self, largo, ancho, altura):
        self.largo, self.ancho, self.altura = largo, ancho, altura

    def volumen(self):
        return self.largo * self.ancho * self.altura

    def superficie(self):
        return 2 * (self.largo * self.ancho + self.largo * self.altura + self.ancho * self.altura)


# ---------------- Dibujos (Canvas 150x150) ----------------
def dibujar_cilindro(c):
    c.create_oval(30, 15, 120, 45, outline="blue", width=2)
    c.create_line(30, 30, 30, 120, fill="blue", width=2)
    c.create_line(120, 30, 120, 120, fill="blue", width=2)
    c.create_arc(30, 105, 120, 135, start=180, extent=180, style="arc", outline="blue", width=2)
    c.create_arc(30, 105, 120, 135, start=0, extent=180, style="arc", outline="blue", dash=(3, 3))


def dibujar_esfera(c):
    c.create_oval(15, 15, 135, 135, outline="blue", width=2)
    c.create_arc(15, 60, 135, 90, start=180, extent=180, style="arc", outline="blue", width=2)
    c.create_arc(15, 60, 135, 90, start=0, extent=180, style="arc", outline="blue", dash=(3, 3))


def dibujar_piramide(c):
    c.create_line(20, 120, 100, 120, 130, 95, fill="blue", width=2)
    c.create_line(20, 120, 50, 95, 130, 95, fill="blue", dash=(3, 3))
    for p in ((20, 120), (100, 120), (130, 95)):
        c.create_line(75, 15, *p, fill="blue", width=2)
    c.create_line(75, 15, 50, 95, fill="blue", dash=(3, 3))


def dibujar_cubo(c):
    c.create_rectangle(20, 50, 100, 130, outline="blue", width=2)
    c.create_line(20, 50, 50, 20, 130, 20, 130, 100, 100, 130, fill="blue", width=2)
    c.create_line(100, 50, 130, 20, fill="blue", width=2)
    c.create_line(20, 130, 50, 100, 130, 100, fill="blue", dash=(3, 3))
    c.create_line(50, 20, 50, 100, fill="blue", dash=(3, 3))


def dibujar_prisma(c):
    c.create_rectangle(15, 60, 105, 130, outline="blue", width=2)
    c.create_line(15, 60, 45, 30, 135, 30, 135, 100, 105, 130, fill="blue", width=2)
    c.create_line(105, 60, 135, 30, fill="blue", width=2)
    c.create_line(15, 130, 45, 100, 135, 100, fill="blue", dash=(3, 3))
    c.create_line(45, 30, 45, 100, fill="blue", dash=(3, 3))


# ---------------- Interfaz ----------------
class VentanaFigura(tk.Toplevel):
    """Ventana genérica: recibe campos, clase de la figura y función de dibujo."""

    def __init__(self, padre, titulo, campos, clase, dibujo):
        super().__init__(padre)
        self.title(titulo)
        self.resizable(False, False)
        self.clase = clase
        self.entradas = []

        izq = tk.Frame(self, padx=15, pady=15)
        izq.pack(side="left")
        for fila, nombre in enumerate(campos):
            tk.Label(izq, text=f"{nombre} (cm):", anchor="w", width=14).grid(row=fila, column=0, pady=3)
            e = tk.Entry(izq, width=15)
            e.grid(row=fila, column=1, pady=3)
            self.entradas.append(e)
        tk.Button(izq, text="Calcular", width=14, command=self.calcular).grid(
            row=len(campos), column=1, pady=8)
        self.lbl_vol = tk.Label(izq, text="Volumen (cm3): ", anchor="w")
        self.lbl_vol.grid(row=len(campos) + 1, column=0, columnspan=2, sticky="w")
        self.lbl_sup = tk.Label(izq, text="Superficie (cm2): ", anchor="w")
        self.lbl_sup.grid(row=len(campos) + 2, column=0, columnspan=2, sticky="w")

        lienzo = tk.Canvas(self, width=150, height=150, bg="white")
        lienzo.pack(side="right", padx=15, pady=15)
        dibujo(lienzo)

    def calcular(self):
        try:
            valores = [float(e.get()) for e in self.entradas]
            if any(v <= 0 for v in valores):
                raise ValueError
            figura = self.clase(*valores)
        except ValueError:
            messagebox.showerror("Error", "Campo vacío, no numérico o no positivo.", parent=self)
            return
        self.lbl_vol.config(text=f"Volumen (cm3): {figura.volumen():.2f}")
        self.lbl_sup.config(text=f"Superficie (cm2): {figura.superficie():.2f}")


class VentanaPrincipal(tk.Tk):
    FIGURAS = [
        ("Cilindro", ["Radio", "Altura"], Cilindro, dibujar_cilindro),
        ("Esfera", ["Radio"], Esfera, dibujar_esfera),
        ("Pirámide", ["Base", "Altura", "Apotema"], Piramide, dibujar_piramide),
        ("Cubo", ["Lado"], Cubo, dibujar_cubo),
        ("Prisma", ["Largo", "Ancho", "Altura"], Prisma, dibujar_prisma),
    ]

    def __init__(self):
        super().__init__()
        self.title("Figuras geométricas")
        self.resizable(False, False)
        marco = tk.Frame(self, padx=20, pady=30)
        marco.pack()
        for nombre, campos, clase, dibujo in self.FIGURAS:
            tk.Button(marco, text=nombre, width=11,
                      command=lambda n=nombre, c=campos, k=clase, d=dibujo:
                      VentanaFigura(self, n, c, k, d)).pack(side="left", padx=5)


if __name__ == "__main__":
    VentanaPrincipal().mainloop()
