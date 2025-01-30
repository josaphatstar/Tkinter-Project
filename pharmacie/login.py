import tkinter as tk
import customtkinter as ctk
import sqlite3
from tkinter import messagebox

class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        self.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        # Créer les labels et les champs de saisie
        ctk.CTkLabel(self, text="Login:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.login_entry = ctk.CTkEntry(self)
        self.login_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        ctk.CTkLabel(self, text="Mot de passe:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.password_entry = ctk.CTkEntry(self, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Ajouter un bouton pour se connecter
        self.login_button = ctk.CTkButton(self, text="Se connecter", command=self.login)
        self.login_button.grid(row=2, columnspan=2, pady=20)

    def login(self):
        login = self.login_entry.get()
        password = self.password_entry.get()

        conn = sqlite3.connect('pharmacie.db')
        c = conn.cursor()
        c.execute("SELECT * FROM Utilisateur WHERE login=? AND mot_de_passe=?", (login, password))
        user = c.fetchone()
        conn.close()

        if user:
            if user[-1] == 1:  # Vérifier si c'est la première connexion
                self.app.show_change_password_page(user)
            else:
                self.app.show_main_page(user)
        else:
            messagebox.showerror("Erreur", "Login ou mot de passe incorrect.")