import tkinter as tk

from tkinter import ttk, messagebox, filedialog
from Modele.livre import Livre
from Modele.bibliotheque import Bibliotheque
from Modele.membre import Membre
from rapports.statistiques import genre_pie_chart, top_auteurs_histogramme, courbe_emprunts_30jours
import csv

biblio = Bibliotheque()
biblio.charger_donnees()


fenetre = tk.Tk()
fenetre.title("📚 Système de Gestion de Bibliothèque")
fenetre.geometry("960x680")
fenetre.configure(bg="#f0f2f5")
fenetre.resizable(False, False)

onglets = ttk.Notebook(fenetre)
onglets.pack(expand=True, fill='both', padx=10, pady=10)


# Vider champs livre
def vider_champs_livre():
    entry_isbn.delete(0, tk.END)
    entry_titre.delete(0, tk.END)
    entry_auteur.delete(0, tk.END)
    entry_annee.delete(0, tk.END)
    entry_genre.delete(0, tk.END)

# Vider champs membre
def vider_champs_membre():
    entry_id_membre.delete(0, tk.END)
    entry_nom_membre.delete(0, tk.END)

# ----------- Gestion Livres --------------------

def ajouter_livre():
    isbn = entry_isbn.get()
    titre = entry_titre.get()
    auteur = entry_auteur.get()
    annee = entry_annee.get()
    genre = entry_genre.get()

    if not isbn or not titre or not auteur or not annee or not genre:
        messagebox.showerror("Erreur", "Tous les champs sont obligatoires.")
        return
    try:
        annee_int = int(annee)
    except ValueError:
        messagebox.showerror("Erreur", "L'année doit être un nombre.")
        return

    nouveau_livre = Livre(isbn, titre, auteur, annee_int, genre)
    biblio.ajouter_livre(nouveau_livre)
    biblio.sauvegarder_donnees()
    messagebox.showinfo("Succès", f"Livre '{titre}' ajouté avec succès.")
    vider_champs_livre()
    afficher_livres()

def supprimer_livre():
    selected = tree_livres.selection()
    if not selected:
        messagebox.showwarning("Attention", "Veuillez sélectionner un livre à supprimer.")
        return
    isbn = tree_livres.item(selected[0])['values'][0]
    confirm = messagebox.askyesno("Confirmer", f"Supprimer le livre ISBN {isbn} ?")
    if confirm:
        try:
            biblio.supprimer_livre(isbn)
            biblio.sauvegarder_donnees()
            afficher_livres()
            messagebox.showinfo("Succès", f"Livre {isbn} supprimé.")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))


def modifier_livre():
    isbn = entry_isbn.get()
    if isbn not in biblio.livres:
        messagebox.showerror("Erreur", "Livre non trouvé pour modification.")
        return

    titre = entry_titre.get()
    auteur = entry_auteur.get()
    annee = entry_annee.get()
    genre = entry_genre.get()

    if not titre or not auteur or not annee or not genre:
        messagebox.showerror("Erreur", "Tous les champs sont obligatoires.")
        return

    try:
        annee_int = int(annee)
    except ValueError:
        messagebox.showerror("Erreur", "L'année doit être un nombre.")
        return

    livre = biblio.livres[isbn]
    livre.titre = titre
    livre.auteur = auteur
    livre.annee = annee_int
    livre.genre = genre

    biblio.sauvegarder_donnees()
    messagebox.showinfo("Succès", f"Livre '{titre}' modifié avec succès.")
    vider_champs_livre()
    afficher_livres()


def afficher_livres(filtre=""):
    filtre = filtre.lower()
    for i in tree_livres.get_children():
        tree_livres.delete(i)
    for livre in biblio.livres.values():
        # Filtrer par titre ou auteur
        if filtre in livre.titre.lower() or filtre in livre.auteur.lower():
            tree_livres.insert("",tk.END, values=(
                livre.isbn, livre.titre, livre.auteur, livre.annee, livre.genre, livre.statut
            ))

def remplir_formulaire_livre(event):
    selected = tree_livres.selection()
    if selected:
        item = tree_livres.item(selected[0])
        vals = item['values']
        entry_isbn.delete(0, tk.END)
        entry_isbn.insert(0, vals[0])
        entry_titre.delete(0, tk.END)
        entry_titre.insert(0, vals[1])
        entry_auteur.delete(0, tk.END)
        entry_auteur.insert(0, vals[2])
        entry_annee.delete(0, tk.END)
        entry_annee.insert(0, vals[3])
        entry_genre.delete(0, tk.END)
        entry_genre.insert(0, vals[4])
def rechercher_livre(event=None):
    texte = entry_recherche_livre.get()
    afficher_livres(texte)

def export_livres_csv():
    path = filedialog.asksaveasfilename(defaultextension=".csv",
                                        filetypes=[("CSV files", "*.csv")])
    if path:
        try:
            with open(path, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["ISBN", "Titre", "Auteur", "Année", "Genre", "Statut"])
                for livre in biblio.livres.values():
                    writer.writerow([livre.isbn, livre.titre, livre.auteur, livre.annee, livre.genre, livre.statut])
            messagebox.showinfo("Succès", f"Livres exportés vers {path}")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

# ----------- Gestion Membres -------------------

def ajouter_membre():
    id_membre = entry_id_membre.get()
    nom_membre = entry_nom_membre.get()

    if not id_membre or not nom_membre:
        messagebox.showerror("Erreur", "Tous les champs sont obligatoires.")
        return

    if id_membre in biblio.membres:
        messagebox.showerror("Erreur", "Ce membre existe déjà.")
        return

    nouveau_membre = Membre(id_membre, nom_membre)
    biblio.enregistrer_membre(nouveau_membre)
    biblio.sauvegarder_donnees()
    messagebox.showinfo("Succès", f"Membre '{nom_membre}' ajouté avec succès.")
    vider_champs_membre()
    afficher_membres()

def supprimer_membre():
    selected = tree_membres.selection()
    if not selected:
        messagebox.showwarning("Attention", "Veuillez sélectionner un membre à supprimer.")
        return
    id_membre = tree_membres.item(selected[0])['values'][0]
    confirm = messagebox.askyesno("Confirmer", f"Supprimer le membre ID {id_membre} ?")
    if confirm:
        try:
            biblio.supprimer_membre(id_membre)
            biblio.sauvegarder_donnees()
            afficher_membres()
            messagebox.showinfo("Succès", f"Membre {id_membre} supprimé.")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

def afficher_membres(filtre=""):
    filtre = filtre.lower()
    for i in tree_membres.get_children():
        tree_membres.delete(i)
    for membre in biblio.membres.values():
        if filtre in membre.nom.lower():
            tree_membres.insert("", tk.END, values=(membre.id, membre.nom))

def rechercher_membre(event=None):
    texte = entry_recherche_membre.get()
    afficher_membres(texte)

def export_membres_csv():
    path = filedialog.asksaveasfilename(defaultextension=".csv",
                                        filetypes=[("CSV files", "*.csv")])
    if path:
        try:
            with open(path, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Nom"])
                for membre in biblio.membres.values():
                    writer.writerow([membre.id, membre.nom])
            messagebox.showinfo("Succès", f"Membres exportés vers {path}")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

# ----------- Gestion Emprunts / Retours ----------

def emprunter():
    id_membre = entry_emprunt_id.get()
    isbn = entry_emprunt_isbn.get()
    try:
        biblio.emprunter_livre(id_membre, isbn)
        biblio.sauvegarder_donnees()
        messagebox.showinfo("Succès", f"Livre {isbn} emprunté par membre {id_membre}.")
        afficher_livres()
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def retourner():
    id_membre = entry_emprunt_id.get()
    isbn = entry_emprunt_isbn.get()
    try:
        biblio.retourner_livre(id_membre, isbn)
        biblio.sauvegarder_donnees()
        messagebox.showinfo("Succès", f"Livre {isbn} retourné par membre {id_membre}.")
        afficher_livres()
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

# ----------- Création Fenêtre et Widgets -------------

fenetre.title("Système de Gestion de Bibliothèque")
fenetre.geometry("900x650")
fenetre.resizable(False, False)

onglets = ttk.Notebook(fenetre)
onglets.pack(expand=True, fill='both')

# --- Onglet Livres ---
onglet_livres = ttk.Frame(onglets)
onglets.add(onglet_livres, text="Livres")

# Formulaire livres
frame_form_livres = ttk.Frame(onglet_livres)
frame_form_livres.pack(padx=10, pady=10, fill='x')

ttk.Label(frame_form_livres, text="ISBN").grid(row=0, column=0, sticky='w')
entry_isbn = ttk.Entry(frame_form_livres)
entry_isbn.grid(row=0, column=1, sticky='ew')

ttk.Label(frame_form_livres, text="Titre").grid(row=1, column=0, sticky='w')
entry_titre = ttk.Entry(frame_form_livres)
entry_titre.grid(row=1, column=1, sticky='ew')

ttk.Label(frame_form_livres, text="Auteur").grid(row=2, column=0, sticky='w')
entry_auteur = ttk.Entry(frame_form_livres)
entry_auteur.grid(row=2, column=1, sticky='ew')

ttk.Label(frame_form_livres, text="Année").grid(row=3, column=0, sticky='w')
entry_annee = ttk.Entry(frame_form_livres)
entry_annee.grid(row=3, column=1, sticky='ew')

ttk.Label(frame_form_livres, text="Genre").grid(row=4, column=0, sticky='w')
entry_genre = ttk.Entry(frame_form_livres)
entry_genre.grid(row=4, column=1, sticky='ew')

btn_ajouter_livre = ttk.Button(frame_form_livres, text="Ajouter Livre", command=ajouter_livre)
btn_ajouter_livre.grid(row=5, column=0, pady=10)

btn_modifier_livre = ttk.Button(frame_form_livres, text="Modifier Livre", command=modifier_livre)
btn_modifier_livre.grid(row=5, column=1, pady=10)


# Recherche livres
frame_recherche_livres = ttk.Frame(onglet_livres)
frame_recherche_livres.pack(padx=10, pady=5, fill='x')

ttk.Label(frame_recherche_livres, text="Recherche (Titre / Auteur) :").pack(side='left')
entry_recherche_livre = ttk.Entry(frame_recherche_livres)
entry_recherche_livre.pack(side='left', fill='x', expand=True, padx=5)
entry_recherche_livre.bind("<KeyRelease>", rechercher_livre)

btn_supprimer_livre = ttk.Button(frame_recherche_livres, text="Supprimer Livre", command=supprimer_livre)
btn_supprimer_livre.pack(side='right', padx=5)

btn_export_livres = ttk.Button(frame_recherche_livres, text="Exporter CSV", command=export_livres_csv)
btn_export_livres.pack(side='right')

# Table livres
columns_livres = ("ISBN", "Titre", "Auteur", "Année", "Genre", "Statut")
tree_livres = ttk.Treeview(onglet_livres, columns=columns_livres, show='headings')
for col in columns_livres:
    tree_livres.heading(col, text=col)
    tree_livres.column(col, width=100)
tree_livres.pack(expand=True, fill='both', padx=10, pady=10)
tree_livres.bind("<<TreeviewSelect>>", remplir_formulaire_livre)
afficher_livres()

# --- Onglet Membres ---
onglet_membres = ttk.Frame(onglets)
onglets.add(onglet_membres, text="👥 Membres")

frame_form_membres = ttk.Frame(onglet_membres)
frame_form_membres.pack(padx=10, pady=10, fill='x')

ttk.Label(frame_form_membres, text="ID Membre").grid(row=0, column=0, sticky='w')
entry_id_membre = ttk.Entry(frame_form_membres)
entry_id_membre.grid(row=0, column=1, sticky='ew')

ttk.Label(frame_form_membres, text="Nom").grid(row=1, column=0, sticky='w')
entry_nom_membre = ttk.Entry(frame_form_membres)
entry_nom_membre.grid(row=1, column=1, sticky='ew')

btn_ajouter_membre = ttk.Button(frame_form_membres, text="Ajouter Membre", command=ajouter_membre)
btn_ajouter_membre.grid(row=2, column=0, columnspan=2, pady=10)

# Recherche membres
frame_recherche_membres = ttk.Frame(onglet_membres)
frame_recherche_membres.pack(padx=10, pady=5, fill='x')

ttk.Label(frame_recherche_membres, text="Recherche (Nom) :").pack(side='left')
entry_recherche_membre = ttk.Entry(frame_recherche_membres)
entry_recherche_membre.pack(side='left', fill='x', expand=True, padx=5)
entry_recherche_membre.bind("<KeyRelease>", rechercher_membre)

btn_supprimer_membre = ttk.Button(frame_recherche_membres, text="Supprimer Membre", command=supprimer_membre)
btn_supprimer_membre.pack(side='right', padx=5)

btn_export_membres = ttk.Button(frame_recherche_membres, text="Exporter CSV", command=export_membres_csv)
btn_export_membres.pack(side='right')

# Table membres
columns_membres = ("ID", "Nom")
tree_membres = ttk.Treeview(onglet_membres, columns=columns_membres, show="headings")
for col in columns_membres:
    tree_membres.heading(col, text=col)
    tree_membres.column(col, width=150)
tree_membres.pack(expand=True, fill='both', padx=10, pady=10)

afficher_membres()

# --- Onglet Statistiques ---
onglet_statistiques = ttk.Frame(onglets)
onglets.add(onglet_statistiques, text="Statistiques")

btn_pie = tk.Button(onglet_statistiques, text="Diagramme circulaire (Genres)", command=lambda: genre_pie_chart(biblio))
btn_pie.pack(pady=10)

btn_hist = tk.Button(onglet_statistiques, text="Top 10 Auteurs", command=lambda: top_auteurs_histogramme(biblio))
btn_hist.pack(pady=10)

btn_courbe = tk.Button(onglet_statistiques, text="Activité 30 derniers jours", command=courbe_emprunts_30jours)
btn_courbe.pack(pady=10)

# --- Onglet Emprunts / Retours ---
onglet_emprunts = ttk.Frame(onglets)
onglets.add(onglet_emprunts, text="Emprunts / Retours")

frame_emprunt = ttk.Frame(onglet_emprunts)
frame_emprunt.pack(padx=20, pady=20)

ttk.Label(frame_emprunt, text="ID Membre").grid(row=0, column=0, sticky="w")
entry_emprunt_id = ttk.Entry(frame_emprunt)
entry_emprunt_id.grid(row=0, column=1)

ttk.Label(frame_emprunt, text="ISBN Livre").grid(row=1, column=0, sticky="w")
entry_emprunt_isbn = ttk.Entry(frame_emprunt)
entry_emprunt_isbn.grid(row=1, column=1)

btn_emprunter = ttk.Button(frame_emprunt, text="Emprunter", command=emprunter)
btn_emprunter.grid(row=2, column=0, pady=10)

btn_retourner = ttk.Button(frame_emprunt, text="Retourner", command=retourner)
btn_retourner.grid(row=2, column=1, pady=10)

# --- Lancer la fenêtre ---
fenetre.mainloop()
