from personagem import Personagem

class Mago(Personagem):

    def __init__(self, nome):
        super().__init__(
            nome=nome,
            vida=90,
            ataque=30,
            defesa=5
        )

        self.mana = 100

    def atacar(self, alvo):
        self.calcular_ataque(alvo, self.ataque)

    def usar_magia(self, alvo):
        if self.mana <= 0:
            print("O mago não possui mana suficiente.")
            return

        self.calcular_ataque(alvo, self.ataque + 25)
        self.mana -= 45
