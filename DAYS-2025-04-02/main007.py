'''
Python List Datatype
A metà strada tra array e liste Java
Può contenere contemporaneamente qualsiasi tipo di dato
'''

var1 = [4, "ciao", True, 10+4j, 1.24E-4]
print(var1, type(var1))
print(var1[1:3])

'''
Tuple: utili ad esempio per gestire i dati di una tabella
Differenze: le liste sono mutabili (valori, lunghezza), le tuple sono immutabili (sola lettura)
'''

var2 = (4, "ciao", True, 10+4j, 1.24E-4)
print(var2, type(var2))
print(var2[1:3])

# Liste e Tuple possono contenere al loro interno altre collezioni.
var3 = ([4, "ciao", True, 10+4j, 1.24E-4], [4, "ciao", True, 10+4j, 1.24E-4])

'''
Tipo Range
'''
var4 = range(5)
#print(var4)

# for i in var4:
#     print(i)

# for i in range(2,5):
#     print(i)

# for i in range(2,7,4):
#     print(i)

for i in range(0,101,2):
    print(i)

print("Fine programma")