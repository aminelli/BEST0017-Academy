

from time import sleep


class Example:
    pass


# Inner Class: Esempio
class Esterna:
    
    class Interna1:
        pass
    
    
    class Interna2:
        pass

obj1 = Esterna.Interna1()

    
from abc import abstractmethod, ABC
        
class FormaGeometrica(ABC):

    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def perimetro(self):
        pass

class Rettangolo(FormaGeometrica):
    
    def __init__(self, larghezza, altezza):
        # super().__init__()
        self.larghezza = larghezza
        self.altezza = altezza
       
    def area(self):
        return self.larghezza * self.altezza

    def perimetro(self):
        return 2 * (self.larghezza + self.altezza)

class Cerchio(FormaGeometrica):
    
    pi = 3
    
    def __init__(self, raggio):
        # super().__init__()
        self.raggio = raggio
       
    def area(self):
        return self.pi * self.raggio ** 2

    def perimetro(self):
        return 2 * self.pi * self.raggio
 
forme = [
    Rettangolo(10, 20),
    Cerchio(10)
]

def calcAree(forme):
    
    for forma in forme: 
        print(f"Obj is Form:  {isinstance(forma, FormaGeometrica)}")
        print(f"Obj is Rettangolo:  {isinstance(forma, Rettangolo)}")
        print(f"Obj is Cerchio:  {isinstance(forma, Cerchio)}")
        if isinstance(forma, FormaGeometrica):
            print(f"areea = {forma.area()}, perimetro = {forma.perimetro()}")
        
calcAree(forme)
 
 
# obj1 = FormaGeometrica()


class Person:
    # Proprietà di classe
    species = "Homo Sapiens (forse)"
    
    # def __new__(cls):
    #    pass
    
    # Costruttore della classe; in pratica viene effettuato l'override del magic (o dunder) method
    def __init__(self, firstName, lastName, age):
        # Proprietà di istanza
        self._firstName = firstName
        self.lastName = lastName
        self.age = age
        
        
    # Getter
    @property
    def firstName(self):
        # INSERIE QUI IL CODICE PER la logica di business per controllare la lettura del dato prima di restiturire il dato stesso
        return self._firstName

    @firstName.setter
    def firstName(self, value):
        # INSERIE QUI IL CODICE PER la Logica di business prima di modificare il valore della proprietà
        self._firstName = value
        # INSERIE QUI IL CODICE PER la Logica di busioness dopo la modificare il valore della proprietà
        
        
    # Distruttore
    def __del__(self):
        print("Oggetto distrutto")

    # Metodo di istanza
    def printData(self):
        print(f"{self.firstName} {self.lastName}, {self.age}")

    # Metodo di classe in python
    @classmethod
    def test(cls):
        print(f"Saluta {cls.species}")
        
    
    # Metodo di classe particolare che può essere richiamato solo tramite il nome classe 
    # e non può essere utilizzato tramite le istanze (oggetti) della stessa
    def test2():
        print(f"Saluta")
        
    # Esempio di Metodo Statico
    @staticmethod
    def test3():
        print("Come Stao")
        
    def __str__(self):
        return f"{self.firstName} {self.lastName}, {self.age}"
    
    def __add__(self, other):
        self.age += other
        return self
    
    def __mul__(self, other):
        self.age *= other
        return self
    
    def __eq__(self, other):
        if (isinstance(other, Person)):
            return self.firstName.lower() == other.firstName.lower() and self.lastName.lower() == other.lastName.lower() 
        else:
            return False
    

def main():
    test = Example()
    
    print(Person.species)
    
    #p1 = Person()
    p1 = Person("John", "Doe", 30)
    p2 = Person("Antonio","Minelli", 20)
    
    
    
    p1.firstName = "Ciao"
    print(p1.firstName)
    # print(p1.species)
    # print(p2.species)
    # Person.species = "Unknow"
    # print(p1.species)
    # print(p2.species)
    
    p1.printData()
    p2.printData()
    
    p1.firstName = "John"
    
    Person.test()
    p1.test()
    
    Person.test2()
    # p2.Test2()
    
    Person.test3()
    p2.test3()
    
    print(p1)
    print(p2)
    
    print(f"p1 e p2 sono uguali? -> {p1 == p2}")
    print(f"p1 e p2 sono uguali? -> {p1.__eq__(p2)}")
    
    
    p1 = None
    # -sleep(20)
    
    print(p2)
    
    print(p2 + 4)
    p2.__add__(5)
    print(p2)
    print(p2 * 4)
    # a = "testo" + 4
    #print ("ciao " + 4)
    
    print ("ciao " * 4)
    
 
    

if __name__ == "__main__":
    main()