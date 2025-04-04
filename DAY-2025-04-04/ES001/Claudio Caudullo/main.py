import json
import os
import re

def generate_new_id(library) -> int:
    """
        Genera un ID univoco per un nuovo libro.

        Args:
            library (list): Lista dei libri
        
        Return:
            int -> ID per il nuovo libro da inserire successivamente in biblioteca
    """    
    if not library:
        return 1
    
    #cerca il massimo id nella biblioteca, e lo ritorna aumentandoolo di 1
    return max(book["id"] for book in library) + 1 

def add_book(library, title, author, year):
    """
        Aggiunge un nuovo libro alla biblioteca con un ID univoco.

        Args:
            library (list): Lista dei libri
            title (string): Titolo del libro da aggiungere
            author (string): Autore del libro da aggiungere
            year (number): Anno del libro da aggiungere
    """    
    new_book = {
        "id": generate_new_id(library),
        "title": title,
        "author": author,
        "year": year,
        "available": True
    }
    library.append(new_book)
    print("✅ Libro aggiunto con successo!")

def remove_book(library, id_book):
    """
        Rimuove un libro dal catalogo dato il suo ID.
        
        Args:
            library (list): Lista dei libri
            id_book (int): ID del libro da eliminare
    """    
    initial_len = len(library)

    #mette nella biblioteca tutti i libri che non hanno come id l'id_book passato come argomento
    library[:] = [book for book in library if book["id"] != id_book] 

    #controlla se la lunghezza della biblioteca è cambiata
    if len(library) == initial_len:
        print(f"❌ Nessun libro trovato con ID {id_book}.")

def search_book(library, key_word) -> list:
    """
        Cerca un libro per titolo o autore e restituisce i risultati trovati.
        
        Args:
            library (list): Lista dei libri
            key_word (string): Stringa da utilizzare per la ricerca del libro

        Return:
            list -> Lista dei libri che hanno una corrispondenza con la key_word in input
    """
    key_word_lower = key_word.lower()

    #costruisce una lista ricercando la key_word nel titolo o nell'autore di ogni libro
    results = [book for book in library if key_word_lower in book["title"].lower() or key_word_lower in book["author"].lower()]
    return results

def lend_book(library, id_book):
    """
        Segna un libro come 'in prestito' se disponibile.
        
        Args:
            library (list): Lista dei libri
            id_book (int): ID libro da prestare
    """
    for book in library:
        if book["id"] == id_book:
            if book["available"]:
                book["available"] = False
                print(f"✅ Il libro '{book['title']}' è stato prestato.")
            else:
                print(f"❌ Il libro '{book['title']}' è già in prestito.")
            return
    print(f"❌ Nessun libro trovato con ID {id_book}.")

def return_book(library, id_book):
    """
        Segna un libro come 'disponibile' se era in prestito.
        
        Args:
            library (list): Lista dei libri
            id_book (int): ID libro di cui cambiare lo stato da "in prestito" a "disponibile"
    """
    for book in library:
        if book["id"] == id_book:
            if not book["available"]:
                book["available"] = True
                print(f"✅ Il libro '{book['title']}' è stato restituito.")
            else:
                print(f"❌ Il libro '{book['title']}' era già disponibile.")
            return
    print(f"❌ Nessun libro trovato con ID {id_book}.")

def show_catalogue(library):
    """
        Mostra tutti i libri disponibili nella biblioteca.
        
        Args:
            library (list): Lista dei libri
    """
    available_books = [book for book in library if book["available"]]
    if not available_books:
        print("ℹ️ Nessun libro disponibile al momento.")
        return
    print("\n📚 Libri disponibili:")
    print("Ordina per: 1) Titolo  2) Autore  3) Anno")
    criterio = input("Scegli un'opzione (1-3): ")

    if criterio == "1":
        key_func = lambda b: b["title"].lower()
    elif criterio == "2":
        key_func = lambda b: b["author"].lower()
    elif criterio == "3":
        key_func = lambda b: b["year"]
    else:
        print("❌ Opzione non valida. Ordino per titolo.")
        key_func = lambda b: b["title"].lower()

    sorted_books = sorted(available_books, key=key_func)

    for book in sorted_books:
        print(f"ID: {book['id']} | {book['title']} di {book['author']} ({book['year']})")

def show_lend_books(library) -> bool:
    """
        Mostra tutti i libri che sono stati prestati.
        
        Args: 
            library (list): Lista dei libri

        Return:
            bool -> Restituisce false se non ci sono libri prestati, true altrimenti
    """
    lend_books = [book for book in library if book["available"] == False]
    if not lend_books:
        print("ℹ️ Al momento tutti i libri sono disponibili.")
        return False
    print("📚 Libri prestati:")
    for book in lend_books:
        print(f"ID: {book['id']} | Titolo: {book['title']} | Autore: {book['author']} | Anno: {book['year']}")
    return True

def save_data(library, file_name):
    """
        Salva i dati della biblioteca in un file JSON.

        Args:
            library (list) : Lista dei libri
            file_name (string): Nome del file su cui salvare la libreria
    """
    try:
        #apro il file in scrittura
        with open(file_name, 'w', encoding='utf-8') as f:
            #creo il json che rappresenta la biblioteca per poi salvarla nel file
            #indent rappresenta il numero di spazi da usare per l'indentazione
            json.dump(library, f, indent=4)
        print(f"✅ Dati salvati in '{file_name}'.")
    except Exception as e:
        print(f"❌ Errore nel salvataggio dei dati: {e}")

def upload_data(file_name):
    """
        Carica i dati della biblioteca da un file JSON.

        Args:
            file_name (string): Nome del file dal quale caricare la libreria
    """
    if not os.path.exists(file_name):
        print(f"❌ Il file '{file_name}' non esiste.")
        return []
    try:
        #apro il file in lettura
        with open(file_name, 'r', encoding='utf-8') as f:
            #deserealizzo il json in un oggeto python (in questo caso una lista)
            library = json.load(f)
        print(f"✅ Dati caricati da '{file_name}'.")
        return library
    except Exception as e:
        print(f"❌ Errore nel caricamento dei dati: {e}")
        return []
    
def show_statistics(library):
    """
        Mostra statistiche della biblioteca:
        - Numero totale di libri
        - Libri disponibili
        - Libri in prestito

        Args:
            library (list): Lista dei libri
    """
    total = len(library)
    available = sum(1 for book in library if book["available"])
    lent = total - available    

    print("\n📊 Statistiche della biblioteca:")
    print(f"Totale libri: {total}")
    print(f"Disponibili: {available}")
    print(f"In prestito: {lent}")

def advanced_search(library, pattern) -> list:
    """
        Cerca libri per titolo o autore usando espressioni regolari.
        Restituisce una lista di risultati.

        Args:
            library (list): Lista dei libri
            pattern (string): Regex da applicare per la ricerca

        Return:
            list -> Lista dei libri che rispettano la regex nel titolo o nell'autore
    """
    try:
        #trasforma la stringa pattern in regex 
        regex = re.compile(pattern)
    except re.error as e:
        print(f"❌ Espressione regolare non valida: {e}")
        return []

    return [book for book in library if regex.search(book["title"]) or regex.search(book["author"])]


def menu():
    """
        Menu testuale per interagire con la biblioteca digitale.
    """
    library = []
    file_name = "bibliotecaGrande.json"

    # Caricamento automatico dei dati all'avvio
    library = upload_data(file_name)

    while True:
        print("\n📚 MENU BIBLIOTECA 📚")
        print("1. Aggiungi un libro")
        print("2. Rimuovi un libro")
        print("3. Cerca un libro")
        print("4. Presta un libro")
        print("5. Restituisci un libro")
        print("6. Mostra catalogo")
        print("7. Salva dati")
        print("8. Carica dati")
        print("9. Statistiche biblioteca")
        print("10. Ricerca avanzata (regex)")
        print("11. Esci")


        scelta = input("👉 Scegli un'opzione (1-11): ")

        if scelta == "1":
            while True:
                title = input("Titolo: ")
                if title.strip() == "": 
                    print("❗️ Inserisci un titolo valido.")
                else: break
            while True:
                author = input("Autore: ")
                if author.strip() == "": 
                    print("❗️ Inserisci un autore valido.")
                else: break
            while True:
                year = input("Anno di pubblicazione: ")
                if not year.isdigit():
                    print("❗️ Inserisci un anno valido.")
                else: break
            add_book(library, title, author, int(year))

        elif scelta == "2":
            show_catalogue(library)
            while True:
                try:
                    id_book = int(input("ID del libro da rimuovere: "))
                    remove_book(library, id_book)
                    break
                except ValueError:
                    print("❗️ Inserisci un ID numerico valido.")

        elif scelta == "3":
            while True:
                keyword = input("Parola chiave per titolo o autore: ")
                if not keyword.strip() == "": break
            results = search_book(library, keyword.strip())
            if results:
                print("🔎 Risultati trovati:")
                for book in results:
                    stato = "Disponibile" if book["available"] else "In prestito"
                    print(f"ID: {book['id']} | {book['title']} di {book['author']} ({book['year']}) - {stato}")
            else:
                print("❌ Nessun risultato trovato.")

        elif scelta == "4":
            show_catalogue(library)
            while True:
                try:
                    id_book = int(input("ID del libro da prestare: "))
                    lend_book(library, id_book)
                    break
                except ValueError:
                    print("❗️ Inserisci un ID numerico valido.")

        elif scelta == "5":
            b = show_lend_books(library)
            if b: 
                while True:
                    try:
                        id_book = int(input("ID del libro da restituire: "))
                        return_book(library, id_book)
                        break
                    except ValueError:
                        print("❗️ Inserisci un ID numerico valido.")

        elif scelta == "6":
            show_catalogue(library)

        elif scelta == "7":
            save_data(library, file_name)

        elif scelta == "8":
            #se volessi fare inserire il nome del file all'utente
            """           
            while True:
                file_name = input("Nome del file da caricare: ")
                if not file_name.strip() == "": break
            """
            library = upload_data(file_name)

        elif scelta == "9":
            print("10. Statistiche biblioteca")
            show_statistics(library)

        elif scelta == "10":
            print("\nℹ️ Esempi di regex:")
            print(" - 'orwell' → trova tutto ciò che contiene 'orwell'")
            print(" - '^Il' → trova titoli o autori che iniziano con 'Il'")
            print(" - '\\b1984\\b' → trova esattamente la parola '1984'")
            print(" - '.*or.*' → trova stringhe che contengono 'or'")
            pattern = input("Inserisci un pattern regex per cercare nei titoli o autori: ")
            risultati = advanced_search(library, pattern)
            if risultati:
                print("🔎 Risultati trovati:")
                for book in risultati:
                    stato = "Disponibile" if book["available"] else "In prestito"
                    print(f"ID: {book['id']} | {book['title']} di {book['author']} ({book['year']}) - {stato}")
            else:
                print("ℹ️ Nessun risultato.")

        elif scelta == "11":
            print("👋 Arrivederci!")
            break

        else:
            print("❌ Opzione non valida. Riprova.")

if __name__ == "__main__":
    menu()

