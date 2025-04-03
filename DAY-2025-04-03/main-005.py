# - Funzioni con argomenti variabili: *args, **kwargs
# Varie sulle funzioni


# Funzione semplice senza parameri
def hello_world():
    print("hello")
    
    
# Funzione con parametri
def hello_2(name):
    print(f"hello {name}")


# Funzione con parametri con valori di ritorno
def calc(a, b):
    return a + b


# Funzione con parametri di default con valori di ritorno
def pow2(base, exponent = 2):
    return base ** exponent

a = pow2(4)
a = pow2(4, 3)


# Fuunzione con commenti di documentazione (docstring)
def rectangle_area_calc(base, height): 
    """
    Calcola l'area di un rettangolo

    Args:
        base (float): base del rettangolo
        height (float): altezza del rettangolo

    Returns:
        float: area del rettangolo
    """    
    return base * height

a: float = 5

a = "tretrue"
a = rectangle_area_calc("tre",2)

print(a)
print("END")


# PARAMETRI: COSE AVANZANTE

# Parametri posizionali e keyword
def greet(name, message ="Ciao", punctuation = "!"):
    return f"{message}, {name}{punctuation}"

print(greet("Mario"))
print(greet("Mario", "Benvenuto"))
print(greet("Mario", punctuation="."))
print(greet(message="Olà", punctuation=".", name="Antonio"))
print(greet(message="Olà", name="Antonio"))


# Parametri *args (numero variabili di argomenti posizionali)
def media(*numbers):
    if not numbers:
        return 0
    
    return sum(numbers) / len(numbers)

print(media())
print(media(1, 2, 3))
print(media(10, 20, 30, 40, 50, 60, 75))

# Parametri **kargs (numero variabili di argomenti keyword)

from datetime import datetime

def create_profile(**details):
    profile = { "created_at": datetime.now() }
    profile.update(details)
    return profile

profile1 = create_profile(
    first_name = "Antonio", 
    last_name = "Minelli",
    city = "Bergamo",
    age = 20
)

profile2 = create_profile(
    last_name = "Isgrò",
    age = 15,
    first_name = "Agostino", 
    city = "Barcellona pozzo di gotto",
    email = "super.agostino@gmail.com"
)

profile3 = create_profile(
    username = "draconis",
    pwd = "1234"
)

print(profile1)
print(profile2)
print(profile3)

# Parametri *args e **kargs (combinazione di numero variabili di argomenti posizionali e keyword)

def format_data(*args, separator = ", ", **kargs):
    args_list = list(args)
    for key, value in kargs.items():
        args_list.append(f"{key}={value}")   
    return separator.join(args_list)

frm1 = format_data("a", "b", "c")
frm2 = format_data("x", "y", separator ="-", first_name = "antonio", last_name = "minelli" )

print(frm1)
print(frm2)


# Uso parametro / per argomenti solo posizionali
def divide(dividend, divisor, /, decimals = 2, prmx = 3):
    return round(dividend / divisor, decimals)

calc1 = divide(10, 3)
calc1 = divide(10, 3, decimals=4)
# calc3 = divide(dividend = 10, divisor = 3, decimals=4)
# calc3 = divide(divisor = 3, dividend = 10, decimals=4)
# calc4 = divide(10, parmx=2, divisor=3 , decimals=4)


# Uso parametro * per argomenti solo keywords

def build_conn(*, host = "localhost", port=8080, debug=False, protocol = "http"):
    return { 
            "host": host, 
            "port": port, 
            "activatedDebug": debug, 
            "protocol" : protocol 
        }

build1 = build_conn(
    host = "127.0.0.1",
    debug=True
)

build2 = build_conn(
    debug=True,
    host = "127.0.0.1",
    port = 80
)

build3 = build_conn()

#build4 = build_conn("1.1.1.1", 8000)


# FUNZIONI CON ANNOTAZIONI DI TIPO

# Funzione base con type hints
def calc_max(values: list[int]) -> int:
    if not values:
        raise ValueError("La lista non può essere vuota")
    return max(values)

x = calc_max([5, 120,6,2])


# Funzione con annotazioni complesse

from typing import List, Dict, Optional, Union, Callable, TypeVar

from typeguard import typechecked
#import enforce

Number = TypeVar("Number", int, float)

# def calcMultiplication(x, y): 
#@typechecked
#@enforce.runtime_validation
def calcMultiplication(x: Number, y: Number) -> Number: 
    
    return x * y

x1 = calcMultiplication(3 , 4)
x2 = calcMultiplication(3.2 , 4.5)
x3 = calcMultiplication(3 , 4.5)
x4 = calcMultiplication(3.2 , 4)
#x4 = calcMultiplication("3.2" , "4")
x5 = calcMultiplication("2", 4)

T = TypeVar("T") # Generics

def exchange(a: T, b: T) -> tuple[T, T]:
    return b, a


x , y = exchange(10, 20)
print(x, y)
s1 , s2 = exchange("ciao", "mondo")
print(s1, s2)


def filter_list(
    items: List[T],
    filter: Callable[[T], bool],
    conversion: Optional[Callable[[T], Union[str, int]]] = None
):
    result = []
    for item in items:
        if filter(item):
            if conversion:
                result.append(conversion(item))
            else:
                result.append(item)
    return result

list1 = [1, 2, 3, 4, 5, 6]
result = filter_list(list1, lambda x: x % 2 == 0)

print("END")