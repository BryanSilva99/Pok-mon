from IA.Heuristicas import acciones_disponibles, mejor_daño_esperado
from Batalla.Danio import calcular_daño


INFINITO = 10**9
PESO_HP = 1
PESO_POKEMON_VIVO = 35
PESO_AMENAZA = 0.4


def elegir_accion_minimax(equipo, equipo_rival, profundidad=2):
    acciones = acciones_disponibles(equipo)

    if not acciones:
        return None

    mejor_accion = acciones[0]
    mejor_score = -INFINITO
    alfa = -INFINITO
    beta = INFINITO

    for accion in acciones:
        equipo_simulado = equipo.copiar()
        rival_simulado = equipo_rival.copiar()

        aplicar_accion_deterministica(equipo_simulado, rival_simulado, accion)
        score = minimax(
            equipo_simulado,
            rival_simulado,
            profundidad - 1,
            maximizando=False,
            alfa=alfa,
            beta=beta,
        )

        if score > mejor_score:
            mejor_score = score
            mejor_accion = accion

        alfa = max(alfa, mejor_score)

    return mejor_accion


def minimax(equipo_ia, equipo_rival, profundidad, maximizando, alfa, beta):
    if profundidad == 0 or batalla_terminada(equipo_ia, equipo_rival):
        return evaluar_estado(equipo_ia, equipo_rival)

    if maximizando:
        mejor_score = -INFINITO

        for accion in acciones_disponibles(equipo_ia):
            equipo_simulado = equipo_ia.copiar()
            rival_simulado = equipo_rival.copiar()
            aplicar_accion_deterministica(equipo_simulado, rival_simulado, accion)

            score = minimax(
                equipo_simulado,
                rival_simulado,
                profundidad - 1,
                maximizando=False,
                alfa=alfa,
                beta=beta,
            )
            mejor_score = max(mejor_score, score)
            alfa = max(alfa, mejor_score)

            if beta <= alfa:
                break

        return mejor_score

    mejor_score = INFINITO

    for accion in acciones_disponibles(equipo_rival):
        equipo_simulado = equipo_ia.copiar()
        rival_simulado = equipo_rival.copiar()
        aplicar_accion_deterministica(rival_simulado, equipo_simulado, accion)

        score = minimax(
            equipo_simulado,
            rival_simulado,
            profundidad - 1,
            maximizando=True,
            alfa=alfa,
            beta=beta,
        )
        mejor_score = min(mejor_score, score)
        beta = min(beta, mejor_score)

        if beta <= alfa:
            break

    return mejor_score


def aplicar_accion_deterministica(equipo, equipo_rival, accion):
    if accion.tipo == "cambiar":
        equipo.cambiar_a(accion.indice)
        return

    atacante = equipo.pokemon_activo()
    defensor = equipo_rival.pokemon_activo()

    if not atacante.esta_vivo():
        return

    if accion.indice < 0 or accion.indice >= len(atacante.movimientos):
        return

    movimiento = atacante.movimientos[accion.indice]
    daño = calcular_daño(atacante, defensor, movimiento)
    daño_esperado = int(daño * movimiento.precision)
    defensor.recibir_daño(max(1, daño_esperado))

    if not defensor.esta_vivo():
        equipo_rival.seleccionar_siguiente_vivo()


def evaluar_estado(equipo_ia, equipo_rival):
    if equipo_ia.tiene_pokemon_vivos() and not equipo_rival.tiene_pokemon_vivos():
        return INFINITO

    if equipo_rival.tiene_pokemon_vivos() and not equipo_ia.tiene_pokemon_vivos():
        return -INFINITO

    hp_ia = hp_total(equipo_ia)
    hp_rival = hp_total(equipo_rival)
    vivos_ia = len(equipo_ia.pokemons_vivos())
    vivos_rival = len(equipo_rival.pokemons_vivos())
    amenaza_ia = mejor_daño_esperado(equipo_ia.pokemon_activo(), equipo_rival.pokemon_activo())
    amenaza_rival = mejor_daño_esperado(equipo_rival.pokemon_activo(), equipo_ia.pokemon_activo())

    return (
        (hp_ia - hp_rival) * PESO_HP
        + (vivos_ia - vivos_rival) * PESO_POKEMON_VIVO
        + (amenaza_ia - amenaza_rival) * PESO_AMENAZA
    )


def hp_total(equipo):
    return sum(pokemon.hp_actual for pokemon in equipo.pokemons)


def batalla_terminada(equipo_ia, equipo_rival):
    return not equipo_ia.tiene_pokemon_vivos() or not equipo_rival.tiene_pokemon_vivos()
