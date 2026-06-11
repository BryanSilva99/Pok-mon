import csv
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from Experimentos.Simulador import ejecutar_serie
from IA.Agentes import (
    AgenteAleatorio,
    AgenteHeuristico,
    AgenteHeuristicoAvanzado,
    AgenteMinimax,
    AgenteOptimizado,
)
from IA.Evolutivo import optimizar_pesos
from IA.Heuristicas import PESOS_AVANZADOS, PESOS_OPTIMIZADOS_INICIALES


SALIDA = RAIZ / "Resultados"
PARTIDAS_COMPARACION = 100
PARTIDAS_PROFUNDIDAD = 20
PARTIDAS_4V4 = 30


def comparaciones_agentes():
    casos = [
        (lambda: AgenteAleatorio(), lambda: AgenteAleatorio(), "Random A", "Random B"),
        (lambda: AgenteHeuristico(), lambda: AgenteAleatorio(), "Heuristico", "Random"),
        (
            lambda: AgenteHeuristicoAvanzado(),
            lambda: AgenteAleatorio(),
            "Avanzado manual",
            "Random",
        ),
        (
            lambda: AgenteHeuristicoAvanzado(),
            lambda: AgenteHeuristico(),
            "Avanzado manual",
            "Heuristico",
        ),
        (
            lambda: AgenteOptimizado(),
            lambda: AgenteHeuristicoAvanzado(),
            "Optimizado",
            "Avanzado manual",
        ),
        (
            lambda: AgenteMinimax(profundidad=2),
            lambda: AgenteAleatorio(),
            "Minimax p2",
            "Random",
        ),
        (
            lambda: AgenteMinimax(profundidad=2),
            lambda: AgenteHeuristico(),
            "Minimax p2",
            "Heuristico",
        ),
    ]
    return [
        ejecutar_serie(creador_1, creador_2, nombre_1, nombre_2, PARTIDAS_COMPARACION)
        for creador_1, creador_2, nombre_1, nombre_2 in casos
    ]


def impacto_profundidad():
    resultados = []
    for profundidad in [1, 2, 3]:
        resultados.append(
            ejecutar_serie(
                lambda profundidad=profundidad: AgenteMinimax(profundidad=profundidad),
                lambda: AgenteAleatorio(),
                f"Minimax p{profundidad}",
                "Random",
                PARTIDAS_PROFUNDIDAD,
            )
        )
    return resultados


def comparacion_4v4():
    casos = [
        (
            lambda: AgenteHeuristicoAvanzado(),
            lambda: AgenteAleatorio(),
            "Avanzado manual 4v4",
            "Random 4v4",
        ),
        (
            lambda: AgenteMinimax(profundidad=2),
            lambda: AgenteHeuristico(),
            "Minimax p2 4v4",
            "Heuristico 4v4",
        ),
    ]
    return [
        ejecutar_serie(
            creador_1,
            creador_2,
            nombre_1,
            nombre_2,
            PARTIDAS_4V4,
            tamano_equipo=4,
        )
        for creador_1, creador_2, nombre_1, nombre_2 in casos
    ]


def guardar_csv(ruta, filas):
    campos = [
        "agente_1",
        "agente_2",
        "partidas",
        "victorias_1",
        "victorias_2",
        "empates",
        "win_rate_1",
        "win_rate_2",
        "turnos_promedio",
        "hp_promedio_1",
        "hp_promedio_2",
    ]
    with open(ruta, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        for fila in filas:
            escritor.writerow({campo: fila[campo] for campo in campos})


def guardar_resultados_geneticos(mejor, historial):
    with open(SALIDA / "genetic_best_weights.json", "w", encoding="utf-8") as archivo:
        json.dump(mejor["pesos"], archivo, indent=2, ensure_ascii=False)

    campos = [
        "generacion",
        "fitness",
        "win_rate_manual",
        "win_rate_heuristico",
        "win_rate_random",
        "pesos",
    ]
    with open(SALIDA / "genetic_history.csv", "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        for fila in historial:
            escritor.writerow(
                {
                    "generacion": fila["generacion"],
                    "fitness": fila["fitness"],
                    "win_rate_manual": fila["win_rate_manual"],
                    "win_rate_heuristico": fila["win_rate_heuristico"],
                    "win_rate_random": fila["win_rate_random"],
                    "pesos": json.dumps(fila["pesos"], ensure_ascii=False),
                }
            )


def tabla_markdown(filas):
    lineas = [
        "| Agente 1 | Agente 2 | Partidas | Win rate A1 | Win rate A2 | Empates | Turnos prom. | HP A1 | HP A2 |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for fila in filas:
        lineas.append(
            "| {agente_1} | {agente_2} | {partidas} | {win_rate_1:.1f}% | "
            "{win_rate_2:.1f}% | {empates} | {turnos_promedio:.2f} | "
            "{hp_promedio_1:.2f} | {hp_promedio_2:.2f} |".format(**fila)
        )
    return "\n".join(lineas)


def tabla_pesos(pesos):
    lineas = ["| Factor | Peso |", "|---|---:|"]
    for nombre, valor in pesos.items():
        lineas.append(f"| {nombre} | {valor:.4f} |")
    return "\n".join(lineas)


def generar_markdown(comparaciones, profundidad, comparaciones_4v4, mejor, historial):
    return f"""# Insumos para el articulo cientifico - Pokefisi

Este archivo contiene los resultados empiricos generados para redactar el articulo final.

## Configuracion experimental

- Combates 3 vs 3 y verificacion experimental 4 vs 4.
- Dataset curado de 30 Pokemon.
- Cada Pokemon dispone de 8 movimientos y usa 4 movimientos seleccionados aleatoriamente.
- Maximo de 200 turnos por partida; si se alcanza ese limite se registra empate.
- Comparaciones principales: {PARTIDAS_COMPARACION} partidas por enfrentamiento.
- Prueba de profundidad Minimax: {PARTIDAS_PROFUNDIDAD} partidas por profundidad.
- Prueba 4 vs 4: {PARTIDAS_4V4} partidas por enfrentamiento.
- Las series alternan el orden de los agentes para reducir sesgo por iniciativa.

## Pesos manuales de la heuristica avanzada

{tabla_pesos(PESOS_AVANZADOS)}

## Pesos optimizados usados por AgenteOptimizado

{tabla_pesos(PESOS_OPTIMIZADOS_INICIALES)}

## Comparacion entre agentes

{tabla_markdown(comparaciones)}

## Impacto de la profundidad de Minimax

{tabla_markdown(profundidad)}

## Verificacion 4 vs 4

{tabla_markdown(comparaciones_4v4)}

## Optimizacion evolutiva

### Evolucion por generacion

| Generacion | Fitness | Win rate vs manual | Win rate vs heuristico | Win rate vs random |
|---:|---:|---:|---:|---:|
{chr(10).join(
    f"| {fila['generacion']} | {fila['fitness']:.4f} | {fila['win_rate_manual']:.1f}% | "
    f"{fila['win_rate_heuristico']:.1f}% | {fila['win_rate_random']:.1f}% |"
    for fila in historial
)}

### Mejores pesos encontrados en la corrida evolutiva

{tabla_pesos(mejor["pesos"])}

### Evaluacion final del mejor individuo

- Fitness final: {mejor["fitness"]:.4f}
- Win rate vs avanzado manual: {mejor["vs_manual"]["win_rate_1"]:.1f}%
- Win rate vs heuristico basico: {mejor["vs_heuristico"]["win_rate_1"]:.1f}%
- Win rate vs random: {mejor["vs_random"]["win_rate_1"]:.1f}%

## Estructura recomendada del articulo

1. Resumen: objetivo, agentes evaluados, metodologia experimental y hallazgos principales.
2. Introduccion: juegos por turnos, toma de decisiones adversarial y motivacion del simulador.
3. Metodologia: modelado de Pokemon, movimientos, formula de dano, agentes y optimizacion.
4. Experimentos: escenarios, numero de partidas, metricas y configuracion de semillas.
5. Resultados: insertar las tablas anteriores.
6. Discusion: interpretar rendimiento, costo de Minimax, ventajas y limites de la optimizacion.
7. Conclusiones: aprendizajes, agente mas competitivo y mejoras futuras.
8. Referencias: Pokemon Showdown, PokeAPI sprites y material teorico de Minimax/algoritmos geneticos.
"""


def main():
    SALIDA.mkdir(exist_ok=True)
    comparaciones = comparaciones_agentes()
    profundidad = impacto_profundidad()
    comparaciones_4v4 = comparacion_4v4()
    mejor, historial = optimizar_pesos()
    datos = {
        "comparaciones": comparaciones,
        "profundidad": profundidad,
        "comparaciones_4v4": comparaciones_4v4,
        "optimizacion": {
            "mejor": mejor,
            "historial": historial,
        },
    }

    with open(SALIDA / "resultados_articulo.json", "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=2, ensure_ascii=False)
    guardar_csv(SALIDA / "comparacion_agentes.csv", comparaciones)
    guardar_csv(SALIDA / "impacto_profundidad.csv", profundidad)
    guardar_csv(SALIDA / "comparacion_4v4.csv", comparaciones_4v4)
    guardar_resultados_geneticos(mejor, historial)
    with open(SALIDA / "insumos_articulo.md", "w", encoding="utf-8") as archivo:
        archivo.write(
            generar_markdown(comparaciones, profundidad, comparaciones_4v4, mejor, historial)
        )

    print(f"Resultados guardados en {SALIDA}")


if __name__ == "__main__":
    main()
