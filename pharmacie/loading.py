import tkinter as tk
import customtkinter as ctk

class LoadingPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.grid(row=0, column=0, padx=20, pady=20)

        # Créer un label pour l'animation de chargement
        self.loading_label = ctk.CTkLabel(self, text="Chargement...", font=("Helvetica", 24))
        self.loading_label.grid(row=0, column=0, padx=10, pady=10)

        # Démarrer l'animation de clignotement
        self.blink()

    def blink(self):
        current_color = self.loading_label.cget("text_color")
        next_color = "white" if current_color == "black" else "black"
        self.loading_label.configure(text_color=next_color)
        self.after(500, self.blink)  # Changer la couleur toutes les 500 ms