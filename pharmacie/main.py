import tkinter as tk
import customtkinter as ctk
from views import AddProductPage, ShowProductsPage, ShowUsersPage
from menu import MenuBar
from login import LoginPage
from loading import LoadingPage

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Pharmacie - Interface Principale")
        self.geometry("400x300")

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

    def show_main_page(self):
        self.login_page.pack_forget()

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

    def show_add_product_page(self):
        # Créer une nouvelle fenêtre pour la page d'ajout de produits
        add_product_window = ctk.CTkToplevel(self)
        add_product_window.title("Ajouter un produit")
        add_product_window.geometry("400x300")
        add_product_window.transient(self)  # Rendre la fenêtre modale
        add_product_window.grab_set()  # Empêcher l'interaction avec la fenêtre principale

        # Ajouter la page d'ajout de produits à la nouvelle fenêtre
        add_product_page = AddProductPage(add_product_window)
        add_product_page.pack(fill="both", expand=True)

    def show_products(self):
        # Créer une nouvelle fenêtre pour afficher les produits
        show_products_window = ctk.CTkToplevel(self)
        show_products_window.title("Produits enregistrés")
        show_products_window.geometry("800x600")  # Définir des dimensions spécifiques
        show_products_window.transient(self)  # Rendre la fenêtre modale
        show_products_window.grab_set()  # Empêcher l'interaction avec la fenêtre principale

        # Ajouter la page d'affichage des produits à la nouvelle fenêtre
        show_products_page = ShowProductsPage(show_products_window)
        show_products_page.pack(fill="both", expand=True)

    def show_users(self):
        # Créer une nouvelle fenêtre pour afficher les utilisateurs
        show_users_window = ctk.CTkToplevel(self)
        show_users_window.title("Utilisateurs enregistrés")
        show_users_window.geometry("800x600")  # Définir des dimensions spécifiques
        show_users_window.transient(self)  # Rendre la fenêtre modale
        show_users_window.grab_set()  # Empêcher l'interaction avec la fenêtre principale

        # Ajouter la page d'affichage des utilisateurs à la nouvelle fenêtre
        show_users_page = ShowUsersPage(show_users_window)
        show_users_page.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()