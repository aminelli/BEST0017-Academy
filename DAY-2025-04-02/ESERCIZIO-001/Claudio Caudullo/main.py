import pandas as pd  # Importa la libreria pandas per la gestione dei dati
import re  # Importa la libreria re per la manipolazione di stringhe con espressioni regolari

# Leggere il contenuto del file CSV
df_original = pd.read_csv("imdb_movies_2024.csv")  # Carica il file CSV in un DataFrame di pandas


df = pd.read_csv("imdb_movies_2024.csv") 

def convert_duration(duration):  # Definisce una funzione per convertire la durata in minuti
    if isinstance(duration, str):  # Controlla se il valore della durata è una stringa
        match = re.match(r'(\d+)h\s*(\d*)m?', duration)  # Usa espressioni regolari per estrarre ore e minuti
        if match:  # Se la durata corrisponde al formato atteso
            hours = int(match.group(1))  # Estrai il valore delle ore
            minutes = int(match.group(2)) if match.group(2) else 0  # Estrai i minuti (se presenti, altrimenti 0)
            return hours * 60 + minutes  # Converte la durata totale in minuti
    return None  # Restituisce None per valori non validi

def initDF():
    global df
    df = pd.read_csv("imdb_movies_2024.csv")  # Carica il file CSV in un DataFrame di pandas
    # Rimuovere il numero di riga dai titoli, eventuali spazi bianchi prima e dopo
    df['Title'] = df['Title'].apply(lambda x: re.sub(r'^\d+\.\s*', '', str(x).strip()))  

    df['Duration'] = df['Duration'].astype(str).apply(convert_duration)  # Applica la funzione di conversione alla colonna della durata

    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')  # Converte la colonna del rating in valori numerici


initDF()

def save_to_csv():  # Funzione per salvare il DataFrame aggiornato nel file CSV
    df_original.to_csv("imdb_movies_2024.csv", index=False)  # Salva il DataFrame nel file CSV sovrascrivendo i dati
    initDF()

def show_menu():  # Funzione per mostrare il menù all'utente
    print("\nMenu:")
    print("1) Ottenere la lista dei film ordinata per titolo")
    print("2) Sapere quanti film hanno una durata >= 2h")
    print("3) Mostrare una tabella contenente il totale di film raggruppati per colonna MPA")
    print("4) Mostrare i film che hanno avuto un rating superiore a 7.5")
    print("5) Aggiungi un film")
    print("6) Elimina un film")
    print("7) Aggiorna un film")
    print("0) Esci")

def add_movie():  # Funzione per aggiungere un film
    global df_original  # Indica che la variabile df sarà modificata
    new_index = len(df_original) + 1  # Determina il nuovo indice numerico
    title = input("Inserisci il titolo del film: ")
    formatted_title = f"{new_index}. {title}"  # Aggiunge il numero progressivo al titolo
    movie_link = input("Inserisci il link del film: ")
    year = input("Inserisci l'anno di uscita: ")
    duration = input("Inserisci la durata (es. 1h 45m): ")
    mpa = input("Inserisci la classificazione MPA: ")
    rating = input("Inserisci il rating: ")
    votes = input("Inserisci il numero di voti: ")
    new_movie = pd.DataFrame([[formatted_title, movie_link, year, duration, mpa, rating, votes]], columns=df_original.columns)
    df_original = pd.concat([df_original, new_movie], ignore_index=True)  # Aggiunge il nuovo film al DataFrame
    save_to_csv()  # Salva le modifiche nel file CSV
    print("Film aggiunto con successo!")

def delete_movie():  # Funzione per eliminare un film
    global df_original  # Indica che la variabile df sarà modificata
    title = input("Inserisci il titolo del film da eliminare (senza numero iniziale): ")
    df_original = df_original[~df_original['Title'].str.match(r'\d+\.\s*' + re.escape(title))]  # Rimuove il film dal DataFrame
    save_to_csv()  # Salva le modifiche nel file CSV
    print("Film eliminato con successo!")

def update_movie():  # Funzione per aggiornare un film
    global df_original  # Indica che la variabile df sarà modificata
    title = input("Inserisci il titolo del film da aggiornare (senza numero iniziale): ")
    mask = df_original['Title'].str.match(r'(\d+)\.\s*' + re.escape(title))  # Trova il film mantenendo il numero iniziale
    if mask.any():
        column = ""
        while column not in df_original.columns:
            column = input(f"Quale campo vuoi aggiornare? ({', '.join(df_original.columns)}): ")
            if column not in df_original.columns:
                print("Opzione non valida. Per favore, inserisci una delle opzioni elencate.")
       
        if column == "Title":
            new_title = input("Inserisci il nuovo titolo: ")
            df_original.loc[mask, 'Title'] = df_original.loc[mask, 'Title'].str.replace(r'(\d+\.\s*)', f'\1{new_title}', regex=True)  # Modifica il titolo mantenendo il numero iniziale
        else:
            new_value = input("Inserisci il nuovo valore: ")
            df_original.loc[mask, column] = new_value  # Aggiorna il valore specificato
        save_to_csv()  # Salva le modifiche nel file CSV
        print("Film aggiornato con successo!")
    else:
        print("Film non trovato.")

while True:  # Loop principale per il menù
    show_menu()
    choice = input("Scegli un'opzione: ")
    
    if choice == "1":
        df_sorted = df.sort_values(by='Title',key=lambda x: x.str.lower())  # Ordina il DataFrame in base ai titoli dei film
        print(df_sorted[['Title', 'Year']].to_string(index=False))  # Stampa i titoli ordinati senza indice
    elif choice == "2":
        movies_2h_or_more = df[df['Duration'] >= 120]  # Filtra i film con durata pari o superiore a 120 minuti
        print("Numero di film con durata >= 2h:", len(movies_2h_or_more))  # Stampa il numero di film
    elif choice == "3":
        mpa_counts = df['MPA'].value_counts().reset_index()  # Conta il numero di film per ogni classificazione MPA
        mpa_counts.columns = ['MPA Rating', 'Total Movies']  # Rinomina le colonne della tabella risultante
        print(mpa_counts.to_string(index=False))  # Stampa la tabella senza indice
    elif choice == "4":
        top_rated_movies = df[df['Rating'] > 7.5]  # Filtra i film con rating maggiore di 7.5
        top_rated_movies_sorted = top_rated_movies.sort_values(by='Rating')  # Ordina per rating in ordine decrescente
        print(top_rated_movies_sorted[['Title', 'Rating']].to_string(index=False))  # Stampa i film con rating > 7.5 senza indice
    elif choice == "5":
        add_movie()
    elif choice == "6":
        delete_movie()
    elif choice == "7":
        update_movie()
    elif choice == "0":
        print("Uscita dal programma.")
        break  # Esce dal loop
    else:
        print("Scelta non valida, riprova.")
