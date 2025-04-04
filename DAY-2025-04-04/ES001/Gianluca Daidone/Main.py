import json
import re

nextID = 1

def addBook(library, title, author, year):
    """
    Adds a new book to the library.
    
    Args:
        library (list): list of dictionary containing book details
        title (str): title of the book
        author (str): author of the book
        year (int): year of publication
    """
    # Aggiungo un nuovo libro alla libreria e incremento nextID
    global nextID
    new_book = {
        "id": nextID,
        "title": title,
        "author": author,
        "year": year,
        "availability": True,
    }
    nextID += 1
    library.append(new_book)
    print(f"Book '{title}' added to the library.")

def deleteBook(library, bookID):
    """
    Deletes a book from the library by its ID.

    Args:
        library (list): list of dictionary containing book details
        bookID (int): identifier of the book to be deleted
    """
    # Cerco il libro da eliminare nella libreia in base all'ID
    # Se lo trovo lo elimino e stampo un messaggio di conferma
    # Se non lo trovo stampo un messaggio di errore
    for book in library:
        if book["id"] == bookID:
            library.remove(book)
            print(f"Book '{book['title']}' removed from the library.")
            return
    print("Book not found.")

def searchBook(library, keyword):
    """
    Searches for books in the library by title or author.

    Args:
        library (list): list of dictionary containing book details
        keyword (str): keyword to search for in title or author

    Returns:
        list: list of books matching the search criteria
    """
    # Cerco i libri nella libreria in base al titolo o all'autore
    try:
        # Compilo l'espressione regolare per la ricerca
        # Potrebbe generare un'eccezione se l'espressione non è valida
        pattern = re.compile(keyword, re.IGNORECASE)
    except re.error:
        print("Invalid search pattern.")
        return []
    
    return [
        book for book in library
        if pattern.search(book["title"]) or pattern.search(book["author"])
    ]

def borrowBook(library, bookID):
    """
    Borrows a book from the library by its ID.

    Args:
        library (list): list of dictionary containing book details
        bookID (int): identifier of the book to be borrowed
    """
    # Cerco il libro da prendere in prestito nella libreria in base all'ID
    for book in library:
        if book["id"] == bookID:
            if book["availability"]:
                book["availability"] = False
                print(f"You have borrowed '{book['title']}'.")
            else:
                print(f"'{book['title']}' is currently unavailable.")
            return
    print("Book not found.")

def returnBook(library, bookID):
    """
    Returns a book to the library by its ID.

    Args:
        library (list): list of dictionary containing book details
        bookID (int): identifier of the book to be returned
    """
    # Cerco il libro da restituire nella libreria in base all'ID
    for book in library:
        if book["id"] == bookID:
            if not book["availability"]:
                book["availability"] = True
                print(f"You have returned '{book['title']}'.")
            else:
                print(f"'{book['title']}' was not borrowed.")
            return
    print("Book not found.")

def displayBooks(library, sortBy="id"):
    """
    Displays all books in the library.

    Args:
        library (list): list of dictionary containing book details
    """
    # Controllo se la libreria è vuota e stampo un messaggio di errore
    if not library:
        print("No books in the library.")
        return
    
    # Stampo la lista dei libri ordinati in base al campo specificato
    print(f"{'ID':<5} {'Title':<40} {'Author':<40} {'Year':<5} {'Availability':<15}")
    for book in sorted(library, key=lambda b: b[sortBy]):
        availability = "Available" if book["availability"] else "Not Available"
        print(
            f"{book['id']:<5} {book['title']:<40} {book['author']:<40} {book['year']:<5} {availability:<15}"
        )

def saveLibrary(library, filename="library.json"):
    """
    Saves the library to a JSON file.

    Args:
        library (list): list of dictionary containing book details
        filename (str, optional): filename to save the library. Defaults to "library.json".
    """
    global nextID
    # Creo un dizionario con la libreria e il prossimo ID
    data = {
        "library": library,
        "nextID": nextID,
    }
    
    # Apro il file in scrittura e salvo i dati in formato JSON
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
    print("Library saved to file.")

def loadLibrary(filename="library.json"):
    """
    Loads the library from a JSON file.

    Args:
        filename (str, optional): filename to load the library from. Defaults to "library.json".

    Returns:
        tuple: library (list), nextID (int) 
    """
    try:
        # Apro il file in lettura e carico i dati in formato JSON
        # Se il file non esiste, restituisco una libreria vuota e nextID = 1
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
        print("Library loaded from file.")
        return data["library"], data["nextID"]
    except FileNotFoundError:
        print("No saved library found. Starting with an empty library.")
        return [], 1

def displayStatistics(library):
    """
    Displays statistics about the library, including total number of books 
    and the number of borrowed books.

    Args:
        library (list): List of dictionaries containing book details.
    """
    # Numero totale di libri
    totalBooks = len(library)  
    # Libri presi in prestito
    borrowedBooks = len([book for book in library if not book["availability"]])  
    
    print(f"Total number of books: {totalBooks}")
    print(f"Number of borrowed books: {borrowedBooks}")
    print(f"Number of available books: {totalBooks - borrowedBooks}")


def menu():
    """
    Displays the menu options for the library management system.

    Returns:
        str: user's choice from the menu
    """
    print("Library Management System")
    print("1. Add Book")
    print("2. Delete Book")
    print("3. Search Book")
    print("4. Borrow Book")
    print("5. Return Book")
    print("6. Display Books")
    print("7. Display Library Statistics")
    print("0. Exit")
    choice = input("Enter your choice: ")
    return choice


def main():
    """
    Main function to run the library management system.
    """
    
    global nextID
    # Carica la libreria esistente o inizia con una nuova libreria
    # Se inizia una nuova libreria, nextID sarà 1
    library, nextID = loadLibrary("library.json")
    
    while True:
        # Mostra il menu e ottieni la scelta dell'utente
        choice = menu()
        match choice:
            # 1. Aggiungi libro
            case "1":
                title = input("Enter book title: ")
                author = input("Enter book author: ")
                year = int(input("Enter publication year: "))
                addBook(library, title, author, year)
                
            # 2. Elimina libro
            case "2":
                bookID = int(input("Enter book ID to delete: "))
                deleteBook(library, bookID)
                
            # 3. Cerca libro
            case "3":
                keyword = input("Enter title or author to search: ")
                results = searchBook(library, keyword)
                if results:
                    displayBooks(results)
                else:
                    print("No matching books found.")

            # 4. Prendi in prestito libro
            case "4":
                bookID = int(input("Enter book ID to borrow: "))
                borrowBook(library, bookID)

            # 5. Restituisci libro
            case "5":
                bookID = int(input("Enter book ID to return: "))
                returnBook(library, bookID)

            # 6. Mostra libri
            case "6":
                print("Sort by: id, title, author, year")
                sortKey = input("Enter sorting field: ").strip().lower()
                if sortKey not in ("id", "title", "author", "year"):
                    print("Invalid sort key. Defaulting to 'id'.")
                    sortKey = "id"
                displayBooks(library, sortBy=sortKey)
                
            # 7. Mostra statistiche
            case "7":
                displayStatistics(library)

            # 0. Esci
            case "0":
                # Salva la libreria su file e esci
                saveLibrary(library, "library.json")
                print("Exiting the program.")
                return

            case _:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()