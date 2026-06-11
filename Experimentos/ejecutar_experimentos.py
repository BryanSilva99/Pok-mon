from IA.Agentes import (
    AgenteAleatorio,
    AgenteHeuristico,
    AgenteHeuristicoAvanzado,
    AgenteMinimax,
    AgenteOptimizado,
)
from Experimentos.Simulador import ejecutar_serie


PARTIDAS = 100
PARTIDAS_PROFUNDIDAD = 10
PARTIDAS_4V4 = 20


def mostrar_resumen(resultado):
    print(f"\n{resultado['agente_1']} vs {resultado['agente_2']}")
    print(f"Partidas: {resultado['partidas']}")
    print(
        f"Victorias {resultado['agente_1']}: {resultado['victorias_1']} "
        f"({resultado['win_rate_1']:.1f}%)"
    )
    print(
        f"Victorias {resultado['agente_2']}: {resultado['victorias_2']} "
        f"({resultado['win_rate_2']:.1f}%)"
    )
    print(f"Empates: {resultado['empates']}")
    print(f"Turnos promedio: {resultado['turnos_promedio']:.2f}")
    print(
        f"HP final promedio: {resultado['agente_1']} "
        f"{resultado['hp_promedio_1']:.2f} | {resultado['agente_2']} "
        f"{resultado['hp_promedio_2']:.2f}"
    )


def ejecutar_comparaciones():
    comparaciones = [
        (
            lambda: AgenteAleatorio(),
            lambda: AgenteAleatorio(),
            "Random A",
            "Random B",
        ),
        (
            lambda: AgenteHeuristico(),
            lambda: AgenteAleatorio(),
            "Heuristico",
            "Random",
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
        (
            lambda: AgenteHeuristicoAvanzado(),
            lambda: AgenteAleatorio(),
            "Heuristico avanzado",
            "Random",
        ),
        (
            lambda: AgenteHeuristicoAvanzado(),
            lambda: AgenteHeuristico(),
            "Heuristico avanzado",
            "Heuristico",
        ),
        (
            lambda: AgenteOptimizado(),
            lambda: AgenteHeuristicoAvanzado(),
            "Optimizado",
            "Avanzado manual",
        ),
    ]

    print("=== COMPARACION DE AGENTES ===")

    for creador_1, creador_2, nombre_1, nombre_2 in comparaciones:
        resultado = ejecutar_serie(
            creador_1,
            creador_2,
            nombre_1,
            nombre_2,
            partidas=PARTIDAS,
        )
        mostrar_resumen(resultado)


def ejecutar_prueba_profundidad():
    print(
        "\n=== IMPACTO DE PROFUNDIDAD MINIMAX VS RANDOM "
        f"({PARTIDAS_PROFUNDIDAD} partidas por profundidad) ==="
    )

    for profundidad in [1, 2, 3]:
        resultado = ejecutar_serie(
            lambda profundidad=profundidad: AgenteMinimax(profundidad=profundidad),
            lambda: AgenteAleatorio(),
            f"Minimax p{profundidad}",
            "Random",
            partidas=PARTIDAS_PROFUNDIDAD,
        )
        mostrar_resumen(resultado)


def ejecutar_verificacion_4v4():
    print(f"\n=== VERIFICACION 4 VS 4 ({PARTIDAS_4V4} partidas) ===")
    casos = [
        (
            lambda: AgenteHeuristicoAvanzado(),
            lambda: AgenteAleatorio(),
            "Heuristico avanzado 4v4",
            "Random 4v4",
        ),
        (
            lambda: AgenteMinimax(profundidad=2),
            lambda: AgenteHeuristico(),
            "Minimax p2 4v4",
            "Heuristico 4v4",
        ),
    ]

    for creador_1, creador_2, nombre_1, nombre_2 in casos:
        resultado = ejecutar_serie(
            creador_1,
            creador_2,
            nombre_1,
            nombre_2,
            partidas=PARTIDAS_4V4,
            tamano_equipo=4,
        )
        mostrar_resumen(resultado)


if __name__ == "__main__":
    ejecutar_comparaciones()
    ejecutar_prueba_profundidad()
    ejecutar_verificacion_4v4()
