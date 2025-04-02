import pandas as pd
import re #libreria per le espressioni regolari

#metto in path_file il file csv
path_file = "imdb_movies_2024.csv"

#carico il file csv contenuto in path_file in un data_frame
data_frame = pd.read_csv(path_file)

#prova del print per vedere se mi ha letto il file
#print(data_frame.head())

#lascio spazio per rendere più leggibile il codice nella console
print("\n")

def no_number_in_title(title):
    # Rimuove il numero iniziale prima del titolo
    return re.sub(r'^\d+\.\s', '', title)  

# Creiamo una nuova colonna con i titoli nuovi senza numero
data_frame["Title without number"] = data_frame["Title"].apply(no_number_in_title)

# Ordinare i film in base al nuovo titolo
data_frame_sorted = data_frame.sort_values("Title without number")

# Stampo tutti i titoli in una lista
#print(data_frame_sorted["Title without number"].tolist())

for title in data_frame_sorted["Title without number"]:
    print(title)

#lascio spazio per rendere più leggibile il codice nella console
print("\n")

# Funzione per convertire la durata in minuti
def duration_to_minutes(duration):
    
    '''
        (\d+)h -> cerca un num seguito da h, come 2h ad esempio
        \s* -> prende eventuali spazi dopo h
        ? -> Rende la parte opzionale (es. "45m" senza ore è valido).
        (\d+)m -> Cerca un numero seguito da "m" (es. "15m").
    '''
    match = re.match(r'(?:(\d+)h\s*)?(?:(\d+)m)?', str(duration))  
    if match:
        hours = int(match.group(1)) if match.group(1) else 0  # Se c'è "h", converti in intero, altrimenti 0
        minutes = int(match.group(2)) if match.group(2) else 0  # Se c'è "m", converti in intero, altrimenti 0
        return hours * 60 + minutes
    
    return 0  # Se non c'è un valore valido, restituisce 0

# Applicare la funzione alla colonna Duration
data_frame["Duration Minutes"] = data_frame["Duration"].apply(duration_to_minutes)

'''
    fa un filtro su un DataFrame pandas (data_frame), restituendo un nuovo DataFrame 
    con le righe che soddisfano la condizione Duration Minutes >= 120.
'''
long_movies = data_frame[data_frame["Duration Minutes"] >= 120]

# Stampare il numero di film con durata >= 2 ore
print(f"Numero di film con durata >= 2 ore: {len(long_movies)}")

#lascio spazio per rendere più leggibile il codice nella console
print("\n")

# 4. Contare i film per classificazione MPA
'''
    value_counts() Conta il numero di occorrenze per ciascun valore presente nella colonna "MPA".
    .reset_index()Trasforma questa la series che si ottiene in un DataFrame.
'''
mpa_counts = data_frame["MPA"].value_counts().reset_index()

'''
    data frame mpa_count ha 2 colonne (i valori di MPA e colonna di conteggio)
    alla colonna di conteggio viene assegnato un nome generico per cui lo imposto io a Total Movies
'''
mpa_counts.columns = ["MPA", "Total Movies"]
print("Totale film per MPA:\n", mpa_counts)

#lascio spazio per rendere più leggibile il codice nella console
print("\n")

# Convertire la colonna Rating in numerico (ignora errori se presenti)
data_frame["Rating"] = pd.to_numeric(data_frame["Rating"], errors="coerce")

# Filtrare i film con rating > 7.5
high_rating_movies = data_frame[data_frame["Rating"] > 7.5]

# Stampare i film con rating richiesto 
# print(high_rating_movies[["Title without number", "Rating"]]) non stampa tutti i film perchè sono tanti

#salvo i film in un nuovo file csv
#high_rating_movies[["Title without number", "Rating"]].to_csv("high_rating_movies.csv", index=False)

#lascio spazio per rendere più leggibile il codice nella console
print("\n")

# Stampo i film con rating richiesto con un toString
print(high_rating_movies[["Title without number", "Rating"]].to_string())  




print("\n")
print("END Program...")