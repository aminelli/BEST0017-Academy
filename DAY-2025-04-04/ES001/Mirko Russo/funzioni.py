"""
📚 Modulo di Gestione Biblioteca Digitale

Ogni libro è rappresentato come un dizionario contenente le informazioni essenziali 
(titolo, autore, anno, disponibilità), e tutti i libri sono memorizzati all'interno di una lista.

🔹 Funzionalità principali:

- generate_id(library): Genera un ID univoco incrementale per un nuovo libro.
- add_book(library, title, author, year): Aggiunge un nuovo libro alla biblioteca.
- remove_book(library, book_id): Rimuove un libro dalla biblioteca dato il suo ID.
- search_book(library, key_word): Cerca libri per titolo o autore (ignorando maiuscole/minuscole).
- lend_book(library, book_id): Imposta un libro come "non disponibile" (prestato).
- return_book(library, book_id): Segna un libro come "disponibile".
- visualize_catalog(library): Mostra tutti i libri ordinati per titolo, autore o anno.
- save_data(library, file_name): Salva la biblioteca in formato JSON su file.
- upload_data(file_name): Carica una biblioteca da un file JSON.
- show_statistics(library): Mostra statistiche sul numero totale di libri, prestati e disponibili.

💡 Note:
- Tutte le operazioni sono eseguite su una lista di dizionari.
- La disponibilità dei libri è gestita tramite il campo booleano "available".
- I dati possono essere salvati e ricaricati in formato JSON.
- È presente gestione base degli errori per ID non trovati o file mancanti.

"""

import json
import re

def generate_id(library):
    """
    Genera un ID univoco per un nuovo libro.

    Parameters:
        library (list): Lista dei dizionari contenenti i libri.

    Returns:
        int: ID incrementale basato sull'ID massimo già presente.
    """
    return max((book['id'] for book in library), default=0) + 1

def add_book(library, title, author, year):
    """
    Aggiunge un nuovo libro alla biblioteca.

    Parameters:
        library (list): Lista dei libri.
        title (str): Titolo del libro.
        author (str): Autore del libro.
        year (int): Anno di pubblicazione.

    Returns:
        None
    """
    book = {
        'id' : generate_id(library),
        "title" : title,
        "author" : author,
        "year" : year,
        "available" : True,
    }
    library.append(book)
    
def remove_book(library, book_id):
    """
    Rimuove un libro dalla biblioteca dato il suo ID.

    Parameters:
        library (list): Lista dei libri.
        book_id (int): ID del libro da rimuovere.

    Returns:
        bool: True se il libro è stato rimosso, False altrimenti.
    """
    for book in library:
        if book["id"] == book_id:
            library.remove(book)
            return True
    print(f"Il libro con {book_id} non è stato trovato!")
    return False

def search_book(library, key_word):
    """
    Cerca libri per titolo o autore.

    Parameters:
        library (list): Lista dei libri.
        key_word (str): Parola chiave da cercare (case-insensitive).

    Returns:
        list: Lista di libri che corrispondono alla parola chiave.
    
    ---- VERSIONE SENZA REGEX ----
    keyword = key_word.lower()
    results = [
        book for book in library
        if keyword in book['title'].lower() or keyword in book["author"].lower()
    ]
    return results
    """
    pattern = re.compile(key_word, re.IGNORECASE)
    results = [
        book for book in library
        if pattern.search(book['title']) or pattern.search(book['author'])
    ]
    return 

def lend_book(library, book_id):
    """
    Segna un libro come non disponibile (prestato).

    Parameters:
        library (list): Lista dei libri.
        book_id (int): ID del libro da prestare.

    Returns:
        bool: True se il libro è stato prestato, False altrimenti.
    """
    for book in library:
        if book["id"] == book_id:
            if book["available"]:
                book["available"] = False
                return True
            else:
                print("Il libro è già stato dato in prestito")
    print(f"Il libro con {book_id} non è stato trovato!")
    return False

def return_book(library, book_id):
    """
    Segna un libro come disponibile (restituito).

    Parameters:
        library (list): Lista dei libri.
        book_id (int): ID del libro da restituire.

    Returns:
        bool: True se la restituzione è avvenuta, False se ID non trovato.
    """
    for book in library:
        if book["id"] == book_id:
            book["available"] = True
            return True
    print(f"Il libro con {book_id} non è stato trovato!")
    

def visualize_catalog(library):
    """
    Mostra i libri presenti nella biblioteca, ordinati per titolo, autore o anno.

    Parameters:
        library (list): Lista dei libri.

    Returns:
        None
    """
    options = ["title", "author", "year"]
    sorting = input(f"Scegli il criterio di visualizzazzione del catalago ({', '.join(options)})\n").strip().lower()
    
    if not library:
        print("La biblioteca è vuota.")
        return
    if sorting not in options:
        print("Criterio non valido. I libri saranno visualizzati per Titolo!")
        sorting = "title"
        
    sorted_library = sorted(library, key=lambda b: b[sorting])
    
    for book in sorted_library:
        book_state = "Disponibile" if book["available"] else "In prestito"
        print(f"{book['id']}: {book['title']} - {book['author']} ({book['year']}) - {book_state}")

    
    
def save_data(library, file_name):
    """
    Salva la biblioteca su file in formato JSON.

    Parameters:
        library (list): Lista dei libri.
        file_name (str): Nome del file su cui salvare i dati.

    Returns:
        None
    """
    try:
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(library, f, ensure_ascii=False, indent=2)
        print(f"Dati salvati correttamente in {file_name}")
    except Exception as e:
        print("Errore durante il salvataggio")
        
def upload_data(file_name):
    """
    Carica i dati della biblioteca da un file JSON.

    Parameters:
        file_name (str): Nome del file da cui leggere i dati.

    Returns:
        list: Lista dei libri caricati dal file, oppure lista vuota se errore.
    """
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            library = json.load(f)
        print(f"Dati caricati correttamente da {file_name}")
        return library
    except FileNotFoundError:
        print(f"File '{file_name}' non trovato")
        return []
    except Exception as e:
        print(f"Errore durante il caricamento: {e}")
        return []
    
def show_statistics(library):
    """
    Mostra statistiche sulla biblioteca:
    - Totale libri
    - Libri in prestito
    - Libri disponibili

    Parameters:
        library (list): Lista dei libri.

    Returns:
        None
    """
    total_books = len(library)
    borrowed = sum(1 for book in library if not book["available"])
    available = total_books - borrowed
    print(f"Libri totali: {total_books}")
    print(f"In prestito: {borrowed}")
    print(f"Disponibili: {available}")
