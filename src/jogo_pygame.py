import random

import pygame

try:
    from .guerreiro import Guerreiro
    from .mago import Mago
    from .Arqueiro import Arqueiro
    from .inimigo import Inimigo
    from .boss import Boss
    from .item import Item
except ImportError:  # pragma: no cover
    from guerreiro import Guerreiro
    from mago import Mago
    from Arqueiro import Arqueiro
    from inimigo import Inimigo
    from boss import Boss
    from item import Item


WIDTH = 1000
HEIGHT = 650

COLORS = {
    "bg": (20, 20, 30),
    "panel": (38, 40, 48),
    "panel2": (55, 58, 68),
    "gold": (255, 195, 66),
    "white": (240, 240, 240),
    "red": (220, 80, 80),
    "green": (90, 200, 120),
    "blue": (95, 160, 255),
    "purple": (170, 120, 255),
    "orange": (255, 154, 66),
    "dark": (10, 10, 18),
    "shadow": (0, 0, 0),
    "gray": (180, 180, 180),
}


def criar_inimigo_padrao():
    nomes = ["Goblin Caçador", "Goblin Espadachim", "Goblin Ladrão", "Goblin Berserker"]
    return Inimigo(
        nome=random.choice(nomes),
        vida=random.randint(70, 110),
        ataque=random.randint(12, 22),
        defesa=random.randint(4, 7),
    )


def criar_boss_final():
    return Boss(nome="Rei Goblin")


class Button:
    def __init__(self, x, y, w, h, label, color, text_color=COLORS["white"]):
        self.rect = pygame.Rect(x, y, w, h)
        self.label = label
        self.color = color
        self.text_color = text_color

    def draw(self, screen, font):
        pygame.draw.rect(screen, COLORS["shadow"], self.rect.move(4, 4), border_radius=12)
        pygame.draw.rect(screen, self.color, self.rect, border_radius=12)
        text = font.render(self.label, True, self.text_color)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def clicked(self, pos):
        return self.rect.collidepoint(pos)


class FloatingText:
    def __init__(self, x, y, text, color, speed=1.5, size=24):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.speed = speed
        self.life = 60
        self.size = size

    def update(self):
        self.y -= self.speed
        self.life -= 1

    def draw(self, screen, font):
        rendered = pygame.font.SysFont("arial", self.size, bold=True).render(self.text, True, self.color)
        screen.blit(rendered, (self.x, self.y))


class BattleGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Reino dos Goblins")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 24)
        self.small = pygame.font.SysFont("arial", 18)
        self.big = pygame.font.SysFont("arial", 30, bold=True)

        self.phase = "menu"
        self.player = None
        self.enemy = None
        self.message = "Escolha sua classe para começar."
        self.player_turn = True
        self.first_enemy_defeated = False
        self.floating_texts = []

        self.menu_buttons = [
            Button(160, 220, 200, 70, "Guerreiro", COLORS["gold"]),
            Button(400, 220, 200, 70, "Mago", COLORS["blue"]),
            Button(640, 220, 200, 70, "Arqueiro", COLORS["green"]),
        ]
        self.action_buttons = [
            Button(80, 500, 160, 60, "Atacar", COLORS["red"]),
            Button(260, 500, 160, 60, "Defender", COLORS["orange"]),
            Button(440, 500, 160, 60, "Magia", COLORS["purple"]),
            Button(620, 500, 160, 60, "Poção", COLORS["green"]),
            Button(800, 500, 120, 60, "Sair", COLORS["panel2"]),
        ]

    def escolher_jogador(self, classe):
        if classe == "Guerreiro":
            self.player = Guerreiro("Arthur")
        elif classe == "Mago":
            self.player = Mago("Merlin")
        elif classe == "Arqueiro":
            self.player = Arqueiro("Legolas")
        else:
            return

        self.player.inventario = [Item("Poção", 20)]
        self.player.vida_maxima = getattr(self.player, "vida_maxima", self.player.vida)
        self.start_battle()

    def start_battle(self):
        self.message = "Batalha iniciada!"
        self.player_turn = True
        self.enemy = criar_inimigo_padrao()
        self.phase = "battle"

    def set_boss_fight(self):
        self.enemy = criar_boss_final()
        self.player_turn = True
        self.message = "Batalha final! O Rei Goblin apareceu."
        self.phase = "boss"

    def draw_health_bar(self, x, y, width, height, value, max_value, color):
        bg = pygame.Rect(x, y, width, height)
        fill_width = width * max(0, value / max_value)
        fill = pygame.Rect(x, y, fill_width, height)

        pygame.draw.rect(self.screen, COLORS["dark"], bg, border_radius=10)
        pygame.draw.rect(self.screen, COLORS["panel2"], bg.inflate(4, 4), border_radius=12)
        pygame.draw.rect(self.screen, color, fill, border_radius=10)

        if value < max_value:
            pygame.draw.rect(self.screen, COLORS["shadow"], bg, 2, border_radius=10)

        text = self.small.render(f"{int(value)}/{int(max_value)}", True, COLORS["white"])
        self.screen.blit(text, (x + width + 10, y - 2))

    def draw_status_panel(self):
        panel = pygame.Rect(50, 40, 900, 130)
        pygame.draw.rect(self.screen, COLORS["panel"], panel, border_radius=18)

        if self.player:
            title = self.big.render(self.player.nome, True, COLORS["white"])
            self.screen.blit(title, (70, 55))
            self.draw_health_bar(70, 100, 300, 20, self.player.vida, self.player.vida_maxima, COLORS["green"])
            if hasattr(self.player, "mana"):
                self.draw_health_bar(70, 125, 300, 15, self.player.mana, self.player.mana_maxima, COLORS["blue"])

        if self.enemy:
            name = self.big.render(self.enemy.nome, True, COLORS["white"])
            self.screen.blit(name, (650, 55))
            self.draw_health_bar(620, 100, 300, 20, self.enemy.vida, self.enemy.vida_maxima, COLORS["red"])

    def draw_entity(self):
        if self.player:
            player_box = pygame.Rect(120, 220, 220, 180)
            pygame.draw.rect(self.screen, COLORS["panel2"], player_box, border_radius=18)
            if self.player.__class__.__name__ == "Guerreiro":
                icon_color = COLORS["gold"]
                icon = "⚔"
            elif self.player.__class__.__name__ == "Mago":
                icon_color = COLORS["blue"]
                icon = "🪄"
            else:
                icon_color = COLORS["green"]
                icon = "🏹"

            icon_text = self.big.render(icon, True, icon_color)
            self.screen.blit(icon_text, (201, 245))
            text = self.font.render(self.player.__class__.__name__, True, COLORS["white"])
            self.screen.blit(text, (155, 348))

            if self.player.esta_vivo():
                pygame.draw.rect(self.screen, COLORS["shadow"], pygame.Rect(150, 300, 160, 10), border_radius=6)
                pygame.draw.rect(self.screen, COLORS["green"], pygame.Rect(150, 300, 160 * (self.player.vida / self.player.vida_maxima), 10), border_radius=6)

        if self.enemy:
            enemy_box = pygame.Rect(650, 220, 220, 180)
            pygame.draw.rect(self.screen, COLORS["panel2"], enemy_box, border_radius=18)
            if self.enemy.__class__.__name__ == "Boss":
                icon = "👑😠"
            else:
                icon = "😠"
            icon_text = self.big.render(icon, True, COLORS["red"])
            self.screen.blit(icon_text, (725, 245))
            text = self.font.render(self.enemy.__class__.__name__, True, COLORS["white"])
            self.screen.blit(text, (705, 348))

            if self.enemy.esta_vivo():
                pygame.draw.rect(self.screen, COLORS["shadow"], pygame.Rect(690, 300, 160, 10), border_radius=6)
                pygame.draw.rect(self.screen, COLORS["red"], pygame.Rect(690, 300, 160 * (self.enemy.vida / self.enemy.vida_maxima), 10), border_radius=6)

    def draw_message_box(self):
        box = pygame.Rect(80, 380, 840, 90)
        pygame.draw.rect(self.screen, COLORS["panel2"], box, border_radius=16)
        text = self.font.render(self.message, True, COLORS["white"])
        self.screen.blit(text, (100, 410))

        for floating in self.floating_texts:
            floating.draw(self.screen, self.font)

    def draw_menu(self):
        self.screen.fill(COLORS["bg"])
        title = self.big.render("REINO DOS GOBLINS", True, COLORS["gold"])
        self.screen.blit(title, (290, 80))
        subtitle = self.font.render("Escolha sua classe:", True, COLORS["white"])
        self.screen.blit(subtitle, (410, 160))

        for btn in self.menu_buttons:
            btn.draw(self.screen, self.font)

    def draw_battle(self):
        self.screen.fill(COLORS["bg"])
        self.draw_status_panel()
        self.draw_entity()
        self.draw_message_box()

        for btn in self.action_buttons:
            btn.draw(self.screen, self.small)

        if self.player and hasattr(self.player, "mana"):
            mana_text = self.small.render(f"Mana: {self.player.mana}/{self.player.mana_maxima}", True, COLORS["blue"])
            self.screen.blit(mana_text, (80, 470))

    def handle_menu_click(self, pos):
        for btn in self.menu_buttons:
            if btn.clicked(pos):
                self.escolher_jogador(btn.label)
                return

    def add_floating_text(self, x, y, text, color, size=24):
        self.floating_texts.append(FloatingText(x, y, text, color, size=size))

    def handle_action_click(self, action):
        if not self.player or not self.enemy:
            return

        if action == "Atacar":
            self.player.atacar(self.enemy)
            if getattr(self.player, "ultimo_resultado", "hit") == "critico":
                self.show_hit_feedback(self.player, self.enemy, self.player.ultimo_dano, critical=True)
            elif getattr(self.player, "ultimo_resultado", "hit") in {"miss", "fail"}:
                self.show_hit_feedback(self.player, self.enemy, 0, failed=True)
            else:
                self.add_floating_text(300, 210, f"-{self.player.ultimo_dano}", COLORS["red"])
            self.message = f"{self.player.nome} atacou {self.enemy.nome}."
        elif action == "Defender":
            self.player.defender()
            self.add_floating_text(300, 210, "Defesa", COLORS["orange"])
            self.message = f"{self.player.nome} está defendendo."
        elif action == "Magia":
            if hasattr(self.player, "usar_magia"):
                self.player.usar_magia(self.enemy)
                if getattr(self.player, "ultimo_resultado", "hit") == "critico":
                    self.show_hit_feedback(self.player, self.enemy, self.player.ultimo_dano, critical=True)
                elif getattr(self.player, "ultimo_resultado", "hit") in {"miss", "fail"}:
                    self.show_hit_feedback(self.player, self.enemy, 0, failed=True)
                else:
                    self.add_floating_text(300, 210, f"-{self.player.ultimo_dano}", COLORS["purple"])
                self.message = f"{self.player.nome} usou magia."
            else:
                self.message = "Esse personagem não possui magia."
                return
        elif action == "Poção":
            if not hasattr(self.player, "inventario") or not self.player.inventario:
                self.message = "Você não tem poções."
                return
            item = self.player.inventario.pop(0)
            self.player.usar_item(item)
            self.add_floating_text(300, 210, "+20", COLORS["green"])
            self.message = f"{self.player.nome} usou {item.nome}."
        elif action == "Sair":
            self.phase = "menu"
            self.player = None
            self.enemy = None
            self.message = "Escolha sua classe para começar."
            return

        if not self.enemy.esta_vivo():
            if self.phase == "battle":
                self.player.vida_maxima += 50
                self.player.vida = min(self.player.vida_maxima, self.player.vida + 50)
                self.player.ataque += 10
                self.first_enemy_defeated = True
                self.message = f"Vitória! {self.enemy.nome} foi derrotado. +50 vida e +10 ataque."
                self.set_boss_fight()
                return

            if self.phase == "boss":
                self.message = "Você venceu o Rei Goblin! O reino agora é seu."
                self.phase = "won"
                return

        if self.player.esta_vivo() and self.enemy.esta_vivo():
            self.enemy.atacar(self.player)
            if getattr(self.enemy, "ultimo_resultado", "hit") == "critico":
                self.show_hit_feedback(self.enemy, self.player, self.enemy.ultimo_dano, critical=True)
            elif getattr(self.enemy, "ultimo_resultado", "hit") in {"miss", "fail"}:
                self.show_hit_feedback(self.enemy, self.player, 0, failed=True)
            else:
                self.add_floating_text(620, 210, f"-{self.enemy.ultimo_dano}", COLORS["red"])
            self.message = f"{self.enemy.nome} atacou {self.player.nome}."

        if not self.player.esta_vivo():
            self.message = "Você morreu. Reiniciando..."
            self.phase = "game_over"

    def show_hit_feedback(self, attacker, defender, amount, critical=False, failed=False):
        if critical:
            if defender is self.player:
                self.add_floating_text(250, 180, "CRITIC", COLORS["gold"], size=28)
            else:
                self.add_floating_text(720, 180, "CRITIC", COLORS["gold"], size=28)
        elif failed:
            if attacker is self.player:
                self.add_floating_text(300, 180, "FAIL", COLORS["gray"], size=28)
            else:
                self.add_floating_text(700, 180, "FAIL", COLORS["gray"], size=28)

        if defender is self.player:
            self.add_floating_text(250, 210, f"-{amount}", COLORS["red"], size=28)
        else:
            self.add_floating_text(720, 210, f"-{amount}", COLORS["red"], size=28)

    def update(self, events):
        for floating in self.floating_texts[:]:
            floating.update()
            if floating.life <= 0:
                self.floating_texts.remove(floating)

        for event in events:
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                if self.phase == "menu":
                    self.handle_menu_click(pos)
                elif self.phase in {"battle", "boss"}:
                    for btn in self.action_buttons:
                        if btn.clicked(pos):
                            self.handle_action_click(btn.label)
                            break
                elif self.phase in {"won", "game_over"}:
                    self.phase = "menu"
                    self.player = None
                    self.enemy = None
                    self.message = "Escolha sua classe para começar."
        return True

    def draw(self):
        if self.phase == "menu":
            self.draw_menu()
        elif self.phase in {"battle", "boss", "won", "game_over"}:
            self.draw_battle()

        if self.phase == "won":
            end_text = self.big.render("VITÓRIA!", True, COLORS["gold"])
            self.screen.blit(end_text, (420, 210))
        if self.phase == "game_over":
            end_text = self.big.render("DERROTA!", True, COLORS["red"])
            self.screen.blit(end_text, (430, 210))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            events = pygame.event.get()
            running = self.update(events)
            self.draw()
            self.clock.tick(60)
        pygame.quit()


def main():
    game = BattleGame()
    game.run()


if __name__ == "__main__":
    main()
