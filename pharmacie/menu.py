import tkinter as tk
from tkinter import messagebox

class MenuBar(tk.Menu):
    def __init__(self, parent):
        super().__init__(parent)

        # Créer le menu "File"
        file_menu = tk.Menu(self, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=parent.quit)
        self.add_cascade(label="File", menu=file_menu)

        # Créer le menu "Edit"
        edit_menu = tk.Menu(self, tearoff=0)
        edit_menu.add_command(label="Undo", command=self.undo)
        edit_menu.add_command(label="Redo", command=self.redo)
        self.add_cascade(label="Edit", menu=edit_menu)

    def new_file(self):
        messagebox.showinfo("New File", "New File command executed")

    def open_file(self):
        messagebox.showinfo("Open File", "Open File command executed")

    def save_file(self):
        messagebox.showinfo("Save File", "Save File command executed")

    def undo(self):
        messagebox.showinfo("Undo", "Undo command executed")

    def redo(self):
        messagebox.showinfo("Redo", "Redo command executed")