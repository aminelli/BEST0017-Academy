import pandas as pd
import seaborn as sns

# leggo il csv tramite pandas
data = pd.read_csv("imdb_movies_2024.csv")

# controllo che tutto sia caricato correttamente
print(data.head(5))

# creo una funzione per rimuovere il numero iniziale
# splitto in base allo spazio e restituisco dal secondo elemento in poi
def clean_title(title):
    return " ".join(title.split(" ")[1:]) if isinstance(title, str) else title

# applico la funzione alla colonna "Title"
data["Title"] = data["Title"].apply(clean_title)

# ordino in base al titolo
data.sort_values(by="Title", inplace=True)

# controllo i risultati
print(data.head(5))

# creo la lista con i titoli dei film
lista_titoli = data["Title"].tolist()
print(lista_titoli)


# creo una funzione che mi permette di pulire "Duration" e trasformare in minuti
def hours_to_minutes(duration) :
    if isinstance(duration, float):  # se duration è float, restituisce direttamente i minuti
        return duration
    
    hours = 0
    minutes = 0
    if "h" in duration:
        hours = int(duration.split("h")[0]) # splitto in base ad "h" e ottengo il numero delle ore
    if "m" in duration:
        minutes = int(duration.split("m")[0].split()[-1]) #prima splitto in base alla "m" e poi in base allo spazio perché la duration è 1h 36m
    return hours * 60 + minutes

# creo una colonna in cui trasformo le ore in minuti
data["Minutes"] = data["Duration"].apply(hours_to_minutes)

print(data.head(5))

# creo un subset con i film che durano almeno 2 ore
film_2h = data[data["Minutes"] >= 120]
print("Numero di film con durata di almeno 2 ore: " , len(film_2h))

# frequenze assolute MPA
print(data.MPA.value_counts())

# creo un subset relativo ad MPA e calcolo la durata media dei film per MPA
MPA_duration = data.groupby("MPA", as_index = False)["Minutes"].mean().round(2)
MPA_duration.columns = ["MPA", "avg_minutes"]
print(MPA_duration)

# mostro graficamente
sns.barplot(x = "MPA", y = "avg_minutes", data = MPA_duration, palette = "deep")

# film con rating > 7.5
films_high_rating = data[data["Rating"] > 7.5]
print(films_high_rating)

# salvo il nuovo file con le modifiche effettuate
data.to_csv("movies_clean.csv", index = False)
print("\nFine Esercizio")