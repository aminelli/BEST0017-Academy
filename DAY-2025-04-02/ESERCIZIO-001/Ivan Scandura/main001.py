import pandas as pd
import re

# Funzione per caricare il file CSV
def load_data(file_path):
    """
    Carica i dati dal file CSV in un DataFrame utilizzando pandas.
    
    :param file_path: Percorso del file CSV
    :return: DataFrame con i dati caricati
    """
    df = pd.read_csv(file_path)  # Legge il file CSV e lo converte in DataFrame
    return df

# Funzione per pulire il titolo rimuovendo il numero iniziale
def clean_title(title):
    
    """
    Rimuove il numero iniziale dal titolo del film utilizzando regex.
    :param title: Titolo originale del film
    :return: Titolo pulito senza numero iniziale
    
    Questa riga di codice utilizza la funzione re.sub() della libreria re (che gestisce le 
    espressioni regolari) per rimuovere una parte specifica di una stringa.
    title è un oggetto (probabilmente una stringa o un altro tipo di dato) e la funzione 
    str(title) lo converte in una stringa, se non lo è già.
    re.sub() è una funzione che cerca una corrispondenza per un modello di espressione regolare 
    (pattern) in una stringa e sostituisce la parte trovata con una nuova stringa.
    La sintassi di re.sub() è: re.sub(pattern, replacement, string) dove:
    pattern: è l'espressione regolare che indica cosa cercare.
    replacement: è la stringa che sostituirà ciò che viene trovato dal pattern.
    string: è la stringa su cui eseguire la ricerca e la sostituzione.
    Questo è il pattern dell'espressione regolare:
    
    ^: indica che la corrispondenza deve avvenire all'inizio della stringa.
    r"d+": r"d" corrisponde a una cifra (0-9) e + significa "una o più" cifre. Quindi, r"d+"
    corrisponde a una sequenza di uno o più numeri.
    .: il punto . è un carattere speciale nelle espressioni regolari (che corrisponde a 
    qualsiasi carattere), quindi viene preceduto da slash per indicare che deve essere interpretato 
    come il punto letterale.
    s+: s corrisponde a uno spazio bianco (inclusi spazi, tabulazioni e ritorni a capo) e + 
    significa "uno o più" spazi bianchi. Quindi, s+ corrisponde a uno o più spazi bianchi.
    """
    return re.sub(r'^\d+\.\s+', '', str(title))  # Rimuove il numero iniziale se presente

# Funzione per convertire la durata in minuti
def duration_to_minutes(duration):
    """
    Converte la durata del film da formato testo (es. '2h 30m') a minuti interi.
    
    :param duration: Durata del film in formato stringa
    :return: Durata in minuti (int) oppure None se non valida
    
    re.match() cerca una corrispondenza all'inizio della stringa. Se il pattern corrisponde a 
    una parte della stringa, re.match() restituisce un oggetto match; altrimenti, restituisce None.
    La sintassi di re.match() è: re.match(pattern, string) dove:
    pattern è l'espressione regolare che stiamo cercando.
    string è la stringa in cui cerchiamo il pattern.
    Il pattern completo cerca una stringa che possa essere nel formato delle ore seguite da "h" 
    (opzionale) e dei minuti seguiti da "m" (anch'essi opzionali).
    """
    match = re.match(r'(?:(\d+)h\s*)?(?:(\d+)m)?', str(duration))  # Estrarre ore e minuti con regex
    
    """
    Qui viene verificato se match è valido, cioè se la funzione re.match() ha trovato una 
    corrispondenza. Se non c'è alcuna corrispondenza (ovvero se match è None), il blocco di 
    codice all'interno non verrà eseguito e la funzione restituirà None
    """
    if match:
        hours = int(match.group(1)) if match.group(1) else 0  # Converte le ore in intero
        minutes = int(match.group(2)) if match.group(2) else 0  # Converte i minuti in intero
        return hours * 60 + minutes  # Calcola la durata totale in minuti
    return None

# Funzione per analizzare i dati
def analyze_movies(df):
    """
    Analizza i dati per estrarre informazioni specifiche:
    - Ordina i film alfabeticamente per titolo pulito.
    - Conta i film con durata di almeno 2 ore.
    - Raggruppa i film per classificazione MPA.
    - Filtra i film con rating superiore a 7.5.
    
    :param df: DataFrame contenente i dati dei film
    :return: Tupla contenente:
        - DataFrame con i titoli ordinati
        - Numero di film con durata >= 2 ore
        - DataFrame con il totale dei film raggruppati per MPA
        - DataFrame con i film aventi rating > 7.5
    """
    # Pulire i titoli e ordinarli alfabeticamente
    #df: DataFrame(struttura dati bidimensionale simile ad una tabella)
    #df_sorted Dataframe ordinato per titolo
    df['Clean Title'] = df['Title'].apply(clean_title)  # Applica la funzione di pulizia titoli
    df_sorted = df.sort_values(by='Clean Title')  # Ordina il DataFrame per titolo
    
    # Convertire la durata in minuti e contare i film >= 2 ore
    df['Duration Minutes'] = df['Duration'].apply(duration_to_minutes)  # Applica la conversione durata
    long_movies_count = (df['Duration Minutes'] >= 120).sum()  # Conta i film con durata >= 120 min
    
    # Contare il numero di film per ciascuna classificazione MPA
    mpa_counts = df.groupby('MPA').size().reset_index(name='Total Films')  # Raggruppa per MPA e conta i film
    
    # Filtrare i film con rating superiore a 7.5
    """
    errors='coerce': Questo argomento indica a pandas di convertire qualsiasi valore che non può 
    essere convertito in un numero in un valore NaN (Not a Number), invece di sollevare un errore.
    """
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')  # Converte la colonna Rating in numerico
    high_rated_movies = df[df['Rating'] > 7.5][['Clean Title', 'Rating']]  # Seleziona i film con rating > 7.5
    
    return df_sorted[['Clean Title']], long_movies_count, mpa_counts, high_rated_movies

# Eseguire l'analisi
file_path = "imdb_movies_2024.csv"

df = load_data(file_path)  # Carica i dati dal file CSV
df_sorted, long_movies_count, mpa_counts, high_rated_movies = analyze_movies(df)  # Esegue l'analisi

# Stampare i risultati
pd.set_option('display.max_rows', None)  # Per forzare Pandas a mostrare tutte le righe

print("Lista ordinata di film:")
#print(df_sorted.head()) Mostra i primi 5 film ordinati
print(df_sorted)
df_sorted.to_csv("df_sorted.csv", index=False) # Salvare i risultati in un file CSV

print(f"\nNumero di film con durata >= 2 ore: {long_movies_count}")  # Stampa il numero di film lunghi

print("\nTotale film per classificazione MPA:")

print(mpa_counts)  # Stampa la tabella con il conteggio per MPA
mpa_counts.to_csv("mpa_counts.csv", index=False) # Salvare i risultati in un file CSV

print("\nFilm con rating superiore a 7.5:")
#print(high_rated_movies.head()) Per mostrare solo i primi 5 film con rating > 7.5
print(high_rated_movies)  # Mostra i film con rating > 7.5
high_rated_movies.to_csv("high_rated_movies.csv", index=False) # Salvare i risultati in un file CSV