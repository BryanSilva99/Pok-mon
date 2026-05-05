from Batalla.Danio import calcular_daño

import random

from Batalla.Tabla_tipos import obtener_modificador_tipo


def turno(p1, p2, mov1, mov2):
    # p1.aplicar_estado_turno()
    # p2.aplicar_estado_turno()

    if p1.velocidad >= p2.velocidad:
        atacar(p1, p2, mov1)
        if p2.esta_vivo():
            atacar(p2, p1, mov2)
    else:
        atacar(p2, p1, mov2)
        if p1.esta_vivo():
            atacar(p1, p2, mov1)


def atacar(atacante, defensor, movimiento):
    import random

    if random.random() <= movimiento.precision:
        mult = obtener_modificador_tipo(movimiento.tipo, defensor.tipo)

        daño = calcular_daño(atacante, defensor, movimiento)
        daño_real = defensor.recibir_daño(daño)

        if mult > 1:
            print("¡Es súper efectivo!")
        elif mult < 1:
            print("No es muy efectivo...")

        return daño_real
    return 0
