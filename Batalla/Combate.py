from Batalla.Danio import calcular_daño

import random


def turno(p1, p2, mov1, mov2):
    p1.aplicar_estado_turno()
    p2.aplicar_estado_turno()

    if p1.velocidad >= p2.velocidad:
        atacar(p1, p2, mov1)
        if p2.esta_vivo():
            atacar(p2, p1, mov2)
    else:
        atacar(p2, p1, mov2)
        if p1.esta_vivo():
            atacar(p1, p2, mov1)


def atacar(atacante, defensor, movimiento):
    if random.random() <= movimiento.precision:
        daño = calcular_daño(atacante, defensor, movimiento)
        return defensor.recibir_daño(daño)
    return 0
