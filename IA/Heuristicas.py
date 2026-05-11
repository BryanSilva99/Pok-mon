import random

from Batalla.Danio import calcular_daño
from Modelos.Accion import Accion


def evaluar(p1, p2):
    return p1.hp_actual - p2.hp_actual


def elegir_mejor_movimiento(p1, p2):
    mejor_mov = None
    mejor_score = -9999

    for mov in p1.movimientos:
        p1_copy = p1.copiar()
        p2_copy = p2.copiar()

        daño = calcular_daño(p1_copy, p2_copy, mov)
        p2_copy.recibir_daño(daño)

        score = evaluar(p1_copy, p2_copy) * mov.precision

        if score > mejor_score:
            mejor_score = score
            mejor_mov = mov

    return mejor_mov


def acciones_disponibles(equipo):
    acciones = []
    pokemon = equipo.pokemon_activo()

    if pokemon.esta_vivo():
        for indice in range(len(pokemon.movimientos)):
            acciones.append(Accion.atacar(indice))

    for indice in equipo.indices_cambios_validos():
        acciones.append(Accion.cambiar(indice))

    return acciones


def elegir_accion_aleatoria(equipo):
    acciones = acciones_disponibles(equipo)
    return random.choice(acciones)


def elegir_accion_heuristica_basica(equipo, equipo_rival):
    atacante = equipo.pokemon_activo()
    defensor = equipo_rival.pokemon_activo()
    mejor_accion = None
    mejor_score = -9999

    for indice, movimiento in enumerate(atacante.movimientos):
        daño = calcular_daño(atacante, defensor, movimiento)
        score = daño * movimiento.precision

        if score > mejor_score:
            mejor_score = score
            mejor_accion = Accion.atacar(indice)

    return mejor_accion


def elegir_reemplazo_aleatorio(equipo):
    cambios = equipo.indices_cambios_validos()

    if not cambios:
        return None

    return random.choice(cambios)


def elegir_reemplazo_heuristico(equipo, equipo_rival):
    cambios = equipo.indices_cambios_validos()

    if not cambios:
        return None

    defensor = equipo_rival.pokemon_activo()
    mejor_indice = cambios[0]
    mejor_score = -9999

    for indice in cambios:
        candidato = equipo.pokemons[indice]
        score = mejor_daño_esperado(candidato, defensor)

        if score > mejor_score:
            mejor_score = score
            mejor_indice = indice

    return mejor_indice


def mejor_daño_esperado(atacante, defensor):
    mejor_score = 0

    for movimiento in atacante.movimientos:
        daño = calcular_daño(atacante, defensor, movimiento)
        score = daño * movimiento.precision

        if score > mejor_score:
            mejor_score = score

    return mejor_score
