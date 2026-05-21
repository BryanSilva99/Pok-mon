from IA.Heuristicas import (
    elegir_accion_aleatoria,
    elegir_accion_heuristica_basica,
    elegir_reemplazo_aleatorio,
    elegir_reemplazo_heuristico,
)
from IA.Minimax import elegir_accion_minimax


class AgenteAleatorio:
    def elegir_accion(self, equipo, equipo_rival):
        return elegir_accion_aleatoria(equipo)

    def elegir_reemplazo(self, equipo, equipo_rival):
        return elegir_reemplazo_aleatorio(equipo)


class AgenteHeuristico:
    def elegir_accion(self, equipo, equipo_rival):
        return elegir_accion_heuristica_basica(equipo, equipo_rival)

    def elegir_reemplazo(self, equipo, equipo_rival):
        return elegir_reemplazo_heuristico(equipo, equipo_rival)


class AgenteMinimax:
    def __init__(self, profundidad=2):
        self.profundidad = profundidad

    def elegir_accion(self, equipo, equipo_rival):
        return elegir_accion_minimax(equipo, equipo_rival, self.profundidad)

    def elegir_reemplazo(self, equipo, equipo_rival):
        return elegir_reemplazo_heuristico(equipo, equipo_rival)
