import random

from Batalla.Danio import calcular_daño, obtener_modificador_defensor


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


def turno_acciones(equipo1, equipo2, accion1, accion2):
    eventos = []

    if accion1.tipo == "cambiar":
        eventos.append(cambiar_pokemon(equipo1, accion1.indice))

    if accion2.tipo == "cambiar":
        eventos.append(cambiar_pokemon(equipo2, accion2.indice))

    if accion1.tipo == "atacar" and accion2.tipo == "atacar":
        p1 = equipo1.pokemon_activo()
        p2 = equipo2.pokemon_activo()

        if p1.velocidad >= p2.velocidad:
            eventos.append(atacar_con_indice(p1, p2, accion1.indice))

            if p2.esta_vivo():
                eventos.append(atacar_con_indice(p2, p1, accion2.indice))
        else:
            eventos.append(atacar_con_indice(p2, p1, accion2.indice))

            if p1.esta_vivo():
                eventos.append(atacar_con_indice(p1, p2, accion1.indice))

    elif accion1.tipo == "atacar":
        eventos.append(
            atacar_con_indice(
                equipo1.pokemon_activo(),
                equipo2.pokemon_activo(),
                accion1.indice,
            )
        )

    elif accion2.tipo == "atacar":
        eventos.append(
            atacar_con_indice(
                equipo2.pokemon_activo(),
                equipo1.pokemon_activo(),
                accion2.indice,
            )
        )

    return eventos


def cambiar_pokemon(equipo, indice_pokemon):
    anterior = equipo.pokemon_activo()
    cambio_exitoso = equipo.cambiar_a(indice_pokemon)

    if not cambio_exitoso:
        return {
            "tipo": "cambio",
            "equipo": equipo.nombre,
            "exitoso": False,
            "pokemon_anterior": anterior.nombre,
        }

    nuevo = equipo.pokemon_activo()
    return {
        "tipo": "cambio",
        "equipo": equipo.nombre,
        "exitoso": True,
        "pokemon_anterior": anterior.nombre,
        "pokemon_nuevo": nuevo.nombre,
    }


def atacar_con_indice(atacante, defensor, indice_movimiento):
    if indice_movimiento < 0 or indice_movimiento >= len(atacante.movimientos):
        return {
            "tipo": "ataque",
            "atacante": atacante.nombre,
            "fallo": True,
            "motivo": "movimiento_invalido",
        }

    movimiento = atacante.movimientos[indice_movimiento]
    return atacar(atacante, defensor, movimiento)


def atacar(atacante, defensor, movimiento):
    if random.random() <= movimiento.precision:
        mult = obtener_modificador_defensor(movimiento, defensor)
        daño = calcular_daño(atacante, defensor, movimiento)
        daño_real = defensor.recibir_daño(daño)

        return {
            "tipo": "ataque",
            "atacante": atacante.nombre,
            "movimiento": movimiento.nombre,
            "daño": daño_real,
            "mult": mult,
            "fallo": False,
        }

    return {
        "tipo": "ataque",
        "atacante": atacante.nombre,
        "movimiento": movimiento.nombre,
        "fallo": True,
    }
