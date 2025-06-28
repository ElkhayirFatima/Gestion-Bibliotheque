import matplotlib.pyplot as plt
from collections import Counter
import csv
from datetime import datetime, timedelta

def genre_pie_chart(biblio):
    genres = [livre.genre for livre in biblio.livres.values()]
    compteur = Counter(genres)

    plt.figure(figsize=(6, 6))
    plt.pie(compteur.values(), labels=compteur.keys(), autopct='%1.1f%%', startangle=90)
    plt.title("Répartition des livres par genre")
    plt.axis("equal")
    plt.show()

def top_auteurs_histogramme(biblio):
    auteurs = [livre.auteur for livre in biblio.livres.values()]
    top = Counter(auteurs).most_common(10)

    noms = [auteur for auteur, _ in top]
    quantites = [nb for _, nb in top]

    plt.figure(figsize=(10, 6))
    plt.bar(noms, quantites, color='skyblue')
    plt.title("Top 10 des auteurs les plus présents")
    plt.xlabel("Auteur")
    plt.ylabel("Nombre de livres")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def courbe_emprunts_30jours():
    dates = []
    try:
        with open("data/historique.csv", "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["action"] == "emprunt":
                    date_action = row.get("date")  # On suppose qu'il y a une colonne date au format 'YYYY-MM-DD'
                    if date_action:
                        dates.append(datetime.strptime(date_action, "%Y-%m-%d"))
    except FileNotFoundError:
        print("Fichier historique non trouvé.")
        return

    today = datetime.today()
    last_30_days = [today - timedelta(days=i) for i in range(29, -1, -1)]  # 30 jours dans l'ordre croissant
    daily_counts = {day.date(): 0 for day in last_30_days}

    for d in dates:
        d_date = d.date()
        if d_date in daily_counts:
            daily_counts[d_date] += 1

    jours = list(daily_counts.keys())
    valeurs = list(daily_counts.values())

    plt.figure(figsize=(10, 5))
    plt.plot(jours, valeurs, marker='o', linestyle='-')
    plt.title("Activité d'emprunts - 30 derniers jours")
    plt.xlabel("Date")
    plt.ylabel("Nombre d'emprunts")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)
    plt.show()
