try:
    from .inimigo import Inimigo
except ImportError:  # pragma: no cover
    from inimigo import Inimigo


class Boss(Inimigo):

    def __init__(self, nome="Rei Goblin"):
        super().__init__(
            nome=nome,
            vida=220,
            ataque=35,
            defesa=20
        )
