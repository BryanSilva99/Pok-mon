import math
from pathlib import Path

import pygame
from PIL import Image, ImageSequence

from Batalla.Combate import turno_acciones
from Datos.PokemonDataset import catalogo_pokemon, crear_equipo_desde_nombres
from IA.Agentes import AgenteHeuristico
from Modelos.Accion import Accion


ROOT = Path(__file__).resolve().parents[1]
SPRITE_DIR = ROOT / "Assets" / "Sprites"

WIDTH = 1024
HEIGHT = 576
FPS = 60
DEFAULT_TEAM_SIZE = 3
AI_TURN_MS = 850

INK = (29, 34, 43)
INK_2 = (58, 67, 82)
PAPER = (244, 238, 214)
PAPER_2 = (232, 222, 190)
PANEL = (250, 245, 220)
PANEL_DARK = (194, 181, 139)
RED = (205, 64, 58)
RED_DARK = (128, 47, 52)
BLUE = (64, 124, 184)
BLUE_DARK = (42, 78, 122)
GREEN = (77, 153, 94)
GREEN_DARK = (44, 99, 74)
GOLD = (229, 181, 73)
CREAM = (255, 250, 226)
SHADOW = (42, 47, 58)
WHITE = (248, 248, 240)
BLACK = (18, 20, 26)
DISABLED = (145, 151, 154)

TYPE_COLORS = {
    "normal": (164, 158, 128),
    "fuego": (220, 100, 52),
    "agua": (68, 126, 198),
    "electrico": (222, 182, 58),
    "planta": (82, 156, 78),
    "hielo": (98, 176, 190),
    "lucha": (174, 70, 58),
    "veneno": (145, 82, 154),
    "tierra": (190, 144, 70),
    "volador": (112, 136, 194),
    "psiquico": (212, 82, 126),
    "bicho": (136, 158, 52),
    "roca": (150, 126, 70),
    "fantasma": (96, 82, 138),
    "dragon": (88, 78, 184),
    "siniestro": (82, 66, 58),
    "acero": (136, 144, 158),
    "hada": (218, 126, 178),
}


def clamp(value, low, high):
    return max(low, min(high, value))


def draw_text(surface, font, text, pos, color=INK, center=False):
    rendered = font.render(text, False, color)
    rect = rendered.get_rect()
    if center:
        rect.center = pos
    else:
        rect.topleft = pos
    surface.blit(rendered, rect)
    return rect


def fit_text(font, text, max_width):
    if font.size(text)[0] <= max_width:
        return text
    clipped = text
    while clipped and font.size(clipped + "..")[0] > max_width:
        clipped = clipped[:-1]
    return clipped + ".."


def draw_panel(surface, rect, fill=PANEL, border=INK, shadow=True):
    if shadow:
        pygame.draw.rect(surface, SHADOW, rect.move(5, 5), border_radius=0)
    pygame.draw.rect(surface, fill, rect, border_radius=0)
    pygame.draw.rect(surface, WHITE, rect.inflate(-8, -8), 2, border_radius=0)
    pygame.draw.rect(surface, border, rect, 4, border_radius=0)


def draw_pixel_pattern(surface, offset=0):
    surface.fill((154, 200, 196))
    for y in range(-16, HEIGHT, 32):
        for x in range(-16, WIDTH, 32):
            color = (137, 185, 185) if (x // 32 + y // 32) % 2 == 0 else (170, 214, 203)
            pygame.draw.rect(surface, color, (x + offset % 32, y, 16, 16))
    pygame.draw.rect(surface, (116, 176, 142), (0, 360, WIDTH, 216))
    pygame.draw.rect(surface, (80, 140, 104), (0, 444, WIDTH, 132))


def load_image_frames(path, scale=2):
    image = Image.open(path)
    frames = []
    iterator = ImageSequence.Iterator(image) if path.suffix.lower() == ".gif" else [image]
    for frame in iterator:
        frame = frame.convert("RGBA")
        w, h = frame.size
        surf = pygame.image.fromstring(frame.tobytes(), (w, h), "RGBA").convert_alpha()
        surf = pygame.transform.scale(surf, (w * scale, h * scale))
        frames.append(surf)
    return frames


class AssetStore:
    def __init__(self):
        self.sprites = {}
        self.card_cache = {}

    def load(self, names):
        for name in names:
            slug = name.lower()
            self.sprites[name] = {}
            for orientation, suffixes in [
                ("front", [".gif", ".png"]),
                ("back", ["_back.gif", "_back.png"]),
            ]:
                for suffix in suffixes:
                    path = SPRITE_DIR / f"{slug}{suffix}"
                    if path.exists():
                        self.sprites[name][orientation] = load_image_frames(path)
                        break

    def sprite(self, name, orientation="front", size=64, frame_index=0):
        key = (name, orientation, size, frame_index)
        if key in self.card_cache:
            return self.card_cache[key]

        frames = self.sprites.get(name, {}).get(orientation)
        if not frames:
            return None
        image = frames[frame_index % len(frames)]
        rect = image.get_rect()
        scale = min(size / rect.width, size / rect.height)
        new_size = (max(1, int(rect.width * scale)), max(1, int(rect.height * scale)))
        scaled = pygame.transform.scale(image, new_size)
        self.card_cache[key] = scaled
        return scaled


class Button:
    def __init__(self, rect, text, action, primary=False):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.action = action
        self.primary = primary
        self.enabled = True
        self.phase = 0

    def update(self):
        self.phase += 1

    def contains(self, pos):
        return self.enabled and self.rect.collidepoint(pos)

    def draw(self, surface, font):
        hovered = self.contains(pygame.mouse.get_pos())
        lift = -2 if hovered else 0
        rect = self.rect.move(0, lift)
        fill = RED if self.primary else CREAM
        border = RED_DARK if self.primary else INK
        text = WHITE if self.primary else INK
        if not self.enabled:
            fill = DISABLED
            border = INK_2
            text = (90, 94, 98)
        elif hovered:
            fill = (230, 82, 70) if self.primary else WHITE

        pygame.draw.rect(surface, SHADOW, rect.move(4, 5))
        pygame.draw.rect(surface, fill, rect)
        pygame.draw.rect(surface, WHITE, rect.inflate(-8, -8), 2)
        pygame.draw.rect(surface, border, rect, 4)
        draw_text(surface, font, self.text, rect.center, text, center=True)


class PokemonCard:
    def __init__(self, data, rect):
        self.data = data
        self.rect = pygame.Rect(rect)
        self.phase = 0

    def update(self):
        self.phase += 1

    def contains(self, pos):
        return self.rect.collidepoint(pos)

    def draw(self, surface, fonts, assets, owner=None, active_team=False, frame_index=0):
        font, small, tiny = fonts
        hovered = self.contains(pygame.mouse.get_pos())
        selected = owner is not None
        blocked = selected and not active_team
        pulse = int(2 * math.sin(self.phase / 8)) if selected else 0
        rect = self.rect.move(0, -2 if hovered else 0)
        fill = (235, 248, 255) if selected else CREAM
        border = BLUE if owner == "equipo1" else GREEN if owner == "equipo2" else INK_2

        pygame.draw.rect(surface, SHADOW, rect.move(3, 4))
        pygame.draw.rect(surface, fill, rect)
        pygame.draw.rect(surface, border, rect.inflate(pulse, pulse), 4 if selected else 2)

        sprite = assets.sprite(self.data["nombre"], "front", 42, frame_index)
        if sprite:
            surface.blit(sprite, sprite.get_rect(center=(rect.centerx, rect.y + 26)))
        else:
            pygame.draw.circle(surface, PAPER_2, (rect.centerx, rect.y + 26), 18)
            draw_text(surface, font, self.data["nombre"][0], (rect.centerx, rect.y + 26), INK, center=True)

        draw_text(surface, tiny, fit_text(tiny, self.data["nombre"], rect.width - 10), (rect.centerx, rect.y + 50), INK, center=True)
        x = rect.x + 7
        for pokemon_type in self.data["tipos"][:2]:
            color = TYPE_COLORS.get(pokemon_type, INK_2)
            chip = pygame.Rect(x, rect.y + 63, 48, 14)
            pygame.draw.rect(surface, color, chip)
            draw_text(surface, tiny, pokemon_type[:5], chip.center, WHITE, center=True)
            x += 52

        stat_w = max(8, int((self.data["velocidad"] / 140) * (rect.width - 14)))
        pygame.draw.rect(surface, (70, 76, 86), (rect.x + 7, rect.bottom - 10, rect.width - 14, 5))
        pygame.draw.rect(surface, GOLD, (rect.x + 7, rect.bottom - 10, stat_w, 5))
        if selected:
            badge = pygame.Rect(rect.right - 54, rect.y + 5, 48, 16)
            pygame.draw.rect(surface, border, badge)
            draw_text(surface, tiny, "Elegido", badge.center, WHITE, center=True)
        if blocked:
            veil = pygame.Surface(rect.size, pygame.SRCALPHA)
            veil.fill((230, 230, 230, 125))
            surface.blit(veil, rect)


class TeamSlot:
    def __init__(self, rect, index):
        self.rect = pygame.Rect(rect)
        self.index = index

    def draw(self, surface, font, tiny, assets, name=None, frame_index=0):
        pygame.draw.rect(surface, PAPER_2, self.rect)
        pygame.draw.rect(surface, INK, self.rect, 3)
        if not name:
            draw_text(surface, tiny, f"Slot {self.index + 1}", self.rect.center, INK_2, center=True)
            return
        sprite = assets.sprite(name, "front", min(28, self.rect.height - 4), frame_index)
        if sprite:
            surface.blit(sprite, sprite.get_rect(center=(self.rect.x + 22, self.rect.centery)))
        draw_text(
            surface,
            tiny,
            fit_text(tiny, name, self.rect.width - 50),
            (self.rect.x + 42, self.rect.centery - tiny.get_height() // 2),
            INK,
        )


class Screen:
    def __init__(self, game):
        self.game = game

    def enter(self):
        pass

    def handle_event(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self, surface):
        pass


class StartScreen(Screen):
    def __init__(self, game):
        super().__init__(game)
        self.button = Button((408, 426, 208, 52), "Comenzar", "mode", primary=True)
        self.ticks = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.button.contains(event.pos):
            self.game.manager.go_to("mode")
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE):
            self.game.manager.go_to("mode")

    def update(self, dt):
        self.ticks += 1
        self.button.update()

    def draw(self, surface):
        f = self.game.fonts
        draw_pixel_pattern(surface, self.ticks // 3)
        y_bob = int(math.sin(self.ticks / 22) * 5)
        for name, pos, size in [
            ("Charizard", (178, 346 + y_bob), 112),
            ("Garchomp", (846, 360 - y_bob), 118),
            ("Jolteon", (144, 170 - y_bob), 84),
        ]:
            sprite = self.game.assets.sprite(name, "front", size, self.ticks // 6)
            if sprite:
                surface.blit(sprite, sprite.get_rect(center=pos))

        title_shadow = f["title"].render("Pokefisi", False, SHADOW)
        title = f["title"].render("Pokefisi", False, CREAM)
        surface.blit(title_shadow, title_shadow.get_rect(center=(WIDTH // 2 + 5, 214 + 5)))
        surface.blit(title, title.get_rect(center=(WIDTH // 2, 214)))
        draw_text(surface, f["medium"], "Combates retro de criaturas por turnos", (WIDTH // 2, 296), INK, center=True)
        if (self.ticks // 32) % 2 == 0:
            draw_text(surface, f["small"], "Presiona ENTER o pulsa comenzar", (WIDTH // 2, 338), INK_2, center=True)
        self.button.draw(surface, f["medium"])


class ModeScreen(Screen):
    def __init__(self, game):
        super().__init__(game)
        self.mode = "player_ia"
        self.back = Button((70, 504, 140, 44), "Volver", "back")
        self.next = Button((806, 504, 150, 44), "Continuar", "next", primary=True)
        self.cards = {
            "player_ia": pygame.Rect(112, 190, 340, 228),
            "ia_ia": pygame.Rect(572, 190, 340, 228),
        }

    def handle_event(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN:
            return
        if self.back.contains(event.pos):
            self.game.manager.go_to("start")
        elif self.next.contains(event.pos):
            self.game.mode = self.mode
            self.game.manager.go_to("size")
        else:
            for mode, rect in self.cards.items():
                if rect.collidepoint(event.pos):
                    self.mode = mode

    def update(self, dt):
        self.back.update()
        self.next.update()

    def draw_option(self, surface, rect, title, subtitle, selected, color, icon):
        pygame.draw.rect(surface, SHADOW, rect.move(6, 7))
        pygame.draw.rect(surface, CREAM if selected else PANEL, rect)
        pygame.draw.rect(surface, color if selected else INK, rect, 5 if selected else 3)
        pygame.draw.rect(surface, WHITE, rect.inflate(-12, -12), 2)
        pygame.draw.circle(surface, color, (rect.x + 62, rect.y + 62), 36)
        draw_text(surface, self.game.fonts["large"], icon, (rect.x + 62, rect.y + 62), WHITE, center=True)
        draw_text(surface, self.game.fonts["large"], title, (rect.x + 36, rect.y + 118), INK)
        draw_text(surface, self.game.fonts["small"], subtitle, (rect.x + 36, rect.y + 162), INK_2)
        draw_text(surface, self.game.fonts["tiny"], "Seleccionado" if selected else "Pulsa para elegir", (rect.x + 36, rect.y + 196), color)

    def draw(self, surface):
        surface.fill((192, 216, 208))
        draw_text(surface, self.game.fonts["large"], "Elige modalidad", (72, 72), INK)
        draw_text(surface, self.game.fonts["medium"], "Selecciona como se tomaran las decisiones.", (76, 126), INK_2)
        self.draw_option(surface, self.cards["player_ia"], "P1 vs IA", "Tu eliges movimientos y cambios.", self.mode == "player_ia", BLUE, "P1")
        self.draw_option(surface, self.cards["ia_ia"], "IA vs IA", "Dos agentes combaten solos.", self.mode == "ia_ia", GREEN, "AI")
        self.back.draw(surface, self.game.fonts["small"])
        self.next.draw(surface, self.game.fonts["small"])


class TeamSizeScreen(Screen):
    def __init__(self, game):
        super().__init__(game)
        self.team_size = DEFAULT_TEAM_SIZE
        self.back = Button((70, 504, 140, 44), "Volver", "back")
        self.next = Button((806, 504, 150, 44), "Continuar", "next", primary=True)
        self.cards = {
            3: pygame.Rect(112, 190, 340, 228),
            4: pygame.Rect(572, 190, 340, 228),
        }

    def enter(self):
        self.team_size = self.game.team_size

    def handle_event(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN:
            return
        if self.back.contains(event.pos):
            self.game.manager.go_to("mode")
        elif self.next.contains(event.pos):
            self.game.team_size = self.team_size
            select = self.game.manager.screens["select"]
            select.configure(self.game.mode, self.team_size)
            self.game.manager.go_to("select")
        else:
            for team_size, rect in self.cards.items():
                if rect.collidepoint(event.pos):
                    self.team_size = team_size

    def update(self, dt):
        self.back.update()
        self.next.update()

    def draw_option(self, surface, rect, title, subtitle, selected, color):
        pygame.draw.rect(surface, SHADOW, rect.move(6, 7))
        pygame.draw.rect(surface, CREAM if selected else PANEL, rect)
        pygame.draw.rect(surface, color if selected else INK, rect, 5 if selected else 3)
        pygame.draw.rect(surface, WHITE, rect.inflate(-12, -12), 2)
        draw_text(surface, self.game.fonts["title"], title, (rect.centerx, rect.y + 72), color, center=True)
        draw_text(surface, self.game.fonts["large"], "VS", (rect.centerx, rect.y + 132), INK, center=True)
        draw_text(surface, self.game.fonts["small"], subtitle, (rect.x + 34, rect.y + 174), INK_2)
        draw_text(surface, self.game.fonts["tiny"], "Seleccionado" if selected else "Pulsa para elegir", (rect.x + 34, rect.y + 204), color)

    def draw(self, surface):
        surface.fill((192, 216, 208))
        draw_text(surface, self.game.fonts["large"], "Tamano de batalla", (72, 72), INK)
        mode_label = "P1 vs IA" if self.game.mode == "player_ia" else "IA vs IA"
        draw_text(surface, self.game.fonts["medium"], f"Modalidad: {mode_label}", (76, 126), INK_2)
        self.draw_option(surface, self.cards[3], "3", "Combate rapido y claro.", self.team_size == 3, BLUE)
        self.draw_option(surface, self.cards[4], "4", "Mas opciones de cambio.", self.team_size == 4, GREEN)
        self.back.draw(surface, self.game.fonts["small"])
        self.next.draw(surface, self.game.fonts["small"])


class PokemonSelectScreen(Screen):
    def __init__(self, game):
        super().__init__(game)
        self.catalog = catalogo_pokemon()
        self.cards = []
        self.team1 = []
        self.team2 = []
        self.team_size = DEFAULT_TEAM_SIZE
        self.active_team = "equipo1"
        self.message = self.selection_message()
        self.mode = "player_ia"
        self.back = Button((40, 522, 118, 38), "Volver", "back")
        self.clear = Button((172, 522, 124, 38), "Limpiar", "clear")
        self.start = Button((812, 522, 170, 38), "Iniciar batalla", "start", primary=True)
        self.team1_button = Button((34, 122, 128, 34), "Equipo 1", "team1", primary=True)
        self.team2_button = Button((176, 122, 128, 34), "Equipo 2", "team2")
        self.create_cards()

    def create_cards(self):
        self.cards = []
        for i, data in enumerate(self.catalog):
            col = i % 6
            row = i // 6
            rect = pygame.Rect(348 + col * 106, 112 + row * 79, 96, 72)
            self.cards.append(PokemonCard(data, rect))

    def configure(self, mode, team_size):
        self.mode = mode
        self.set_team_size(team_size)
        self.message = self.selection_message()

    def selection_message(self):
        equipo = "Equipo 1" if self.active_team == "equipo1" else "Equipo 2"
        return f"Elige {self.team_size} criaturas para {equipo}."

    def current_team(self):
        return self.team1 if self.active_team == "equipo1" else self.team2

    def other_team(self):
        return self.team2 if self.active_team == "equipo1" else self.team1

    def ready(self):
        return len(self.team1) == self.team_size and len(self.team2) == self.team_size

    def handle_event(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN:
            return
        if self.back.contains(event.pos):
            self.game.manager.go_to("size")
            return
        if self.clear.contains(event.pos):
            self.current_team().clear()
            self.message = "Equipo limpio."
            return
        if self.start.contains(event.pos):
            if not self.ready():
                self.message = "Completa ambos equipos antes de iniciar."
                return
            self.game.start_battle(self.team1, self.team2)
            return
        if self.team1_button.contains(event.pos):
            self.active_team = "equipo1"
            self.team1_button.primary = True
            self.team2_button.primary = False
            self.message = self.selection_message()
            return
        if self.team2_button.contains(event.pos):
            self.active_team = "equipo2"
            self.team1_button.primary = False
            self.team2_button.primary = True
            self.message = self.selection_message()
            return
        for card in self.cards:
            if card.contains(event.pos):
                self.toggle(card.data["nombre"])
                return

    def toggle(self, name):
        current = self.current_team()
        other = self.other_team()
        if name in current:
            current.remove(name)
            self.message = f"{name} removido."
        elif name in other:
            self.message = f"{name} ya esta en el otro equipo."
        elif len(current) >= self.team_size:
            self.message = f"Ese equipo ya tiene {self.team_size} criaturas."
        else:
            current.append(name)
            self.message = f"{name} elegido."

    def set_team_size(self, team_size):
        self.team_size = team_size
        self.game.team_size = team_size
        self.team1 = self.team1[:team_size]
        self.team2 = self.team2[:team_size]
        self.message = self.selection_message()

    def update(self, dt):
        self.start.enabled = self.ready()
        for button in [
            self.back,
            self.clear,
            self.start,
            self.team1_button,
            self.team2_button,
        ]:
            button.update()
        for card in self.cards:
            card.update()

    def draw_team_panel(self, surface, title, team, rect, active):
        fill = (232, 246, 255) if active else PANEL
        draw_panel(surface, rect, fill=fill, border=BLUE if active else INK)
        draw_text(
            surface,
            self.game.fonts["small"],
            f"{title}: {len(team)}/{self.team_size}",
            (rect.x + 14, rect.y + 12),
            INK,
        )
        for i in range(self.team_size):
            slot = TeamSlot((rect.x + 14, rect.y + 38 + i * 26, rect.width - 28, 24), i)
            slot.draw(
                surface,
                self.game.fonts["small"],
                self.game.fonts["tiny"],
                self.game.assets,
                team[i] if i < len(team) else None,
                pygame.time.get_ticks() // 120,
            )

    def draw(self, surface):
        surface.fill((198, 216, 204))
        draw_text(surface, self.game.fonts["large"], "Seleccion de equipo", (34, 28), INK)
        mode_label = "P1 vs IA" if self.mode == "player_ia" else "IA vs IA"
        draw_text(surface, self.game.fonts["small"], f"{mode_label} | {self.team_size} vs {self.team_size}", (38, 82), INK_2)
        self.team1_button.draw(surface, self.game.fonts["tiny"])
        self.team2_button.draw(surface, self.game.fonts["tiny"])
        self.draw_team_panel(surface, "Equipo 1", self.team1, pygame.Rect(32, 170, 292, 150), self.active_team == "equipo1")
        self.draw_team_panel(surface, "Equipo 2", self.team2, pygame.Rect(32, 342, 292, 154), self.active_team == "equipo2")
        draw_text(surface, self.game.fonts["medium"], "Criaturas disponibles", (348, 62), INK)
        draw_text(surface, self.game.fonts["tiny"], self.message, (350, 90), INK_2)
        for card in self.cards:
            owner = "equipo1" if card.data["nombre"] in self.team1 else "equipo2" if card.data["nombre"] in self.team2 else None
            card.draw(
                surface,
                (self.game.fonts["small"], self.game.fonts["tiny"], self.game.fonts["micro"]),
                self.game.assets,
                owner,
                owner == self.active_team,
                pygame.time.get_ticks() // 120,
            )
        self.back.draw(surface, self.game.fonts["tiny"])
        self.clear.draw(surface, self.game.fonts["tiny"])
        self.start.draw(surface, self.game.fonts["tiny"])


class BattleScreen(Screen):
    def __init__(self, game):
        super().__init__(game)
        self.mode = "player_ia"
        self.team_size = DEFAULT_TEAM_SIZE
        self.team1 = None
        self.team2 = None
        self.agent1 = AgenteHeuristico()
        self.agent2 = AgenteHeuristico()
        self.messages = []
        self.buttons = []
        self.interface_mode = "moves"
        self.finished = False
        self.last_ai_turn = 0

    def setup(self, mode, names1, names2, team_size=DEFAULT_TEAM_SIZE):
        self.mode = mode
        self.team_size = team_size
        name1 = "Player 1" if mode == "player_ia" else "IA 1"
        name2 = "IA" if mode == "player_ia" else "IA 2"
        self.team1 = crear_equipo_desde_nombres(name1, names1)
        self.team2 = crear_equipo_desde_nombres(name2, names2)
        self.messages = ["Elige un movimiento"] if mode == "player_ia" else ["Combate automatico"]
        self.buttons = self.move_buttons() if mode == "player_ia" else []
        self.interface_mode = "moves"
        self.finished = False
        self.last_ai_turn = pygame.time.get_ticks()

    def move_buttons(self):
        pokemon = self.team1.pokemon_activo()
        buttons = []
        positions = [(552, 444), (750, 444), (552, 492), (750, 492)]
        for i, move in enumerate(pokemon.movimientos[:4]):
            buttons.append(Button((positions[i][0], positions[i][1], 178, 36), move.nombre, Accion.atacar(i)))
        if self.team1.indices_cambios_validos():
            buttons.append(Button((354, 492, 156, 36), "Cambiar", "switch"))
        return buttons

    def switch_buttons(self, allow_back=True):
        buttons = []
        positions = [(552, 444), (750, 444), (552, 492)]
        for n, idx in enumerate(self.team1.indices_cambios_validos()[:3]):
            pokemon = self.team1.pokemons[idx]
            buttons.append(Button((positions[n][0], positions[n][1], 178, 36), pokemon.nombre, Accion.cambiar(idx)))
        if allow_back:
            buttons.append(Button((354, 492, 156, 36), "Volver", "moves"))
        return buttons

    def event_text(self, event):
        if event["tipo"] == "cambio":
            if event["exitoso"]:
                return f"{event['equipo']} cambio a {event['pokemon_nuevo']}"
            return f"{event['equipo']} no pudo cambiar"
        if event["fallo"]:
            return f"{event['atacante']} fallo"
        return f"{event['atacante']} uso {event['movimiento']} ({event['daño']})"

    def add_messages(self, texts):
        self.messages.extend(texts)
        self.messages = self.messages[-4:]

    def ai_replace(self, team, rival, agent):
        if team.pokemon_activo().esta_vivo():
            return None
        idx = agent.elegir_reemplazo(team, rival)
        if idx is None:
            return None
        old = team.pokemon_activo().nombre
        team.cambiar_a(idx)
        return f"{team.nombre} envia a {team.pokemon_activo().nombre} por {old}"

    def finish(self, texts, winner):
        texts.append(f"Gana {winner}")
        self.finished = True
        self.add_messages(texts)
        self.buttons = [Button((354, 492, 156, 36), "Inicio", "home", primary=True)]

    def review_state(self, texts, human_replace=False):
        replacement = self.ai_replace(self.team2, self.team1, self.agent2)
        if replacement:
            texts.append(replacement)
        if not self.team1.tiene_pokemon_vivos():
            self.finish(texts, self.team2.nombre)
            return "done"
        if not self.team2.tiene_pokemon_vivos():
            self.finish(texts, self.team1.nombre)
            return "done"
        if human_replace and not self.team1.pokemon_activo().esta_vivo():
            texts.append("Elige tu siguiente criatura")
            self.buttons = self.switch_buttons(allow_back=False)
            self.interface_mode = "replace"
            self.add_messages(texts)
            return "replace"
        return None

    def play_ai_turn(self):
        if self.finished:
            return
        action1 = self.agent1.elegir_accion(self.team1, self.team2)
        action2 = self.agent2.elegir_accion(self.team2, self.team1)
        events = turno_acciones(self.team1, self.team2, action1, action2)
        texts = [self.event_text(event) for event in events]
        replacement = self.ai_replace(self.team1, self.team2, self.agent1)
        if replacement:
            texts.append(replacement)
        if self.review_state(texts):
            return
        self.add_messages(texts)

    def handle_button(self, button):
        if button.action == "home":
            self.game.manager.go_to("start")
            return
        if button.action == "switch":
            self.interface_mode = "switch"
            self.buttons = self.switch_buttons()
            self.add_messages(["Elige una criatura"])
            return
        if button.action == "moves":
            self.interface_mode = "moves"
            self.buttons = self.move_buttons()
            return
        if self.interface_mode == "replace":
            old = self.team1.pokemon_activo().nombre
            self.team1.cambiar_a(button.action.indice)
            self.add_messages([f"Adelante {self.team1.pokemon_activo().nombre}", f"{old} no puede pelear"])
            self.interface_mode = "moves"
            self.buttons = self.move_buttons()
            return
        action1 = button.action
        action2 = self.agent2.elegir_accion(self.team2, self.team1)
        events = turno_acciones(self.team1, self.team2, action1, action2)
        texts = [self.event_text(event) for event in events]
        result = self.review_state(texts, human_replace=True)
        if result == "done":
            return
        if result == "replace":
            return
        self.add_messages(texts)
        self.buttons = self.move_buttons()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button.contains(event.pos):
                    self.handle_button(button)
                    break
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.manager.go_to("start")

    def update(self, dt):
        for button in self.buttons:
            button.update()
        if self.mode == "ia_ia" and not self.finished:
            now = pygame.time.get_ticks()
            if now - self.last_ai_turn >= AI_TURN_MS:
                self.play_ai_turn()
                self.last_ai_turn = now

    def draw_hp_box(self, surface, pokemon, rect, align_right=False):
        draw_panel(surface, rect, fill=CREAM, border=INK, shadow=True)
        draw_text(surface, self.game.fonts["small"], pokemon.nombre, (rect.x + 14, rect.y + 10), INK)
        pct = pokemon.hp_actual / pokemon.hp_max
        bar = pygame.Rect(rect.x + 48, rect.y + 44, rect.width - 70, 10)
        pygame.draw.rect(surface, INK, bar)
        color = GREEN if pct > 0.5 else GOLD if pct > 0.2 else RED
        pygame.draw.rect(surface, color, (bar.x + 2, bar.y + 2, int((bar.width - 4) * pct), bar.height - 4))
        draw_text(surface, self.game.fonts["tiny"], f"HP {pokemon.hp_actual}/{pokemon.hp_max}", (rect.x + 14, rect.y + 62), INK_2)

    def draw_party(self, surface, team, x, y):
        for i, pokemon in enumerate(team.pokemons):
            cx = x + i * 26
            top = RED if pokemon.esta_vivo() else DISABLED
            pygame.draw.circle(surface, WHITE, (cx, y), 9)
            pygame.draw.arc(surface, top, (cx - 9, y - 9, 18, 18), math.pi, math.tau, 8)
            pygame.draw.circle(surface, INK, (cx, y), 9, 2)

    def draw_text_box(self, surface):
        draw_panel(surface, pygame.Rect(32, 424, 470, 124), fill=CREAM, border=INK)
        for i, msg in enumerate(self.messages[-4:]):
            draw_text(surface, self.game.fonts["small"], fit_text(self.game.fonts["small"], msg, 430), (52, 444 + i * 24), INK)
        draw_panel(surface, pygame.Rect(526, 424, 462, 124), fill=PANEL, border=INK)
        if self.mode == "ia_ia" and not self.finished:
            draw_text(surface, self.game.fonts["medium"], "Batalla automatica", (552, 456), INK)
            draw_text(surface, self.game.fonts["small"], "Los agentes estan decidiendo.", (552, 494), INK_2)
        for button in self.buttons:
            button.draw(surface, self.game.fonts["tiny"])

    def draw(self, surface):
        surface.fill((150, 200, 208))
        pygame.draw.rect(surface, (176, 222, 204), (0, 156, WIDTH, 268))
        pygame.draw.rect(surface, (102, 165, 112), (0, 332, WIDTH, 92))
        pygame.draw.ellipse(surface, (72, 130, 88), (132, 306, 300, 70))
        pygame.draw.ellipse(surface, (96, 154, 104), (598, 166, 270, 56))

        player = self.team1.pokemon_activo()
        enemy = self.team2.pokemon_activo()
        frame_index = pygame.time.get_ticks() // 90
        p_sprite = self.game.assets.sprite(player.nombre, "back", 150, frame_index)
        e_sprite = self.game.assets.sprite(enemy.nombre, "front", 126, frame_index)
        if p_sprite:
            surface.blit(p_sprite, p_sprite.get_rect(midbottom=(286, 352)))
        if e_sprite:
            surface.blit(e_sprite, e_sprite.get_rect(midbottom=(734, 192)))
        self.draw_hp_box(surface, enemy, pygame.Rect(52, 52, 310, 90))
        self.draw_hp_box(surface, player, pygame.Rect(642, 296, 310, 90))
        self.draw_party(surface, self.team2, 78, 150)
        self.draw_party(surface, self.team1, 668, 394)
        self.draw_text_box(surface)


class ScreenManager:
    def __init__(self, game):
        self.game = game
        self.screens = {}
        self.current = None
        self.fade = 255
        self.fade_dir = -1

    def register(self, name, screen):
        self.screens[name] = screen

    def go_to(self, name):
        self.current = self.screens[name]
        self.current.enter()
        self.fade = 255
        self.fade_dir = -1

    def handle_event(self, event):
        if self.current:
            self.current.handle_event(event)

    def update(self, dt):
        if self.current:
            self.current.update(dt)
        if self.fade > 0:
            self.fade = clamp(self.fade - 18, 0, 255)

    def draw(self, surface):
        if self.current:
            self.current.draw(surface)
        if self.fade > 0:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.fill(BLACK)
            overlay.set_alpha(self.fade)
            surface.blit(overlay, (0, 0))


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Pokefisi")
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.mode = "player_ia"
        self.team_size = DEFAULT_TEAM_SIZE
        self.fonts = self.load_fonts()
        self.assets = AssetStore()
        self.assets.load([entry["nombre"] for entry in catalogo_pokemon()] + ["Pikachu"])
        self.manager = ScreenManager(self)
        self.manager.register("start", StartScreen(self))
        self.manager.register("mode", ModeScreen(self))
        self.manager.register("size", TeamSizeScreen(self))
        self.manager.register("select", PokemonSelectScreen(self))
        self.manager.register("battle", BattleScreen(self))
        self.manager.go_to("start")

    def load_fonts(self):
        names = ["Press Start 2P", "Perfect DOS VGA 437", "monospace", "couriernew", "arial"]

        def make(size, bold=False):
            for name in names:
                path = pygame.font.match_font(name)
                if path:
                    return pygame.font.Font(path, size)
            return pygame.font.SysFont("monospace", size, bold=bold)

        return {
            "title": make(68, True),
            "large": make(34, True),
            "medium": make(22, True),
            "small": make(16),
            "tiny": make(13),
            "micro": make(10),
        }

    def start_battle(self, names1, names2):
        battle = self.manager.screens["battle"]
        battle.setup(self.mode, names1, names2, self.team_size)
        self.manager.go_to("battle")

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.manager.handle_event(event)
            self.manager.update(dt)
            self.manager.draw(self.window)
            pygame.display.flip()
        pygame.quit()


def main():
    Game().run()
