from Batalla.Tabla_tipos import obtener_modificador_tipo


ESCALA_DANIO = 0.25


def obtener_modificador_defensor(movimiento, defensor):
    tipos_defensor = getattr(defensor, "tipos", [defensor.tipo])
    mult = 1.0

    for tipo in tipos_defensor:
        mult *= obtener_modificador_tipo(movimiento.tipo, tipo)

    return mult


def calcular_daño(atacante, defensor, movimiento):
    base = (atacante.ataque / defensor.defensa) * movimiento.potencia
    mult = obtener_modificador_defensor(movimiento, defensor)

    daño = base * ESCALA_DANIO * mult
    return max(1, int(daño))
