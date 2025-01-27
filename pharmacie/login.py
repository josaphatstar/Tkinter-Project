import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import sqlite3

class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.grid(row=0, column=0, padx=20, pady=20)

        # Créer les labels et les champs de saisie
        ctk.CTkLabel(self, text="Nom d'utilisateur:").grid(row=0, column=0, padx=10, pady=10)
        self.username_entry = ctk.CTkEntry(self)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(self, text="Mot de passe:").grid(row=1, column=0, padx=10, pady=10)
        self.password_entry = ctk.CTkEntry(self, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        # Ajouter un bouton pour soumettre le formulaire
        self.login_button = ctk.CTkButton(self, text="Se connecter", command=self.login)
        self.login_button.grid(row=2, columnspan=2, pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        conn = sqlite3.connect('pharmacie.db')
        c = conn.cursor()
        c.execute("SELECT * FROM Utilisateur WHERE login=? AND mot_de_passe=?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            messagebox.showinfo("Succès", "Connexion réussie !")
            self.app.show_main_page()
        else:
            messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect.")