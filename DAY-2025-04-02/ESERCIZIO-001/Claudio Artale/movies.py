import pandas as pd
import re

# Funzione per rimuovere articoli iniziali
def pulisci_titolo(titolo):
    # Rimuove l'indice numerico iniziale, es. "1. " → ""
    titolo = re.sub(r'^\d+\.\s*', '', titolo)
    
    # Rimuove articoli iniziali (The, A, An) solo se sono all'inizio
    titolo = re.sub(r'^(The|A|An)\s+', '', titolo, flags=re.IGNORECASE)
    
    return titolo

def durata_in_minuti(durata_str):
    if isinstance(durata_str, str):
        match = re.match(r'(?:(\d+)h)?\s*(?:(\d+)m)?', durata_str.strip())
        ore = int(match.group(1)) if match and match.group(1) else 0
        minuti = int(match.group(2)) if match and match.group(2) else 0
        return ore * 60 + minuti
    else:
        return 0  # oppure puoi restituire None

# Carica il file CSV in un DataFrame
df = pd.read_csv("imdb_movies_2024.csv")

#1. Ordinamento dei film in base al titolo

# Dataframe con titoli ordinati
df['Title_senza_articoli'] = df['Title'].apply(pulisci_titolo)

# Ordina in base alla colonna pulita, poi rimuovila
df_ordinato = (
    df.sort_values(by='Title_senza_articoli')
      .drop(columns=['Title_senza_articoli'])
      .reset_index(drop=True)
)

#print(df_ordinato['Title'])

#2. Filtraggio dei film con durata > 120 minuti

df['Durata_in_minuti'] = df['Duration'].apply(durata_in_minuti)

"""
df_sorted_by_durata = df[df['Durata_in_minuti'] >= 120].reset_index(drop=True)  #maschera booleana
"""

df_120_minutes_movies = (df.query("Durata_in_minuti >= 120")
.sort_values(by="Durata_in_minuti")
.reset_index(drop=True)
)

#print(df_120_minutes_movies)

#3. Raggruppamento per MPA

conteggio_mpa = df.groupby('MPA').size().reset_index(name='Totale_film')
print(conteggio_mpa)

#4. Filtraggio dei film con rating > 7.5

df_rating_alto = (df.query("Rating > 7.5")
.sort_values(by="Rating", ascending=False)
.reset_index(drop=True))

print(df_rating_alto[['Title', 'Rating', 'Durata_in_minuti']])


