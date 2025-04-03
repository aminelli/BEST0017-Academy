# uso di map

numbers = [1, 2, 3, 4, 5, 6, 10, 123]

names = [("antonio",1021), ("giuseppe",32) , ("marco",3) ]


def square(n):
    return n ** 2

square2 = lambda n: n **2

sum2 = lambda a, b: a + b

calc = square(5)
calc = sum2(5, 3)

even_and_odd = lambda n: "Pari" if n % 2 == 0 else "Dispari"
test1 = even_and_odd(4)

isEven = lambda n: n % 2 == 0 

sortedNamesById = sorted(names, key=lambda x: x[1] )

print(sortedNamesById)

listEven = list(filter(isEven, numbers))
print(listEven)

mapping = map(square, numbers)

mapping2 = map(
    lambda n: n **2, 
    numbers
)

mapping2 = map(
    square2, 
    numbers
)


print(numbers)
print(list(mapping))
print(list(mapping2))