import pandas as pd
from film_filter import *

file_path = 'imdb_movies_2024.csv'

filtra_film_lunghi(file_path)
ordina_per_titoli(file_path)
conta_film_per_mpa(file_path)
best_films(file_path, 7.5)