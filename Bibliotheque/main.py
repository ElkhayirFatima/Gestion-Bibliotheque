from Modele.bibliotheque import Bibliotheque
from Modele.livre import Livre
from Modele.membre import Membre
from rapports.statistiques import genre_pie_chart

biblio = Bibliotheque()
biblio.charger_donnees()

def afficher_menu():
    print("\n=== GESTION BIBLIOTHÈQUE ===")
    print("1. Ajouter un livre")
    print("2. Inscrire un membre")
    print("3. Emprunter un livre")
    print("4. Rendre un livre")
    print("5. Lister tous les livres")
    print("6. Afficher les statistiques")
    print("7. Sauvegarder et quitter")

while True:
    afficher_menu()
    choix = input("Entrez votre choix : ")

    if choix == "1":
        isbn = input("ISBN : ")
        titre = input("Titre : ")
        auteur = input("Auteur : ")
        annee = int(input("Année : "))
        genre = input("Genre : ")
        livre = Livre(isbn, titre, auteur, annee, genre)
        biblio.ajouter_livre(livre)
        print("Livre ajouté avec succès.")

    elif choix == "2":
        membre_id = input("ID du membre : ")
        nom = input("Nom : ")
        biblio.enregistrer_membre(Membre(membre_id, nom))
        print("Membre inscrit avec succès.")

    elif choix == "3":
        membre_id = input("ID du membre : ")
        isbn = input("ISBN du livre : ")
        try:
            biblio.emprunter_livre(membre_id, isbn)
            print("Livre emprunté avec succès.")
        except Exception as e:
            print(f"Erreur : {e}")

    elif choix == "4":
        membre_id = input("ID du membre : ")
        isbn = input("ISBN du livre : ")
        try:
            biblio.retourner_livre(membre_id, isbn)
            print("Livre retourné avec succès.")
        except Exception as e:
            print(f"Erreur : {e}")

    elif choix == "5":
        print("\nListe des livres :")
        for livre in biblio.livres.values():
            print(f"{livre.isbn} | {livre.titre} | {livre.auteur} | {livre.annee} | {livre.genre} | {livre.statut}")

    elif choix == "6":
        genre_pie_chart(biblio)

    elif choix == "7":
        biblio.sauvegarder_donnees()
        print("Données sauvegardées. Au revoir !")
        break

    else:
        print("Choix invalide. Réessayez.")
