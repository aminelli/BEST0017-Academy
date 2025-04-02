import pandas as pd  

class Film:
    
    def __init__(self, title, link, year, duration, MPA, rating, votes):
        self.title = title
        self.link = link
        self.year = year
        self.duration=duration
        self.MPA=MPA
        self.rating=rating
        self.votes=votes
        
def extract_hours(duration):
    if isinstance(duration, str) and "h" in duration:
        try:
            hours = int(duration.split("h")[0].strip())  # Prende il numero prima di "h"
            return hours
        except ValueError:
            return None
    return None

df = pd.read_csv("imdb_movies_2024.csv") 

film_list=list()
for index, row in df.iterrows():
    film = Film(row["Title"], row["Movie Link"], row["Year"], row["Duration"], row["MPA"], row["Rating"], row["Votes"])
    film_list.append(film)

#Leggere il contenuto del file imdb_movies_2024.csv
for film in film_list:
    print(vars(film))

#Ottenere la lista dei film ordinata per titolo (attenzione c'è una difficoltà da gestire)
lista_ordinata=film_list.sort(key=lambda film: film.title.split(".")[1].strip()[0])

#Sapere quanti film hanno una durata >= 2h
count=0
for film in film_list:
    if pd.isna(film.duration) or film.duration == "PG-13":
        continue  
    hours = extract_hours(film.duration)
    if hours is not None and hours >= 2:
        count += 1 
print(count)

#Mostrare una tabella contenente il totale di film raggruppati per colonna MPA (per il significato dell'MPA vedere nota sottostante)
mpa_count = df['MPA'].value_counts()
mpa_count_df = mpa_count.reset_index()
mpa_count_df.columns = ['MPA', 'Number of Movies']
print(mpa_count_df)


#Mostrare i film che hanno avuto un rating superiore a 7.5
for film in film_list:
    if pd.isna(film.rating):
        continue  
    rating = float(film.rating)
    if rating is not None and rating > 7.5:
       print(vars(film))

    

