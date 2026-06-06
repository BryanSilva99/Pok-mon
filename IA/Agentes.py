from IA.Heuristicas import (
    elegir_accion_aleatoria,
    elegir_accion_heuristica_avanzada,
    elegir_accion_heuristica_basica,
    elegir_reemplazo_aleatorio,
    elegir_reemplazo_heuristico_avanzado,
    elegir_reemplazo_heuristico,
    PESOS_OPTIMIZADOS_INICIALES,
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


class AgenteHeuristicoAvanzado:
    def __init__(self, pesos=None):
        self.pesos = pesos

    def elegir_accion(self, equipo, equipo_rival):
        return elegir_accion_heuristica_avanzada(equipo, equipo_rival, self.pesos)

    def elegir_reemplazo(self, equipo, equipo_rival):
        return elegir_reemplazo_heuristico_avanzado(equipo, equipo_rival, self.pesos)


class AgenteOptimizado(AgenteHeuristicoAvanzado):
    def __init__(self):
        super().__init__(PESOS_OPTIMIZADOS_INICIALES)


class AgenteMinimax:
    def __init__(self, profundidad=2):
        self.profundidad = profundidad

    def elegir_accion(self, equipo, equipo_rival):
        return elegir_accion_minimax(equipo, equipo_rival, self.profundidad)

    def elegir_reemplazo(self, equipo, equipo_rival):
        return elegir_reemplazo_heuristico(equipo, equipo_rival)
