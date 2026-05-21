from Batalla.Combate import turno_acciones
from IA.Agentes import AgenteAleatorio, AgenteMinimax
from main import crear_equipos, mostrar_estado, mostrar_evento, revisar_pokemon_debilitado


def ejecutar_demo_minimax():
    equipo_minimax, equipo_aleatorio = crear_equipos()
    equipo_minimax.nombre = "Minimax"
    equipo_aleatorio.nombre = "Aleatorio"

    agente_minimax = AgenteMinimax(profundidad=2)
    agente_aleatorio = AgenteAleatorio()
    turno_numero = 1

    while equipo_minimax.tiene_pokemon_vivos() and equipo_aleatorio.tiene_pokemon_vivos():
        print(f"\n--- TURNO {turno_numero} ---")
        mostrar_estado(equipo_minimax)
        mostrar_estado(equipo_aleatorio)

        accion_minimax = agente_minimax.elegir_accion(equipo_minimax, equipo_aleatorio)
        accion_aleatoria = agente_aleatorio.elegir_accion(equipo_aleatorio, equipo_minimax)
        eventos = turno_acciones(
            equipo_minimax,
            equipo_aleatorio,
            accion_minimax,
            accion_aleatoria,
        )

        for evento in eventos:
            mostrar_evento(evento)

        revisar_pokemon_debilitado(equipo_minimax, equipo_aleatorio, agente_minimax)
        revisar_pokemon_debilitado(equipo_aleatorio, equipo_minimax, agente_aleatorio)
        turno_numero += 1

    print("\n=== RESULTADO ===")

    if equipo_minimax.tiene_pokemon_vivos():
        print("Gana Minimax")
    else:
        print("Gana Aleatorio")


if __name__ == "__main__":
    ejecutar_demo_minimax()
