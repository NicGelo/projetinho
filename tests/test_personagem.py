from unittest.mock import patch

from src.guerreiro import Guerreiro
from src.personagem import Personagem


class InimigoTeste(Personagem):
    def atacar(self, alvo):
        return None


def test_guerreiro_esta_vivo():
    guerreiro = Guerreiro("Arthur")
    assert guerreiro.esta_vivo() is True


def test_personagem_recebe_dano():
    personagem = InimigoTeste("Teste", 100, 10, 5)

    personagem.receber_dano(30)
    assert personagem.vida == 75

    personagem.receber_dano(200)
    assert personagem.vida == 0


def test_personagem_morre():
    personagem = InimigoTeste("Teste", 20, 10, 0)
    personagem.receber_dano(25)

    assert personagem.esta_vivo() is False
    assert personagem.vida == 0


def test_guerreiro_ataca():
    guerreiro = Guerreiro("Arthur")
    alvo = InimigoTeste("Goblin", 80, 10, 0)

    with patch("src.personagem.random.randint", return_value=11):
        guerreiro.atacar(alvo)

    assert alvo.vida == 55
