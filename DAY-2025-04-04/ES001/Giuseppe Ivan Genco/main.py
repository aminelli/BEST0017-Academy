# Importo la libreria json per la gestione dei file .json
# Importo la libreria re per la ricerca avanzata con regex sulle stringhe
import json
import re

# Metodo per l'aggiunta di un libro alla libreria
# Genero un nuovo oggetto libro che aggiungerò alla libreria generando l'id automaticamente
def add_book(library, title, author, year):
    """
    Add a new book to the library.

    Args:
        library (list): The library to which the book will be added.
        title (str): The title of the book.
        author (str): The author of the book.
        year (int): The year the book was published.

    Returns:
        None
    """
    new_book = {
        "id": generate_id(library),
        "title": title,
        "author": author,
        "year": year,
        "available": True
    }
    library.append(new_book)
    print(f"Book '{title}' added successfully!")

# Metodo per la generazione di un di univoco alla creazione di un nuovo libro
# Genero un id univoco per ogni libro che creo stando attento agli id già presenti
def generate_id(library):
    """
    Generate a unique id for a new book.

    Args:
        library (list): The library to which the book will be added.

    Returns:
        int: The unique id for the new book.
    """
    
    id_list = [book["id"] for book in library]
    if len(id_list) < 1:
        return 1
    else:
        return max(id_list) + 1

# Metodo che rimuove un libro dalla libreria. 
# Si scorre tutta la libreria fino a quando non si becca
# l'id del libro che vogliamo eliminare e nel caso in cui lo troviamo quest'ultimo verrà eliminato.
# Nel caso in cui non esistano libri con l'id inserito viene stampato un messaggio in output che lo notifica
def remove_book(library, book_id):
    """
    Remove a book from the library by its id.

    Args:
        library (list): The library from which the book will be removed.
        book_id (int): The id of the book to be removed.

    Returns:
        None
    """
    for book in library:
        if book["id"] == book_id:
            library.remove(book)
            print(f"Book '{book['title']}' removed successfully!")
            return
    print("ID not found!")

# Metodo per la ricerca di uno o più libri.
# Creo la lista dei risultati con una list comprension che scorre tutti i libri ed inserisce nella
# lista result soltanto quelli che hanno nel titolo o nel autore la sottostringa "keyword".
# Se la lista result è vuota (quindi non abbiamo trovato alcun libro che contenga la nostra keyword)
# ritorniamo una stringa che ci notifica che non è stato trovato alcun libro
def search_book(library, keyword):
    """
    Search for one or more books in the library by a keyword.

    Args:
        library (list): The library to search.
        keyword (str): The keyword to search for.

    Returns:
        list or str: A list of books that match the keyword if any are found, otherwise a string indicating that no results were found.
    """
    results = [book for book in library if re.search(keyword, book["title"], re.IGNORECASE) or 
                 re.search(keyword, book["author"], re.IGNORECASE)]
    return results if len(results) < 1 else "No results found."

# Metodo per il prestito di un libro.
# Scorro la libreria ed in base all'id fornito cerco il libro, quando lo trovo imposto la disponibilità
# a  False. Se il libro non è disponibile stampo un messaggio che indica che il libro è già in prestito
# Nel caso in cui non si riesca a trovare un libro con l'Id fornito notifico che il libro non è stato trovato
def lend_book(library, book_id):
    """
    Lend a book from the library using its id.

    Args:
        library (list): The library from which the book will be lent.
        book_id (int): The id of the book to be lent.

    Returns:
        None
    """

    for book in library:
        if book["id"] == book_id:
            if book["available"]:
                book["available"] = False
                print(f"Book '{book['title']}' lent!")
            else:
                print("Book already lent!")
            return
    print("Book not found!")

# Metodo per la consegna di un libro in prestito
# Vado a scorrere di nuovo tutta la libreria fino a quando non trovo il libro con lo stesso id,
# nel momento in cui lo trovo vado ad impostare la disponibilità a true e stampo un messaggio.
# Nel caso in cui il libro con l'id inserito non venga trovato stampiamo un messaggio che lo notifica
def return_book(library, book_id):
    """
    Return a book to the library by its id.

    Args:
        library (list): The library to which the book will be returned.
        book_id (int): The id of the book to be returned.

    Returns:
        None
    """

    for book in library:
        if book["id"] == book_id:
            book["available"] = True
            print(f"Book '{book['title']}' returned!")
            return
    print("Book not found!")

# Metodo per la visualizzazione di tutti i libri della libreria
# Vado ad ordinare la lista Library con il metodo "sort()" utilizzando una labda che ordina
# sulla chiava passata come arogemenot della funzione. 
# Sorro sulla lista dei libri oridnati e li vado a stampare tutti modificando per ognuno
# la chiave "disponibilità" stampando "disponibile" se non è stato dato in prestite e "in prestito"
# se non fosse così.
def view_catalog(library, sort_by="title"):
    """
    Display all books in the library sorted by the specified attribute.

    Args:
        library (list): The library containing the books to be displayed.
        sort_by (str): The attribute by which to sort the books (default is "title").

    Returns:
        None
    """

    sorted_catalog = sorted(library, key=lambda x: x[sort_by])
    for book in sorted_catalog:
        status = "Available" if book["available"] else "Lent out"
        print(f"{book['id']}. {book['title']} - {book['author']} ({book['year']}) - {status}")

# Metodo per il salvaggio della liberia su file JSON
# Vado ad aprire il file json passato con argomento in sola scrittura per poi salvare la
# libreria su quel file.
def save_data(library, file_name):
    """
    Save the library to a JSON file.

    Args:
        library (list): The library to be saved.
        file_name (str): The name of the file to which the library will be saved.

    Returns:
        None
    """
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(library, f, indent=4, ensure_ascii=False)
    print("Data saved successfully!")

# Metodo per il caricamento della Libreria da file JSON
# Vado ad aprire il file json passato con argomento in sola lettura per poi trasformare il
# suo contenuto il un dizionario. Tutto ciò intercetta eventuali eccezzioni nel caso in cui il 
# file non esista e se succede crea una nuova libreria vuota restituendo lista vuota.
def load_data(file_name) -> list : 
    """
    Load the library from a JSON file.

    Args:
        file_name (str): The name of the file from which to load the library.

    Returns:
        list: The library loaded from the specified file, or an empty list if the file does not exist.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("File not found, starting a new library.")
        return []

# Metodo per la visualizazione delle statistiche della libreria
# Vado ad prendermi la lunghezza della lista Library per capire quanti libri ho nella libreria
# ed inoltre vado a creare una nuova lista che contiene tutti i libri in prestito, dopo aver fatto
# ciò ne prendo la lunghezza.
# Alla fine stampo la lunghezza della libreria, la lunghezza della lista dei libri in prestito e il
# totale dei libri disponibili al prestito
def library_statistics(library):
    """
    Print the total number of books in the library, the number of books that are currently
    lent out, and the number of books that are available for lending.

    Args:
        library (list): The library from which to gather the statistics.
    """
    total = len(library)
    lent_out = len([book for book in library if not book["available"]])
    print(f"Total books: {total}, Lent out: {lent_out}, Available: {total - lent_out}")

# Metodo che avvia il menu di gestione della libreria
def menu():
    library = load_data("library.json")
    while True:
        print("\nLibrary")
        print("1. Add Book")
        print("2. Remove Book")
        print("3. Search Book")
        print("4. Lend Book")
        print("5. Return Book")
        print("6. View Catalog")
        print("7. Show Statistics")
        print("8. Save and Exit")
        choice = input("Choose an option: ")
        
        match choice:
            case "1":
                title = input("Enter book title: ")
                author = input("Enter book author: ")
                year = input("Enter book year: ")
                add_book(library, title, author, year)
            case "2":
                book_id = int(input("Enter book ID to remove: "))
                remove_book(library, book_id)
            case "3":
                keyword = input("Enter keyword to search: ")
                results = search_book(library, keyword)
                print(results)
            case "4":
                book_id = int(input("Enter book ID to lend: "))
                lend_book(library, book_id)
            case "5":
                book_id = int(input("Enter book ID to return: "))
                return_book(library, book_id)
            case "6":
                order_by = input("Enter sorting key: ")
                view_catalog(library, order_by)
            case "7":
                library_statistics(library)
            case "8":
                save_data(library, "library.json")
                print("Exiting... Data saved.")
                break
            case _:
                print("Invalid choice, please try again.")


menu()
