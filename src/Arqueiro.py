from personagem import Personagem


class Arqueiro(Personagem):

    def __init__(self, nome):
        super().__init__(
            nome=nome,
            vida=100,
            ataque=20,
            defesa=12
        )

    def atacar(self, alvo):
        self.calcular_ataque(alvo, self.ataque)

    def flecha_precisa(self, alvo):
        self.calcular_ataque(alvo, self.ataque + 8)
