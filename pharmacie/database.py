import sqlite3

# Étape 1: Créer ou ouvrir le fichier de base de données SQLite
conn = sqlite3.connect('pharmacie.db')
c = conn.cursor()

# Étape 2: Création des tables

# Table Utilisateur
c.execute('''
CREATE TABLE IF NOT EXISTS Utilisateur (
    id_user INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    login TEXT UNIQUE NOT NULL,
    mot_de_passe TEXT NOT NULL,
    privilege TEXT CHECK(privilege IN ('Admin', 'Pharmacien')) NOT NULL,
    first_login INTEGER DEFAULT 1
)
''')

# Table Produit
c.execute('''
CREATE TABLE IF NOT EXISTS Produit (
    code INTEGER PRIMARY KEY AUTOINCREMENT,
    designation TEXT NOT NULL,
    quantite INTEGER NOT NULL CHECK(quantite >= 0),
    date_expiration DATE NOT NULL
)
''')

# Table Historique
c.execute('''
CREATE TABLE IF NOT EXISTS Historique (
    id_historique INTEGER PRIMARY KEY AUTOINCREMENT,
    utilisateur_id INTEGER NOT NULL,
    action_type TEXT CHECK(action_type IN ('Ajout', 'Modification', 'Suppression')) NOT NULL,
    produit_id TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (utilisateur_id) REFERENCES Utilisateur(id_user),
    FOREIGN KEY (produit_id) REFERENCES Produit(code)
)
''')

print("Tables créées avec succès !")

# Étape 3: Insérer un utilisateur administrateur par défaut
try:
    c.execute('''
    INSERT INTO Utilisateur (nom, prenom, login, mot_de_passe, privilege)
    VALUES ('Admin', 'Super', 'admin', 'admin123', 'Admin')
    ''')
    print("Administrateur par défaut ajouté avec succès !")
except sqlite3.IntegrityError:
    print("L'utilisateur administrateur existe déjà.")

# Sauvegarder les changements et fermer la connexion
conn.commit()
conn.close()