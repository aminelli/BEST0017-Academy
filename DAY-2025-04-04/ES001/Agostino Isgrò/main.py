import json
import re

def aggiungi_libro(biblioteca, titolo, autore, anno):
    """_summary_

    Args:
        biblioteca (_type_): _description_
        titolo (_type_): _description_
        autore (_type_): _description_
        anno (_type_): _description_
    """
    nuovo_libro = {
        "id": len(biblioteca) + 1,
        "titolo": titolo,
        "autore": autore,
        "anno": anno,
        "disponibile": True
    }
    biblioteca.append(nuovo_libro)


def rimuovi_libro(biblioteca, id_libro):
    biblioteca[:] = [libro for libro in biblioteca if libro["id"] != id_libro]


def cerca_libro(biblioteca, parola_chiave):
    return [libro for libro in biblioteca if parola_chiave.lower() in libro["titolo"].lower() or parola_chiave.lower() in libro["autore"].lower()]


def presta_libro(biblioteca, id_libro):
    for libro in biblioteca:
        if libro["id"] == id_libro and libro["disponibile"]:
            libro["disponibile"] = False
            return True
    return False


def restituisci_libro(biblioteca, id_libro):
    for libro in biblioteca:
        if libro["id"] == id_libro and not libro["disponibile"]:
            libro["disponibile"] = True
            return True
    return False


def visualizza_catalogo(biblioteca):
    for libro in biblioteca:
        stato = "Disponibile" if libro["disponibile"] else "Non disponibile"
        print(f"{libro['id']}: {libro['titolo']} di {libro['autore']} ({libro['anno']}) - {stato}")
        
        
def statistiche_biblioteca(biblioteca):
    totale_libri = len(biblioteca)  # Numero totale di libri
    in_prestito = sum(1 for libro in biblioteca if not libro["disponibile"])  # Libri non disponibili
    disponibili = totale_libri - in_prestito  # Libri disponibili

    
    print("Totale libri:", totale_libri, "Libri disponibili:", disponibili, "Libri in prestito:", in_prestito) 
  
    
def ordina_libri(biblioteca, ordinamento="titolo"):
    # Ordinare i libri in base al criterio scelto
    if ordinamento == "titolo":
        biblioteca = sorted(biblioteca, key=lambda libro: libro["titolo"].lower())
    elif ordinamento == "autore":
        biblioteca = sorted(biblioteca, key=lambda libro: libro["autore"].lower())
    elif ordinamento == "anno":
        biblioteca = sorted(biblioteca, key=lambda libro: libro["anno"])

    # Mostrare la lista dei libri ordinati
    print("libri ordinati per",ordinamento)
    
    for libro in biblioteca:
        stato = "Disponibile" if libro["disponibile"] else "Non disponibile"
        print(f"{libro['id']}: {libro['titolo']} di {libro['autore']} ({libro['anno']}) - {stato}")
    
        
def ricerca_avanzata(biblioteca, campo, pattern):
    risultati = []
    
    #creare la regex
    try:
        regex = re.compile(pattern, re.IGNORECASE)
    except re.error:
        print("Pattern non valido")
        return []

    # Controllo per quale campo cercare
    if campo == "titolo":
        for libro in biblioteca:
            if regex.search(libro["titolo"]):  # Cerca nel titolo
                risultati.append(libro)
                
    elif campo == "autore":
        for libro in biblioteca:
            if regex.search(libro["autore"]):  # Cerca nell'autore
                risultati.append(libro)
                
    elif campo == "anno":
        for libro in biblioteca:
            if regex.search(str(libro["anno"])):  # Cerca nell'anno (convertito in stringa)
                risultati.append(libro)
                
    for libro in risultati:
        stato = "Disponibile" if libro["disponibile"] else "Non disponibile"
        print(f"{libro['id']}: {libro['titolo']} di {libro['autore']} ({libro['anno']}) - {stato}")
    
### salva e preleva i dati all'interno di un file JSON 
def salva_dati(biblioteca, nome_file):
    with open(nome_file, "w") as file:
        json.dump(biblioteca, file, indent=4)

def carica_dati(nome_file):
    try:
        with open(nome_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("File JSON non trovato. Creane uno nuovo salvando la biblioteca.")
        return []
    

#MAIN
#CREO UNA LISTA E GESTISCO I DATI TRAMITE LE FUNZIONI CREATE SOPRA
biblioteca = []
aggiungi_libro(biblioteca, "1984", "George Orwell", 1949)
aggiungi_libro(biblioteca, "Il Signore degli Anelli", "J.R.R. Tolkien", 1954)
aggiungi_libro(biblioteca, "libro1", "autore1",1900)
aggiungi_libro(biblioteca, "Il Grande Gatsby", "F. Scott Fitzgerald", 1925)
aggiungi_libro(biblioteca, "Cento Anni di Solitudine", "Gabriel García Márquez", 1967)
aggiungi_libro(biblioteca, "Il Piccolo Principe", "Antoine de Saint-Exupéry", 1943)
aggiungi_libro(biblioteca, "Moby Dick", "Herman Melville", 1851)
aggiungi_libro(biblioteca, "Orgoglio e Pregiudizio", "Jane Austen", 1813)

visualizza_catalogo(biblioteca)

print()
rimuovi_libro(biblioteca,1)
visualizza_catalogo(biblioteca)

print()
presta_libro(biblioteca, 3)
visualizza_catalogo(biblioteca)

print()
restituisci_libro(biblioteca, 3)
visualizza_catalogo(biblioteca)

print()
print(cerca_libro(biblioteca,"autore1"))

print()
print()
salva_dati(biblioteca, "biblioteca.json")
biblioteca = carica_dati("biblioteca.json")
visualizza_catalogo(biblioteca)

print()
statistiche_biblioteca(biblioteca)

print()
ordina_libri(biblioteca, ordinamento="titolo")

print()
ricerca_avanzata(biblioteca, "anno", "19")
