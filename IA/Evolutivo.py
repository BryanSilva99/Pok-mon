import random

from Experimentos.Simulador import ejecutar_serie
from IA.Heuristicas import PESOS_AVANZADOS


NOMBRES_PESOS = tuple(PESOS_AVANZADOS.keys())


def crear_individuo():
    valores = {nombre: random.random() for nombre in NOMBRES_PESOS}
    return normalizar_pesos(valores)


def normalizar_pesos(pesos):
    pesos_positivos = {nombre: max(0.001, pesos[nombre]) for nombre in NOMBRES_PESOS}
    total = sum(pesos_positivos.values())
    return {nombre: valor / total for nombre, valor in pesos_positivos.items()}


def evaluar_fitness(pesos, partidas_por_rival=10):
    from IA.Agentes import AgenteAleatorio, AgenteHeuristico, AgenteHeuristicoAvanzado

    contra_manual = ejecutar_serie(
        lambda: AgenteHeuristicoAvanzado(pesos),
        lambda: AgenteHeuristicoAvanzado(),
        "Candidato",
        "Manual",
        partidas=partidas_por_rival,
    )
    contra_basico = ejecutar_serie(
        lambda: AgenteHeuristicoAvanzado(pesos),
        lambda: AgenteHeuristico(),
        "Candidato",
        "Heuristico",
        partidas=partidas_por_rival,
    )
    contra_random = ejecutar_serie(
        lambda: AgenteHeuristicoAvanzado(pesos),
        lambda: AgenteAleatorio(),
        "Candidato",
        "Random",
        partidas=partidas_por_rival,
    )

    win_rate_manual = contra_manual["win_rate_1"] / 100
    win_rate_basico = contra_basico["win_rate_1"] / 100
    win_rate_random = contra_random["win_rate_1"] / 100
    margen_hp_manual = (
        contra_manual["hp_promedio_1"] - contra_manual["hp_promedio_2"]
    ) / 180

    fitness = (
        win_rate_manual * 0.50
        + win_rate_basico * 0.25
        + win_rate_random * 0.20
        + margen_hp_manual * 0.05
    )

    return {
        "pesos": pesos,
        "fitness": fitness,
        "vs_manual": contra_manual,
        "vs_heuristico": contra_basico,
        "vs_random": contra_random,
    }


def seleccionar_padres(evaluados, cantidad):
    ordenados = sorted(evaluados, key=lambda individuo: individuo["fitness"], reverse=True)
    return ordenados[:cantidad]


def cruzar(padre_1, padre_2):
    hijo = {}

    for nombre in NOMBRES_PESOS:
        mezcla = random.random()
        hijo[nombre] = padre_1[nombre] * mezcla + padre_2[nombre] * (1 - mezcla)

    return normalizar_pesos(hijo)


def mutar(pesos, probabilidad=0.25, intensidad=0.12):
    mutado = pesos.copy()

    for nombre in NOMBRES_PESOS:
        if random.random() < probabilidad:
            mutado[nombre] += random.uniform(-intensidad, intensidad)

    return normalizar_pesos(mutado)


def optimizar_pesos(
    tamaño_poblacion=8,
    generaciones=5,
    partidas_por_rival=10,
    semilla=7,
):
    random.seed(semilla)
    poblacion = [PESOS_AVANZADOS.copy()]
    poblacion.extend(crear_individuo() for _ in range(tamaño_poblacion - 1))
    historial = []

    for generacion in range(1, generaciones + 1):
        evaluados = [
            evaluar_fitness(individuo, partidas_por_rival)
            for individuo in poblacion
        ]
        evaluados.sort(key=lambda individuo: individuo["fitness"], reverse=True)
        mejor = evaluados[0]
        historial.append(
            {
                "generacion": generacion,
                "fitness": mejor["fitness"],
                "pesos": mejor["pesos"],
                "win_rate_manual": mejor["vs_manual"]["win_rate_1"],
                "win_rate_heuristico": mejor["vs_heuristico"]["win_rate_1"],
                "win_rate_random": mejor["vs_random"]["win_rate_1"],
            }
        )

        padres = seleccionar_padres(evaluados, max(2, tamaño_poblacion // 2))
        nueva_poblacion = [padres[0]["pesos"].copy()]

        while len(nueva_poblacion) < tamaño_poblacion:
            padre_1, padre_2 = random.sample(padres, 2)
            hijo = cruzar(padre_1["pesos"], padre_2["pesos"])
            nueva_poblacion.append(mutar(hijo))

        poblacion = nueva_poblacion

    evaluacion_final = evaluar_fitness(historial[-1]["pesos"], partidas_por_rival * 3)
    return evaluacion_final, historial
