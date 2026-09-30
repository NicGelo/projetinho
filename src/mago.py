try:
    from .personagem import Personagem
except ImportError:  # pragma: no cover
    from personagem import Personagem


class Mago(Personagem):

    def __init__(self, nome):
        super().__init__(
            nome=nome,
            vida=90,
            ataque=30,
            defesa=5
        )
        self.mana_maxima = 100
        self.mana = self.mana_maxima

    def defender(self):
        super().defender()
        self.mana = min(self.mana_maxima, self.mana + 35)
        print(f"{self.nome} recuperou 35 de mana. Mana atual: {self.mana}/{self.mana_maxima}.")

    def atacar(self, alvo):
        self.calcular_ataque(alvo, self.ataque)

    def usar_magia(self, alvo):
        if self.mana <= 0:
            print("O mago não possui mana suficiente.")
            return

        self.calcular_ataque(alvo, self.ataque + 25)
        self.mana = max(0, self.mana - 45)
