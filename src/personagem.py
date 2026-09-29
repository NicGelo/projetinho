import random
from abc import ABC, abstractmethod


class Personagem(ABC):

    def __init__(self, nome, vida, ataque, defesa):
        self.nome = nome
        self.vida = vida
        self.vida_maxima = vida
        self.ataque = ataque
        self.defesa = defesa

    def esta_vivo(self):
        return self.vida > 0

    def receber_dano(self, dano):
        dano_efetivo = max(0, dano - self.defesa)
        self.vida = max(0, self.vida - dano_efetivo)
        pass

    def calcular_ataque(self, alvo, dano_base):
        valor = random.randint(1, 20)

        if valor == 1:
            self.vida = max(0, self.vida - 10)
            print(f"{self.nome} falhou criticamente e recebeu 10 de dano.")
            return

        if 2 <= valor <= 9:
            print(f"{self.nome} errou o ataque.")
            return

        if valor == 10:
            dano = 10
            print(f"{self.nome} acertou com dano mínimo: {dano}.")
        elif 11 <= valor <= 19:
            dano = dano_base
            print(f"{self.nome} acertou o ataque e causou {dano} de dano.")
        else:
            dano = int(dano_base * 1.5)
            print(f"{self.nome} acertou um golpe crítico! Dano: {dano}.")

        alvo.receber_dano(dano)

    @abstractmethod
    def atacar(self, alvo):
        pass

    def usar_item(self, item):
        item.usar(self)

    def mostrar_status(self):
        print(
            f"{self.nome} | "
            f"Vida: {self.vida} | "
            f"Ataque: {self.ataque} | "
            f"Defesa: {self.defesa}"
        )
