import json
import re

menu = """ 
0. Exit
1. Add Book
2. Remove Book
3. Search Book
4. Search Book regex
5. Borrow Book
6. Return Book
7. View Catalogue
8. Save Data
9. Upload Data
10. Stats
"""


# 1. 
# definizione della funzione per aggiungere un nuovo libro
def add_book(library: list, title: str, author: str, year: int):
    
    # se la libreria esiste cerco l'id maggiore e aggiungo 1
    if library:
        new_id = max(book["id"] for book in library) + 1
    else:
        # se la libreria non esiste assegna id = 1
        new_id = 1
        
    # creo il dizionario per il libro    
    new_book = {
        "id" : new_id,
        "title" : title,
        "author" : author,
        "year" : year,
        "available" : True
    }
    
    # aggiungo il libro alla biblioteca e lo stampo
    library.append(new_book)
    print(new_book)


# 2.
# definizione della funzione per rimuovere un libro dalla biblioteca
def remove_book(library: list, id: int):
    
    #try:
    book_found = False
    
    # ciclo per confrontare gli id dei libri con l'id dell'input
    for book in library:
        if book["id"] == id:
            book_found = True
            library.remove(book)
            print(f"Book '{book['title']}' deleted\n{"-" * 30}")
    # se non trova corrispondenze manda un messaggio di errore
    if not book_found:
        raise ValueError(f"No book found with ID {id}")
    
    #except ValueError as e:
    #    print(f"Error: {e}\n{"-" * 30}")


# 3.a
# definizione della funzione per cercare un libro
def search_book(library: list, keyword: str):
    
    #try: 
        # creo una lista con i risultati e trasformo la keyword in casefold
    results = []
    keyword = keyword.casefold()
    # ordino i libri
    sorted_library = sorted(library, key=lambda book: book["title"].casefold())
    
    # cerco i libri che contengono la keyword e li inserisco nella lista
    for book in sorted_library:
        if keyword in book["title"].casefold() or keyword in book["author"].casefold():
            results.append(book)
    # mostro la lista
    if results:    
        for book in results:
            print(f"""
ID: {book["id"]}
Title: {book["title"]}
Author: {book["author"]}
Year of Publication: {book["year"]}
Available: {"Yes" if book["available"] else "No"}
{"-" * 30}""")  
                
    # se la lista è vuota manda un errore
    else:
        raise ValueError(f"No books found for keyword {keyword}")

    #except ValueError as e:
    #    print(f"Error: {e}\n{"-" * 30}")
        
        
# 3.b        
# definizione della funzione avanzata per cercare un libro
def search_book_advanced(library: list, keyword: str):
    #try: 
    # Creo una lista con i risultati
    results = []
    
    # trasformo la keyword in casefold 
    keyword_pattern = re.compile(keyword, re.IGNORECASE)
    
    # ordino i libri per titolo 
    sorted_library = sorted(library, key=lambda book: book["title"].casefold())
    
    # cerco i libri che contengono la keyword usando le espressioni regolari
    for book in sorted_library:
        if re.search(keyword_pattern, book["title"]) or re.search(keyword_pattern, book["author"]):
            results.append(book)
    # mostro i risultati
    if results:    
        for book in results:
            print(f"""
ID: {book["id"]}
Title: {book["title"]}
Author: {book["author"]}
Year of Publication: {book["year"]}
Available: {"Yes" if book["available"] else "No"}
{"-" * 30}""")  
                
    # se la lista è vuota mando un errore
    else:
        raise ValueError(f"No books found for keyword '{keyword}'")

    #except ValueError as e:
    #    print(f"Error: {e}\n{"-" * 30}")


# 4.
# definizione della funzione per il prestito dei libri
def borrow_book(library: list, id: int):
    
    #try:
    # inizializzo la variabile book_found
    book_found = False
    
    # cerco il libro nella biblioteca
    for book in library:
        if book["id"] == id:
            book_found = True # se trova il libro 
            
            # se il libro è disponibile
            if book["available"]:
                book["available"] = False # segno che il libro non è più disponibile
                print(f"'{book['title']}' has been borrowed\n{"-" * 30}")
            else:
                print(f"Book '{book['title']}' is already borrowed\n{"-" * 30}")
    
    # se il libro non viene trovato
    if not book_found:
        raise ValueError(f"No book found with ID {id}\n")

    #except ValueError as e:
    #    print(f"Error: {e}\n{"-" * 30}")


# 5.
# definizione della funzione per la restituzione del libro 
def return_book(library: list, id: int):
    #try:
    # inizializzo la variabile book_found
    book_found = False 
    # cerco il libro nella biblioteca
    for book in library:
        if book["id"] == id:
            book_found = True
            # se il libro è già disponibile, non è stato preso in prestito
            if book["available"]:
                print(f"Book '{book['title']}' is already available\n{"-" * 30}")
            else:
                # segnalo che il libro è stato restituito e ora è disponibile
                book["available"] = True
                print(f"Book '{book['title']}' has been returned and is now available\n{"-" * 30}")
            break  # esco dal ciclo
    if not book_found:
        raise ValueError(f"No book found with ID {id}")

    #except ValueError as e:
    #    print(f"Error: {e}\n{"-" * 30}")
        
   
# 6.      
# definizione della funzione per visualizzare il catalogo
def view_catalogue(library: list):
    
    sorted_library = sorted(library, key=lambda book: book["title"].casefold())
    
    for book in sorted_library:
        print(f"""
ID: {book["id"]}
Title: {book["title"]}
Author: {book["author"]}
Year of Publication: {book["year"]}
Available: {"Yes" if book["available"] else "No"}
{"-" * 30}""")  
        
        
# 7. 
# definizione della funzione per salvare la biblioteca
def save_data(library: list, filename: str):
    
    # apro il file in modalità scrittura (crea il file se non esiste)
    with open(filename, 'w', encoding='utf-8') as file:
        
        # scrivo la lista della biblioteca nel file JSON
        json.dump(library, file, ensure_ascii=False, indent=4)
        print(f"Library data has been saved to {filename}\n{"-" * 30}")


# 8. 
# definizione della funzione per caricare una biblioteca
def upload_data(filename: str):
    # apro il file in modalità lettura
    with open(filename, 'r', encoding='utf-8') as file:
        
        # carico i dati JSON dal file e li converto in una lista di dizionari
        library = json.load(file)
        
        print(f"Library data has been loaded from {filename}\n{"-" * 30}")
        return library
        

# 9.    
# statistiche sui libri
def stats(library: list):
    
    n_books = 0
    n_books_borrowed = 0
    
    for book in library:
        n_books += 1
        if book["available"] == False:
            n_books_borrowed +=1
            
    n_books_available = n_books - n_books_borrowed
            
    print(f""" 
Number of books: {n_books}
Number of borrowed books: {n_books_borrowed}
Number of available books: {n_books_available}""")
            
            
library = []
add_book(library, "Il nome della rosa", "Umberto Eco", 1980)
add_book(library, "1984", "George Orwell", 1949)
add_book(library, "Orgoglio e pregiudizio", "Jane Austen", 1813)
add_book(library, "Il piccolo principe", "Antoine de Saint-Exupéry", 1943)
add_book(library, "Cent'anni di solitudine", "Gabriel García Márquez", 1967)

from enum import Enum

class MenuItem(Enum):
    EXIT = 0
    ADD_BOOK = 1
    REMOVE_BOOK = 2
    SEARCH_BOOK = 3
    SEARCH_BOOK_REGEX = 4
    BORROW_BOOK = 5
    RETURN_BOOK = 6
    VIEW_CATALOGUE = 7
    SAVE_DATA = 8
    UPLOAD_DATA = 9
    STATS = 10


while(True):
    print(menu)
    
    choice = int(input("Choose a number: "))
    
    try: 
        match choice:
            case MenuItem.ADD_BOOK.value: 
                inp_title = input("Title: ")
                inp_author = input("Author: ")
                inp_year = int(input("Year: "))
                add_book(library, inp_title, inp_author, inp_year)

            case MenuItem.REMOVE_BOOK.value:
                inp_id = int(input("ID: "))
                remove_book(library, inp_id)

            case MenuItem.SEARCH_BOOK.value:
                inp_keyword = input("Keyword: ")
                search_book(library, inp_keyword)

            case MenuItem.SEARCH_BOOK_REGEX.value: 
                inp_keyword = input("Keyword: ")
                search_book_advanced(library, inp_keyword)

            case MenuItem.BORROW_BOOK.value:
                inp_id = int(input("ID: "))
                borrow_book(library, inp_id)

            case MenuItem.RETURN_BOOK.value:
                inp_id = int(input("ID: "))       
                return_book(library, inp_id)

            case MenuItem.VIEW_CATALOGUE.value:
                view_catalogue(library)

            case MenuItem.SAVE_DATA.value: 
                save_data(library, "library.json")

            case MenuItem.UPLOAD_DATA.value:
                upload_data("library.json")

            case MenuItem.STATS.value:
                stats(library)

            case MenuItem.EXIT.value:
                break
            
            case _:
                print("Error")

    except ZeroDivisionError as e:
        print(e)
    except Exception as e: 
        print(f"Error: {e}\n{"-" * 30}")
         

print("Bye")
            

