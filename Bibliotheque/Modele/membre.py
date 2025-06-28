class Membre:
    def __init__(self, membre_id, nom):
        self.id = membre_id
        self.nom = nom
        self.livres_empruntes = []

    def emprunter(self, isbn):
        if isbn not in self.livres_empruntes:
            self.livres_empruntes.append(isbn)

    def retourner(self, isbn):
        if isbn in self.livres_empruntes:
            self.livres_empruntes.remove(isbn)

    def __str__(self):
        return f"{self.nom} (ID: {self.id})"
