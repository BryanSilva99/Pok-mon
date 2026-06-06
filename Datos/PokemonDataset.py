import csv
import random
from pathlib import Path

from Modelos.Equipo import Equipo
from Modelos.Movimiento import Movimiento
from Modelos.Pokemon import Pokemon


RUTA_CSV = Path(__file__).resolve().parent.parent / "All_Pokemon.csv"

TIPOS = {
    "Normal": "normal",
    "Fire": "fuego",
    "Water": "agua",
    "Electric": "electrico",
    "Grass": "planta",
    "Ice": "hielo",
    "Fighting": "lucha",
    "Poison": "veneno",
    "Ground": "tierra",
    "Flying": "volador",
    "Psychic": "psiquico",
    "Bug": "bicho",
    "Rock": "roca",
    "Ghost": "fantasma",
    "Dragon": "dragon",
    "Dark": "siniestro",
    "Steel": "acero",
    "Fairy": "hada",
}

NOMBRES_SELECCIONADOS = [
    "Garchomp",
    "Tyranitar",
    "Venusaur",
    "Charizard",
    "Blastoise",
    "Gengar",
    "Alakazam",
    "Dragonite",
    "Arcanine",
    "Jigglypuff",
    "Gallade",
    "Lucario",
    "Gyarados",
    "Salamence",
    "Raichu",
    "Scizor",
    "Snorlax",
    "Metagross",
    "Sceptile",
    "Swampert",
    "Blaziken",
    "Torterra",
    "Infernape",
    "Empoleon",
    "Crobat",
    "Azumarill",
    "Vaporeon",
    "Flareon",
    "Jolteon",
    "Togekiss",
]

MOVIMIENTOS = {
    "Air Slash": ("volador", 75, 0.95),
    "Aqua Tail": ("agua", 90, 0.9),
    "Aura Sphere": ("lucha", 80, 1.0),
    "Bite": ("siniestro", 60, 1.0),
    "Blaze Kick": ("fuego", 85, 0.9),
    "Body Slam": ("normal", 85, 1.0),
    "Brick Break": ("lucha", 75, 1.0),
    "Bullet Punch": ("acero", 40, 1.0),
    "Close Combat": ("lucha", 120, 1.0),
    "Confusion": ("psiquico", 50, 1.0),
    "Crunch": ("siniestro", 80, 1.0),
    "Dragon Claw": ("dragon", 80, 1.0),
    "Dragon Pulse": ("dragon", 90, 1.0),
    "Dragon Rush": ("dragon", 100, 0.75),
    "Earth Power": ("tierra", 90, 1.0),
    "Earthquake": ("tierra", 100, 1.0),
    "Energy Ball": ("planta", 90, 1.0),
    "Extreme Speed": ("normal", 80, 1.0),
    "Feint Attack": ("siniestro", 60, 1.0),
    "Fire Blast": ("fuego", 110, 0.85),
    "Fire Fang": ("fuego", 65, 0.95),
    "Flamethrower": ("fuego", 90, 1.0),
    "Flare Blitz": ("fuego", 120, 1.0),
    "Flash Cannon": ("acero", 80, 1.0),
    "Focus Blast": ("lucha", 120, 0.7),
    "Giga Drain": ("planta", 75, 1.0),
    "Grass Knot": ("planta", 80, 1.0),
    "Hydro Pump": ("agua", 110, 0.8),
    "Hyper Beam": ("normal", 150, 0.9),
    "Ice Beam": ("hielo", 90, 1.0),
    "Ice Fang": ("hielo", 65, 0.95),
    "Iron Head": ("acero", 80, 1.0),
    "Leaf Blade": ("planta", 90, 1.0),
    "Mega Punch": ("normal", 80, 0.85),
    "Meteor Mash": ("acero", 90, 0.9),
    "Moonblast": ("hada", 95, 1.0),
    "Outrage": ("dragon", 120, 1.0),
    "Poison Fang": ("veneno", 50, 1.0),
    "Psychic": ("psiquico", 90, 1.0),
    "Psycho Cut": ("psiquico", 70, 1.0),
    "Quick Attack": ("normal", 40, 1.0),
    "Razor Leaf": ("planta", 55, 0.95),
    "Return": ("normal", 100, 1.0),
    "Rock Slide": ("roca", 75, 0.9),
    "Rock Throw": ("roca", 50, 0.9),
    "Rollout": ("roca", 30, 0.9),
    "Shadow Ball": ("fantasma", 80, 1.0),
    "Shadow Claw": ("fantasma", 70, 1.0),
    "Sludge Bomb": ("veneno", 90, 1.0),
    "Surf": ("agua", 90, 1.0),
    "Swift": ("normal", 60, 1.0),
    "Thunder": ("electrico", 110, 0.7),
    "Thunder Punch": ("electrico", 75, 1.0),
    "Thunderbolt": ("electrico", 90, 1.0),
    "Tri Attack": ("normal", 80, 1.0),
    "Water Pulse": ("agua", 60, 1.0),
    "Waterfall": ("agua", 80, 1.0),
    "Wing Attack": ("volador", 60, 1.0),
    "X-Scissor": ("bicho", 80, 1.0),
    "Zen Headbutt": ("psiquico", 80, 0.9),
}

MOVIMIENTOS_POR_POKEMON = {
    "Garchomp": ["Earthquake", "Dragon Claw", "Dragon Rush", "Crunch", "Rock Slide", "Fire Fang", "Aqua Tail", "Slash"],
    "Tyranitar": ["Crunch", "Rock Slide", "Earthquake", "Fire Fang", "Ice Fang", "Thunder Punch", "Hyper Beam", "Body Slam"],
    "Venusaur": ["Razor Leaf", "Giga Drain", "Energy Ball", "Sludge Bomb", "Earthquake", "Body Slam", "Grass Knot", "Hyper Beam"],
    "Charizard": ["Flamethrower", "Fire Blast", "Air Slash", "Wing Attack", "Dragon Claw", "Slash", "Fire Fang", "Hyper Beam"],
    "Blastoise": ["Surf", "Hydro Pump", "Water Pulse", "Ice Beam", "Bite", "Aqua Tail", "Body Slam", "Hyper Beam"],
    "Gengar": ["Shadow Ball", "Sludge Bomb", "Psychic", "Focus Blast", "Thunderbolt", "Dark Pulse", "Energy Ball", "Confusion"],
    "Alakazam": ["Psychic", "Psycho Cut", "Focus Blast", "Shadow Ball", "Energy Ball", "Confusion", "Swift", "Hyper Beam"],
    "Dragonite": ["Outrage", "Dragon Claw", "Dragon Rush", "Fire Punch", "Thunder Punch", "Aqua Tail", "Wing Attack", "Hyper Beam"],
    "Arcanine": ["Flamethrower", "Flare Blitz", "Fire Fang", "Extreme Speed", "Crunch", "Bite", "Iron Head", "Body Slam"],
    "Jigglypuff": ["Return", "Body Slam", "Moonblast", "Hyper Beam", "Rollout", "Swift", "Mega Punch", "Thunderbolt"],
    "Gallade": ["Close Combat", "Psycho Cut", "Psychic", "Leaf Blade", "Night Slash", "Brick Break", "Earthquake", "Slash"],
    "Lucario": ["Aura Sphere", "Close Combat", "Flash Cannon", "Iron Head", "Extreme Speed", "Dragon Pulse", "Crunch", "Bullet Punch"],
    "Gyarados": ["Waterfall", "Aqua Tail", "Hydro Pump", "Ice Fang", "Bite", "Crunch", "Dragon Rush", "Hyper Beam"],
    "Salamence": ["Outrage", "Dragon Claw", "Dragon Rush", "Flamethrower", "Fire Blast", "Crunch", "Wing Attack", "Hyper Beam"],
    "Raichu": ["Thunderbolt", "Thunder", "Thunder Punch", "Quick Attack", "Swift", "Iron Tail", "Body Slam", "Hyper Beam"],
    "Scizor": ["Bullet Punch", "X-Scissor", "Iron Head", "Slash", "Quick Attack", "Brick Break", "Night Slash", "Hyper Beam"],
    "Snorlax": ["Body Slam", "Return", "Crunch", "Earthquake", "Hyper Beam", "Rollout", "Mega Punch", "Thunder Punch"],
    "Metagross": ["Meteor Mash", "Zen Headbutt", "Psychic", "Iron Head", "Earthquake", "Rock Slide", "Bullet Punch", "Hyper Beam"],
    "Sceptile": ["Leaf Blade", "Energy Ball", "Giga Drain", "Razor Leaf", "Dragon Pulse", "Earthquake", "Quick Attack", "X-Scissor"],
    "Swampert": ["Earthquake", "Surf", "Hydro Pump", "Waterfall", "Ice Beam", "Rock Slide", "Aqua Tail", "Body Slam"],
    "Blaziken": ["Blaze Kick", "Flare Blitz", "Flamethrower", "Fire Blast", "Close Combat", "Brick Break", "Thunder Punch", "Quick Attack"],
    "Torterra": ["Earthquake", "Razor Leaf", "Energy Ball", "Giga Drain", "Crunch", "Rock Slide", "Body Slam", "Leaf Blade"],
    "Infernape": ["Close Combat", "Flare Blitz", "Flamethrower", "Fire Blast", "Mach Punch", "Thunder Punch", "Grass Knot", "Quick Attack"],
    "Empoleon": ["Surf", "Hydro Pump", "Flash Cannon", "Iron Head", "Ice Beam", "Waterfall", "Aqua Tail", "Drill Peck"],
    "Crobat": ["Air Slash", "Wing Attack", "Poison Fang", "Sludge Bomb", "Bite", "X-Scissor", "Shadow Ball", "Swift"],
    "Azumarill": ["Waterfall", "Aqua Tail", "Surf", "Hydro Pump", "Ice Beam", "Body Slam", "Rollout", "Moonblast"],
    "Vaporeon": ["Surf", "Hydro Pump", "Water Pulse", "Ice Beam", "Bite", "Quick Attack", "Body Slam", "Hyper Beam"],
    "Flareon": ["Flamethrower", "Fire Blast", "Flare Blitz", "Fire Fang", "Bite", "Quick Attack", "Body Slam", "Hyper Beam"],
    "Jolteon": ["Thunderbolt", "Thunder", "Thunder Punch", "Quick Attack", "Swift", "Shadow Ball", "Hyper Beam", "Body Slam"],
    "Togekiss": ["Air Slash", "Moonblast", "Aura Sphere", "Psychic", "Shadow Ball", "Extreme Speed", "Swift", "Hyper Beam"],
}

ALIAS_MOVIMIENTOS = {
    "Dark Pulse": ("siniestro", 80, 1.0),
    "Drill Peck": ("volador", 80, 1.0),
    "Fire Punch": ("fuego", 75, 1.0),
    "Iron Tail": ("acero", 100, 0.75),
    "Mach Punch": ("lucha", 40, 1.0),
    "Night Slash": ("siniestro", 70, 1.0),
    "Slash": ("normal", 70, 1.0),
}


def cargar_filas_csv():
    with open(RUTA_CSV, newline="", encoding="utf-8") as archivo:
        return list(csv.DictReader(archivo))


def cargar_pokemon_seleccionados():
    filas = {
        fila["Name"]: fila
        for fila in cargar_filas_csv()
        if fila["Name"] in NOMBRES_SELECCIONADOS
        and fila["Mega Evolution"] == "0.0"
        and fila["Alolan Form"] == "0.0"
        and fila["Galarian Form"] == "0.0"
    }
    faltantes = [nombre for nombre in NOMBRES_SELECCIONADOS if nombre not in filas]
    if faltantes:
        raise ValueError(f"Faltan Pokemon en {RUTA_CSV}: {', '.join(faltantes)}")

    return [filas[nombre] for nombre in NOMBRES_SELECCIONADOS]


def crear_movimiento(nombre):
    tipo, potencia, precision = MOVIMIENTOS.get(nombre, ALIAS_MOVIMIENTOS.get(nombre))
    return Movimiento(nombre, potencia, precision, tipo)


def crear_pokemon_desde_fila(fila):
    nombre = fila["Name"]
    tipo_primario = TIPOS[fila["Type 1"]]
    tipo_secundario = TIPOS.get(fila["Type 2"]) if fila["Type 2"] else None
    movimientos_disponibles = [
        crear_movimiento(nombre_movimiento)
        for nombre_movimiento in MOVIMIENTOS_POR_POKEMON[nombre]
    ]
    pokemon = Pokemon(
        nombre,
        int(fila["HP"]),
        max(int(fila["Att"]), int(fila["Spa"])),
        max(int(fila["Def"]), int(fila["Spd"])),
        int(fila["Spe"]),
        tipo_primario,
    )
    pokemon.tipo_secundario = tipo_secundario
    pokemon.tipos = [tipo for tipo in [tipo_primario, tipo_secundario] if tipo]
    pokemon.definir_movimientos_disponibles(movimientos_disponibles)

    for movimiento in random.sample(movimientos_disponibles, 4):
        pokemon.aprender_movimiento(movimiento)

    return pokemon


def crear_pool_pokemon():
    return [crear_pokemon_desde_fila(fila) for fila in cargar_pokemon_seleccionados()]


def crear_pokemon_por_nombre(nombre):
    for fila in cargar_pokemon_seleccionados():
        if fila["Name"] == nombre:
            return crear_pokemon_desde_fila(fila)

    raise ValueError(f"Pokemon no disponible: {nombre}")


def crear_equipo_desde_nombres(nombre_equipo, nombres):
    return Equipo(nombre_equipo, [crear_pokemon_por_nombre(nombre) for nombre in nombres])


def catalogo_pokemon():
    catalogo = []

    for fila in cargar_pokemon_seleccionados():
        tipos = [TIPOS[fila["Type 1"]]]
        if fila["Type 2"]:
            tipos.append(TIPOS[fila["Type 2"]])
        catalogo.append(
            {
                "nombre": fila["Name"],
                "tipos": tipos,
                "hp": int(fila["HP"]),
                "ataque": max(int(fila["Att"]), int(fila["Spa"])),
                "defensa": max(int(fila["Def"]), int(fila["Spd"])),
                "velocidad": int(fila["Spe"]),
            }
        )

    return catalogo


def crear_equipo_aleatorio(nombre, cantidad=3):
    filas = cargar_pokemon_seleccionados()
    seleccionados = random.sample(filas, cantidad)
    return Equipo(nombre, [crear_pokemon_desde_fila(fila) for fila in seleccionados])


def nombres_disponibles():
    return list(NOMBRES_SELECCIONADOS)
