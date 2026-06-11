import random

from Batalla.Danio import calcular_daño
from Batalla.Tabla_tipos import obtener_modificador_tipo
from Modelos.Accion import Accion


PESOS_AVANZADOS = {
    "hp": 0.28,
    "vivos": 0.22,
    "tipo": 0.12,
    "velocidad": 0.08,
    "amenaza": 0.12,
    "ko": 0.08,
    "riesgo": 0.06,
    "calidad_activo": 0.04,
}
PESOS_OPTIMIZADOS_INICIALES = {
    "hp": 0.1414,
    "vivos": 0.2836,
    "tipo": 0.1675,
    "velocidad": 0.1068,
    "amenaza": 0.2507,
    "ko": 0.0200,
    "riesgo": 0.0200,
    "calidad_activo": 0.0100,
}


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
    return random.choice(acciones_disponibles(equipo))


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


def elegir_accion_heuristica_avanzada(equipo, equipo_rival, pesos=None):
    mejor_accion = None
    mejor_score = -9999

    for accion in acciones_disponibles(equipo):
        equipo_simulado = equipo.copiar()
        rival_simulado = equipo_rival.copiar()
        aplicar_accion_para_heuristica(equipo_simulado, rival_simulado, accion)
        score = evaluar_estado_avanzado(equipo_simulado, rival_simulado, pesos)

        if score > mejor_score:
            mejor_score = score
            mejor_accion = accion

    return mejor_accion


def elegir_reemplazo_aleatorio(equipo):
    cambios = equipo.indices_cambios_validos()
    return random.choice(cambios) if cambios else None


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


def elegir_reemplazo_heuristico_avanzado(equipo, equipo_rival, pesos=None):
    cambios = equipo.indices_cambios_validos()

    if not cambios:
        return None

    mejor_indice = cambios[0]
    mejor_score = -9999

    for indice in cambios:
        equipo_simulado = equipo.copiar()
        equipo_simulado.cambiar_a(indice)
        score = evaluar_estado_avanzado(equipo_simulado, equipo_rival, pesos)

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


def evaluar_estado_avanzado(equipo, equipo_rival, pesos=None):
    pesos = pesos or PESOS_AVANZADOS
    factores = {
        "hp": diferencia_hp_normalizada(equipo, equipo_rival),
        "vivos": diferencia_vivos_normalizada(equipo, equipo_rival),
        "tipo": ventaja_tipo_normalizada(equipo, equipo_rival),
        "velocidad": velocidad_normalizada(equipo, equipo_rival),
        "amenaza": amenaza_normalizada(equipo, equipo_rival),
        "ko": ko_normalizado(equipo, equipo_rival),
        "riesgo": riesgo_normalizado(equipo, equipo_rival),
        "calidad_activo": calidad_activo_normalizada(equipo, equipo_rival),
    }

    return sum(pesos[nombre] * valor for nombre, valor in factores.items())


def aplicar_accion_para_heuristica(equipo, equipo_rival, accion):
    if accion.tipo == "cambiar":
        equipo.cambiar_a(accion.indice)
        return

    atacante = equipo.pokemon_activo()
    defensor = equipo_rival.pokemon_activo()
    movimiento = atacante.movimientos[accion.indice]
    daño = calcular_daño(atacante, defensor, movimiento)
    daño_esperado = max(1, int(daño * movimiento.precision))
    defensor.recibir_daño(daño_esperado)


def diferencia_hp_normalizada(equipo, equipo_rival):
    hp_equipo = sum(pokemon.hp_actual for pokemon in equipo.pokemons)
    hp_rival = sum(pokemon.hp_actual for pokemon in equipo_rival.pokemons)
    hp_max_equipo = sum(pokemon.hp_max for pokemon in equipo.pokemons)
    hp_max_rival = sum(pokemon.hp_max for pokemon in equipo_rival.pokemons)
    return hp_equipo / hp_max_equipo - hp_rival / hp_max_rival


def diferencia_vivos_normalizada(equipo, equipo_rival):
    vivos_equipo = len(equipo.pokemons_vivos()) / len(equipo.pokemons)
    vivos_rival = len(equipo_rival.pokemons_vivos()) / len(equipo_rival.pokemons)
    return vivos_equipo - vivos_rival


def ventaja_tipo_normalizada(equipo, equipo_rival):
    ventaja_equipo = mejor_modificador_tipo(
        equipo.pokemon_activo(),
        equipo_rival.pokemon_activo(),
    )
    ventaja_rival = mejor_modificador_tipo(
        equipo_rival.pokemon_activo(),
        equipo.pokemon_activo(),
    )
    return (ventaja_equipo - ventaja_rival) / 2


def velocidad_normalizada(equipo, equipo_rival):
    velocidad_equipo = equipo.pokemon_activo().velocidad
    velocidad_rival = equipo_rival.pokemon_activo().velocidad
    velocidad_maxima = max(velocidad_equipo, velocidad_rival, 1)
    return (velocidad_equipo - velocidad_rival) / velocidad_maxima


def amenaza_normalizada(equipo, equipo_rival):
    amenaza_equipo = mejor_daño_esperado(
        equipo.pokemon_activo(),
        equipo_rival.pokemon_activo(),
    )
    amenaza_rival = mejor_daño_esperado(
        equipo_rival.pokemon_activo(),
        equipo.pokemon_activo(),
    )
    amenaza_maxima = max(amenaza_equipo, amenaza_rival, 1)
    return (amenaza_equipo - amenaza_rival) / amenaza_maxima


def ko_normalizado(equipo, equipo_rival):
    activo = equipo.pokemon_activo()
    rival = equipo_rival.pokemon_activo()
    ko_equipo = 1 if mejor_daño_esperado(activo, rival) >= rival.hp_actual else 0
    ko_rival = 1 if mejor_daño_esperado(rival, activo) >= activo.hp_actual else 0
    return ko_equipo - ko_rival


def riesgo_normalizado(equipo, equipo_rival):
    activo = equipo.pokemon_activo()
    rival = equipo_rival.pokemon_activo()
    amenaza_rival = mejor_daño_esperado(rival, activo)
    amenaza_equipo = mejor_daño_esperado(activo, rival)
    riesgo_rival = amenaza_rival / max(activo.hp_actual, 1)
    presion_equipo = amenaza_equipo / max(rival.hp_actual, 1)
    return limitar(presion_equipo - riesgo_rival, -1, 1)


def calidad_activo_normalizada(equipo, equipo_rival):
    calidad_equipo = calidad_pokemon(equipo.pokemon_activo())
    calidad_rival = calidad_pokemon(equipo_rival.pokemon_activo())
    calidad_maxima = max(calidad_equipo, calidad_rival, 1)
    return (calidad_equipo - calidad_rival) / calidad_maxima


def calidad_pokemon(pokemon):
    hp_ratio = pokemon.hp_actual / max(pokemon.hp_max, 1)
    ofensiva = pokemon.ataque / max(pokemon.ataque + pokemon.defensa, 1)
    velocidad = pokemon.velocidad / max(pokemon.velocidad + 100, 1)
    return hp_ratio * 0.5 + ofensiva * 0.3 + velocidad * 0.2


def limitar(valor, minimo, maximo):
    return max(minimo, min(maximo, valor))


def mejor_modificador_tipo(atacante, defensor):
    if not atacante.movimientos:
        return 1.0

    return max(
        obtener_modificador_tipo(movimiento.tipo, defensor.tipo)
        for movimiento in atacante.movimientos
    )
