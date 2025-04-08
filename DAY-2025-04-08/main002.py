
class Libro:
    
    def __init__(self, titolo, autore, prezzo, isbn):
        self.titolo = titolo
        self.autore = autore
        self.prezzo = prezzo
        self.isbn = isbn    
        
    def __respr__(self):
        return f"Libro: {self.titolo}, Autore: {self.autore}, Prezzo: {self.prezzo}, ISBN: {self.isbn}"
    
    def __eq__(self, value):
        return isinstance(value, Libro) and self.isbn == value.isbn
    
    
from dataclasses import dataclass, field
from typing import List


@dataclass
class Libro2:
    titolo: str
    autore: str
    prezzo: str
    isbn: str

@dataclass(order=True)
class Studente:
    # order=True genera anche i metodi di confronto < > ....
    matricola: int
    nome: str
    cognome: str
    esami: List[str] = field(default_factory=list)
    
    def aggiungi_esame(self, esame:str):
        self.esami.append(esame)
        
s1 = Studente(123, "Mario", "Rossi")

s1.aggiungi_esame("Matematica")
s1.aggiungi_esame("Informatica")

s2 = Studente(1233, "Mario", "Verdi")

print(s1)
print(s1 < s2)