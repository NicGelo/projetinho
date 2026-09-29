from personagem import Personagem


class Inimigo(Personagem):

    def __init__(self, nome, vida, ataque, defesa):
        super().__init__(
            nome=nome,
            vida=170,
            ataque=40,
            defesa=15
        )

    def atacar(self, alvo):
        self.calcular_ataque(alvo, self.ataque)
