from poção import Item
from guerreiro import Guerreiro
from mago import Mago
from arqueiro import Arqueiro
from Inimigo import Inimigo
from turnos import Batalha


def escolher_classe():
    print("\nEscolha sua classe:")
    print("1 - Guerreiro")
    print("2 - Mago")
    print("3 - Arqueiro")

    while True:
        escolha = input("Digite o número da classe: ")

        if escolha == "1":
            jogador = Guerreiro("Arthur")
            break
        elif escolha == "2":
            jogador = Mago("Merlin")
            break
        elif escolha == "3":
            jogador = Arqueiro("Legolas")
            break
        else:
            print("Opção inválida. Escolha 1, 2 ou 3.")

    jogador.inventario = [Item("Poção", 20)]
    return jogador


def criar_inimigo_padrao():
    return Inimigo(
        nome="Goblin",
        vida=100,
        ataque=15,
        defesa=5
    )


def criar_boss_final():
    return Inimigo(
        nome="Rei Goblin",
        vida=220,
        ataque=35,
        defesa=20
    )


def jogar_uma_rodada():
    jogador = escolher_classe()

    inimigo = criar_inimigo_padrao()
    batalha = Batalha(jogador, inimigo)
    batalha.iniciar()

    if not jogador.esta_vivo():
        print("\nVocê morreu! Reiniciando o jogo...\n")
        return False

    print("\nVocê venceu o primeiro inimigo!")

    boss = criar_boss_final()
    batalha_final = Batalha(jogador, boss)
    batalha_final.iniciar()

    if not jogador.esta_vivo():
        print("\nVocê morreu diante do Rei Goblin. O jogo reiniciará...\n")
        return False

    print("\nParabéns, você é novo rei dos Goblins")
    return True


def main():
    while True:
        jogar_uma_rodada()


if __name__ == "__main__":
    main()
