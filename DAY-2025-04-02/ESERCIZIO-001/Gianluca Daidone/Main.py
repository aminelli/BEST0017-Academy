import csv
import re
from collections import defaultdict

# - Ottenere la lista dei film ordinata per titolo (attenzione c'è una difficoltà da gestire)
def listOrderByTitle(csv):

    def clean_title(row):
        # cerca nella colonna titolo i numeri iniziali e li rimpiazza con ''
        # lo faccio utilizzando il metodo sub del modulo re che mi permette di usare le espressioni regolari
        # esse trovano più numeri seguiti da un punto seguiti dagli spazi
        return re.sub(r'^\d+\.\s*', '', row["Title"])
    
    # ogni elemento della lista viene passato alla funzione specificata in key
    # la funzione deve restituire il valore usato per ordinare
    dati = sorted(csv, key=clean_title)

    # stampo la lista
    for row in dati:
        print(row)

# - Sapere quanti film hanno una durata >= 2h
def listByDuration(csv):

    def get_hours(duration):
        # trova il numero di ore (se presente)
        match = re.match(r"(\d+)h", duration)
        if match:
            return int(match.group(1))  # restituisce il numero di ore (group permette di accedere ai valori di match)
        return 0  # se non ci sono ore 

    count = 0
    for row in csv:
        # estrarre la durata dalla riga Duration
        duration = row["Duration"]
        
        # calcolare le ore e confrontarle con 2
        if get_hours(duration) >= 2:
            count += 1  # incrementa il contatore se la durata è >= 2 ore
            # print(row)
    
    print(f"Film con durata >= 2h: {count}")

# - Mostrare una tabella contenente il totale di film raggruppati per colonna MPA (per il significato dell'MPA vedere nota sottostante)
def listGroupByMPA(csv):
    
    # crea un dizionario che conta il numero di film per ogni valore di MPA
    # String -> int (se non esiste lo inserisce e inizializza a 0)
    mpaCount = defaultdict(int) 
    
    for row in csv:
        mpa = row["MPA"]  # estrai il valore di MPA
        if row["MPA"] == "":
            mpa = "Empty"
        mpaCount[mpa] += 1  # Incrementa il conteggio per quel valore di MPA
    
    # stampiamo il dizionario
    # items restituisce un coppia chiave valore 
    for key, value in mpaCount.items():
        print(f"{key}\t\t\t{value}")

# - Mostrare i film che hanno avuto un rating superiore a 7.5
def listByRating(csv):

    for row in csv:
        # estrai il rating e lo convertiamo in float
        rating = 0
        if row["Rating"] != '': # alcuni non hanno il rating
            rating = float(row["Rating"])  
        # controlla se il rating è maggiore di 7.5
        if rating > 7.5:
            print(row)

    
# antonio.minelli@etlforma.com

# - Leggere il contenuto del file imdb_movies_2024.csv
# apro il file CSV 'imdb_movies_2024.csv' in modalità lettura con encoding 'utf-8'
with open('imdb_movies_2024.csv', newline="", encoding='utf-8') as csv_file:

    # creo un oggetto csv.DictReader che permette di leggere il file CSV come un dizionario
    # la riga prima riga del CSV viene usata come chiavi del dizionario
    # il delimitatore dei campi è la virgola
    csv_reader = csv.DictReader(csv_file, delimiter = ",")

    #listOrderByTitle(csv_reader)
    #listByDuration(csv_reader)
    listGroupByMPA(csv_reader)
    #listByRating(csv_reader)

print('fine programma')