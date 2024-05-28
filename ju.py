import tkinter as tk
from tkinter import ttk
import random

class JuegoTresEnRayaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tres en Raya")
        self.puntaje = [0, 0]  
        self.crear_interfaz()

    def crear_interfaz(self):
        self.turno_actual = random.choice([0, 1])
        self.tablero = [["-" for _ in range(3)] for _ in range(3)]
        self.botones = []
        for i in range(3):
            fila = []
            for j in range(3):
                boton = tk.Button(self.root, text="", width=8, height=4, font=("Helvetica", 24),
                                  command=lambda fila=i, columna=j: self.jugar(fila, columna))
                boton.grid(row=i, column=j)
                fila.append(boton)
            self.botones.append(fila)

    def jugar(self, fila, columna):
        if self.tablero[fila][columna] == "-":
            self.tablero[fila][columna] = "X" if self.turno_actual == 0 else "O"
            if self.tablero[fila][columna] == "X":
                self.botones[fila][columna].config(text=self.tablero[fila][columna], fg="blue")  
            else:
                self.botones[fila][columna].config(text=self.tablero[fila][columna])  
            if self.comprobar_ganador():
                self.puntaje[self.turno_actual] += 1
                mensaje_jugadores = "Jugador 1 con ficha O\nJugador 2 con ficha X"
                mensaje_puntaje = f" {self.puntaje[0]} - {self.puntaje[1]}"
                ficha_ganadora = "X" if self.turno_actual == 0 else "O"
                mensaje_ganador = f"Ganador: Jugador con la ficha {ficha_ganadora}"
                self.mostrar_mensaje("Fin del juego", mensaje_jugadores, mensaje_ganador, mensaje_puntaje)
                self.reiniciar_juego()
            elif self.tablero_completo():
                self.mostrar_mensaje("Fin del juego", "Empate")
                self.reiniciar_juego()
            else:
                self.turno_actual = 1 - self.turno_actual

    def comprobar_ganador(self):
        for fila in self.tablero:
            if fila[0] == fila[1] == fila[2] != "-":
                return True
        # Comprobación por columnas
        for columna in range(3):
            if self.tablero[0][columna] == self.tablero[1][columna] == self.tablero[2][columna] != "-":
                return True
        # Comprobación por diagonales
        if self.tablero[0][0] == self.tablero[1][1] == self.tablero[2][2] != "-" or \
                self.tablero[0][2] == self.tablero[1][1] == self.tablero[2][0] != "-":
            return True
        return False

    def tablero_completo(self):
        for fila in self.tablero:
            if "-" in fila:
                return False
        return True

    def mostrar_mensaje(self, titulo, mensaje_jugadores, mensaje_ganador, mensaje_puntaje):
        popup = tk.Toplevel(self.root)
        popup.title(titulo)
        popup.geometry("500x250")
        ttk.Label(popup, text=mensaje_jugadores, font=("Helvetica", 12)).pack(pady=5)
        ttk.Label(popup, text=mensaje_ganador, font=("Helvetica", 12)).pack(pady=5)
        ttk.Label(popup, text=mensaje_puntaje, font=("Helvetica", 12)).pack(pady=5)
        ttk.Button(popup, text="Aceptar", command=popup.destroy).pack()
        popup.bind("<Button-1>", lambda event: popup.destroy())  

    def reiniciar_juego(self):
        self.turno_actual = 1 - self.turno_actual  
        self.tablero = [["-" for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.botones[i][j].config(text="", fg="black")  

if __name__ == "__main__":
    root = tk.Tk()
    juego = JuegoTresEnRayaGUI(root)
    root.mainloop()
