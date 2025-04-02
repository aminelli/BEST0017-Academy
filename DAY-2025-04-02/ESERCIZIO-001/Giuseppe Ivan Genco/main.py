# Importo pandas per leggere e gesitre il file csv
import pandas


# Leggo il file csv con il metodo read_csv e lo inserisco nella variabile 'df' Oggetto di tipo DataFrame
# DataFrame = struttura dati tabellare bidimensionale, simile a un foglio di calcolo o a una tabella di database SQL
df = pandas.read_csv('imdb_movies_2024.csv')


# Imposto pandas in modo da mostrare tutte le colonne del DataFrame quando lo stampo in output
# pandas.set_option('display.max_columns', None)



# Stampo le prime 40 righe del DataFrame
print(df.head(40))



# Ordino il DataFrame lessicograficamente, prima però modifico momentaneamente i valori della colonna Title
# andando a applicare la funzione delle stringhe 'replace' con una regex che mi becca tutti i numeri seguiti
# da un punto e da un eventuale spazio
df_title = df.sort_values( by='Title', key=lambda col: col.str.replace(r'^\d+\.\s*', '', regex=True) )



# Stampo le prime 40 righe del DataFrame
print(df_title.head(40))



# Creo il filtro da applicare alla colonna 'Duration' con il quale andrò a beccare i film che hanno durata maggiore a 2 ore
df_duration = df['Duration'].str.startswith('2h') == True



# Creo una lista contente i nomi delle colonne che voglio stampare 
columns = ['Title', 'Duration']



# Stampo le prime 40 righe del DataFrame
print(df[df_duration][columns].head(40))



# Raggruppo per i valori contenuti nella colonna 'MPA' e poi con il metodo 'size()' calcolo la dimensione di ogni gruppo
df_MPA = df.groupby('MPA').size()
print('\n')



# Stampo le occorrenze di ogni gruppo trovato
print(df_MPA)



# Creo il filtro da applicare alla colonna 'Rating' con il quale andrò a beccare tutti i film che hanno valutazione superiore a 7.5
df_rating = df['Rating'] > 7.5


# Stampo le prime 40 righe del DataFrame
print(df[df_rating].head(40))








