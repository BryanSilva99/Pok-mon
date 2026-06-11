import random

from Batalla.Combate import turno_acciones
from main import crear_equipos


MAX_TURNOS = 200


def simular_partida(
    agente_1,
    agente_2,
    nombre_1,
    nombre_2,
    semilla=None,
    tamano_equipo=3,
):
    if semilla is not None:
        random.seed(semilla)

    equipo_1, equipo_2 = crear_equipos(tamano_equipo)
    equipo_1.nombre = nombre_1
    equipo_2.nombre = nombre_2
    turno = 0

    while (
        equipo_1.tiene_pokemon_vivos()
        and equipo_2.tiene_pokemon_vivos()
        and turno < MAX_TURNOS
    ):
        accion_1 = agente_1.elegir_accion(equipo_1, equipo_2)
        accion_2 = agente_2.elegir_accion(equipo_2, equipo_1)

        turno_acciones(equipo_1, equipo_2, accion_1, accion_2)
        reemplazar_si_es_necesario(equipo_1, equipo_2, agente_1)
        reemplazar_si_es_necesario(equipo_2, equipo_1, agente_2)
        turno += 1

    ganador = determinar_ganador(equipo_1, equipo_2, nombre_1, nombre_2)

    return {
        "ganador": ganador,
        "turnos": turno,
        "hp_final_1": hp_total(equipo_1),
        "hp_final_2": hp_total(equipo_2),
        "vivos_1": len(equipo_1.pokemons_vivos()),
        "vivos_2": len(equipo_2.pokemons_vivos()),
    }


def ejecutar_serie(
    creador_agente_1,
    creador_agente_2,
    nombre_1,
    nombre_2,
    partidas=100,
    tamano_equipo=3,
):
    resultados = []

    for numero_partida in range(partidas):
        if numero_partida % 2 == 0:
            resultado = simular_partida(
                creador_agente_1(),
                creador_agente_2(),
                nombre_1,
                nombre_2,
                semilla=numero_partida,
                tamano_equipo=tamano_equipo,
            )
        else:
            resultado = simular_partida(
                creador_agente_2(),
                creador_agente_1(),
                nombre_2,
                nombre_1,
                semilla=numero_partida,
                tamano_equipo=tamano_equipo,
            )
            resultado = invertir_perspectiva(resultado)

        resultados.append(resultado)

    return resumir_resultados(resultados, nombre_1, nombre_2)


def reemplazar_si_es_necesario(equipo, equipo_rival, agente):
    if equipo.pokemon_activo().esta_vivo():
        return

    reemplazo = agente.elegir_reemplazo(equipo, equipo_rival)

    if reemplazo is not None:
        equipo.cambiar_a(reemplazo)


def determinar_ganador(equipo_1, equipo_2, nombre_1, nombre_2):
    if equipo_1.tiene_pokemon_vivos() and not equipo_2.tiene_pokemon_vivos():
        return nombre_1

    if equipo_2.tiene_pokemon_vivos() and not equipo_1.tiene_pokemon_vivos():
        return nombre_2

    return "Empate"


def resumir_resultados(resultados, nombre_1, nombre_2):
    partidas = len(resultados)
    victorias_1 = sum(r["ganador"] == nombre_1 for r in resultados)
    victorias_2 = sum(r["ganador"] == nombre_2 for r in resultados)
    empates = sum(r["ganador"] == "Empate" for r in resultados)
    turnos_promedio = sum(r["turnos"] for r in resultados) / partidas
    hp_promedio_1 = sum(r["hp_final_1"] for r in resultados) / partidas
    hp_promedio_2 = sum(r["hp_final_2"] for r in resultados) / partidas

    return {
        "agente_1": nombre_1,
        "agente_2": nombre_2,
        "partidas": partidas,
        "victorias_1": victorias_1,
        "victorias_2": victorias_2,
        "empates": empates,
        "win_rate_1": victorias_1 / partidas * 100,
        "win_rate_2": victorias_2 / partidas * 100,
        "turnos_promedio": turnos_promedio,
        "hp_promedio_1": hp_promedio_1,
        "hp_promedio_2": hp_promedio_2,
    }


def hp_total(equipo):
    return sum(pokemon.hp_actual for pokemon in equipo.pokemons)


def invertir_perspectiva(resultado):
    return {
        "ganador": resultado["ganador"],
        "turnos": resultado["turnos"],
        "hp_final_1": resultado["hp_final_2"],
        "hp_final_2": resultado["hp_final_1"],
        "vivos_1": resultado["vivos_2"],
        "vivos_2": resultado["vivos_1"],
    }
