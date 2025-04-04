import json
import re

library = []
ultimo_id = 0

def add_book (titolo, autore, anno): #crea un libro e lo aggiunge alla biblioteca
    """Aggiunge un nuovo libro alla biblioteca.

    Args:
        titolo (str): Il titolo del libro.
        autore (str): L'autore del libro.
        anno (int): L'anno di pubblicazione del libro.

    Side Effects:
        Modifica la lista globale `library` aggiungendo un nuovo libro.
        Incrementa la variabile globale `ultimo_id`.
        Salva i dati aggiornati nel file 'library.json'.

    Prints:
        Messaggio di conferma dell'aggiunta del libro con il suo ID.
    """
    global ultimo_id #usa l'ultimo id
    ultimo_id += 1 #incrementa l'ultimo id
    libro = {
        "id": ultimo_id,
        "titolo": titolo,
        "autore": autore,
        "anno": anno,
        "disponibile": True
    }
    library.append(libro) #aggiunge il libro alla biblioteca
    save_data("library.json") #salva la biblioteca
    print(f"\nLibro '{titolo}' aggiunto correttamente. ID {libro['id']}.")

def remove_book(library, id_libro): #rimuove un libro dalla biblioteca
    """Rimuove un libro dalla biblioteca dato il suo ID.

    Args:
        id_libro (int): L'ID del libro da rimuovere.

    Side Effects:
        Modifica la lista globale `library` rimuovendo il libro specificato.
        Salva i dati aggiornati nel file 'library.json'.

    Prints:
        Messaggio di conferma della rimozione o di errore se il libro non è trovato.
    """
    for libro in library:
        if libro["id"] == id_libro:
            library.remove(libro)
            print(f"\nIl libro '{libro['titolo']}'è stato rimosso.")
            return
    print("\nLibro non trovato.")
    save_data("library.json")

def search_book(keyword): #cerca un libro

    """Cerca libri nella biblioteca che corrispondono alla parola chiave nel titolo o nell'autore.

    Args:
        keyword (str): La parola chiave da cercare.

    Prints:
        Elenco dei libri trovati con il loro stato (Disponibile/In prestito) o un messaggio se nessun libro è trovato.
    """
    
    pattern = re.compile(keyword, re.IGNORECASE) #compilo la regex col flag re.IGNORECASE per fare una ricerca case-insensitive

    risultati = [
        libro for libro in library
        if re.search(pattern, libro["titolo"]) or re.search(pattern, libro["autore"]) #cerco i libri che corrispondono al pattern nel titolo o nell'autore
    ]
    
    if risultati:
        print("\nRisultati della ricerca:")
        for libro in risultati:
            stato = "Disponibile" if libro["disponibile"] else "In prestito"
            print(f"{libro['id']}. {libro['titolo']} di {libro['autore']} ({libro['anno']}) - {stato}")
    else:
        print("\nNessun libro trovato.")

def rent_book(id_libro): #presta un libro

    """Segna un libro come 'In prestito' dato il suo ID.

    Args:
        id_libro (int): L'ID del libro da prestare.

    Side Effects:
        Modifica l'attributo `disponibile` del libro specificato.
        Salva i dati aggiornati nel file 'library.json'.

    Prints:
        Messaggio di conferma del prestito o di errore se il libro non è disponibile o non è trovato.
    """

    libro = next((libro for libro in library if libro["id"] == id_libro), None) #trova il libro con l'id specificato
    if libro:
        if libro["disponibile"]: #controllo che effettivamente il libro sia disponibile
            libro["disponibile"] = False
            print(f"\nLibro '{libro['titolo']}' prestato.")
        else:
            print("\nQuesto libro è già in prestito a qualcuno.")
    else:
        print("\nLibro non trovato.")
    save_data("library.json")

def return_book(id_libro): #restituisce un libro
    """Segna un libro come 'Disponibile' dato il suo ID.

    Args:
        id_libro (int): L'ID del libro da restituire.

    Side Effects:
        Modifica l'attributo `disponibile` del libro specificato.
        Salva i dati aggiornati nel file 'library.json'.

    Prints:
        Messaggio di conferma della restituzione o di errore se il libro è già disponibile o non è trovato.
    """
    libro = next((libro for libro in library if libro["id"] == id_libro), None) #trova il libro con l'id specificato 
    if libro:
        if not libro["disponibile"]: #controllo che effettivamente il libro sia in prestito
            libro["disponibile"] = True
            print(f"\nLibro '{libro['titolo']}' restituito.")
        else:
            print("\nQuesto libro è già disponibile.")
    else:
        print("\nLibro non trovato.")
    save_data("library.json")

def show_library():#mostra il catalogo della biblioteca
    """Mostra il catalogo dei libri ordinati alfabeticamente per titolo, indicando il numero totale di libri disponibili e in prestito.

    Prints:
        Numero totale di libri disponibili e in prestito.
        Elenco dei libri con il loro stato (Disponibile/In prestito) o un messaggio se la biblioteca è vuota.
    """
    if not library: 
        print("\nLa biblioteca è vuota.")
        return

    libri_ordinati = sorted(library, key=lambda libro: libro["titolo"].lower()) #ordino i libri per titolo in ordine alfabetico

    disponibili = sum(1 for libro in libri_ordinati if libro["disponibile"]) #conto i libri disponibili
    prestati = len(libri_ordinati) - disponibili
    
    print("\nCatalogo:")
    print(f"\nNumero di libri disponibili: {disponibili}")
    print(f"Numero di libri in prestito: {prestati}")
    for libro in libri_ordinati:
        stato = "Disponibile" if libro["disponibile"] else "In prestito"
        print(f"\n {libro['titolo']} - {libro['autore']} ({libro['anno']}) - {stato} (id: {libro['id']})")


def save_data(nome_file):
    """Salva i dati attuali della biblioteca in un file JSON.

    Args:
        nome_file (str): Il nome del file in cui salvare i dati.

    Side Effects:
        Scrive i dati della biblioteca nel file specificato.

    Prints:
        Messaggio di conferma del salvataggio o di errore in caso di problemi.
    """
    try:
        dati = {
            "libri": library,
            "ultimo_id": ultimo_id
        }
        with open(nome_file, 'w', encoding='utf-8') as f:
            json.dump(dati, f, indent=4, ensure_ascii=False)
        print(f"\nDati salvati correttamente in '{nome_file}'.")
    except Exception as e:
        print(f"\nErrore durante il salvataggio: {e}")

def upload_data(nome_file):
    """Carica i dati della biblioteca da un file JSON.

    Se il file non esiste, inizializza la biblioteca come vuota e imposta
    l'ultimo ID a 0, evitando così errori durante l'esecuzione.

    Args:
        nome_file (str): Il percorso del file JSON da cui caricare i dati.

    Side Effects:
        Aggiorna le variabili globali `library` e `ultimo_id` con i dati
        caricati dal file.
        Se il file non viene trovato, inizializza `library` come lista vuota
        e `ultimo_id` come 0.

    Prints:
        - Messaggio di conferma con il nome del file e l'ultimo ID caricato.
        - Messaggio di avviso se il file non viene trovato.
    """
    global library, ultimo_id
    try:
        with open(nome_file, 'r', encoding='utf-8') as f:
            dati = json.load(f)
            library = dati.get("libri", [])
            ultimo_id = dati.get("ultimo_id", 0)
            print(f"Dati caricati da '{nome_file}'. Ultimo ID: {ultimo_id}")
    except FileNotFoundError:
        print(f"File '{nome_file}' non trovato.")
        library = []
        ultimo_id = 0


def menu():
  
    upload_data("library.json")

    while True:
        print("\nBIBLIOTECA NAZIONALE")
        print("1. Aggiungi libro")
        print("2. Rimuovi libro")
        print("3. Cerca libro")
        print("4. Presta libro")
        print("5. Restituisci libro")
        print("6. Visualizza catalogo")
        print("7. Salva dati")
        print("8. Carica dati")
        print("9. Esci\n")
        scelta = input("Scegli un'opzione:")

        match scelta:
            case "1":
                titolo = input("Titolo: ")
                autore = input("Autore: ")
                try:
                    anno = int(input("Anno: "))
                    add_book(titolo, autore, anno)
                except ValueError:
                    print("Errore: L'anno deve essere un numero.")
            case "2":
                try:
                    id_libro = int(input("\nID del libro da rimuovere: "))
                    remove_book(id_libro)
                except ValueError:
                    print("Errore: Inserisci un ID valido.")
            case "3":
                keyword = input("\nParola chiave (titolo o autore): ")
                search_book(keyword)
            case "4":
                try:
                    show_library()
                    id_libro = int(input("\nID del libro da prestare: "))
                    rent_book(id_libro)
                except ValueError:
                    print("Errore: Inserisci un ID valido.")
            case "5":
                try:
                    show_library()
                    id_libro = int(input("ID del libro da restituire: "))
                    return_book(id_libro)
                except ValueError:
                    print("Errore: Inserisci un ID valido.")
            case "6":
                show_library()
            case "7":
                save_data("library.json")
            case "8":
                upload_data("library.json")
            case "9":
                print("Uscita dalla biblioteca")
                break
            case _:
                print("Scelta non valida. Riprova.")