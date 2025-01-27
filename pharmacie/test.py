import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import customtkinter as ctk
import sqlite3
from datetime import datetime

class AddProductPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        # ... (code existant)

class ModifyProductPage(ctk.CTkFrame):
    def __init__(self, parent, product):
        super().__init__(parent)
        # ... (code existant)

class ShowProductsPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.grid(row=0, column=0, padx=20, pady=20)

        # Créer un Treeview pour afficher les produits
        self.tree = ttk.Treeview(self, columns=("code", "designation", "quantite", "date_expiration", "jours_avant_expiration"), show="headings", height=20)
        self.tree.heading("code", text="Code")
        self.tree.heading("designation", text="Désignation")
        self.tree.heading("quantite", text="Quantité")
        self.tree.heading("date_expiration", text="Date d'Expiration")
        self.tree.heading("jours_avant_expiration", text="Jours avant Expiration")
        self.tree.pack(side=tk.LEFT, fill="both", expand=True)

        # Ajouter des tags pour les couleurs
        self.tree.tag_configure('red', background='red')
        self.tree.tag_configure('orange', background='orange')
        self.tree.tag_configure('yellow', background='yellow')
        self.tree.tag_configure('green', background='green')

        # Créer un Frame pour les boutons
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        # Ajouter les boutons d'action
        self.modify_button = ctk.CTkButton(self.button_frame, text="Modifier", command=self.modify_selected_product)
        self.modify_button.pack(pady=5)
        self.delete_button = ctk.CTkButton(self.button_frame, text="Supprimer", command=self.delete_selected_product)
        self.delete_button.pack(pady=5)

        # Ajouter un bouton pour l'interrupteur
        self.toggle_button = ctk.CTkButton(self.button_frame, text="Afficher/Masquer Couleurs", command=self.toggle_colors)
        self.toggle_button.pack(pady=5)

        # État de l'affichage des couleurs
        self.colors_visible = True

        # Récupérer les produits de la base de données
        self.load_products()

    def load_products(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        conn = sqlite3.connect('pharmacie.db')
        c = conn.cursor()
        c.execute("SELECT code, designation, quantite, date_expiration FROM Produit")
        for row in c.fetchall():
            code, designation, quantite, date_expiration = row
            jours_avant_expiration = self.calculate_days_before_expiration(date_expiration)
            tag = self.get_tag_based_on_days(jours_avant_expiration) if self.colors_visible else ''
            self.tree.insert("", "end", values=(code, designation, quantite, date_expiration, jours_avant_expiration), tags=(tag,))
        conn.close()

    def calculate_days_before_expiration(self, date_expiration):
        expiration_date = datetime.strptime(date_expiration, '%Y-%m-%d')
        current_date = datetime.now()
        days_before_expiration = (expiration_date - current_date).days
        return days_before_expiration

    def get_tag_based_on_days(self, days_before_expiration):
        if days_before_expiration < 90:  # moins de 3 mois
            return 'red'
        elif days_before_expiration < 180:  # moins de 6 mois
            return 'orange'
        elif days_before_expiration < 270:  # moins de 9 mois
            return 'yellow'
        elif days_before_expiration >= 365:  # 12 mois ou plus
            return 'green'
        return ''

    def toggle_colors(self):
        self.colors_visible = not self.colors_visible
        self.load_products()

    def modify_selected_product(self):
        selected_item = self.tree.selection()
        if selected_item:
            code = self.tree.item(selected_item, "values")[0]
            conn = sqlite3.connect('pharmacie.db')
            c = conn.cursor()
            c.execute("SELECT * FROM Produit WHERE code=?", (code,))
            product = c.fetchone()
            conn.close()
            if product:
                modify_product_window = ctk.CTkToplevel(self)
                modify_product_window.title("Modifier un produit")
                modify_product_window.geometry("400x300")
                modify_product_window.transient(self)  # Rendre la fenêtre modale
                modify_product_window.grab_set()  # Empêcher l'interaction avec la fenêtre principale

                modify_product_page = ModifyProductPage(modify_product_window, product)
                modify_product_page.pack(fill="both", expand=True)

    def delete_selected_product(self):
        selected_item = self.tree.selection()
        if selected_item:
            code = self.tree.item(selected_item, "values")[0]
            confirm = messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer ce produit ?")
            if confirm:
                self.delete_product(code)

    def delete_product(self, code):
        conn = sqlite3.connect('pharmacie.db')
        c = conn.cursor()
        c.execute("DELETE FROM Produit WHERE code=?", (code,))
        conn.commit()
        conn.close()
        self.load_products()

class ShowUsersPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.grid(row=0, column=0, padx=20, pady=20)

        # Créer un Treeview pour afficher les utilisateurs
        self.tree = ttk.Treeview(self, columns=("id_user", "nom", "prenom", "privilege"), show="headings")
        self.tree.heading("id_user", text="ID")
        self.tree.heading("nom", text="Nom")
        self.tree.heading("prenom", text="Prénom")
        self.tree.heading("privilege", text="Privilège")
        self.tree.pack(side=tk.LEFT, fill="both", expand=True)

        # Récupérer les utilisateurs de la base de données
        self.load_users()

    def load_users(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        conn = sqlite3.connect('pharmacie.db')
        c = conn.cursor()
        c.execute("SELECT id_user, nom, prenom, login, privilege FROM Utilisateur")
        for row in c.fetchall():
            self.tree.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4]))
        conn.close()

class PharmacyApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Pharmacie - Gestion des produits")
        self.geometry("400x300")

        # Créer une instance de la page d'ajout de produits
        self.add_product_page = AddProductPage(self)
        self.add_product_page.grid(row=0, column=0, padx=20, pady=20)

if __name__ == "__main__":
    app = PharmacyApp()
    app.mainloop()