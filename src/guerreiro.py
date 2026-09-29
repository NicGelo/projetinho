from personagem import Personagem


class Guerreiro(Personagem):

    def __init__(self, nome):
        super().__init__(
            nome=nome,
            vida=130,
            ataque=25,
            defesa=15
        )

    def atacar(self, alvo):
        self.calcular_ataque(alvo, self.ataque)
