# film_filter.py
import pandas as pd

def ordina_per_titoli(file_path):

  # Leggo il file CSV
  df = pd.read_csv(file_path, encoding='utf-8')

  # Rimuovo eventuali spazi nei nomi delle colonne
  df.columns = df.columns.str.strip()

  # Creo una regex per rimuovere i numeri all'inizio del titolo, altrimenti non avremo mai un vero ordine alfabetico
  df['Title'] = df['Title'].str.replace(r'^\d+\.\s*', '', regex=True)

  df_sorted = df.sort_values(by='Title') # Ordina alfabeticamente

  df_sorted.to_csv('ordinato.csv', index=False)  # Salva il risultato in un nuovo file CSV per visualizzarlo meglio


def filtra_film_lunghi(file_path):

  # Carica il CSV
  df = pd.read_csv(file_path, encoding='utf-8')

  # Rimuovo eventuali spazi nei nomi delle colonne
  df.columns = df.columns.str.strip()

  # Per contare i film che durano 2 ore o più, decido di convertire il primo carattere in intero e controllare che
  # dopo la cifra vi sia una "h" a indicare le ore per aggirare il problema dei film sotto l'ora di durata

  df['FirstDigit'] = df['Duration'].astype(str).str.extract(r'(\d)h')  # Estrai il numero prima di "h"

  # Converti in numerico, gestendo gli errori
  df['FirstDigit'] = pd.to_numeric(df['FirstDigit'], errors='coerce')

  # Filtro i film con durata >= 2 ore (prima cifra >= 2) e mi assicuro che ci sia "h"
  film_lunghi = df[(df['FirstDigit'] >= 2) & df['Duration'].str.contains('h')]

  # Faccio un print giusto per vedere il numero totale di film lunghi
  print(f"Numero di film con durata >= 2 ore: {len(film_lunghi)}")

  # Salvo il risultato in un altro file
  film_lunghi.to_csv('film_lunghi.csv', index=False)


def conta_film_per_mpa(file_path):
  # Carica il CSV
  df = pd.read_csv(file_path, encoding='utf-8')

  # Rimuove spazi nei nomi delle colonne
  df.columns = df.columns.str.strip()

  # Raggruppa i film per MPA e conta il numero di film per ogni categoria
  conteggio_mpa = df['MPA'].value_counts()

  # Crea un DataFrame con il conteggio
  conteggio_mpa_df = conteggio_mpa.reset_index()
  conteggio_mpa_df.columns = ['MPA', 'Numero di Film']

  # Salva il risultato in un nuovo file CSV
  conteggio_mpa_df.to_csv('conteggio_film_per_mpa.csv', index=False)

  # Ritorna il DataFrame con i conteggi
  return conteggio_mpa_df

def best_films(file_path, rating_threshold):
  # Carica il CSV
  df = pd.read_csv(file_path, encoding='utf-8')

  # Rimuove spazi nei nomi delle colonne
  df.columns = df.columns.str.strip()

  # Filtra i film con una valutazione pari o superiore a quella indicata
  best_films_df = df[df['Rating'] >= rating_threshold]

  # Ordina i film dal rating più alto al più basso
  best_films_df = best_films_df.sort_values(by='Rating', ascending=False)

  # Salva il risultato in un nuovo file CSV
  best_films_df.to_csv('best_films.csv', index=False)