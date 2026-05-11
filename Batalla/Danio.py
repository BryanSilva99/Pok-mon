from Batalla.Tabla_tipos import obtener_modificador_tipo


ESCALA_DANIO = 0.25


def calcular_daño(atacante, defensor, movimiento):
    base = (atacante.ataque / defensor.defensa) * movimiento.potencia
    mult = obtener_modificador_tipo(movimiento.tipo, defensor.tipo)

    daño = base * ESCALA_DANIO * mult
    return max(1, int(daño))
