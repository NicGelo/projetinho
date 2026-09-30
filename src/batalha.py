try:
    from .item import Item
except ImportError:  # pragma: no cover
    from item import Item


class Batalha:

    def __init__(self, jogador, inimigo):
        self.jogador = jogador
        self.inimigo = inimigo

    def iniciar(self):
        print("=" * 50)
        print("        INÍCIO DA BATALHA")
        print(f"{self.jogador.nome} vs {self.inimigo.nome}")
        print("=" * 50)

        turno = 0

        while self.jogador.esta_vivo() and self.inimigo.esta_vivo():
            turno += 1
            print(f"\n=== Turno {turno} ===")
            print("\n--- STATUS ---")
            self.jogador.mostrar_status()
            self.inimigo.mostrar_status()

            print("\n--- AÇÕES ---")
            print("1 - Atacar")

            tem_magia = hasattr(self.jogador, "mana")
            if tem_magia:
                print("2 - Usar magia (custa 45 mana)")
                print("3 - Defender")
                print("4 - Usar item")
                print("5 - Fugir")
            else:
                print("2 - Defender")
                print("3 - Usar item")
                print("4 - Fugir")

            opcao = input("Escolha uma opção: ").strip()

            if opcao == "1":
                self.jogador.atacar(self.inimigo)

            elif tem_magia and opcao == "2":
                if self.jogador.mana < 45:
                    print(f"Mana insuficiente! Você tem {self.jogador.mana}/{self.jogador.mana_maxima}.")
                    continue
                if hasattr(self.jogador, "usar_magia"):
                    self.jogador.usar_magia(self.inimigo)
                else:
                    print("Este personagem não possui magia.")

            elif (tem_magia and opcao == "3") or (not tem_magia and opcao == "2"):
                self.jogador.defender()

            elif (tem_magia and opcao == "4") or (not tem_magia and opcao == "3"):
                if not hasattr(self.jogador, "inventario"):
                    self.jogador.inventario = [Item("Poção", 20)]

                if not self.jogador.inventario:
                    print("Você não possui itens.")
                    continue

                item = self.jogador.inventario.pop(0)
                self.jogador.usar_item(item)
                print(f"{self.jogador.nome} usou {item.nome}.")

            elif (tem_magia and opcao == "5") or (not tem_magia and opcao == "4"):
                print("Você fugiu da batalha!")
                return

            else:
                print("Opção inválida. Escolha uma ação válida.")
                continue

            if not self.inimigo.esta_vivo():
                print(f"\n{self.inimigo.nome} foi derrotado!")
                break

            print(f"\n{self.inimigo.nome} está atacando...")
            self.inimigo.atacar(self.jogador)

        if not self.jogador.esta_vivo():
            print(f"\n{self.inimigo.nome} venceu a batalha!")
        elif not self.inimigo.esta_vivo():
            print(f"\n{self.jogador.nome} venceu a batalha!")
        else:
            print("\nA batalha foi encerrada.")
