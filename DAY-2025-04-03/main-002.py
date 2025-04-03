# - Cicli: for, while, con break, continue, e else

from enum import Enum

class WeekDay(Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7


class OrderStatus(Enum):
    Opened = "O",
    Closed = "C",
    Canceled = "A"
    Deleted = "D",
    Temp = "T"

for day in WeekDay:
    print(day.name, day.value)

print("\r\n")

frutti = ["mela", "banana", "pera"]

for frutto in frutti:
    print(frutto)
    
print("\r\n")

messaggio = "testo messsaggio"
for car in messaggio:
    print(car)

    
# uso di liste
numeri = [1, 2, 3, 4, 5, 6, 7, 8, 9]

print("\r\n")

# uso continue
for num in numeri:
    if num % 2 != 0:
        continue
    print(f"{num} è pari")
else:
    print("Ciclo completato con successo")
    
print("\r\n")

# uso break e dimostrazione bypass else in caso di break

for num in numeri:
    if num % 2 == 0:
        break
    print(f"{num} è dispari")
else:
    print("Ciclo completato con successo")



# Tupla

print("\r\n")

dati = (3, 4, 5)

for dato in dati:
    print(dato ** 2)

# uso dictionary

dati = {
    "nome" : "Antonio",
    "cognome" : "Minelli",
    "eta" : 20
}

print(dati["nome"])
print(dati["cognome"])
print(dati["eta"])

print("\r\n")
for fieldName in dati:
    print(f" nome campo: {fieldName}, valore {dati[fieldName]} ")

print("\r\n")

print(dati.values())
print(dati.keys())
print(dati.items())

print("\r\n")


for key in dati:
    print(f" nome campo: {key}, valore {dati[key]} ")

for key in dati.keys():
    print(f" nome campo: {key}, valore {dati[key]} ")

for value in dati.values():
    print(f" valore: {value}")

for key, value in dati.items():
    print(f" nome campo: {key}, valore {value} ")


# Uso range


print("\r\n")


for el in range(5):
    print(el)

# uso else in ciclo
for el in range(5):
    print(el)
else:
    print("Ciclo completato con successo")

for i in range(0, 100, 10):
    print(i)    


for i in range(10, -1, -1):
    print(f"Countdown {i}")


colori = ["rosso", "bianco", "verde", "nero"]
for index, color in enumerate(colori, start = 1):
    print(f"Colore {index}: {color}")
    
print("\r\n") 

matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]


for row in matrix:
    for el in row:
        print(el, end=' ')
    print()

for i, row in enumerate(matrix):
    for j, el in enumerate(row):
        print(f"[{i},{j}] = {el}")


quadrati = [ [ x ** 2 for x in row ] for row in matrix]
print(matrix)
print(quadrati)

print("END")    
 






# - Esercizi pratici: gestire condizioni e cicli per risolvere semplici problemi
# - Funzioni e Parametri
# - Definire una funzione: sintassi base con def
# - Parametri e ritorno di valori
# - Funzioni con argomenti variabili: *args, **kwargs
# - Esercizi pratici: scrivere funzioni per risolvere piccoli problemi

