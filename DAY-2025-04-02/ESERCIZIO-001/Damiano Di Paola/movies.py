import pandas as pd
import re

def converti_durata(durata): # funzione per la conversione in minuti del campo Durata
    match = re.match(r'(?:(\d+)h)?\s*(?:(\d+)m)?', str(durata))  # cerco ore e minuti (?: evita la cattura di gruppi non rilevanti)
    ore = int(match.group(1)) if match.group(1) else 0
    minuti = int(match.group(2)) if match.group(2) else 0
    return ore * 60 + minuti 

''' PREMESSA GENERALE: per mia formazione ed abitudine, mi sono sempre trovato molto più a mio agio a lavorare con le collection built-in di Python.
Pur tuttavia, ho voluto "forzarmi" a usare pandas e i dataframe, che sicuramente trovano molta più applicazione in ambiti professionali. '''

with (open('esercizio001/imdb_movies_2024.csv', 'r', encoding= "utf-8-sig") as input): # apro il file con un with statement per chiuderlo automaticamente

    movies_df = pd.read_csv(input, sep=',') # leggo il file con pandas
    # print(movies.columns.tolist()) # stampo la lista dei nomi delle colonne (TEST)
    
    '''TASK 1'''
    # non è utile che nel titolo sia presente anche la posizione (si presume in base agli incassi). estraggo il valore con una regex e ne creo una nuova colonna in posizione 0.
    movies_df["Position"] = movies_df["Title"].str.extract(r"^(\d+)\.")
    movies_df.insert(0, "Position", movies_df.pop("Position"))

    # nel campo Title elimino con una regex il numero e lo spazio
    movies_df["Title"] = movies_df["Title"].str.replace(r"^\d+\.\s", "", regex=True)
  
    # ordino il dataframe sul campo Title ripulito
    print('\n\n', movies_df.sort_values(by="Title", ascending=True))

    '''
    TASK 1 senza pandas
    titles_list = movies_df['Title'].tolist() # creo una lista con i titoli dei film
    # l'espressione regolare r'^\d+\.\s' cerca un numero seguito da un punto e uno spazio all'inizio della stringa
    titles_list = [re.sub(r'^\d+\.\s', '', title) for title in titles_list] # cancello la sottostringa da tutti i dati con una list comprehension
    # ordino la lista dei titoli in ordine alfabetico, e stampo 
    titles_list.sort() 
    print(titles_list)
    '''


    '''TASK 2'''
    # creo una nuova colonna con la durata convertita in minuti tramite la mia funzione
    movies_df["Duration_mins"] = movies_df["Duration"].apply(converti_durata)

    # conto quante righe del dataframe rispondono positivamente al controllo booleano sulla mia nuova colonna, e stampo
    long_movies_count = (movies_df["Duration_mins"] >= 120).sum()
    print('\n\n', "Film lunghi almeno 2 ore: ", long_movies_count)


    '''TASK 3'''
    # effettuo alcuni raggruppamenti: Null, Not Rated e Unrated dovrebbero rientrare nello stesso conteggio
    movies_df["MPA"] = movies_df["MPA"].fillna("Not Rated")
    movies_df["MPA"] = movies_df["MPA"].replace("Unrated", "Not Rated")

    # conto i film per valore della colonna "MPA" e salvo i risultati in un nuovo dataframe
    mpa_table = movies_df["MPA"].value_counts().reset_index()

    # rinomino le colonne per chiarezza, e stampo
    mpa_table.columns = ["MPA", "Movie count"]
    print('\n\n', mpa_table)


    '''TASK 4'''
    # filtro il dataframe di partenza con un controllo booleano sul campo Rating, e stampo il dataframe risultante
    good_movies = (movies_df[movies_df["Rating"] > 7.5])
    print('\n\n', good_movies)

print("Fine programma")