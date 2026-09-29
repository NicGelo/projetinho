from poção import Item


class Batalha:

    def __init__(self, jogador, inimigo):
        self.jogador = jogador
        self.inimigo = inimigo

    def iniciar(self):

        print("=" * 40)
        print("        INÍCIO DA BATALHA")
        print("=" * 40)

        while self.jogador.esta_vivo() and self.inimigo.esta_vivo():

            print("\n--- STATUS ---")
            self.jogador.mostrar_status()
            self.inimigo.mostrar_status()

            print("\n--- AÇÕES ---")
            print("1 - Atacar")

            tem_magia = hasattr(self.jogador, "mana")
            if tem_magia:
                print("2 - Usar magia")
                print("3 - Usar item")
                print("4 - Fugir")
            else:
                print("2 - Usar item")
                print("3 - Fugir")

            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                self.jogador.atacar(self.inimigo)

            elif tem_magia and opcao == "2":
                if hasattr(self.jogador, "usar_magia"):
                    self.jogador.usar_magia(self.inimigo)
                else:
                    print("Este personagem não possui magia.")

            elif (tem_magia and opcao == "3") or (not tem_magia and opcao == "2"):
                if not hasattr(self.jogador, "inventario"):
                    self.jogador.inventario = [Item("Poção", 20)]

                if not self.jogador.inventario:
                    print("Você não possui itens.")
                    continue

                item = self.jogador.inventario.pop(0)
                self.jogador.usar_item(item)
                print(f"{self.jogador.nome} usou {item.nome}.")

            elif (tem_magia and opcao == "4") or (not tem_magia and opcao == "3"):
                print("Você fugiu da batalha!")
                return

            else:
                print("Opção inválida.")
                continue

            if not self.inimigo.esta_vivo():
                break

            self.inimigo.atacar(self.jogador)

        if not self.jogador.esta_vivo():
            print(f"{self.inimigo.nome} venceu a batalha!")
        elif not self.inimigo.esta_vivo():
            print(f"{self.jogador.nome} venceu a batalha!")
        else:
            print("A batalha foi encerrada.")
