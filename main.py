from Batalla.Combate import turno_acciones
from Datos.PokemonDataset import crear_equipo_aleatorio
from IA.Agentes import AgenteAleatorio, AgenteHeuristico
from Modelos.Equipo import Equipo
from Modelos.Movimiento import Movimiento
from Modelos.Pokemon import Pokemon


def crear_movimientos():
    return {
        "rayo_carga": Movimiento("Rayo Carga", 50, 0.95, "electrico"),
        "placaje_electrico": Movimiento("Placaje Electrico", 90, 1.0, "electrico"),
        "golpe_cuerpo": Movimiento("Golpe Cuerpo", 85, 1.0, "normal"),
        "placaje": Movimiento("Placaje", 35, 1.0, "normal"),
        "rayo_solar": Movimiento("Rayo Solar", 120, 0.8, "planta"),
        "energibola": Movimiento("Energibola", 90, 0.9, "planta"),
        "ascuas": Movimiento("Ascuas", 40, 1.0, "fuego"),
        "pistola_agua": Movimiento("Pistola Agua", 40, 1.0, "agua"),
    }


def crear_pokemon(nombre, hp, ataque, defensa, velocidad, tipo, movimientos):
    pokemon = Pokemon(nombre, hp, ataque, defensa, velocidad, tipo)

    for movimiento in movimientos:
        pokemon.aprender_movimiento(movimiento)

    return pokemon


def crear_equipos():
    return crear_equipos_desde_dataset()


def crear_equipos_desde_dataset(tamano_equipo=3):
    equipo_jugador = crear_equipo_aleatorio("Heuristico", tamano_equipo)
    equipo_rival = crear_equipo_aleatorio("Aleatorio", tamano_equipo)

    return equipo_jugador, equipo_rival


def crear_equipos_demo_original():
    mov = crear_movimientos()

    pikachu = crear_pokemon(
        "Pikachu",
        60,
        55,
        40,
        90,
        "electrico",
        [mov["rayo_carga"], mov["placaje"], mov["golpe_cuerpo"], mov["placaje_electrico"]],
    )
    charmander = crear_pokemon(
        "Charmander",
        60,
        52,
        43,
        65,
        "fuego",
        [mov["ascuas"], mov["placaje"], mov["golpe_cuerpo"]],
    )
    squirtle = crear_pokemon(
        "Squirtle",
        60,
        48,
        65,
        43,
        "agua",
        [mov["pistola_agua"], mov["placaje"], mov["golpe_cuerpo"]],
    )

    bulbasaur = crear_pokemon(
        "Bulbasaur",
        60,
        50,
        45,
        40,
        "planta",
        [mov["placaje"], mov["rayo_solar"], mov["energibola"], mov["golpe_cuerpo"]],
    )
    charmander_rival = crear_pokemon(
        "Charmander Rival",
        60,
        52,
        43,
        65,
        "fuego",
        [mov["ascuas"], mov["placaje"], mov["golpe_cuerpo"]],
    )
    squirtle_rival = crear_pokemon(
        "Squirtle Rival",
        60,
        48,
        65,
        43,
        "agua",
        [mov["pistola_agua"], mov["placaje"], mov["golpe_cuerpo"]],
    )

    equipo_jugador = Equipo("Heuristico", [pikachu, charmander, squirtle])
    equipo_rival = Equipo("Aleatorio", [bulbasaur, charmander_rival, squirtle_rival])

    return equipo_jugador, equipo_rival


def mostrar_estado(equipo):
    activo = equipo.pokemon_activo()
    print(f"{equipo.nombre}: {activo.nombre} ({activo.hp_actual}/{activo.hp_max} HP)")


def mostrar_evento(evento):
    if evento["tipo"] == "cambio":
        if evento["exitoso"]:
            print(
                f"{evento['equipo']} cambio de {evento['pokemon_anterior']} "
                f"a {evento['pokemon_nuevo']}"
            )
        else:
            print(f"{evento['equipo']} intento cambiar, pero no pudo")
        return

    if evento["fallo"]:
        movimiento = evento.get("movimiento", "un movimiento")
        print(f"{evento['atacante']} uso {movimiento}... fallo")
        return

    print(
        f"{evento['atacante']} uso {evento['movimiento']} "
        f"e hizo {evento['daño']} daño"
    )

    if evento["mult"] > 1:
        print("Es super efectivo")
    elif evento["mult"] < 1:
        print("No es muy efectivo")


def revisar_pokemon_debilitado(equipo, equipo_rival, agente):
    if equipo.pokemon_activo().esta_vivo():
        return

    reemplazo = agente.elegir_reemplazo(equipo, equipo_rival)

    if reemplazo is not None:
        pokemon_anterior = equipo.pokemon_activo().nombre
        equipo.cambiar_a(reemplazo)
        pokemon_nuevo = equipo.pokemon_activo().nombre
        print(f"{equipo.nombre} envia a {pokemon_nuevo} porque {pokemon_anterior} cayo")


def ejecutar_demo_consola():
    equipo_jugador, equipo_rival = crear_equipos()
    agente_jugador = AgenteHeuristico()
    agente_rival = AgenteAleatorio()
    turno_numero = 1

    while equipo_jugador.tiene_pokemon_vivos() and equipo_rival.tiene_pokemon_vivos():
        print(f"\n--- TURNO {turno_numero} ---")
        mostrar_estado(equipo_jugador)
        mostrar_estado(equipo_rival)

        accion_jugador = agente_jugador.elegir_accion(equipo_jugador, equipo_rival)
        accion_rival = agente_rival.elegir_accion(equipo_rival, equipo_jugador)

        eventos = turno_acciones(equipo_jugador, equipo_rival, accion_jugador, accion_rival)

        for evento in eventos:
            mostrar_evento(evento)

        revisar_pokemon_debilitado(
            equipo_jugador,
            equipo_rival,
            agente_jugador,
        )
        revisar_pokemon_debilitado(
            equipo_rival,
            equipo_jugador,
            agente_rival,
        )

        turno_numero += 1

    print("\n=== RESULTADO ===")

    if equipo_jugador.tiene_pokemon_vivos():
        print(f"Gana {equipo_jugador.nombre}")
    else:
        print(f"Gana {equipo_rival.nombre}")


if __name__ == "__main__":
    ejecutar_demo_consola()
