from Batalla.Danio import calcular_daño
from IA.Heuristicas import (
    acciones_disponibles,
    evaluar_estado_avanzado,
    mejor_daño_esperado,
)


INFINITO = 10**9
PESO_HP = 1
PESO_POKEMON_VIVO = 35
PESO_AMENAZA = 0.4


def elegir_accion_minimax(equipo, equipo_rival, profundidad=2):
    acciones = acciones_busqueda(equipo)

    if not acciones:
        return None

    mejor_accion = acciones[0]
    mejor_score = -INFINITO
    alfa = -INFINITO

    for accion in acciones:
        score = evaluar_respuestas_rival(
            equipo,
            equipo_rival,
            accion,
            profundidad,
            alfa,
            INFINITO,
        )

        if score > mejor_score:
            mejor_score = score
            mejor_accion = accion

        alfa = max(alfa, mejor_score)

    return mejor_accion


def minimax(equipo_ia, equipo_rival, profundidad, alfa, beta):
    if profundidad == 0 or batalla_terminada(equipo_ia, equipo_rival):
        return evaluar_estado(equipo_ia, equipo_rival)

    acciones_ia = acciones_busqueda(equipo_ia)
    if not acciones_ia:
        return evaluar_estado(equipo_ia, equipo_rival)

    mejor_score = -INFINITO

    for accion_ia in acciones_ia:
        score = evaluar_respuestas_rival(
            equipo_ia,
            equipo_rival,
            accion_ia,
            profundidad,
            alfa,
            beta,
        )
        mejor_score = max(mejor_score, score)
        alfa = max(alfa, mejor_score)

        if alfa >= beta:
            break

    return mejor_score


def evaluar_respuestas_rival(
    equipo_ia,
    equipo_rival,
    accion_ia,
    profundidad,
    alfa,
    beta,
):
    acciones_rival = acciones_busqueda(equipo_rival)

    if not acciones_rival:
        return evaluar_estado(equipo_ia, equipo_rival)

    peor_score = INFINITO

    for accion_rival in acciones_rival:
        equipo_simulado = equipo_ia.copiar()
        rival_simulado = equipo_rival.copiar()
        resolver_turno_deterministico(
            equipo_simulado,
            rival_simulado,
            accion_ia,
            accion_rival,
        )

        score = minimax(
            equipo_simulado,
            rival_simulado,
            profundidad - 1,
            alfa,
            beta,
        )
        peor_score = min(peor_score, score)
        beta = min(beta, peor_score)

        if beta <= alfa:
            break

    return peor_score


def acciones_busqueda(equipo):
    acciones = acciones_disponibles(equipo)

    if equipo.pokemon_activo().esta_vivo():
        ataques = [accion for accion in acciones if accion.tipo == "atacar"]
        cambios = [accion for accion in acciones if accion.tipo == "cambiar"]
        return ataques + cambios[:1]

    return [accion for accion in acciones if accion.tipo == "cambiar"]


def resolver_turno_deterministico(equipo_ia, equipo_rival, accion_ia, accion_rival):
    if accion_ia.tipo == "cambiar":
        equipo_ia.cambiar_a(accion_ia.indice)

    if accion_rival.tipo == "cambiar":
        equipo_rival.cambiar_a(accion_rival.indice)

    if accion_ia.tipo == "atacar" and accion_rival.tipo == "atacar":
        pokemon_ia = equipo_ia.pokemon_activo()
        pokemon_rival = equipo_rival.pokemon_activo()

        if pokemon_ia.velocidad >= pokemon_rival.velocidad:
            ejecutar_ataque_esperado(pokemon_ia, pokemon_rival, accion_ia.indice)

            if pokemon_rival.esta_vivo():
                ejecutar_ataque_esperado(pokemon_rival, pokemon_ia, accion_rival.indice)
        else:
            ejecutar_ataque_esperado(pokemon_rival, pokemon_ia, accion_rival.indice)

            if pokemon_ia.esta_vivo():
                ejecutar_ataque_esperado(pokemon_ia, pokemon_rival, accion_ia.indice)

    elif accion_ia.tipo == "atacar":
        ejecutar_ataque_esperado(
            equipo_ia.pokemon_activo(),
            equipo_rival.pokemon_activo(),
            accion_ia.indice,
        )

    elif accion_rival.tipo == "atacar":
        ejecutar_ataque_esperado(
            equipo_rival.pokemon_activo(),
            equipo_ia.pokemon_activo(),
            accion_rival.indice,
        )


def ejecutar_ataque_esperado(atacante, defensor, indice_movimiento):
    if not atacante.esta_vivo():
        return

    if indice_movimiento < 0 or indice_movimiento >= len(atacante.movimientos):
        return

    movimiento = atacante.movimientos[indice_movimiento]
    daño = calcular_daño(atacante, defensor, movimiento)
    daño_esperado = max(1, int(daño * movimiento.precision))
    defensor.recibir_daño(daño_esperado)


def evaluar_estado(equipo_ia, equipo_rival):
    if equipo_ia.tiene_pokemon_vivos() and not equipo_rival.tiene_pokemon_vivos():
        return INFINITO

    if equipo_rival.tiene_pokemon_vivos() and not equipo_ia.tiene_pokemon_vivos():
        return -INFINITO

    return evaluar_estado_avanzado(equipo_ia, equipo_rival) * 1000


def amenaza_activa(equipo_atacante, equipo_defensor):
    atacante = pokemon_disponible(equipo_atacante)
    defensor = pokemon_disponible(equipo_defensor)

    if atacante is None or defensor is None:
        return 0

    return mejor_daño_esperado(atacante, defensor)


def pokemon_disponible(equipo):
    activo = equipo.pokemon_activo()

    if activo.esta_vivo():
        return activo

    vivos = equipo.pokemons_vivos()
    return vivos[0] if vivos else None


def hp_total(equipo):
    return sum(pokemon.hp_actual for pokemon in equipo.pokemons)


def batalla_terminada(equipo_ia, equipo_rival):
    return not equipo_ia.tiene_pokemon_vivos() or not equipo_rival.tiene_pokemon_vivos()
