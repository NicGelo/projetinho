import random


class Personagem:

    def __init__(self, nome, vida, ataque, defesa):
        self.nome = nome
        self.vida = vida
        self.vida_maxima = vida
        self.ataque = ataque
        self.defesa = defesa
        self.defendendo = False
        self.ultimo_resultado = "hit"
        self.ultimo_dano = 0
        self.ultimo_critico = False
        self.ultimo_fail = False

    def esta_vivo(self):
        return self.vida > 0

    def defender(self):
        self.defendendo = True
        print(f"{self.nome} entrou em modo de defesa.")

    def receber_dano(self, dano):
        dano_total = max(0, int(dano))

        if self.defendendo:
            dano_total = int(dano_total * 0.2)
            print(f"{self.nome} defendeu e reduziu o dano em 80%.")
            self.defendendo = False

        dano_efetivo = max(0, dano_total - self.defesa)
        self.vida = max(0, self.vida - dano_efetivo)

    def calcular_ataque(self, alvo, dano_base):
        valor = random.randint(1, 20)

        if valor == 1:
            self.ultimo_resultado = "fail"
            self.ultimo_dano = 0
            self.ultimo_critico = False
            self.ultimo_fail = True
            self.receber_dano(10)
            print(f"{self.nome} falhou criticamente e recebeu 10 de dano.")
            return

        if 2 <= valor <= 9:
            self.ultimo_resultado = "miss"
            self.ultimo_dano = 0
            self.ultimo_critico = False
            self.ultimo_fail = True
            print(f"{self.nome} errou o ataque.")
            return

        if valor == 10:
            dano = 10
            self.ultimo_resultado = "hit"
            self.ultimo_critico = False
            self.ultimo_fail = False
            self.ultimo_dano = dano
            print(f"{self.nome} acertou com dano mínimo: {dano}.")
        elif 11 <= valor <= 19:
            dano = dano_base
            self.ultimo_resultado = "hit"
            self.ultimo_critico = False
            self.ultimo_fail = False
            self.ultimo_dano = dano
            print(f"{self.nome} acertou o ataque e causou {dano} de dano.")
        else:
            dano = max(10, int(dano_base * 1.5))
            self.ultimo_resultado = "critico"
            self.ultimo_critico = True
            self.ultimo_fail = False
            self.ultimo_dano = dano
            print(f"{self.nome} acertou um golpe crítico! Dano: {dano}.")

        alvo.receber_dano(dano)
        alvo.ultimo_dano_recebido = dano
        alvo.ultimo_resultado_recebido = self.ultimo_resultado

    def atacar(self, alvo):
        raise NotImplementedError("Cada personagem deve implementar seu próprio ataque.")

    def usar_item(self, item):
        item.usar(self)

    def mostrar_status(self):
        status = (
            f"{self.nome} | "
            f"Vida: {self.vida} | "
            f"Ataque: {self.ataque} | "
            f"Defesa: {self.defesa}"
        )

        if self.defendendo:
            status += " | Estado: Defendendo"
        else:
            status += " | Estado: Atacando"

        if hasattr(self, "mana"):
            status += f" | Mana: {self.mana}/{self.mana_maxima}"

        print(status)
