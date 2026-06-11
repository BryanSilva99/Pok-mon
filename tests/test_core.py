from Batalla.Combate import turno_acciones
from Batalla.Danio import calcular_daño
from IA.Evolutivo import NOMBRES_PESOS, crear_individuo, normalizar_pesos
from IA.Heuristicas import (
    acciones_disponibles,
    elegir_accion_heuristica_avanzada,
    elegir_accion_heuristica_basica,
    evaluar_estado_avanzado,
)
from IA.Minimax import elegir_accion_minimax
from Modelos.Accion import Accion
from Modelos.Equipo import Equipo
from Modelos.Movimiento import Movimiento
from Modelos.Pokemon import Pokemon


def movimiento(nombre="Golpe", potencia=50, precision=1.0, tipo="normal"):
    return Movimiento(nombre, potencia, precision, tipo)


def pokemon(nombre, hp=100, ataque=60, defensa=50, velocidad=50, tipo="normal"):
    p = Pokemon(nombre, hp, ataque, defensa, velocidad, tipo)
    for mov in [
        movimiento("Rapido", 40, 1.0, tipo),
        movimiento("Fuerte", 80, 0.9, tipo),
        movimiento("Seguro", 30, 1.0, "normal"),
        movimiento("Riesgo", 100, 0.7, tipo),
    ]:
        p.aprender_movimiento(mov)
    p.definir_movimientos_disponibles(p.movimientos[:])
    return p


def equipo(nombre, cantidad=3):
    return Equipo(nombre, [pokemon(f"{nombre}-{i}") for i in range(cantidad)])


def test_calcular_daño_respeta_minimo_y_no_modifica_estado():
    atacante = pokemon("Atacante", ataque=80)
    defensor = pokemon("Defensor", defensa=200)
    mov = movimiento(potencia=1)

    daño = calcular_daño(atacante, defensor, mov)

    assert daño >= 1
    assert defensor.hp_actual == defensor.hp_max


def test_recibir_daño_debilita_sin_hp_negativo():
    p = pokemon("Objetivo", hp=30)

    recibido = p.recibir_daño(999)

    assert recibido == 30
    assert p.hp_actual == 0
    assert not p.esta_vivo()


def test_equipo_detecta_fin_de_combate():
    e = equipo("A", cantidad=3)
    for p in e.pokemons:
        p.recibir_daño(p.hp_actual)

    assert not e.tiene_pokemon_vivos()
    assert e.pokemons_vivos() == []


def test_acciones_disponibles_incluye_ataques_y_cambios_validos():
    e = equipo("A", cantidad=3)

    acciones = acciones_disponibles(e)

    assert sum(a.tipo == "atacar" for a in acciones) == 4
    assert {a.indice for a in acciones if a.tipo == "cambiar"} == {1, 2}


def test_turno_acciones_permte_cambiar_y_atacar():
    e1 = equipo("A", cantidad=3)
    e2 = equipo("B", cantidad=3)

    eventos = turno_acciones(e1, e2, Accion.cambiar(1), Accion.atacar(0))

    assert e1.indice_activo == 1
    assert any(evento["tipo"] == "cambio" and evento["exitoso"] for evento in eventos)
    assert e1.pokemon_activo().hp_actual < e1.pokemon_activo().hp_max


def test_heuristica_basica_devuelve_accion_de_ataque_valida():
    accion = elegir_accion_heuristica_basica(equipo("A"), equipo("B"))

    assert accion.tipo == "atacar"
    assert 0 <= accion.indice < 4


def test_heuristica_avanzada_devuelve_accion_valida_y_score_numerico():
    e1 = equipo("A")
    e2 = equipo("B")

    accion = elegir_accion_heuristica_avanzada(e1, e2)
    score = evaluar_estado_avanzado(e1, e2)

    assert accion.tipo in {"atacar", "cambiar"}
    assert isinstance(score, float)


def test_minimax_devuelve_accion_valida():
    accion = elegir_accion_minimax(equipo("A"), equipo("B"), profundidad=1)

    assert accion.tipo == "atacar"
    assert 0 <= accion.indice < 4


def test_pesos_geneticos_son_validos_y_normalizados():
    individuo = crear_individuo()
    pesos = normalizar_pesos({nombre: 2.0 for nombre in NOMBRES_PESOS})

    assert set(individuo) == set(NOMBRES_PESOS)
    assert set(pesos) == set(NOMBRES_PESOS)
    assert abs(sum(individuo.values()) - 1.0) < 1e-9
    assert abs(sum(pesos.values()) - 1.0) < 1e-9
    assert all(valor > 0 for valor in individuo.values())
