# Uso di zip

lista1 = [1, 2, 3]
lista2 = ["Rosso", "Verde", "Giallo"]

# accorpamento è lazy: ovvero all'esecuzione della riga successiva, non accorpa ancora
zipped = zip(lista1, lista2)

print(type(zipped))

print(zipped)

# questo è il punto in zip accorpa i dati delle due liste
lista3 = list(zipped)
print(lista3)

# OUTPUT
# [(1, 'Rosso'), (2, 'Verde'), (3, 'Giallo')]


lista1 = [1, 2, 3, 4]
lista2 = ["Rosso", "Verde", "Giallo"]

# accorpamento è lazy: ovvero all'esecuzione della riga successiva, non accorpa ancora
zipped = zip(lista1, lista2)

print(type(zipped))

print(zipped)

# questo è il punto in zip accorpa i dati delle due liste
lista3 = list(zipped)
print(lista3)


lista1 = [1, 2, 3]
lista2 = ["Rosso", "Verde", "Giallo", "Blue"]

# accorpamento è lazy: ovvero all'esecuzione della riga successiva, non accorpa ancora
zipped = zip(lista1, lista2)

print(type(zipped))

print(zipped)

# questo è il punto in zip accorpa i dati delle due liste
lista3 = list(zipped)
print(lista3)


lista1 = range(4)
lista2 = ["Rosso", "Verde", "Giallo", "Blue"]

# accorpamento è lazy: ovvero all'esecuzione della riga successiva, non accorpa ancora
zipped = zip(lista1, lista2, strict = True)

print(type(zipped))

print(zipped)

# questo è il punto in zip accorpa i dati delle due liste
lista3 = list(zipped)
print(lista3)


lx1 = [1, 2, 3]
ly1 = [4, 5, 6]
print(lx1)
print(ly1)

zip1 = zip(lx1,ly1)


# lx2, ly2 = zip(*zip(lx1, ly1))
lx2, ly2 = zip(*zip1)

lz1 = list(zip1)

if (lx1 == list(lx2) and ly1 == list(ly2)):
    print("sono le stesse liste")
else:
    print("non sono le stesse liste")


# Destrutturazione lista con assegnazione multipla
x, y, z = [1, 2, 3]

primo, _, terzo = [1, 2, 3]

a, b, *others = [1, 2, 3, 5, 6, 7]



person = {'first_name': 'antonio', 'last_name': 'minelli', 'city': 'bergamo'}
person_others = {'age': 20, 'work': 'nullafacente'}

# first_name = person['first_name']
# last_name = person['last_name']
# city = person['city']

# {first_name, last_name, city} = person

first_name, last_name, city = person.values()

pr1 = {**person, **person_others}
print(pr1)

pr2 = person | person_others
print(pr2)

# {city, first_name } = person




print("END")