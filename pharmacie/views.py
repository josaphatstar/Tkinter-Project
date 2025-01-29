import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import customtkinter as ctk
import sqlite3
from datetime import datetime

class AddProductPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.grid(row=0, column=0, padx=20, pady=20)

        # Créer les labels
        ctk.CTkLabel(self, text="Désignation:").grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkLabel(self, text="Quantité:").grid(row=1, column=0, padx=10, pady=10)
        ctk.CTkLabel(self, text="Date d'Expiration:").grid(row=2, column=0, padx=10, pady=10)

        # Créer les champs de saisie
        self.designation_entry = ctk.CTkEntry(self)
        self.quantite_entry = ctk.CTkEntry(self)

        # Créer les combobox pour la date d'expiration
        self.expiration_day_combobox = ttk.Combobox(self, values=[str(i) for i in range(1, 32)], width=4)
        self.expiration_month_combobox = ttk.Combobox(self, values=[str(i) for i in range(1, 13)], width=4)
        self.expiration_year_combobox = ttk.Combobox(self, values=[str(i) for i in range(datetime.now().year, datetime.now().year + 20)], width=6)

        # Positionner les champs de saisie
        self.designation_entry.grid(row=0, column=1, padx=10, pady=10)
        self.quantite_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Positionner les combobox pour la date d'expiration
        self.expiration_day_combobox.grid(row=2, column=1, padx=2, pady=10, sticky='w')
        self.expiration_month_combobox.grid(row=2, column=1, padx=2, pady=10)
        self.expiration_year_combobox.grid(row=2, column=1, padx=2, pady=10, sticky='e')

        # Ajouter un bouton pour soumettre le formulaire
        self.submit_button = ctk.CTkButton(self, text="Ajouter Produit", command=self.add_product)
        self.submit_button.grid(row=3, columnspan=2, pady=20)

    def add_product(self):
        designation = self.designation_entry.get()
        quantite = self.quantite_entry.get()
        expiration_day = self.expiration_day_combobox.get()
        expiration_month = self.expiration_month_combobox.get()
        expiration_year = self.expiration_year_combobox.get()

        try:
            # Vérification de la quantité
            quantite = int(quantite)
            if quantite < 0:
                raise ValueError("La quantité doit être un entier positif.")

            # Vérification des valeurs des combobox
            if expiration_day not in self.expiration_day_combobox['values']:
                raise ValueError("Jour d'expiration invalide.")
            if expiration_month not in self.expiration_month_combobox['values']:
                raise ValueError("Mois d'expiration invalide.")
            if expiration_year not in self.expiration_year_combobox['values']:
                raise ValueError("Année d'expiration invalide.")

            # Conversion de la date d'expiration
            expiration_date = datetime(int(expiration_year), int(expiration_month), int(expiration_day))
            expiration = expiration_date.strftime('%Y-%m-%d')

            conn = sqlite3.connect('pharmacie.db')
            c = conn.cursor()
            c.execute('''
                INSERT INTO Produit (designation, quantite, date_expiration)
                VALUES (?, ?, ?)
            ''', (designation, quantite, expiration))
            conn.commit()
            messagebox.showinfo("Info", "Produit ajouté avec succès !")
        except ValueError as ve:
            messagebox.showerror("Erreur", f"Erreur de validation: {ve}")
        except sqlite3.IntegrityError:
            messagebox.showerror("Erreur", "Erreur lors de l'ajout du produit.")
        finally:
            conn.close()

class ModifyProductPage(ctk.CTkFrame):
    def __init__(self, parent, product):
        super().__init__(parent)

        self.product = product
        self.grid(row=0, column=0, padx=20, pady=20)

        # Créer les labels
        ctk.CTkLabel(self, text="Désignation:").grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkLabel(self, text="Quantité:").grid(row=1, column=0, padx=10, pady=10)
        ctk.CTkLabel(self, text="Date d'Expiration:").grid(row=2, column=0, padx=10, pady=10)

        # Créer les champs de saisie
        self.designation_entry = ctk.CTkEntry(self)
        self.designation_entry.insert(0, product[1])
        self.quantite_entry = ctk.CTkEntry(self)
        self.quantite_entry.insert(0, product[2])

        # Créer les combobox pour la date d'expiration
        expiration_date = datetime.strptime(product[3], '%Y-%m-%d')
        self.expiration_day_combobox = ttk.Combobox(self, values=[str(i) for i in range(1, 32)], width=4)
        self.expiration_day_combobox.set(expiration_date.day)
        self.expiration_month_combobox = ttk.Combobox(self, values=[str(i) for i in range(1, 13)], width=4)
        self.expiration_month_combobox.set(expiration_date.month)
        self.expiration_year_combobox = ttk.Combobox(self, values=[str(i) for i in range(datetime.now().year, datetime.now().year + 10)], width=6)
        self.expiration_year_combobox.set(expiration_date.year)

        # Positionner les champs de saisie
        self.designation_entry.grid(row=0, column=1, padx=10, pady=10)
        self.quantite_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Positionner les combobox pour la date d'expiration
        self.expiration_day_combobox.grid(row=2, column=1, padx=2, pady=10, sticky='w')
        self.expiration_month_combobox.grid(row=2, column=1, padx=2, pady=10)
        self.expiration_year_combobox.grid(row=2, column=1, padx=2, pady=10, sticky='e')

        # Ajouter un bouton pour soumettre le formulaire
        self.submit_button = ctk.CTkButton(self, text="Modifier Produit", command=self.modify_product)
        self.submit_button.grid(row=3, columnspan=2, pady=20)

    def modify_product(self):
        designation = self.designation_entry.get()
        quantite = self.quantite_entry.get()
        expiration_day = self.expiration_day_combobox.get()
        expiration_month = self.expiration_month_combobox.get()
        expiration_year = self.expiration_year_combobox.get()

        try:
            # Vérification de la quantité
            quantite = int(quantite)
            if quantite < 0:
                raise ValueError("La quantité doit être un entier positif.")

            # Vérification des valeurs des combobox
            if expiration_day not in self.expiration_day_combobox['values']:
                raise ValueError("Jour d'expiration invalide.")
            if expiration_month not in self.expiration_month_combobox['values']:
                raise ValueError("Mois d'expiration invalide.")
            if expiration_year not in self.expiration_year_combobox['values']:
                raise ValueError("Année d'expiration invalide.")

            # Conversion de la date d'expiration
            expiration_date = datetime(int(expiration_year), int(expiration_month), int(expiration_day))
            expiration = expiration_date.strftime('%Y-%m-%d')

            conn = sqlite3.connect('pharmacie.db')
            c = conn.cursor()
            c.execute('''
                UPDATE Produit
                SET designation = ?, quantite = ?, date_expiration = ?
                WHERE code = ?
            ''', (designation, quantite, expiration, self.product[0]))
            conn.commit()
            messagebox.showinfo("Info", "Produit modifié avec succès !")
        except ValueError as ve:
            messagebox.showerror("Erreur", f"Erreur de validation: {ve}")
        except sqlite3.IntegrityError:
            messagebox.showerror("Erreur", "Erreur lors de la modification du produit.")
        finally:
            conn.close()

class ShowProductsPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.grid(row=0, column=0, padx=20, pady=20)

        # Définir les styles pour le Treeview
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"), anchor="center")
        style.configure("Treeview", rowheight=25, font=("Helvetica", 10), background="white", foreground="black", fieldbackground="white")
        style.map("Treeview", background=[("selected", "gray")])

        # Ajouter un label et une barre de recherche avec un placeholder manuel
        self.search_var = tk.StringVar()
        self.search_label = ctk.CTkLabel(self, text="Recherche :")
        self.search_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.search_entry = ctk.CTkEntry(self, textvariable=self.search_var)
        self.search_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.search_entry.bind("<KeyRelease>", self.update_treeview)
        self.search_entry.bind("<FocusIn>", self.clear_placeholder)
        self.search_entry.bind("<FocusOut>", self.set_placeholder)

        # Définir le placeholder
        self.placeholder_text = "Rechercher un produit"
        self.set_placeholder()

        # Créer un Treeview pour afficher les produits
        self.tree = ttk.Treeview(self, columns=("code", "designation", "quantite", "date_expiration", "jours_avant_expiration"), show="headings", height=20)
        self.tree.heading("code", text="Code")
        self.tree.heading("designation", text="Désignation")
        self.tree.heading("quantite", text="Quantité")
        self.tree.heading("date_expiration", text="Date d'Expiration")
        self.tree.heading("jours_avant_expiration", text="Jours avant Expiration")

        # Centrer les contenus dans les colonnes
        self.tree.column("code", anchor="center")
        self.tree.column("designation", anchor="center")
        self.tree.column("quantite", anchor="center")
        self.tree.column("date_expiration", anchor="center")
        self.tree.column("jours_avant_expiration", anchor="center")

        self.tree.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Ajouter des tags pour les couleurs
        self.tree.tag_configure('red', background='red')
        self.tree.tag_configure('orange', background='orange')
        self.tree.tag_configure('yellow', background='yellow')
        self.tree.tag_configure('green', background='green')

        # Créer un Frame pour les boutons
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.grid(row=2, column=0, columnspan=2, pady=10)

        # Ajouter les boutons d'action
        self.modify_button = ctk.CTkButton(self.button_frame, text="Modifier", command=self.modify_selected_product)
        self.modify_button.pack(side="left", padx=5)
        self.delete_button = ctk.CTkButton(self.button_frame, text="Supprimer", command=self.delete_selected_product)
        self.delete_button.pack(side="left", padx=5)

        # Ajouter un bouton pour l'interrupteur
        self.toggle_button = ctk.CTkButton(self.button_frame, text="Afficher/Masquer Couleurs", command=self.toggle_colors)
        self.toggle_button.pack(side="left", padx=5)

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

    def update_treeview(self, event):
        search_term = self.search_var.get().lower()
        for item in self.tree.get_children():
            self.tree.delete(item)
        conn = sqlite3.connect('pharmacie.db')
        c = conn.cursor()
        c.execute("SELECT code, designation, quantite, date_expiration FROM Produit WHERE LOWER(designation) LIKE ?", ('%' + search_term + '%',))
        for row in c.fetchall():
            code, designation, quantite, date_expiration = row
            jours_avant_expiration = self.calculate_days_before_expiration(date_expiration)
            tag = self.get_tag_based_on_days(jours_avant_expiration) if self.colors_visible else ''
            self.tree.insert("", "end", values=(code, designation, quantite, date_expiration, jours_avant_expiration), tags=(tag,))
        conn.close()

    def set_placeholder(self, event=None):
        if not self.search_var.get():
            self.search_entry.insert(0, self.placeholder_text)

    def clear_placeholder(self, event=None):
        if self.search_entry.get() == self.placeholder_text:
            self.search_entry.delete(0, tk.END)


class ShowUsersPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.grid(row=0, column=0, padx=20, pady=20)

        # Définir les styles pour le Treeview
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"), anchor="center")
        style.configure("Treeview", rowheight=25, font=("Helvetica", 10), background="white", foreground="black", fieldbackground="white")
        style.map("Treeview", background=[("selected", "gray")])

        # Créer un Treeview pour afficher les utilisateurs
        self.tree = ttk.Treeview(self, columns=("id_user", "nom", "prenom", "privilege"), show="headings")
        self.tree.heading("id_user", text="ID")
        self.tree.heading("nom", text="Nom")
        self.tree.heading("prenom", text="Prénom")
        self.tree.heading("privilege", text="Privilège")

        # Centrer les contenus dans les colonnes
        self.tree.column("id_user", anchor="center", width=100)
        self.tree.column("nom", anchor="center", width=150)
        self.tree.column("prenom", anchor="center", width=150)
        self.tree.column("privilege", anchor="center", width=150)

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

class RecordProductOutPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.grid(row=0, column=0, padx=20, pady=20)

        # Ajouter une barre de recherche pour chercher le produit par nom
        self.search_var = tk.StringVar()
        self.search_entry = ctk.CTkEntry(self, textvariable=self.search_var, placeholder_text="Rechercher un produit")
        self.search_entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.search_entry.bind("<KeyRelease>", self.update_product_list)

        # Ajouter un Treeview pour afficher les produits correspondants
        self.tree = ttk.Treeview(self, columns=("code", "designation", "quantite"), show="headings", height=5)
        self.tree.heading("code", text="Code")
        self.tree.heading("designation", text="Désignation")
        self.tree.heading("quantite", text="Quantité")
        self.tree.column("code", anchor="center")
        self.tree.column("designation", anchor="center")
        self.tree.column("quantite", anchor="center")
        self.tree.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.tree.bind("<<TreeviewSelect>>", self.on_product_select)

        # Ajouter un label pour afficher la quantité disponible
        ctk.CTkLabel(self, text="Quantité disponible:").grid(row=2, column=0, padx=10, pady=10)
        self.available_quantity_label = ctk.CTkLabel(self, text="")
        self.available_quantity_label.grid(row=2, column=1, padx=10, pady=10)

        # Ajouter un champ pour saisir la quantité à sortir
        ctk.CTkLabel(self, text="Quantité sortie:").grid(row=3, column=0, padx=10, pady=10)
        self.quantity_entry = ctk.CTkEntry(self)
        self.quantity_entry.grid(row=3, column=1, padx=10, pady=10)

        # Ajouter un bouton pour enregistrer la sortie
        self.record_button = ctk.CTkButton(self, text="Enregistrer la sortie", command=self.record_product_out)
        self.record_button.grid(row=4, column=0, columnspan=2, pady=10)

    def update_product_list(self, event):
        search_term = self.search_var.get().lower()
        for item in self.tree.get_children():
            self.tree.delete(item)
        conn = sqlite3.connect('pharmacie.db')
        c = conn.cursor()
        c.execute("SELECT code, designation, quantite FROM Produit WHERE LOWER(designation) LIKE ?", ('%' + search_term + '%',))
        for row in c.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

    def on_product_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            code, designation, quantite = self.tree.item(selected_item, "values")
            self.available_quantity_label.configure(text=str(quantite))
            self.selected_product_code = code

    def record_product_out(self):
        code = self.selected_product_code
        quantity = int(self.quantity_entry.get())

        conn = sqlite3.connect('pharmacie.db')
        c = conn.cursor()

        # Vérifier si le produit existe et récupérer la quantité actuelle
        c.execute("SELECT quantite FROM Produit WHERE code=?", (code,))
        result = c.fetchone()
        if result:
            current_quantity = result[0]
            if current_quantity >= quantity:
                # Mettre à jour la quantité du produit
                new_quantity = current_quantity - quantity
                c.execute("UPDATE Produit SET quantite=? WHERE code=?", (new_quantity, code))
                conn.commit()
                messagebox.showinfo("Info", "Sortie enregistrée avec succès !")
                self.update_product_list(None)  # Mettre à jour la liste des produits
            else:
                messagebox.showerror("Erreur", "Quantité insuffisante en stock.")
        else:
            messagebox.showerror("Erreur", "Produit non trouvé.")

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