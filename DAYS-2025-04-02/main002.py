# TODO: da aggiustare
def fattoriale(n):
    if n == 0 or n == 1:  # Caso base
        return 1
    else:
        return n * fattoriale(n - 1)  # Passo ricorsivo

# Esempio di utilizzo
numero = 5
print(f"Il fattoriale di {numero} è {fattoriale(numero)}")
