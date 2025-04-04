import json
import re

def generate_id(biblioteca):
    """
    Genera un nuovo ID univoco per un libro, incrementando l'ID massimo esistente.
    
    Args:
        biblioteca (list): Lista dei libri nella biblioteca.
        
    Returns:
        int: ID univoco generato.
    """
    # Se la lista è vuota (nessun libro ancora presente)
    if not biblioteca:
        # Il primo ID sarà 1
        return 1
    # Altrimenti, troviamo l'ID massimo già presente e aggiungiamo 1
    return max(libro["id"] for libro in biblioteca) + 1

def add_book(library, title, author, year):
    """
    Aggiunge un nuovo libro alla biblioteca.
    
    Args:
        library (list): Lista dei libri.
        title (str): Titolo del libro.
        author (str): Autore del libro.
        year (int): Anno di pubblicazione.
    """
    new_book = {
        "id": generate_id(library),
        "title": title,
        "author": author,
        "year": year,
        "disponibile": True
    }
    
    # Aggiungiamo il dizionario del libro alla lista
    library.append(new_book)
    
    #stampo per confermare l'aggiunta del libro
    print(f'Libro aggiunto: {title} di {author} ({year})')

def remove_book(library, id_book):
    """
    Rimuove un libro dalla biblioteca dato il suo ID.
    
    Args:
        library (list): Lista dei libri.
        id_book (int): ID del libro da rimuovere.
    """
    # Cicliamo ogni libro nella lista
    for book in library:
        # Se troviamo l'ID corrispondente
        if book["id"] == id_book:
            # Rimuoviamo il libro dalla lista
            library.remove(book)
            print(f' Libro con ID {id_book} rimosso.')
            return
    
    # Se arriviamo qui, nessun libro aveva l'ID cercato
    print(f'Nessun libro trovato con ID {id_book}.')

# Funzione per cercare libri in base a una parola chiave (titolo o autore)
def search_book(library, keyword):
    """
    Cerca libri nella biblioteca per parola chiave in titolo o autore.
    
    Args:
        library (list): Lista dei libri.
        keyword (str): Parola chiave da cercare.
        
    Returns:
        list: Lista di libri che corrispondono alla ricerca.
    """
    
    # Converte la parola chiave in minuscolo per confronto case-insensitive
    keyword = keyword.lower()
    
    # Lista di libri che contengono la parola chiave nel titolo o nell'autore

    res = [
        book for book in library
        if keyword in book["title"].lower() or keyword in book["author"].lower()
    ]
    
    # Se la lista dei risultati è vuota
    if not res:
        print(f"Nessun libro contiene la parola {keyword}")
    else:
        print("Risultati delle corrispondenze: ")
        # Mostriamo tutti i risultati trovati
        for book in res:
            print(f'ID {book["id"]}: "{book["title"]}" di {book["author"]} ({book["year"]}) - {"Disponibile" if book["disponibile"] else "In prestito"}')
    # Restituisce la lista dei risultati trovati
    return res

# Funzione per prestare un libro (segna come non disponibile)
def lend_book(library, id_book):
    """
    Imposta un libro come non disponibile (prestato).
    
    Args:
        library (list): Lista dei libri.
        id_book (int): ID del libro da prestare.
    """
    for book in library:
        if book["id"] == id_book:
            # Se il libro è disponibile
            if book["disponibile"]:
                # Cambiamo lo stato a 'non disponibile'
                book["disponibile"] = False
                print(f'Libro "{book["title"]}" prestato con successo.')
            else:
                print(f'Il libro "{book["title"]}" è già in prestito.')
            return
    print(f'Nessun libro trovato con ID {id_book}.')

# Funzione per restituire un libro (segna come disponibile)
def return_book(library, id_book):
    """
    Imposta un libro come disponibile (restituito).
    
    Args:
        library (list): Lista dei libri.
        id_book (int): ID del libro da restituire.
    """
    for libro in library:
        if libro["id"] == id_book:
            if not libro["disponibile"]:
                # Se era in prestito cambiamo lo stato a disponibile
                libro["disponibile"] = True
                print(f'Libro "{libro["title"]}" restituito con successo.')
            else:
                print(f'Il libro "{libro["title"]}" non era in prestito.')
                #Già disponibile
            return
    print(f'Nessun libro trovato con ID {id_book}.')

def show_library(library):
    """
    Mostra l'elenco dei libri nella biblioteca, ordinati secondo il criterio scelto.
    
    Args:
        library (list): Lista dei libri.
    """
    if not library:
        print("La biblioteca non ha libri.")
        return
    
    # Richiede all'utente il criterio con cui ordinare i libri
    print("Come vuoi che ti mostri i libri?")
    print("1. Titolo")
    print("2. Autore")
    print("3. Anno")
    scelta_ordine = input("Scelta (1-3): ")

    # Ordina i libri in base alla scelta dell’utente e uso le lambda per farlo
    if scelta_ordine == "1":
        book_sorted = sorted(library, key=lambda x: x["title"].lower())
    elif scelta_ordine == "2":
        book_sorted = sorted(library, key=lambda x: x["author"].lower())
    elif scelta_ordine == "3":
        book_sorted = sorted(library, key=lambda x: x["year"])
    else:
        print("Scelta non valida. Mostro l'ordine originale.")
        book_sorted = library
        
    print("\nLibri della Biblioteca:")
    for book in book_sorted:
        stato_libro = "Disponibile" if book["disponibile"] else "In prestito"
        print(f'ID {book["id"]}: "{book["title"]}" di {book["author"]} ({book["year"]}) - {stato_libro}')

def save_data(library, nome_file):
    """
    Salva i dati della biblioteca in un file JSON.
    
    Args:
        library (list): Lista dei libri.
        nome_file (str): Nome del file in cui salvare i dati.
    """
    try:
        # Apre il file in scrittura
        with open(nome_file, "w", encoding="utf-8") as f:
            # Scrive il contenuto in formato leggibile
            json.dump(library, f, ensure_ascii=False, indent=4)
        print(f'Dati salvati in "{nome_file}".')
    except Exception as e:
        print(f'Errore durante il salvataggio: {e}')

# Funzione per caricare i dati della biblioteca da file JSON
def load_data(nome_file):
    """
    Carica i dati della biblioteca da un file JSON.
    
    Args:
        nome_file (str): Nome del file da cui caricare i dati.
        
    Returns:
        list: Lista dei libri caricati, oppure lista vuota se errore.
    """
    try:
        with open(nome_file, "r", encoding="utf-8") as f:
            # Carica il contenuto dal file
            biblioteca = json.load(f)
        print(f'Dati caricati da "{nome_file}".')
        return biblioteca
    except FileNotFoundError:
        # File non trovato
        print(f'Il file "{nome_file}" non esiste.')
        return []
    except json.JSONDecodeError:
        # Formato non valido
        print(f'Errore nella lettura del file JSON.')
        return []
    

def stats_library(library):
    """
        Calcola e mostra le statistiche della biblioteca.

        Args:
        library (list): Una lista di dizionari, dove ogni dizionario rappresenta un libro
                        con le chiavi "id", "title", "author", "year", "disponibile".

        Functionality:
            - Calcola il numero totale di libri nella biblioteca.
            - Conta quanti libri sono disponibili.
            - Calcola il numero di libri attualmente in prestito.
            - Stampa tutte queste informazioni all'utente
        """
    # Conteggio totale dei libri
    tot = len(library) 
    
    #variabile che conterrà i libri disponibili
    disp = 0
    
    #conto i libri disponibili
    for book in library:
        if book["disponibile"]:
            disp += 1 
    
    #calcolo quelli in prestito come la differenza tra il totale e quelli disponibili
    in_prestito = tot - disp
    
    print(" STATISTICHE DELLA BIBLIOTECA")
    print(f"Totale libri: {tot}")
    print(f"Libri disponibili: {disp}")
    print(f"Libri in prestito: {in_prestito}")
    
def search_book_regex(library):
    """
    Esegue una ricerca avanzata di libri nella biblioteca utilizzando espressioni regolari (regex).
    L'utente può usare simboli speciali per cercare titoli o autori in modo flessibile.

    Args:
        library (list): La lista dei libri presenti nella biblioteca.

    Returns:
        list: Una lista di libri che corrispondono al pattern di ricerca fornito.
    """
    print("\n RICERCA AVANZATA")
    print("Rendi la tua ricerca più potente:")
    print("  .    -> un qualsiasi carattere singolo")
    print("  .*   -> qualsiasi sequenza di caratteri")
    print("  ^    -> inizio stringa")
    print("  $    -> fine stringa")
    print("Esempio: ^Il.* → trova titoli che iniziano con 'Il'")

    pattern = input("\nInserisci il pattern di ricerca: ")

    try:
        # Compila il pattern inserito dall'utente come espressione regolare e ignoro 
        # differenza tra maiuscole e minuscole
        regex = re.compile(pattern, re.IGNORECASE)  

        # Crea una lista di libri che corrispondono al pattern nel titolo o nell'autore
        risultati = [
            book for book in library
            if regex.search(book["title"]) or regex.search(book["author"])
        ]

        # Se ci sono risultati, li stampa uno per uno
        if risultati:
            print("\nRISULTATI TROVATI:")
            for book in risultati:
                # Determina lo stato del libro (Disponibile o In prestito)
                stato = "Disponibile" if book["disponibile"] else "In prestito"
                # Stampa le informazioni del libro trovato
                print(f'ID {book["id"]}: "{book["title"]}" di {book["author"]} ({book["year"]}) - {stato}')
        else:
            # Nessun risultato trovato per il pattern dato
            print(" Nessun libro trovato con questo pattern.")
            
        # Ritorna la lista dei libri trovati
        return risultati

    except re.error:
        # In caso di errore nella compilazione dell'espressione regolare (pattern non valido)
        print("Espressione regolare non valida. Controlla il pattern e riprova.")
        return []

def show_menu():
    """
        Stampa il menu principale delle operazioni disponibili per la gestione della biblioteca.
    """
    print("\n OPERAZIONI DISPONIBILI")
    print("1. Aggiungi libro")
    print("2. Rimuovi libro")
    print("3. Cerca libro (semplice)")
    print("4. Cerca libro (regex)")
    print("5. Presta libro")
    print("6. Restituisci libro")
    print("7. Visualizza libri")
    print("8. Salva libri su file")
    print("9. Carica libri da file")
    print("10. Mostra statistiche") 
    print("11. Esci")


def gestisci_menu():
    biblioteca = []  # Inizializziamo la biblioteca come lista vuota
    
    while True:
        show_menu()
        scelta = input("Seleziona un'opzione (1-11): ")
        
        if scelta == "1":
            print()
            titolo = input("Titolo: ")
            autore = input("Autore: ")
            anno = input("Anno di pubblicazione: ")
            try:
                anno = int(anno)
                add_book(biblioteca, titolo, autore, anno)
            except ValueError:
                print("Anno non valido.")
        
        elif scelta == "2":
            print()
            try:
                id_libro = int(input("ID del libro da rimuovere: "))
                remove_book(biblioteca, id_libro)
            except ValueError:
                print("Inserisci un numero valido.")

        elif scelta == "3":
            print()
            parola = input("Parola chiave per la ricerca: ")
            search_book(biblioteca, parola)

        elif scelta == "4":
            print()
            search_book_regex(biblioteca)

        elif scelta == "5":
            print()
            try:
                id_libro = int(input("ID del libro da prestare: "))
                lend_book(biblioteca, id_libro)
            except ValueError:
                print("Inserisci un numero valido.")
        
        elif scelta == "6":
            print()
            try:
                id_libro = int(input("ID del libro da restituire: "))
                return_book(biblioteca, id_libro)
            except ValueError:
                print("Inserisci un numero valido.")

        elif scelta == "7":
            print()
            show_library(biblioteca)

        elif scelta == "8":
            print()
            nome_file = input("Nome del file in cui salvare (es. biblioteca.json): ")
            save_data(biblioteca, nome_file)

        elif scelta == "9":
            print()
            nome_file = input("Nome del file da cui caricare (es. biblioteca.json): ")
            biblioteca = load_data(nome_file)

        elif scelta == "10":
            print()
            stats_library(biblioteca)

        elif scelta == "11":
            print()
            print("EXIT....")
            break

        else:
            print("Scelta non valida. Inserisci un numero da 1 a 11.")

# Avvia il menu
if __name__ == "__main__":
    gestisci_menu()
