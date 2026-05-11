from pathlib import Path

import pygame
from PIL import Image, ImageSequence

from Batalla.Combate import turno_acciones
from IA.Agentes import AgenteAleatorio
from main import crear_equipos
from Modelos.Accion import Accion

RAIZ_PROYECTO = Path(__file__).resolve().parents[1]

ANCHO = 900
ALTO = 600
FPS = 60

PANEL_INFERIOR_Y = 430
LOG_RECT = pygame.Rect(24, 448, 400, 132)
COMANDOS_RECT = pygame.Rect(444, 448, 426, 132)
BOTON_ANCHO = 190
BOTON_ALTO = 38
BOTON_X_1 = 454
BOTON_X_2 = 664
BOTON_Y_1 = 448
BOTON_Y_2 = 492
BOTON_Y_3 = 536
POSICIONES_BOTONES = [
    (BOTON_X_1, BOTON_Y_1, BOTON_ANCHO, BOTON_ALTO),
    (BOTON_X_2, BOTON_Y_1, BOTON_ANCHO, BOTON_ALTO),
    (BOTON_X_1, BOTON_Y_2, BOTON_ANCHO, BOTON_ALTO),
    (BOTON_X_2, BOTON_Y_2, BOTON_ANCHO, BOTON_ALTO),
]
BOTON_SECUNDARIO = (BOTON_X_1, BOTON_Y_3, BOTON_ANCHO, BOTON_ALTO)

JUGADOR_PANEL_POS = (480, 305)
RIVAL_PANEL_POS = (100, 32)
JUGADOR_PLATAFORMA = pygame.Rect(112, 308, 300, 80)
RIVAL_PLATAFORMA = pygame.Rect(426, 160, 240, 54)
JUGADOR_SPRITE_POS = (250, 350)
RIVAL_SPRITE_POS = (550, 185)
JUGADOR_INDICADORES_POS = (504, 405)
RIVAL_INDICADORES_POS = (126, 132)

BLANCO = (245, 245, 245)
NEGRO = (30, 30, 30)
TEXTO_SUAVE = (48, 58, 65)
AZUL_FONDO = (124, 190, 222)
VERDE_SUELO = (110, 180, 110)
VERDE_CLARO = (164, 220, 142)
VERDE_OSCURO = (68, 145, 86)
AZUL_CIELO_CLARO = (185, 225, 245)
GRIS_PANEL = (235, 235, 235)
GRIS_BORDE = (60, 60, 60)
CARD_FONDO = (252, 250, 238)
CARD_BORDE = (49, 61, 75)
CARD_SOMBRA = (58, 87, 70)
BOTON_FONDO = (255, 248, 224)
BOTON_FONDO_HOVER = (255, 235, 166)
BOTON_BORDE = (63, 76, 92)
BOTON_SOMBRA = (105, 105, 105)
PANEL_FONDO = (238, 242, 236)
VERDE_HP = (70, 190, 80)
AMARILLO_HP = (230, 190, 55)
ROJO_HP = (220, 70, 70)
AZUL_ACTIVO = (45, 120, 210)
GRIS_DEBILITADO = (150, 150, 150)
ROJO_POKEBOLA = (220, 65, 65)

SPRITES = {
    "Pikachu": {"front": "pikachu.gif", "back": "pikachu_back.gif"},
    "Bulbasaur": {"front": "bulbasaur.gif", "back": "bulbasaur_back.gif"},
    "Charmander": {"front": "charmander.gif", "back": "charmander_back.gif"},
    "Charmander Rival": {"front": "charmander.gif", "back": "charmander_back.gif"},
    "Squirtle": {"front": "squirtle.gif", "back": "squirtle_back.gif"},
    "Squirtle Rival": {"front": "squirtle.gif", "back": "squirtle_back.gif"},
}


class Boton:
    def __init__(self, rect, texto, accion):
        self.rect = pygame.Rect(rect)
        self.texto = texto
        self.accion = accion

    def dibujar(self, pantalla, fuente):
        mouse_encima = self.contiene(pygame.mouse.get_pos())
        fondo = BOTON_FONDO_HOVER if mouse_encima else BOTON_FONDO
        sombra = self.rect.move(3, 3)

        pygame.draw.rect(pantalla, BOTON_SOMBRA, sombra, border_radius=7)
        pygame.draw.rect(pantalla, fondo, self.rect, border_radius=7)
        pygame.draw.rect(pantalla, BOTON_BORDE, self.rect, 2, border_radius=7)
        texto_boton = ajustar_texto(self.texto, fuente, self.rect.width - 16)
        texto = fuente.render(texto_boton, True, TEXTO_SUAVE)
        texto_rect = texto.get_rect(center=self.rect.center)
        pantalla.blit(texto, texto_rect)

    def contiene(self, posicion):
        return self.rect.collidepoint(posicion)


def ajustar_texto(texto, fuente, ancho_maximo):
    if fuente.size(texto)[0] <= ancho_maximo:
        return texto

    texto_corto = texto
    while texto_corto and fuente.size(texto_corto + "...")[0] > ancho_maximo:
        texto_corto = texto_corto[:-1]

    return texto_corto + "..."


def dibujar_card(pantalla, rect, fondo=CARD_FONDO, borde=CARD_BORDE):
    sombra = rect.move(4, 5)
    pygame.draw.rect(pantalla, CARD_SOMBRA, sombra, border_radius=9)
    pygame.draw.rect(pantalla, fondo, rect, border_radius=9)
    pygame.draw.rect(pantalla, borde, rect, 2, border_radius=9)


def color_hp(porcentaje):
    if porcentaje > 0.5:
        return VERDE_HP
    if porcentaje > 0.2:
        return AMARILLO_HP
    return ROJO_HP


def dibujar_barra_hp(pantalla, x, y, pokemon, ancho=180, alto=16):
    porcentaje = pokemon.hp_actual / pokemon.hp_max

    pygame.draw.rect(pantalla, (38, 45, 48), (x, y, ancho, alto), border_radius=5)
    pygame.draw.rect(
        pantalla,
        color_hp(porcentaje),
        (x + 2, y + 2, int((ancho - 4) * porcentaje), alto - 4),
        border_radius=5,
    )


def dibujar_escenario(pantalla):
    pantalla.fill(AZUL_FONDO)
    pygame.draw.rect(pantalla, AZUL_CIELO_CLARO, (0, 0, ANCHO, 170))
    pygame.draw.rect(pantalla, VERDE_CLARO, (0, 170, ANCHO, 260))
    pygame.draw.rect(pantalla, VERDE_SUELO, (0, 330, ANCHO, 100))

    pygame.draw.ellipse(pantalla, VERDE_OSCURO, JUGADOR_PLATAFORMA)
    pygame.draw.ellipse(pantalla, VERDE_CLARO,
                        JUGADOR_PLATAFORMA.inflate(-24, -12).move(0, -8))
    pygame.draw.ellipse(pantalla, VERDE_OSCURO, RIVAL_PLATAFORMA)
    pygame.draw.ellipse(pantalla, VERDE_CLARO,
                        RIVAL_PLATAFORMA.inflate(-22, -10).move(0, -7))

    pygame.draw.rect(pantalla, GRIS_PANEL, (0, PANEL_INFERIOR_Y, ANCHO, 170))
    pygame.draw.rect(pantalla, GRIS_BORDE,
                     (0, PANEL_INFERIOR_Y, ANCHO, 170), 3)


def dibujar_panel_pokemon(pantalla, fuente, fuente_pequena, x, y, pokemon):
    rect = pygame.Rect(x, y, 300, 84)
    dibujar_card(pantalla, rect)

    nombre = fuente.render(pokemon.nombre, True, TEXTO_SUAVE)
    etiqueta_hp = fuente_pequena.render("HP", True, (227, 178, 44))
    hp = fuente_pequena.render(
        f"{pokemon.hp_actual}/{pokemon.hp_max}", True, TEXTO_SUAVE)

    pantalla.blit(nombre, (x + 16, y + 10))
    pantalla.blit(etiqueta_hp, (x + 18, y + 48))
    dibujar_barra_hp(pantalla, x + 54, y + 48, pokemon, ancho=156, alto=14)
    pantalla.blit(hp, (x + 218, y + 45))


def cargar_gif(ruta, escala=2):
    imagen = Image.open(ruta)
    frames = []

    for frame in ImageSequence.Iterator(imagen):
        frame_rgba = frame.convert("RGBA")
        ancho, alto = frame_rgba.size
        datos = frame_rgba.tobytes()
        superficie = pygame.image.fromstring(
            datos, (ancho, alto), "RGBA").convert_alpha()
        superficie = pygame.transform.scale(
            superficie,
            (ancho * escala, alto * escala),
        )
        frames.append(superficie)

    return frames


def cargar_sprites():
    sprites = {}
    carpeta_sprites = RAIZ_PROYECTO / "Assets" / "Sprites"

    for nombre, archivos in SPRITES.items():
        sprites[nombre] = {}

        for orientacion, archivo in archivos.items():
            ruta = carpeta_sprites / archivo
            if ruta.exists():
                sprites[nombre][orientacion] = cargar_gif(ruta)

    return sprites


def dibujar_pokemon(
    pantalla,
    fuente_grande,
    x,
    y,
    pokemon,
    color,
    sprites,
    tick,
    orientacion,
):
    frames = sprites.get(pokemon.nombre, {}).get(orientacion)
    if frames:
        indice_frame = (tick // 8) % len(frames)
        sprite = frames[indice_frame]
        rect = sprite.get_rect(midbottom=(x, y))
        pantalla.blit(sprite, rect)
        return

    pygame.draw.circle(pantalla, color, (x, y), 55)
    inicial = fuente_grande.render(pokemon.nombre[0], True, BLANCO)
    pantalla.blit(inicial, inicial.get_rect(center=(x, y)))


def dibujar_indicadores_equipo(pantalla, equipo, x, y):
    for indice, pokemon in enumerate(equipo.pokemons):
        centro_x = x + indice * 28
        centro = (centro_x, y)
        color_superior = ROJO_POKEBOLA
        color_inferior = BLANCO
        borde = GRIS_BORDE

        if not pokemon.esta_vivo():
            color_superior = GRIS_DEBILITADO
            color_inferior = (220, 220, 220)

        if indice == equipo.indice_activo and pokemon.esta_vivo():
            borde = AZUL_ACTIVO

        pygame.draw.circle(pantalla, color_inferior, centro, 10)
        pygame.draw.arc(
            pantalla,
            color_superior,
            (centro_x - 10, y - 10, 20, 20),
            3.14,
            6.28,
            10,
        )
        pygame.draw.line(pantalla, GRIS_BORDE,
                         (centro_x - 9, y), (centro_x + 9, y), 2)
        pygame.draw.circle(pantalla, borde, centro, 10, 2)
        pygame.draw.circle(pantalla, BLANCO, centro, 3)
        pygame.draw.circle(pantalla, GRIS_BORDE, centro, 3, 1)


def dibujar_log(pantalla, fuente, mensajes):
    dibujar_card(pantalla, LOG_RECT, fondo=PANEL_FONDO)

    for indice, linea in enumerate(mensajes[-4:]):
        linea_visible = ajustar_texto(linea, fuente, LOG_RECT.width - 32)
        texto_mensaje = fuente.render(linea_visible, True, TEXTO_SUAVE)
        pantalla.blit(texto_mensaje, (LOG_RECT.x + 16,
                      LOG_RECT.y + 14 + indice * 28))


def dibujar_panel_comandos(pantalla):
    dibujar_card(pantalla, COMANDOS_RECT, fondo=PANEL_FONDO)


def crear_botones_movimientos(equipo):
    botones = []
    pokemon = equipo.pokemon_activo()

    for indice, movimiento in enumerate(pokemon.movimientos[:4]):
        botones.append(
            Boton(POSICIONES_BOTONES[indice],
                  movimiento.nombre, Accion.atacar(indice))
        )

    if equipo.indices_cambios_validos():
        botones.append(Boton(BOTON_SECUNDARIO, "Cambiar", "mostrar_cambios"))

    return botones


def crear_botones_cambio(equipo, permitir_volver=True):
    botones = []

    for numero, indice in enumerate(equipo.indices_cambios_validos()[:4]):
        pokemon = equipo.pokemons[indice]
        texto = f"{pokemon.nombre} {pokemon.hp_actual}/{pokemon.hp_max}"
        botones.append(
            Boton(POSICIONES_BOTONES[numero], texto, Accion.cambiar(indice)))

    if permitir_volver:
        botones.append(Boton(BOTON_SECUNDARIO, "Volver", "volver_movimientos"))

    return botones


def mostrar_evento(evento):
    if evento["tipo"] == "cambio":
        if evento["exitoso"]:
            return f"{evento['equipo']} cambio a {evento['pokemon_nuevo']}"
        return f"{evento['equipo']} intento cambiar, pero no pudo"

    if evento["fallo"]:
        return f"{evento['atacante']} fallo"

    return f"{evento['atacante']} uso {evento['movimiento']} e hizo {evento['daño']} dano"


def elegir_reemplazo_ia_si_cayo(equipo, equipo_rival, agente):
    if equipo.pokemon_activo().esta_vivo():
        return None

    indice = agente.elegir_reemplazo(equipo, equipo_rival)
    if indice is None:
        return None

    anterior = equipo.pokemon_activo().nombre
    equipo.cambiar_a(indice)
    return f"{equipo.nombre} envia a {equipo.pokemon_activo().nombre} porque {anterior} cayo"


def agregar_mensajes(historial, nuevos_mensajes):
    historial.extend(nuevos_mensajes)
    return historial[-4:]


def crear_fuente(nombres, tamano, negrita=False):
    for nombre in nombres:
        fuente_disponible = pygame.font.match_font(nombre)
        if fuente_disponible:
            return pygame.font.Font(fuente_disponible, tamano)

    return pygame.font.SysFont("arial", tamano, bold=negrita)


def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Pokefisi - Batalla")
    reloj = pygame.time.Clock()
    fuente = crear_fuente(["segoeui", "arial"], 21)
    fuente_pequena = crear_fuente(["segoeui", "arial"], 15)
    fuente_grande = crear_fuente(["segoeuisemibold", "arial"], 42, negrita=True)
    sprites = cargar_sprites()

    equipo_jugador, equipo_rival = crear_equipos()
    agente_rival = AgenteAleatorio()
    mensajes = ["Elige un movimiento"]
    botones = crear_botones_movimientos(equipo_jugador)
    modo_interfaz = "movimientos"
    terminado = False
    corriendo = True

    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

            if evento.type == pygame.MOUSEBUTTONDOWN and not terminado:
                for boton in botones:
                    if boton.contiene(evento.pos):
                        if boton.accion == "mostrar_cambios":
                            mensajes = agregar_mensajes(
                                mensajes,
                                ["Elige un Pokemon para cambiar"],
                            )
                            botones = crear_botones_cambio(equipo_jugador)
                            modo_interfaz = "cambios"
                            break

                        if boton.accion == "volver_movimientos":
                            mensajes = agregar_mensajes(
                                mensajes, ["Elige un movimiento"])
                            botones = crear_botones_movimientos(equipo_jugador)
                            modo_interfaz = "movimientos"
                            break

                        if modo_interfaz == "reemplazo":
                            pokemon_anterior = equipo_jugador.pokemon_activo().nombre
                            equipo_jugador.cambiar_a(boton.accion.indice)
                            mensajes = agregar_mensajes(
                                mensajes,
                                [
                                    f"Adelante {equipo_jugador.pokemon_activo().nombre}",
                                    f"{pokemon_anterior} ya no puede pelear",
                                ],
                            )
                            botones = crear_botones_movimientos(equipo_jugador)
                            modo_interfaz = "movimientos"
                            break

                        accion_jugador = boton.accion
                        accion_rival = agente_rival.elegir_accion(
                            equipo_rival, equipo_jugador)
                        eventos = turno_acciones(
                            equipo_jugador,
                            equipo_rival,
                            accion_jugador,
                            accion_rival,
                        )

                        textos = [mostrar_evento(e) for e in eventos]
                        reemplazo_rival = elegir_reemplazo_ia_si_cayo(
                            equipo_rival,
                            equipo_jugador,
                            agente_rival,
                        )

                        if reemplazo_rival:
                            textos.append(reemplazo_rival)

                        if not equipo_jugador.tiene_pokemon_vivos():
                            textos.append("Gana el rival")
                            terminado = True
                        elif not equipo_rival.tiene_pokemon_vivos():
                            textos.append("Gana el jugador")
                            terminado = True
                        elif not equipo_jugador.pokemon_activo().esta_vivo():
                            textos.append("Elige tu siguiente Pokemon")
                            botones = crear_botones_cambio(
                                equipo_jugador,
                                permitir_volver=False,
                            )
                            modo_interfaz = "reemplazo"
                            mensajes = agregar_mensajes(mensajes, textos)
                            break

                        mensajes = agregar_mensajes(mensajes, textos)
                        botones = crear_botones_movimientos(equipo_jugador)
                        modo_interfaz = "movimientos"
                        break

        dibujar_escenario(pantalla)

        jugador = equipo_jugador.pokemon_activo()
        rival = equipo_rival.pokemon_activo()

        dibujar_panel_pokemon(
            pantalla,
            fuente,
            fuente_pequena,
            RIVAL_PANEL_POS[0],
            RIVAL_PANEL_POS[1],
            rival,
        )
        dibujar_panel_pokemon(
            pantalla,
            fuente,
            fuente_pequena,
            JUGADOR_PANEL_POS[0],
            JUGADOR_PANEL_POS[1],
            jugador,
        )
        dibujar_indicadores_equipo(
            pantalla,
            equipo_rival,
            RIVAL_INDICADORES_POS[0],
            RIVAL_INDICADORES_POS[1],
        )
        dibujar_indicadores_equipo(
            pantalla,
            equipo_jugador,
            JUGADOR_INDICADORES_POS[0],
            JUGADOR_INDICADORES_POS[1],
        )
        tick = pygame.time.get_ticks() // 16
        dibujar_pokemon(
            pantalla,
            fuente_grande,
            JUGADOR_SPRITE_POS[0],
            JUGADOR_SPRITE_POS[1],
            jugador,
            (235, 190, 65),
            sprites,
            tick,
            "back",
        )
        dibujar_pokemon(
            pantalla,
            fuente_grande,
            RIVAL_SPRITE_POS[0],
            RIVAL_SPRITE_POS[1],
            rival,
            (95, 170, 95),
            sprites,
            tick,
            "front",
        )

        dibujar_log(pantalla, fuente, mensajes)
        dibujar_panel_comandos(pantalla)

        for boton in botones:
            boton.dibujar(pantalla, fuente)

        pygame.display.flip()
        reloj.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
