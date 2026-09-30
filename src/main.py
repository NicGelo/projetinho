import random

try:
    from .item import Item
    from .guerreiro import Guerreiro
    from .mago import Mago
    from .Arqueiro import Arqueiro
    from .inimigo import Inimigo
    from .boss import Boss
    from .batalha import Batalha
except ImportError:  # pragma: no cover
    from item import Item
    from guerreiro import Guerreiro
    from mago import Mago
    from Arqueiro import Arqueiro
    from inimigo import Inimigo
    from boss import Boss
    from batalha import Batalha


def exibir_boas_vindas():
    print("\n" + "=" * 60)
    print("        BEM-VINDO AO REINO DOS GOBLINS")
    print("=" * 60)
    print("Sua missão: derrotar os goblins e vencer o Rei Goblin.")
    print("Mas cuidado: cada derrota pode custar seu reino...")
    print("=" * 60)


def escolher_classe():
    print("\nEscolha sua classe:")
    print("1 - Guerreiro")
    print("2 - Mago")
    print("3 - Arqueiro")

    while True:
        escolha = input("Digite o número da classe: ").strip()

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
    print(f"\nVocê escolheu {jogador.nome}!")
    return jogador


def criar_inimigo_padrao():
    nomes = ["Goblin Caçador", "Goblin Espadachim", "Goblin Ladrão", "Goblin Berserker"]
    return Inimigo(
        nome=random.choice(nomes),
        vida=random.randint(70, 110),
        ataque=random.randint(12, 22),
        defesa=random.randint(4, 7)
    )


def criar_boss_final():
    return Boss(nome="Rei Goblin")


def jogar_uma_rodada():
    jogador = escolher_classe()

    print("\nVocê avança para o campo dos goblins...")
    inimigo = criar_inimigo_padrao()
    batalha = Batalha(jogador, inimigo)
    batalha.iniciar()

    if not jogador.esta_vivo():
        print("\nVocê morreu na jornada! Reiniciando o jogo...\n")
        return False

    jogador.vida_maxima += 50
    jogador.vida = min(jogador.vida_maxima, jogador.vida + 50)
    jogador.ataque += 10
    print(f"\nVitória! Você derrotou {inimigo.nome} e ganhou +50 de vida e +10 de ataque!")
    print("Agora a arena final o espera...")

    boss = criar_boss_final()
    batalha_final = Batalha(jogador, boss)
    batalha_final.iniciar()

    if not jogador.esta_vivo():
        print("\nVocê caiu diante do Rei Goblin. O reino precisa de um novo herói...\n")
        return False

    print("\nParabéns! Você derrotou o Rei Goblin e se tornou o novo Rei Goblin.")
    print("A guerra terminou, mas a lenda agora começa.")
    return True


def main():
    try:
        from src.jogo_pygame import main as pygame_main
        pygame_main()
    except ImportError:
        exibir_boas_vindas()
        while True:
            jogar_uma_rodada()


if __name__ == "__main__":
    main()
