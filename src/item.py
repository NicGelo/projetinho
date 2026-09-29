class Item:

    def __init__(self, nome, valor):
        self.nome = nome
        self.valor = valor

    def usar(self, personagem):
        vida_maxima = getattr(personagem, 'vida_maxima', float('inf'))
        personagem.vida = min(vida_maxima, personagem.vida + self.valor)
