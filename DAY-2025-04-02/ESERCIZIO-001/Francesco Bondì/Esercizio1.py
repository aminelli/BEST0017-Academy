import pandas as pd # per leggere il file csv
import re # per espressioni regolari

df = pd.read_csv("imdb_movies_2024.csv", encoding="utf-8", sep=",")


# Funzione per rimuovere il numero iniziale dal titolo tramite regex (inizia con un + di un numero [0-9] e termina con un . e segue con uno spazio)
def remove_number(title):
    return re.sub(r'^\d+\.\s*', '', str(title))

#Funzione per convertire la durata espressa nel formato HH h MM m in minuti
def duration_to_minutes(duration):
    if pd.isna(duration) or not isinstance(duration, str):
        return 0  # Se la durata è NaN o non è una stringa ritorna 0

    # Pulisce gli spazi extra
    duration = duration.strip()

    # Se la durata è solo in ore
    if 'h' in duration and 'm' not in duration:
        hours = int(duration.replace('h', '').strip())  # Rimuove 'h' e converte in intero
        return hours * 60  # Converte le ore in minuti

    # Se la durata è solo in minuti
    elif 'min' in duration and 'h' not in duration:
        minutes = int(duration.replace('m', '').strip())  # Rimuove 'm' e converte in intero
        return minutes  # Restituisce i minuti direttamente

    # Se la durata è sia in ore che minuti
    elif 'h' in duration and 'm' in duration:
        parts = duration.split()  # Divide la stringa in ore e minuti
        hours = int(parts[0].replace('h', '').strip())  # Rimuove 'h' e converte in intero
        minutes = int(parts[1].replace('m', '').strip())  # Rimuove 'min' e converte in intero
        return hours * 60 + minutes  # Somma ore e minuti

    return 0  # Se non riesce a riconoscere il formato, restituisce 0


def print_sorted_titles(df):

    df["Title"] = df["Title"].apply(remove_number)

    #ordino i titoli nell'oggetto Pandas Series 
    sorted_titles = df["Title"].sort_values()

    # stampo i titoli dei filmi orninati in modo crescente 
    for i, title in enumerate(sorted_titles, start=1):
        print(f"{i}. {title}")


def print_long_movies(df):

    # Crea una nuova colonna duration in minutes in cui viene scritta la durata in minuti nel formato mmm
    df['duration_in_minutes'] = df['Duration'].apply(duration_to_minutes)

    # Filtrare i film con durata >= 2 ore (120 minuti)
    movies_2h_or_more = df[df['duration_in_minutes'] >= 120]

    # Stampare i titoli dei film con durata >= 2 ore
    for i, title in enumerate(movies_2h_or_more["Title"], start=1):
        print(f"{i}. {title}")


def print_mpa_counts(df):
    # ci sono gruppi diversi da MPA
    #mpa_counts = df.groupby('MPA').size().reset_index(name='Total Movies')

    #assegno io i gruppi
    mpa_ratings = ['G', 'PG', 'PG-13', 'R', 'NC-17']
    df_mpa = df[df['MPA'].isin(mpa_ratings)]

    # Raggruppa per la colonna MPA e calcola il numero di film per ciascun tipo di classificazione. con resetindex() converto l'incide in una colonna che conterrà il conteggio
    #groupby restituisce un oggetto che rappresenta i dati divisi in gruppi. 
    mpa_counts = df_mpa.groupby('MPA').size().reset_index(name='Total Movies')

    # Stampa la tabella
    print(mpa_counts)


def print_high_rating_movies(df):

    # Filtra la colonna Rating per includere solo i film con rating superiore a 7.5
    high_rating_movies = df[df['Rating'] > 7.5]

    # Mostra solo i titoli dei film
    high_rating_titles = high_rating_movies['Title']

    # Stampa i titoli
    for i, title in enumerate(high_rating_titles, start=1):
        print(f"{i}. {title}")


# Step 1: Ordinare i titoli
print("Step 1: Ordina e stampa i titoli")
print_sorted_titles(df)

# Step 2: Stampare i titoli dei film con durata >= 2 ore
print("\nStep 2: Titoli dei film con durata >= 2 ore")
print_long_movies(df)

# Step 3: Stampare la tabella delle classificazioni MPA
print("\nStep 3: Tabella delle classificazioni MPA")
print_mpa_counts(df)

# Step 4: Stampare i titoli dei film con rating > 7.5
print("\nStep 4: Titoli dei film con rating > 7.5")
print_high_rating_movies(df)

