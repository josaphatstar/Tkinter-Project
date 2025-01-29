import tkinter as tk
import customtkinter as ctk
from views import AddProductPage, ShowProductsPage, ShowUsersPage, RecordProductOutPage, AddUserPage
from menu import MenuBar
from login import LoginPage
from loading import LoadingPage

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Pharmacie - Interface Principale")
        self.geometry("400x300")

        # Stocker les informations de l'utilisateur connecté
        self.current_user = None

        # Afficher la page de chargement au démarrage
        self.show_loading_page()

    def show_loading_page(self):
        self.loading_page = LoadingPage(self, self)
        self.loading_page.pack(fill="both", expand=True)
        self.after(3000, self.show_login_page)  # Attendre 3 secondes avant de passer à la page de connexion

    def show_login_page(self):
        self.loading_page.pack_forget()
        self.login_page = LoginPage(self, self)
        self.login_page.pack(fill="both", expand=True)

    import tkinter as tk
import customtkinter as ctk
from views import AddProductPage, ShowProductsPage, ShowUsersPage, RecordProductOutPage, AddUserPage
from menu import MenuBar
from login import LoginPage
from loading import LoadingPage

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Pharmacie - Interface Principale")
        self.geometry("400x300")

        # Stocker les informations de l'utilisateur connecté
        self.current_user = None

        # Afficher la page de chargement au démarrage
        self.show_loading_page()

    def show_loading_page(self):
        self.loading_page = LoadingPage(self, self)
        self.loading_page.pack(fill="both", expand=True)
        self.after(3000, self.show_login_page)  # Attendre 3 secondes avant de passer à la page de connexion

    def show_login_page(self):
        self.loading_page.pack_forget()
        self.login_page = LoginPage(self, self)
        self.login_page.pack(fill="both", expand=True)

    def show_main_page(self, user):
        self.login_page.pack_forget()
        self.current_user = user

        # Créer la barre de menus
        menubar = MenuBar(self)
        self.config(menu=menubar)

        # Créer un bouton pour ajouter un produit
        self.add_product_button = ctk.CTkButton(self, text="Ajouter un produit", command=self.show_add_product_page)
        self.add_product_button.pack(pady=10)

        # Créer un bouton pour afficher les produits enregistrés
        self.show_products_button = ctk.CTkButton(self, text="Afficher les produits", command=self.show_products)
        self.show_products_button.pack(pady=10)

        # Créer un bouton pour afficher la liste des utilisateurs
        self.show_users_button = ctk.CTkButton(self, text="Afficher les utilisateurs", command=self.show_users)
        self.show_users_button.pack(pady=10)

        # Créer un bouton pour enregistrer les sorties de produits
        self.record_product_out_button = ctk.CTkButton(self, text="Enregistrer une sortie", command=self.show_record_product_out_page)
        self.record_product_out_button.pack(pady=10)

        # Créer un bouton pour ajouter un utilisateur (accessible uniquement aux administrateurs)
        if self.current_user[5] == 'Admin':  # Utiliser l'indice approprié pour accéder à 'privilege'
            self.add_user_button = ctk.CTkButton(self, text="Ajouter un utilisateur", command=self.show_add_user_page)
            self.add_user_button.pack(pady=10)

    def show_add_product_page(self):
        # Créer une nouvelle fenêtre pour la page d'ajout de produits
        add_product_window = ctk.CTkToplevel(self)
        add_product_window.title("Ajouter un produit")
        add_product_window.geometry("400x300")  # Augmenter les dimensions spécifiques

        # Ajouter la page d'ajout de produits à la nouvelle fenêtre
        add_product_page = AddProductPage(add_product_window)
        add_product_page.pack(fill="both", expand=True)

    def show_products(self):
        # Créer une nouvelle fenêtre pour afficher les produits
        show_products_window = ctk.CTkToplevel(self)
        show_products_window.title("Produits enregistrés")
        show_products_window.geometry("1000x600")  # Définir des dimensions spécifiques

        # Ajouter la page d'affichage des produits à la nouvelle fenêtre
        show_products_page = ShowProductsPage(show_products_window)
        show_products_page.pack(fill="both", expand=True)

    def show_users(self):
        # Créer une nouvelle fenêtre pour afficher les utilisateurs
        show_users_window = ctk.CTkToplevel(self)
        show_users_window.title("Utilisateurs enregistrés")
        show_users_window.geometry("600x400")  # Définir des dimensions spécifiques

        # Ajouter la page d'affichage des utilisateurs à la nouvelle fenêtre
        show_users_page = ShowUsersPage(show_users_window)
        show_users_page.pack(fill="both", expand=True)

    def show_record_product_out_page(self):
        # Créer une nouvelle fenêtre pour enregistrer les sorties de produits
        record_product_out_window = ctk.CTkToplevel(self)
        record_product_out_window.title("Enregistrer une sortie")
        record_product_out_window.geometry("600x350")  # Augmenter les dimensions spécifiques
       

        # Ajouter la page d'enregistrement des sorties à la nouvelle fenêtre
        record_product_out_page = RecordProductOutPage(record_product_out_window)
        record_product_out_page.pack(fill="both", expand=True)

    def show_add_user_page(self):
        # Créer une nouvelle fenêtre pour la page d'ajout d'utilisateurs
        add_user_window = ctk.CTkToplevel(self)
        add_user_window.title("Ajouter un utilisateur")
        add_user_window.geometry("350x350")  # Augmenter les dimensions spécifiques


        # Ajouter la page d'ajout d'utilisateurs à la nouvelle fenêtre
        add_user_page = AddUserPage(add_user_window)
        add_user_page.pack(fill="both", expand=True)

    def center_window(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
