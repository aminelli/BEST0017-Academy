import pandas as pd

# 1 lettura del file csv
df = pd.read_csv("imdb_movies_2024.csv")

# 2 Ottenere la lista dei film ordinata per titolo (attenzione c'è una difficoltà da gestire)
def title_extraction(testo):
    if isinstance(testo, str) and '.' in testo:
        return testo.split('.', 1)[1].strip() #split() separa gli elementi dopo il primo punto. #[1] prende parte dopo il punto (prima carattere subito dopo)
    return testo                              #strip() rimuove spazi iniziali e finali della stringa
    
df['Title'] = df['Title'].apply(title_extraction)
df_ordinato= df.sort_values('Title')
print("\n Lista dei film ordinata per titolo: \n")
print(df_ordinato[['Title']].to_string(index=False))
df_ordinato[['Title','Movie Link','Year','Duration', 'MPA', 'Rating', 'Votes']].to_csv("film_ordine_alfabetico.csv", index=False)



# 3 Sapere quanti film hanno una durata >= 2h
film = df[df_ordinato['Duration'].str.contains(r'2h', regex=True, na=False)].copy() #dava errore quindi ho usato copy() per creare una copia indipendente
def check_minuti(duration):
    try:
        parti = duration.split('2h', 1)
        if len(parti) > 1:
            minuti = parti[1].strip().rstrip('m')  # rimuove spazi e "m" finale
            if minuti.isdigit():
                return int(minuti)
        return 0
    except:
        return 0

film['Minuti'] = film['Duration'].apply(check_minuti)
film = film.sort_values(by='Minuti', ascending=False)
film = film.drop(columns=['Minuti'])

print("Film con durata >= 2 ore:")
print(film[['Title', 'Duration']])
film[['Title','Movie Link','Year','Duration', 'MPA', 'Rating', 'Votes']].to_csv("film_2h+.csv", index=False)


# 4 Mostrare una tabella contenente il totale di film raggruppati per colonna MPA (per il significato dell'MPA vedere nota sottostante)
'''value_count() conta i valori per ogni indice MPA, 
reset_index sposta quel valore in una colonna in modo da raggrupparli''' 
mpa = df_ordinato['MPA'].value_counts().reset_index() 
mpa.columns = ["MPA", "N° Film"]
mpa.to_csv("mpa.csv", index=False)
print(mpa)



# 5 Mostrare i film che hanno avuto un rating superiore a 7.5
film_rating = df[df_ordinato['Rating'] > 7.5]
film_rating[['Title', 'Rating']] = film_rating.sort_values(by='Rating', ascending=False).to_csv("rating.csv", index=False)
print("\n File csv salvato: rating.csv")
