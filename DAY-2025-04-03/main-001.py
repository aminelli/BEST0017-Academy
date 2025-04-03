# Enum

from enum import Enum

class WeekDay(Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7

class Sex(Enum):
    Male = "MA"
    Female = "FE"
      
print(WeekDay.FRIDAY)
print(WeekDay.FRIDAY.value)
print(WeekDay.FRIDAY.name)

a = Sex.Male

# - Condizioni: if, elif, else

x = 10
if x > 5:
    print("x è maggiore di 5")
elif x == 5:
    print("x è uguale a 5")
else:
    print("x è minore di 5")

y = WeekDay.FRIDAY






if y == WeekDay.FRIDAY:
    print("oggi è venerdi")
elif y == WeekDay.SATURDAY:
    print("oggi è sabato")
elif y == WeekDay.SUNDAY:
    print("oggi è domenica")
elif y == WeekDay.MONDAY:
    print("oggi è lunedì")
elif y == WeekDay.TUESDAY:
    print("oggi è martedì")
elif y == WeekDay.WEDNESDAY:
    print("oggi è mercoledì")
elif y == WeekDay.THURSDAY:
    print("oggi è giovedì")
else:
    print("Strano")


if y == WeekDay.SATURDAY or y==WeekDay.SUNDAY:
    print("oggi è weekend")
    if y == WeekDay.SATURDAY:
        print("oggi è sabato")
    elif y == WeekDay.SUNDAY:
        print("oggi è domenica")
else:
    print("oggi non è weekend")
      
 
x1 = 5
x2 = 6

if x1 < x2:
    print("x1 è minore di x2")
elif x1 > x2:
    print("x1 è maggiore di x2")
else:
    print("x1 è uguale a x2")

if any([x1 < x2, x1 > x2]):
    print("x1 diverso da x2")
else:
    print("x1 è uguale a x2")
    
if y in [WeekDay.SATURDAY, WeekDay.SUNDAY]:
    print("oggi è weekend")
else:
    print("oggi non è weekend")

# - Condizioni: switch -> in python match

match y:
    case WeekDay.MONDAY:
        print("LUN")
    case WeekDay.TUESDAY:
        print("MAR")
    case WeekDay.WEDNESDAY:
        print("MER")
    case WeekDay.THURSDAY:
        print("GIO")
    case WeekDay.FRIDAY:
        print("VEN")
    case WeekDay.SATURDAY:
        print("SAB")
    case WeekDay.SUNDAY:
        print("DOM")
    case _:
        print("Strano")

# tupla = (1, "test")
# tupla = (2, "pippo")
tupla = (4, "pippo")

match tupla:
    case (1,"test"):
        print("Il primo valore deve essere 1 e il secondo test")
    case (2, _):
        print("Primo valore deve essere 2")
    case (_, "pippo"):
        print("secondo valore deve essere pippo")
    case _:
        print("Tutti gli altri casi")

valore = [1, 2, 3]

match valore:
    case int():
        print("valore è un intero")
    case str():
        print("valore è una string")
    case list():
        print("valore è una lista")
    case _:
        print(f"valore è di tipo {type(valore)}") 

dati = {
    "nome" : "Antonio",
    "cognome" : "Minelli",
    "eta" : 20
}

match dati:
    case {"nome": str(nome), "eta" : int(eta)}:
        print(f"Nome: {nome}, eta: {eta}")
    case _:
        print("Dictionary non valido")
        
numeri = [1, 2, 3, 4]
#numeri = "stringa"

match numeri:
    case [first, *others]:
        print(f"Primo numero: {first}, Altri numeri {others}")    
    # case [first, second, *others]:
    #    print(f"Primo numero: {first}, Altri numeri {others}")    
    case _:
        print("Lista non valida")

match numeri:
    case [a, b, c , d, *others]:
        print(f"Primo numero: {a}, Altri numeri {others}")    
    case _:
        print("Lista non valida")

match numeri:
    case [a, b, c , d, e, *others]:
        print(f"Primo numero: {e}, Altri numeri {others}")    
    case _:
        print("Lista non valida")

match numeri:
    case [first, *others, last]:
        print(f"Primo numero: {first}, Altri numeri {others}, Ultimo {last}")    
    case _:
        print("Lista non valida")

match numeri:
    case [first, *others, _]:
        print(f"Primo numero: {first}, Altri numeri {others}")    
    case _:
        print("Lista non valida")
        
        
## OPERATORE TERNARIO + INTERPOLAZIONE STRINGHE
# isWeek = y in [WeekDay.SATURDAY, WeekDay.SUNDAY] ? "OK" : "KO"
# isWeek = condizione ? vero : falso
# # isWeek = vero if condizione: falso
# sintassi python: risultato_atteso = condizionevalore_se_vera_condizione if condizione else condizionevalore_se_falsa
messaggio = "è weekend" if y in [WeekDay.SATURDAY, WeekDay.SUNDAY] else "non è weekend"

x1 = 3

print("Pari") if x % 2 == 0 else print("Dispari")

Y = WeekDay.SATURDAY
x = WeekDay.FRIDAY if y == WeekDay.FRIDAY else WeekDay.SATURDAY
print(x) 

def segno(num):
    return "Positivo" if num > 0 else "Negativo" if num < 0 else "Zero"

print (f"4 è : {segno(4)}")
print (f"-4 è : {segno(-4)}")
print (f"0 è : {segno(0)}")

x = 4
print (f"il numero {x} è : {segno(x)}")
print (f"il numero {x} è : {"Positivo" if x > 0 else "Negativo" if x < 0 else "Zero"}")
print ("il numero {0} è : {1}".format(4, segno(4)))
# L'esempio successivo è corretto ma deprecato
print ("il numero %d è : %s" % (x, segno(4)) )

from string import Template

template_str = Template("il numero $numero è : $segno ")
print(template_str.substitute(numero=x, segno=segno(4)))


