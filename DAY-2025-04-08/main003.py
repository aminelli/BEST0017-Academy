
class Volatile:
    
    def vola(self):
        return "Sto volando da Volatile"
    
    def parla(self):
        return "Sto parlando"
    
class AnimaleAcquatico:
    def nuota(Self):
        
        return "Sto nuotando"
    
    def parla(self):
        return "Sto parlando da AnimaleAcquatico"

    
class Pinguino(Volatile, AnimaleAcquatico):
    
    def __init__(self, nome):
        self.nome = nome
        
    def parla(self):
        super().parla()
        return "Sto parlando da Pinguino"

p1 = Pinguino("Pinguino")
print(p1.nuota())
print(p1.vola())
print(p1.parla())