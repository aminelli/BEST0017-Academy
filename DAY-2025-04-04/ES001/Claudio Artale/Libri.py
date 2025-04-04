import json
from typing import Callable, List, Optional, Dict
import re

def show_menu():
    print("\n📘 Menu della Biblioteca Digitale")
    print("1) ➕ Aggiungi libro")
    print("2) 🗑️ Rimuovi libro")
    print("3) 🔍 Cerca libro (parola chiave)")
    print("4) 📕 Presta libro")
    print("5) 📗 Restituisci libro")
    print("6) 📚 Visualizza catalogo (libri disponibili)")
    print("7) 📊 Mostra statistiche")
    print("0) ❌ Esci")

def salva_dati(biblioteca: List[dict], nome_file: str = "biblioteca.json"):
    """
    Salva i dati della biblioteca su file JSON.
    """
    with open(nome_file, "w", encoding="utf-8") as f:
        json.dump(biblioteca, f, indent=4, ensure_ascii=False)


def carica_dati(nome_file: str = "biblioteca.json") -> List[dict]:
    """
    Carica i dati da un file JSON. Se il file non esiste, restituisce una lista vuota.
    """
    try:
        with open(nome_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File '{nome_file}' non trovato. Creazione nuova biblioteca.")
        return []


def aggiungi_libro(biblioteca: List[dict], titolo: str, autore: str, anno: int):
    """
    Aggiunge un nuovo libro alla biblioteca, assegnando un ID univoco.
    """
    nuovo_id = max((libro["id"] for libro in biblioteca), default=0) + 1
    nuovo_libro = {
        "id": nuovo_id,
        "titolo": titolo,
        "autore": autore,
        "anno": anno,
        "disponibile": True
    }
    biblioteca.append(nuovo_libro)
    print(f"Libro aggiunto con ID {nuovo_id}: '{titolo}' di {autore}")


libri_disponibili_cache = None

def filtroPerID(id_target: int) -> Callable[[dict], bool]:
    """
    Restituisce un filtro per cercare un libro con un ID specifico.
    """
    return lambda libro: libro["id"] == id_target


def filtroPerDisponibilità(disponibile: bool) -> Callable[[dict], bool]:
    """
    Restituisce un filtro per verificare se un libro è disponibile o in prestito.
    """
    return lambda libro: libro["disponibile"] == disponibile


def filtroPerRegex(pattern: str, campo: str = "entrambi") -> Callable[[dict], bool]:
    """
    Restituisce un filtro per cercare un pattern regex su titolo, autore o entrambi.
    
    :param pattern: l'espressione regolare da cercare
    :param campo: "titolo", "autore" o "entrambi"
    :return: funzione filtro
    """
    try:
        regex = re.compile(pattern, re.IGNORECASE)
    except re.error:
        print("Espressione regolare non valida.")
        return lambda libro: False

    if campo == "titolo":
        return lambda libro: bool(regex.search(libro["titolo"]))
    elif campo == "autore":
        return lambda libro: bool(regex.search(libro["autore"]))
    else:
        return lambda libro: bool(
            regex.search(libro["titolo"]) or regex.search(libro["autore"])
        )



def cerca_libro(
    items: List[dict],
    filtro: Callable[[dict], bool],
    usa_cache: bool = False,
    ordina_per: Optional[str] = None
) -> List[dict]:
    """
    Restituisce una lista di libri che soddisfano un filtro.
    Può usare una cache se il filtro è sulla disponibilità.
    Può ordinare i risultati per titolo, autore o anno.

    :param items: Lista dei libri (dizionari)
    :param filtro: Funzione che filtra i libri
    :param usa_cache: Se True, usa/ripristina la cache per i libri disponibili
    :param ordina_per: Criterio di ordinamento opzionale ("titolo", "autore", "anno")
    :return: Lista di libri filtrati e (eventualmente) ordinati
    """
    global libri_disponibili_cache

    if usa_cache:
        if libri_disponibili_cache is not None:
            risultati = libri_disponibili_cache
        else:
            risultati = [item for item in items if filtro(item)]
            libri_disponibili_cache = risultati
    else:
        risultati = [item for item in items if filtro(item)]

    if ordina_per and ordina_per in {"titolo", "autore", "anno"}:
        risultati = sorted(
            risultati,
            key=lambda libro: str(libro.get(ordina_per, "")).lower()
            if isinstance(libro.get(ordina_per), str)
            else libro.get(ordina_per)
        )

    return risultati



     
def rimuovi_libro(biblioteca: List[dict], id_libro: int) -> Optional[dict]:
    """
    Rimuove un libro dalla biblioteca se disponibile.
    
    :param biblioteca: Lista dei libri
    :param id_libro: ID del libro da rimuovere
    :return: Il libro rimosso o None se non trovato/non disponibile
    """
    libri_trovati = cerca_libro(biblioteca, filtroPerID(id_libro))
    if libri_trovati:
        libro = libri_trovati[0]
        if libro.get("disponibile", False):
            biblioteca.remove(libro)
            print(f"🗑️ Libro rimosso: '{libro['titolo']}' di {libro['autore']}")
            return libro
        else:
            print(f"Il libro '{libro['titolo']}' non è disponibile (già in prestito).")
    else:
        print("Nessun libro trovato con l'ID specificato.")
    return None



def restituisci_libro(biblioteca: List[dict], id_libro: int) -> Optional[dict]:
    """
    Segna un libro come disponibile se era stato prestato.

    :param biblioteca: Lista dei libri
    :param id_libro: ID del libro da restituire
    :return: Il libro restituito o None se già disponibile
    """
    global libri_disponibili_cache

    libroDaRestituire = cerca_libro(biblioteca, filtroPerID(id_libro))
    if libroDaRestituire:
        libro = libroDaRestituire[0]
        if not libro.get("disponibile", True):
            libro["disponibile"] = True
            print(f"Libro restituito: '{libro['titolo']}' di {libro['autore']}'")
            if libri_disponibili_cache is not None:
                libri_disponibili_cache.append(libro)
            return libro

    print("Nessun libro da restituire con quell'ID.")
    return None

    
def visualizza_catalogo(biblioteca: List[dict], ordina_per: Optional[str] = "titolo"):
    """
    Mostra tutti i libri disponibili nella biblioteca, ordinati secondo un criterio.

    Utilizza la cache dei libri disponibili per non dover riordinare ogni volta che viene invocato.
    
    :param biblioteca: Lista dei libri presenti nella biblioteca
    :param ordina_per: Criterio di ordinamento ("titolo", "autore", "anno"). Default: "titolo"
    """
    libri_disponibili = cerca_libro(
        biblioteca,
        filtroPerDisponibilità(True),
        usa_cache=True,
        ordina_per=ordina_per
    )
    
    if not libri_disponibili:
        print("Nessun libro disponibile al momento.")
        return

    print(f"Catalogo dei libri disponibili (ordinati per {ordina_per}):\n")
    for libro in libri_disponibili:
        print(f"ID {libro['id']} - '{libro['titolo']}' di {libro['autore']} ({libro['anno']})")



def mostra_statistiche(biblioteca: List[dict]):
    """
    Calcola e mostra le statistiche della biblioteca:
    - Numero totale di libri
    - Libri disponibili
    - Libri in prestito

    Usa la cache dei libri disponibili se già presente.
    
    :param biblioteca: Lista dei libri presenti nella biblioteca
    """
    global libri_disponibili_cache

    # Usa la cache se disponibile, altrimenti la popola
    if libri_disponibili_cache is None:
        libri_disponibili_cache = [libro for libro in biblioteca if libro.get("disponibile", False)]

    totali = len(biblioteca)
    disponibili = len(libri_disponibili_cache)
    in_prestito = totali - disponibili

    print("\n Statistiche della biblioteca:")
    print(f"• Totale libri: {totali}")
    print(f"• Libri disponibili: {disponibili}")
    print(f"• Libri in prestito: {in_prestito}")




def main():
    biblioteca = carica_dati()

    while True:
        show_menu()
        scelta = input("Seleziona un'opzione: ")

        if scelta == "1":
            titolo = input("Titolo: ")
            autore = input("Autore: ")
            anno = int(input("Anno: "))
            aggiungi_libro(biblioteca, titolo, autore, anno)

        elif scelta == "2":
            id_libro = int(input("ID del libro da rimuovere: "))
            rimuovi_libro(biblioteca, id_libro)

        elif scelta == "3":
            pattern = input("🔍 Inserisci una regex per titolo/autore (Invio per visualizzare tutto): ").strip()

            if not pattern:
                # Nessun filtro: mostra tutto il catalogo
                visualizza_catalogo(biblioteca)
            else:
                campo = input("Vuoi cercare per 'titolo', 'autore' o 'entrambi'? [default: entrambi]: ").strip().lower()
                if campo not in {"titolo", "autore", "entrambi", ""}:
                    print("Campo non valido. Uso 'entrambi' come default.")
                    campo = "entrambi"
                elif campo == "":
                    campo = "entrambi"

                risultati = cerca_libro(biblioteca, filtroPerRegex(pattern, campo))
                if risultati:
                    print(f"\nRisultati della ricerca ({campo}):\n")
                    for libro in risultati:
                        print(f"{libro['id']} - {libro['titolo']} di {libro['autore']} ({libro['anno']})")
                else:
                    print("Nessun risultato trovato.")


        elif scelta == "4":
            id_libro = int(input("ID del libro da prestare: "))
            presta_libro(biblioteca, id_libro)

        elif scelta == "5":
            id_libro = int(input("ID del libro da restituire: "))
            restituisci_libro(biblioteca, id_libro)

        elif scelta == "6":
            criterio = input("Ordina per (titolo, autore, anno) [default: titolo]: ").strip().lower()
            if criterio not in {"titolo", "autore", "anno", ""}:
                print("Ordinamento non valido. Uso 'titolo' come default.")
                criterio = "titolo"
            elif criterio == "":
                criterio = "titolo"

            visualizza_catalogo(biblioteca, ordina_per=criterio)
        
        elif scelta == "7":
            mostra_statistiche(biblioteca)

        elif scelta == "0":
            salva_dati(biblioteca)
            print("Arrivederci!")
            break

        else:
            print("Opzione non valida.")

if __name__ == "__main__":
    main()


