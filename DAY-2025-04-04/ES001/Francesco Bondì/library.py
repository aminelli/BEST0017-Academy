import json
import re


def sort_books(library):
    """
    Ordina la lista di libri prima per titolo e poi per autore.

    Parameters:
    library (list): Una lista di dizionari che rappresentano i libri. Ogni dizionario contiene informazioni 
                    come 'title', 'author', 'year', 'avaible'.

    La funzione ordina la lista di libri **in-place**, quindi modifica direttamente l'ordine degli elementi
    nella lista passata come parametro.

    """
    #funzione lambda per ordinare i libri in base al titolo e all'autore
    #la funzione lambda restituisce una tupla con il titolo e l'autore del libro
    #la funzione sort ordina i libri in base alla tupla restituita dalla funzione lambda
    #in questo modo i libri vengono ordinati prima per titolo e poi per autore
    library.sort(key=lambda x: (x['title'].lower(), x['author'].lower())) 



def add_book(library, title, author, year):
    """
    Aggiunge un nuovo libro al catalogo.
    Parameters:
    library (list): La lista che rappresenta il catalogo dei libri.
    title (str): Il titolo del libro.
    author (str): L'autore del libro.
    year (int): L'anno di pubblicazione del libro.
    """
    global ID  # Utilizza la variabile globale ID
    book = {
        'id': ID,
        'title': title,
        'author': author,
        'year': year,
        'avaible': True
    }
    library.append(book)
    print(f"Libro '{title}' aggiunto con successo!")
    #incremento dell'ID per il prossimo libro
    ID += 1



def remove_book(library, id):
    """
    Rimuove un libro dal catalogo in base al suo ID.

    Parameters:
    library (list): La lista che rappresenta il catalogo dei libri.
    id (int): L'ID del libro da rimuovere.
    """
    for book in library:
        if book['id'] == id:
            library.remove(book)
            print(f"Libro '{book['title']}' rimosso con successo!")
            return
    print(f"Book con ID {id} non trovato.")


def search_book(library, key_word):
    """
    Cerca un libro nel catalogo per titolo o autore. Se la key_word è presente nel titolo o nell'autore,
    stampa le informazioni del libro.

    Parameters:
    library (list): La lista che rappresenta il catalogo dei libri.
    key_word (str): Parola chiave per cercare nei titoli o autori dei libri.
    """
    for book in library:
        if key_word.lower() in book['title'].lower() or key_word.lower() in book['author'].lower():
            print(f"Libro trovato: {book['title']} di {book['author']} ({book['year']})")
            return
    print(f"Book '{key_word}' non trovato.")

def give_book(library, id):
    """
    Segna un libro come preso in prestito e setta il campo avaible del libro come False.

    Parameters:
    library (list): La lista che rappresenta il catalogo dei libri.
    id (int): L'ID del libro da prendere in prestito.
    """
    for book in library:
        if book['id'] == id:
            if book['avaible']:
                book['avaible'] = False
                print(f"Libro '{book['title']}' è stato preso in prestito.")
            else:
                print(f"Libro '{book['title']}' non è disponibile.")
            return
    print(f"Book con ID {id} non trovato.")


def return_book(library, id):
    """
    Segna un libro come restituito settando avaiable a false.

    Parameters:
    library (list): La lista che rappresenta il catalogo dei libri.
    id (int): L'ID del libro da restituire.
    """
    for book in library:
        if book['id'] == id:
            if not book['avaible']:
                book['avaible'] = True
                print(f"Libro '{book['title']}' è stato restituito.")
            else:
                print(f"Libro '{book['title']}' non è stato preso in prestito.")
            return
    print(f"Book con ID {id} non trovato.")


def show_catalog(library):
    """
    Mostra l'elenco completo dei libri nel catalogo.

    Parameters:
    library (list): La lista che rappresenta il catalogo dei libri.

    Stampa:
    catalog (list): Una lista di dizionari (ordinati con la funzione sort_books) contenenti i libri con status disponibili.
    """
    catalog =[]
    if not library:
        # Verifica se la libreria è vuota. Se lo è, stampa un messaggio e termina la funzione
        print("Il catalogo è vuoto.")
        return
    # Usa la list comprehension per creare una lista di dizionari contenenti solo i libri disponibili
    # Per ogni libro nella libreria, se il libro è disponibile (book['avaible'] == True),
    # crea un dizionario con 'id', 'title', 'author', e imposta 'status' come 'Disponibile'
    catalog = [
        {'id': book['id'], 'title': book['title'], 'author': book['author'], 'status': 'Disponibile'}
        for book in library if book['avaible']
    ]
    sort_books(catalog)
    for book in catalog:
        print(f"ID: {book['id']} {book['title']} di {book['author']} - {book['status']}")



def save_to_file(library, filename):
    """
    Salva il catalogo dei libri in un file JSON.

    Parameters:
    library (list): La lista che rappresenta il catalogo dei libri.
    filename (str): Il nome del file in cui salvare i dati.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(library, file, indent=4, ensure_ascii=False)
        print(f"Catalogo salvato in '{filename}'")
    except (IOError, TypeError) as e:
        print(f"Errore nel salvataggio del file: {e}")




def load_from_file(filename):
    """
    Carica il catalogo dei libri da un file JSON.

    Parameters:
    filename (str): Il nome del file da cui caricare i dati.
    """
    global library, ID
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            library = json.load(file)
            highest_id = max(book['id'] for book in library)
            ID = highest_id + 1  # Imposta l'ID come massimo + 1
        print(f"Catalogo caricato da '{filename}'")
    except FileNotFoundError:
        print(f"File '{filename}' non trovato.")
    except json.JSONDecodeError:
        print(f"Errore nella decodifica del file '{filename}'. Il file potrebbe essere danneggiato.")
    

def statistics(library):
    """
    Calcola e stampa il totale dei libri, il numero di libri disponibili e il numero di libri non disponibili.

    Parameters:
    library (list): Una lista di dizionari che rappresentano i libri. Ogni dizionario contiene informazioni 
                    come 'title', 'author', 'year', 'avaible'.

    Stampa:
    Il numero totale dei libri, il numero dei libri disponibili e il numero dei libri non disponibili.
    """
    all_books = len(library)
    #list comprehension per contare i libri disponibili e non disponibili
    available_books = sum(1 for book in library if book['avaible'])
    unavailable_books = len(library) - available_books
    print(f"Totale libri: {all_books}")
    print(f"Libri disponibili: {available_books}")
    print(f"Libri non disponibili: {unavailable_books}")



def get_year():
    """
    Chiede all'utente di inserire un anno di pubblicazione valido, verificando che sia un numero di 4 cifre.

    La funzione continua a richiedere l'input finché l'anno inserito non è valido. Un anno valido deve essere un 
    numero intero di 4 cifre compreso tra 1000 e 9999.

    Returns:
        int: L'anno di pubblicazione inserito dall'utente, se valido.

    Se l'anno inserito non è valido o non è un numero intero, viene mostrato un messaggio di errore e viene richiesto 
    un nuovo input.
    """
    while True:
        try:
            year = int(input("Inserisci l'anno di pubblicazione: "))
            # Controllo che l'anno sia di 4 cifre
            if 1000 <= year <= 2025:
                return year
            else:
                print("Errore: L'anno deve essere un numero di 4 cifre tra 1000 e 9999.")
        except ValueError:
            print("Errore: Inserisci un numero valido per l'anno.")



def advanced_search(library, keyword):
    """
    Esegue una ricerca avanzata nei libri in base alla parola chiave nel titolo, autore o anno.
    
    Parametri:
    - library (list): La lista di libri, dove ogni libro è un dizionario con 'title', 'author', 'year'.
    - keyword (str): La parola chiave da cercare (può essere nel titolo, autore o anno).
    
    Print:
    - Una lista di libri che corrispondono alla parola chiave.
    """
    matching_books = []
    
    # Compilazione del pattern per la ricerca, ignorando maiuscole e minuscole
    # la re mi permette di utilizare funzioni avanzate per la ricerca come il match e il search, IGNORECASE
    keyword_pattern = re.compile(str(keyword), re.IGNORECASE)

    for book in library:
        # Verifica se la parola chiave corrisponde nel titolo, autore o anno
        if (keyword_pattern.search(book['title']) or
            keyword_pattern.search(book['author']) or
            (str(book['year']) == str(keyword))):
            matching_books.append(book)

    if matching_books:
        print("Libri trovati:")
        for book in matching_books:
            print(f"ID: {book['id']} {book['title']} di {book['author']} ({book['year']})")
    else:
        print("Nessun libro trovato con la parola chiave fornita.")
    

def get_input_with_cancel(prompt):
    """
    Funzione che chiede l'input all'utente e consente di annullare l'operazione.
    Se l'utente inserisce 'n' (per annullare), la funzione restituirà None.
    
    Parameters:
    - prompt (str): Il messaggio da mostrare all'utente.
    
    Returns:
    - str: L'input dell'utente o None se l'utente ha annullato l'operazione.
    """
    user_input = input(f"{prompt} (Inserisci 'annulla' per annullare): ")
    if user_input.lower() == 'annulla':
        return None  # Se l'utente annulla
    return user_input




#lista che rappresenta il catalogo dei libri
#ogni libro è un dizionario con le chiavi 'id', 'title', 'author', 'year' e 'avaible'
library = []

# ID è una variabile globale che tiene traccia dell'ID del libro corrente.
# Inizialmente è impostato a 1, ma viene incrementato quando si aggiungono nuovi libri.
ID = 1

print("Benvenuto nel sistema di gestione della biblioteca!")

while True:

    print("\n")
    print("1. Aggiungi libro")
    print("2. Rimuovi libro")
    print("3. Cerca libro")
    print("4. Prendi in prestito libro")
    print("5. Restituisci libro")
    print("6. Mostra catalogo")
    print("7. Salva catalogo")
    print("8. Carica catalogo")
    print("9. Statistiche")
    print("10. Ricerca avanzata")
    print("0. Esci")
    print("Scegli un'opzione:")



    choice = input(">> ")
    if choice == '1':
        title = get_input_with_cancel("Inserisci il titolo del libro")
        if title is None:
            print("Operazione annullata.")
            continue
        
        author = get_input_with_cancel("Inserisci l'autore del libro")
        if author is None:
            print("Operazione annullata.")
            continue
        
        year = get_year()  # Funzione esistente
        if year is None:
            print("Operazione annullata.")
            continue
        
        add_book(library, title, author, year)

    elif choice == '2':
        id_input = input("Inserisci l'ID del libro da rimuovere: ")
        if id_input.lower() == 'n':
            print("Operazione annullata.")
            continue
        
        try:
            id = int(id_input)
            remove_book(library, id)
        except ValueError:
            print("ID non valido, operazione annullata.")
            continue

    elif choice == '3':
        key_word = get_input_with_cancel("Inserisci il titolo o l'autore del libro da cercare")
        if key_word is None:
            print("Operazione annullata.")
            continue
        search_book(library, key_word)

    elif choice == '4':
        id_input = input("Inserisci l'ID del libro da prendere in prestito: ")
        if id_input.lower() == 'n':
            print("Operazione annullata.")
            continue
        try:
            id = int(id_input)
            give_book(library, id)
        except ValueError:
            print("ID non valido, operazione annullata.")
            continue

    elif choice == '5':
        id_input = input("Inserisci l'ID del libro da restituire: ")
        if id_input.lower() == 'n':
            print("Operazione annullata.")
            continue
        try:
            id = int(id_input)
            return_book(library, id)
        except ValueError:
            print("ID non valido, operazione annullata.")
            continue

    elif choice == '6':
        show_catalog(library)

    elif choice == '7':
        filename = get_input_with_cancel("Inserisci il nome del file per salvare il catalogo")
        if filename is None:
            print("Operazione annullata.")
            continue
        save_to_file(library, filename)

    elif choice == '8':
        filename = get_input_with_cancel("Inserisci il nome del file da cui caricare il catalogo")
        if filename is None:
            print("Operazione annullata.")
            continue
        load_from_file(filename)

    elif choice == '9':
        statistics(library)

    elif choice == '10':
        keyword = get_input_with_cancel("Inserisci la parola chiave da cercare (titolo, autore o anno)")
        if keyword is None:
            print("Operazione annullata.")
            continue
        advanced_search(library, keyword)

    elif choice == '0':
        print("Uscita dal programma.")
        break

    else:
        print("Opzione non valida. Riprova.")
    