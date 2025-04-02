import pandas as pd

###################
# carico il file csv in un dataframe di pandas
df = pd.read_csv('imdb_movies_2024.csv') 

# rimpiazzo con la stringa vuota il numero ordinale nel titolo con il metodo replace passando un regular expression
# ^ significa solo a inizio stringa, \d+ significa una o più cifre e \. per considerare anche il punto
df["Title"] = df["Title"].str.replace(r'^\d+\.', '', regex=True) 

# ordino il df in base al titolo
df_ordinato = df.sort_values(by="Title")
print("---DF ORDINATO PER TITOLO---")
# print(df_ordinato)
print(df_ordinato.head().to_string())


###################
# print(df[df["Duration"].notna()].count())
# mi creo un nuovo df senza valori null (ci sono 6 na) e che contengano la lettera h nel campo duration  (per non intaccare quello originale)
# (i record che non hanno 'h' avranno durata sicuramente minore di 1h oppure hanno scritto qualcosa che non è un tempo)
nn_df = df[df["Duration"].notna() & df["Duration"].str.contains('h')]

# utilizzo i metodi delle stringhe per ottenere l'ora e convertirla a intero
nn_df["Hours"] = nn_df["Duration"].str.split('h').str[0].astype(int)

# seleziono solo i record che hanno ora maggiore o uguale a 2
# print("---FILM CON DURATA >= 2H---")
# print(nn_df[nn_df["Hours"] >= 2].head().to_string())
print("Numero di film con durata > 2h: ", len(nn_df[nn_df["Hours"] >= 2]))




###################
# ordino i record in base all'ordine dei valori MPA
df_MPA = df.sort_values(by="MPA")
print("---DF ORDINATO PER MPA---")
# print(df_MPA)
print(df_MPA.head().to_string())


###################
# prendo solo i record con valutazione maggiore o uguale a 7.5
df_rating = df[df["Rating"] >= 7.5].sort_values(by="Rating", ascending=False)
print("---FILM CON VALUTAZIONE >= 7.5---")
# print(df_rating)
print(df_rating.head().to_string())