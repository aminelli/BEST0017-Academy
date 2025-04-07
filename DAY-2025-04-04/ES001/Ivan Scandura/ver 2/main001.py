import json
import re
import os

def clear_screen():
    """
    Pulisce lo schermo della console.
    """
    # Verifica il sistema operativo e usa il comando appropriato per pulire lo schermo
    os.system("cls" if os.name == "nt" else "clear")

# Inizializza l'ID per i nuovi libri
next_id = 1

def add_book(library, title, author, year):
    """
    Aggiunge un nuovo libro alla biblioteca.

    Args:
        library (list): Lista di dizionari che rappresentano i libri nella biblioteca.
        title (str): Titolo del libro da aggiungere.
        author (str): Autore del libro.
        year (int): Anno di pubblicazione del libro.

    Returns:
        None
    """
    # Usa la variabile globale next_id
    global next_id
    book = {
        "id": next_id,
        "title": title,
        "author": author,
        "year": year,
        "available": True
    }
    # Aggiunge il libro alla lista della biblioteca
    library.append(book)
    # Incrementa l'ID per il prossimo book
    next_id += 1
    print(f"Libro '{title}' aggiunto con ID {book['id']}.")

def remove_book(library, book_id):
    """
    Rimuove un libro dalla biblioteca utilizzando il suo ID.

    Args:
        library (list): Lista di dizionari che rappresentano i libri nella biblioteca.
        book_id (int): ID del libro da rimuovere.

    Returns:
        None
    """
    founded = False
    # Itera su ogni libro nella biblioteca
    for book in library:
        # Se l'ID del libro corrisponde
        if book["id"] == book_id:
            # Rimuove il libro dalla lista
            library.remove(book)
            print(f"book ID {book_id} rimosso.")
            founded = True
            break
    if not founded:
        # Se l'ID non esiste, mostra un errore
        print("Libro non trovato!")

def search_book(library, keyword):
    """
    Cerca un libro nella biblioteca per titolo o autore.

    Args:
        library (list): Lista di dizionari che rappresentano i libri nella biblioteca.
        keyword (str): Parola chiave per la ricerca (può essere parte del titolo o dell'autore).

    Returns:
        None
    """
    # La list comprehension in Python è una sintassi compatta per creare nuove 
    # liste applicando un’espressione a ciascun elemento di una sequenza 
    # (come una lista, un intervallo, un dizionario, ecc.). Consente di scrivere 
    # cicli for in modo più conciso e leggibile, ed è utile quando si vuole 
    # costruire una lista basata su un’altra lista (o qualsiasi altro oggetto 
    # iterabile) applicando un’operazione a ciascun elemento.
    # Vantaggi della List Comprehension:
    # Più compatta: Permette di scrivere il codice in modo conciso.
    # Più leggibile: Riduce la necessità di scrivere loop espliciti e rendendo 
    # il codice più leggibile.
    # Più efficiente: Può essere più veloce rispetto ad un ciclo for tradizionale.
    # Questa è una list comprehension che itera su ogni elemento della lista library.
    # Filtra i libri che contengono la parola chiave nel titolo o nell'autore
    results = [book for book in library if keyword.lower() in book["title"].lower() or keyword.lower() in book["author"].lower()]
    print_books(results)

def advanced_search(library):
    """
    Esegue una ricerca avanzata nella biblioteca utilizzando un'espressione regolare.

    Args:
        library (list): Lista di dizionari che rappresentano i libri nella biblioteca.
        pattern (str): Espressione regolare per la ricerca.

    Returns:
        None
    """
    if not library:
        print("Nessun libro presente! Nessuna ricerca possibile!")
        return

    #.strip() rimuove gli spazi vuoti (whitespace) all’inizio e alla fine della stringa inserita.
    #query = input("Inserisci una parola o parte del titolo/autore/anno da cercare: ").strip()
    #if not query:
        #print("Ricerca annullata: nessun termine inserito.")
        #return
    # La funzione re.compile() serve a compilare un’espressione regolare in un 
    # pattern che può essere utilizzato per eseguire ricerche multiple. 
    # In altre parole, crea un oggetto che rappresenta un’espressione regolare 
    # precompilata, che può essere utilizzata per cercare, sostituire, o dividere 
    # il testo in modo più efficiente.
    # La funzione re.escape() prende una stringa (in questo caso query) e 
    # restituisce una versione della stringa dove tutti i caratteri speciali 
    # dell’espressione regolare (come ., *, +, ?, ecc.) vengono “scappati”,
    # cioè preceduti dal carattere di escape \
    #pattern = re.compile(re.escape(query), re.IGNORECASE)
    

    #results = []
    #for book in library:
        #if (
            #pattern.search(book["title"])
            #or pattern.search(book["author"])
            #or pattern.search(str(book["year"]))
        #):
            #results.append(book)

    #if results:
        # Usa enumerate() per ottenere sia l’indice (i) che l’elemento (book) 
        # dalla lista results.
        # start=1 fa partire la numerazione da 1 invece che da 0.
        #for i, book in enumerate(results, start=1):
            #print(f"{i}. {book['title']} - {book['author']} ({book['year']}) {'Disponibile' if book['available'] else 'In prestito'}")
    #else:
        #print("Nessun risultato trovato!")
        
    #Cerca libri pubblicati tra il 1800 e il 1899
    """
    r": Questo è un prefisso che indica una raw string in Python. Le raw string 
    non interpretano i caratteri di escape (come \n, \t, ecc.) come normali 
    stringhe, quindi tutto ciò che segue viene preso letteralmente. Ad esempio, 
    in una normale stringa, d rappresenterebbe un carattere di escape, mentre in 
    una raw string d viene interpretato come un carattere di espressione regolare 
    (un numero).
	18: Questi sono i caratteri fissi “18”, che verranno cercati esattamente nel 
    testo.
    d{2}: Qui:
    d è un metacarattere che rappresenta qualsiasi cifra (equivalente a [0-9]).
	{2} è un quantificatore che indica che la parte precedente (d) deve
    apparire esattamente due volte. Quindi, questa parte della regex cerca due 
    cifre consecutive.
    """
    pattern = re.compile(r"18\d{2}", re.IGNORECASE)
    
    # Lista per i risultati
    results = []
    
    for book in library:
        if (pattern.search(book["title"]) or
            pattern.search(book["author"]) or
            pattern.search(str(book["year"]))):
            results.append(book)
            
    # Mostra i risultati
    if results:
        print("Libri trovati pubblicati nell'Ottocento:")
        for book in results:
            print(f"- {book['title']} di {book['author']} ({book['year']})")
    else:
        print("Nessun libro trovato pubblicato tra il 1800 e il 1899.")

def lend_book(library, book_id):
    """
    Segna un libro come "in prestito" se è disponibile.

    Args:
        library (list): Lista di dizionari che rappresentano i libri nella biblioteca.
        book_id (int): ID del libro da prestare.

    Returns:
        None
    """
    founded = False
    # Itera su ogni libro nella biblioteca
    for book in library:
        # Se l'ID del libro corrisponde
        if book["id"] == book_id:
            # Se il libro è disponibile
            if book["available"]:
                # Segna il libro come in prestito
                book["available"] = False
                print(f"Libro ID {book_id} ora è in prestito.")
                founded = True
                break
            else:
                # Se il libro non è disponibile
                print("Libro già in prestito!")
                founded = True
                break
            # Esce dalla funzione
    if not founded:
        print("Libro non trovato!")

def return_book(library, book_id):
    """
    Segna un libro come disponibile dopo la restituzione.

    Args:
        library (list): Lista di dizionari che rappresentano i libri nella biblioteca.
        book_id (int): ID del libro da restituire.

    Returns:
        None
    """
    founded = False
    # Itera su ogni libro nella biblioteca
    for book in library:
        # Se l'ID del libro corrisponde
        if book["id"] == book_id:
            # Segna il libro come disponibile
            book["available"] = True
            print(f"Libro ID {book_id} restituito.")
            founded = True
            break
    # Se l'ID non esiste
    if not founded:
        # Se l'ID non esiste, mostra un errore
        print("Libro non trovato!")

def view_catalog(library, sort_key=None):
    """
    Mostra tutti i libri nella biblioteca, con opzione di ordinamento.

    Args:
        library (list): Lista di dizionari che rappresentano i libri nella biblioteca.
        sort_key (str, optional): Chiave per ordinare i libri (es. "title", "author", "year"). Default è None.

    Returns:
        None
    """
    # Se è stata fornita una chiave di ordinamento
    if sort_key:
        try:
            # La funzione lambda consente di estrarre il valore del campo indicato 
            # da sort_key per ogni elemento della lista.
            # Per esempio, se sort_key è "title", la lista verrà ordinata per il 
            # titolo di ciascun libro. Puoi usare qualsiasi campo presente nei 
            # dizionari dei libri (come title, author, year).
            # La b nella funzione lambda è un nome arbitrario per rappresentare 
            # ogni singolo elemento della lista su cui la funzione di ordinamento 
            # sta operando. In questo caso, ogni elemento della lista library è un 
            # dizionario che rappresenta un libro, e b rappresenta ciascun libro 
            # durante il processo di ordinamento.
            library = sorted(library, key=lambda b: b[sort_key])
        # Se la chiave di ordinamento non esiste nei libri
        except KeyError:
            print("Chiave di ordinamento non valida!")
    print_books(library)

def print_books(books):
    """
    Stampa l'elenco dei libri in un formato leggibile.

    Args:
        books (list): Lista di dizionari che rappresentano i libri da stampare.

    Returns:
        None
    """
    # Se la lista è vuota
    if not books:
        print("Nessun libro trovato!")
    # Itera su ogni libro
    for book in books:
        # Mostra lo stato del libro (disponibile o in prestito)
        status = "Disponibile" if book["available"] else "In prestito"
        print(f"ID: {book['id']} | {book['title']} di {book['author']} ({book['year']}) - {status}")

def save_data(library, filename):
    """
    Salva i dati della biblioteca su un file JSON.

    Args:
        library (list): Lista di dizionari che rappresentano i libri da salvare.
        filename (str): Nome del file dove salvare i dati.

    Returns:
        None
    """
    try:
        # Apre il file in modalità scrittura
        with open(filename, "w") as file:
            # La funzione json.dump() è utilizzata per serializzare (scrivere) 
            # un oggetto Python in un file JSON.
            # indent=4: È un parametro opzionale che controlla il formato di 
            # indentazione nel file JSON.
            # L’argomento 4 indica che ogni livello di indentazione (ovvero, 
            # la distanza tra gli oggetti e le righe di JSON) sarà di 4 spazi. 
            # In questo modo, il file JSON risultante sarà ben formattato e 
            # leggibile (un formato “pretty print”). Se non fornisci questo 
            # parametro, il JSON sarà scritto in formato “compresso”, senza 
            # spazi extra.
            json.dump(library, file, indent=4)
        print(f"Dati salvati in '{filename}'.")
    # Se c'è un errore durante il salvataggio
    except Exception as e:
        print(f"Errore nel salvataggio del file JSON: {e}")

def load_data(filename):
    """
    Carica i dati della biblioteca da un file JSON.

    Args:
        filename (str): Nome del file da cui caricare i dati.

    Returns:
        list: La lista dei libri caricata dal file JSON.
    """
    global next_id
    try:
        # Apre il file in modalità lettura
        with open(filename, "r") as file:
            # Carica i dati dal file JSON
            library = json.load(file)
            if library:
                # Imposta next_id come l'ID più alto + 1
                next_id = max(book["id"] for book in library) + 1
            print(f"Dati caricati da '{filename}'.")
            return library
    # Se il file non esiste
    except FileNotFoundError:
        print("File non trovato!")
        # Restituisce una lista vuota
        return []
    # Se c'è un errore nel file JSON
    except json.JSONDecodeError:
        print("Errore nel file JSON!")
        # Restituisce una lista vuota
        return []

from collections import defaultdict
# Funzione con statistiche aggiuntive sulla biblioteca
def show_stats(library):
    """
    Mostra le statistiche sulla biblioteca: totale libri, in prestito e disponibili 
    e statistiche avanzate, inclusi i libri per autore,
    il libro più vecchio, il libro più recente, e altri dati utili.
    Args:
        library (list): Lista di dizionari che rappresentano i libri.

    Returns:
        None
    """
    if not library:
        # Se la biblioteca è vuota, mostra un messaggio di avviso
        print("Il catalogo è vuoto. Nessuna statistica disponibile.")
        return
    total = len(library)
    # Questa è una list comprehension, un costrutto che permette di creare una 
    # lista in modo compatto.
    # b rappresenta ogni singolo libro (un dizionario) all’interno della lista 
    # library. La list comprehension itera su ogni libro nella lista library.
    # if not b["available"]: è un filtro che seleziona solo i libri che non sono 
    # disponibili. 
    lent = len([b for b in library if not b["available"]])
    available = total - lent
    
    # Numero di libri per autore
    # La riga authors_count = defaultdict(int) crea un dizionario con valori di 
    # tipo intero predefiniti (int) utilizzando la classe defaultdict della 
    # libreria collections di Python.
    # defaultdict(int): defaultdict è una sottoclasse del dizionario (dict) 
    # che permette di specificare un valore predefinito per ogni chiave che non 
    # esiste ancora nel dizionario. In questo caso, se provi ad accedere a una 
    # chiave che non esiste, Python creerà automaticamente quella chiave e 
    # le assegnerà un valore predefinito, che in questo caso è un intero con 
    # valore 0 (int() è equivalente a 0).
    authors_count = defaultdict(int)
    for book in library:
        authors_count[book["author"]] += 1
    
    # Il libro più vecchio e il più recente
    oldest_book = min(library, key=lambda b: b["year"], default=None)
    newest_book = max(library, key=lambda b: b["year"], default=None)
    
    # Statistiche per anno
    books_per_year = defaultdict(int)
    for book in library:
        books_per_year[book["year"]] += 1
    
    print(f"Statistiche biblioteca:")
    print(f"Totale libri: {total}")
    print(f"In prestito: {lent}")
    print(f"Disponibili: {available}")
    
    # Libri per autore
    print("\nLibri per autore:")
    for author, count in sorted(authors_count.items()):
        print(f"{author}: {count}")
    
    # Il libro più vecchio
    if oldest_book:
        print(f"Libro più vecchio: {oldest_book['title']} ({oldest_book['year']})")
    
    # Il libro più recente
    if newest_book:
        print(f"Libro più recente: {newest_book['title']} ({newest_book['year']})")
    
    # Libri per anno
    print("\nLibri per anno:")
    for year, count in sorted(books_per_year.items()):
        print(f"{year}: {count}")
        
    import csv
    # Salva le statistiche in un file CSV
    with open("library_statistics.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Statistic Type", "Detail", "Value"])
        writer.writerow(["Total Books", "", total])
        writer.writerow(["Books Lent", "", lent])
        writer.writerow(["Books Available", "", available])
        writer.writerow(["Oldest Book", "", f"{oldest_book['title']} ({oldest_book['year']})" if oldest_book else "N/A"])
        writer.writerow(["Newest Book", "", f"{newest_book['title']} ({newest_book['year']})" if newest_book else "N/A"])
        writer.writerow(["Books per Author", "", ""])
        # Ordinamento per il numero di libri (valore)
        #sorted_authors = sorted(authors_count.items(), key=lambda x: x[1], reverse=True)
        for author, count in sorted(authors_count.items()):
            writer.writerow(["", author, count])
        writer.writerow(["Books per Year", "", ""])
        for year, count in sorted(books_per_year.items()):
            writer.writerow(["", year, count])
    print("Statistiche salvate in 'library_statistics.csv'.")
        
def menu():
    """
    Mostra il menu principale per interagire con la biblioteca e gestire le operazioni.

    Args:
        None

    Returns:
        None
    """
    from enum import Enum
    # Definisce un enum per le opzioni del menu
    class MenuOption(Enum):
        ADD_BOOK = 1
        REMOVE_BOOK = 2
        SEARCH_BOOK = 3
        ADVANCED_SEARCH = 4
        LEND_BOOK = 5
        RETURN_BOOK = 6
        VIEW_CATALOG = 7
        SAVE_DATA = 8
        LOAD_DATA = 9
        SHOW_STATS = 10
        EXIT = 0
    
    # Inizializza la biblioteca come una lista vuota
    library = []
    while True:
        input("Premi Invio per continuare...")
        clear_screen()
        print("\n--- Biblioteca Digitale ---")
        print("1. Aggiungi libro")
        print("2. Rimuovi libro")
        print("3. Cerca libro (titolo o autore)")
        print("4. Ricerca avanzata: Libri pubblicati tra il 1800 e il 1899")
        print("5. Presta libro")
        print("6. Restituisci libro")
        print("7. Visualizza catalogo")
        print("8. Salva dati")
        print("9. Carica dati")
        print("10. Statistiche")
        print("0. Esci")
        try:
            choice = int(input("Scegli un'opzione: "))
            choice_enum = MenuOption(choice)
        except ValueError:
            print("Inserisci un numero valido.")
            input("Premi Invio per continuare...")
            continue
        except Exception:
            print("Scelta non valida. Riprova.")
            input("Premi Invio per continuare...")
            continue

        match choice_enum:
            case MenuOption.ADD_BOOK:
                clear_screen()
                title = input("Titolo: ")
                author = input("Autore: ")
                year = int(input("Anno: "))
                add_book(library, title, author, year)

            case MenuOption.REMOVE_BOOK:
                book_id = int(input("ID del libro da rimuovere: "))
                remove_book(library, book_id)

            case MenuOption.SEARCH_BOOK:
                keyword = input("Parola chiave: ")
                search_book(library, keyword)
                
            case MenuOption.ADVANCED_SEARCH:
                advanced_search(library)

            case MenuOption.LEND_BOOK:
                book_id = int(input("ID del libro da prestare: "))
                lend_book(library, book_id)

            case MenuOption.RETURN_BOOK: 
                book_id = int(input("ID del libro da restituire: "))
                return_book(library, book_id)

            case MenuOption.VIEW_CATALOG:
                sort_key = input("Ordinare per (title, author, year)? Premi Invio per nessun ordinamento: ")
                view_catalog(library, sort_key if sort_key else None)

            case MenuOption.SAVE_DATA:
                filename = input("Nome file per salvare: ")
                save_data(library, filename)

            case MenuOption.LOAD_DATA:
                filename = input("Nome file da caricare: ")
                library = load_data(filename)

            case MenuOption.SHOW_STATS:
                show_stats(library)

            case MenuOption.EXIT: 
                print("Uscita dal programma.")
                break

            case _:
                print("Scelta non valida. Riprova.")

# Avvio del programma
# Avvia il menu principale solo se il file è eseguito come script principale
# •	Python assegna alla variabile speciale __name__ il valore "__main__". 
# Quindi, se il file viene eseguito direttamente (ad esempio python script.py), 
# la condizione __name__ == "__main__" risulta vera ed esegue il blocco di codice 
# che segue. 
# In questo caso, il blocco di codice esegue la funzione menu(), che avvia 
# l’interazione dell’utente con il programma.
if __name__ == "__main__":
    menu()