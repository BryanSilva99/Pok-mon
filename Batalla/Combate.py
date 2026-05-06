from Batalla.Danio import calcular_daño

import random

from Batalla.Tabla_tipos import obtener_modificador_tipo


def turno(p1, p2, mov1, mov2):
    eventos = []

    if p1.velocidad >= p2.velocidad:
        eventos.append(atacar(p1, p2, mov1))

        if p2.esta_vivo():
            eventos.append(atacar(p2, p1, mov2))
    else:
        eventos.append(atacar(p2, p1, mov2))

        if p1.esta_vivo():
            eventos.append(atacar(p1, p2, mov1))

    return eventos


def atacar(atacante, defensor, movimiento):
    if random.random() <= movimiento.precision:
        mult = obtener_modificador_tipo(movimiento.tipo, defensor.tipo)

        daño = calcular_daño(atacante, defensor, movimiento)
        daño_real = defensor.recibir_daño(daño)

        return {
            "atacante": atacante.nombre,
            "movimiento": movimiento.nombre,
            "daño": daño_real,
            "mult": mult,
            "fallo": False
        }

    return {
        "atacante": atacante.nombre,
        "movimiento": movimiento.nombre,
        "fallo": True
    }
