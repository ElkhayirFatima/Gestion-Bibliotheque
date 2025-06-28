import os
import csv
from datetime import datetime
from Modele.livre import Livre
from Modele.membre import Membre
from Exception.exceptions import *


class Bibliotheque:
    def __init__(self):
        self.livres = {}
        self.membres = {}
        self.historique = []

        # Créer le dossier 'data' s'il n'existe pas
        if not os.path.exists("../data"):
            os.makedirs("../data")

    def ajouter_livre(self, livre):
        self.livres[livre.isbn] = livre

    def supprimer_livre(self, isbn):
        if isbn in self.livres:
            del self.livres[isbn]
        else:
            raise LivreInexistantError(f"Livre {isbn} introuvable.")

    def enregistrer_membre(self, membre):
        self.membres[membre.id] = membre

    def supprimer_membre(self, id_membre):
        if id_membre in self.membres:
            del self.membres[id_membre]
        else:
            raise MembreInexistantError(f"Membre {id_membre} introuvable.")

    def emprunter_livre(self, membre_id, isbn):
        if membre_id not in self.membres:
            raise MembreInexistantError(f"Membre {membre_id} non trouvé.")
        if isbn not in self.livres:
            raise LivreInexistantError(f"Livre {isbn} non trouvé.")

        livre = self.livres[isbn]
        membre = self.membres[membre_id]

        if livre.statut != "disponible":
            raise LivreIndisponibleError()
        if len(membre.livres_empruntes) >= 3:
            raise QuotaEmpruntDepasseError()

        membre.emprunter(isbn)
        livre.statut = "emprunté"
        date_actuelle = datetime.now().strftime("%Y-%m-%d")
        self.historique.append((date_actuelle, "emprunt", isbn, membre_id))
    def retourner_livre(self, membre_id, isbn):
        if membre_id not in self.membres:
            raise MembreInexistantError(f"Membre {membre_id} introuvable.")
        if isbn not in self.livres:
            raise LivreInexistantError(f"Livre {isbn} introuvable.")

        membre = self.membres[membre_id]
        membre.retourner(isbn)
        self.livres[isbn].statut = "disponible"
        date_actuelle = datetime.now().strftime("%Y-%m-%d")
        self.historique.append((date_actuelle, "retour", isbn, membre_id))

    def sauvegarder_donnees(self):
        with open("../data/livres.txt", "w", encoding="utf-8") as f:
            for livre in self.livres.values():
                ligne = ";".join([
                    livre.isbn, livre.titre, livre.auteur,
                    str(livre.annee), livre.genre, livre.statut
                ])
                f.write(ligne + "\n")

        with open("../data/membres.txt", "w", encoding="utf-8") as f:
            for membre in self.membres.values():
                livres_empruntes = ",".join(membre.livres_empruntes)
                f.write(f"{membre.id};{membre.nom};{livres_empruntes}\n")

        with open("../data/historique.csv", "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "action", "isbn", "id_membre"])
            writer.writerows(self.historique)

    def charger_donnees(self):
        try:
            with open("../data/livres.txt", "r", encoding="utf-8") as f:
                first_line = True
                for line in f:
                    if first_line:
                        # Ignorer la ligne d'en-tête si elle contient "annee"
                        if "annee" in line.lower():
                            first_line = False
                            continue
                    first_line = False
                    isbn, titre, auteur, annee, genre, statut = line.strip().split(";")
                    self.ajouter_livre(Livre(isbn, titre, auteur, int(annee), genre, statut))
        except FileNotFoundError:
            pass

        try:
            with open("../data/membres.txt", "r", encoding="utf-8") as f:
                first_line = True
                for line in f:
                    if first_line:
                        # Ignorer la ligne d'en-tête si elle contient "id"
                        if "id" in line.lower():
                            first_line = False
                            continue
                    first_line = False
                    membre_id, nom, livres_str = line.strip().split(";")
                    membre = Membre(membre_id, nom)
                    if livres_str:
                        membre.livres_empruntes = livres_str.split(",")
                    self.enregistrer_membre(membre)
        except FileNotFoundError:
            pass

        try:
            with open("../data/historique.csv", "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)  # Utiliser DictReader
                for row in reader:
                    self.historique.append((
                        row["date"],
                        row["action"],
                        row["isbn"],
                        row["id_membre"]  # Corrigé ici
                    ))
        except FileNotFoundError:
            pass