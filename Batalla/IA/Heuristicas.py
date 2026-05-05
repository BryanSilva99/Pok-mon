from Batalla.Danio import calcular_daño


def evaluar(p1, p2):
    return p1.hp_actual - p2.hp_actual


# heuristica para elegir movimiento: daño esperado (potencia * precisión) al oponente
def elegir_mejor_movimiento(p1, p2):
    mejor_mov = None
    mejor_score = -9999

    for mov in p1.movimientos:
        # copiar estado
        p1_copy = p1.copiar()
        p2_copy = p2.copiar()

        # calcular y aplicar daño en la simulación
        daño = calcular_daño(p1_copy, p2_copy, mov)
        p2_copy.recibir_daño(daño)

        # evaluar estado resultante
        score = evaluar(p1_copy, p2_copy) * mov.precision

        if score > mejor_score:
            mejor_score = score
            mejor_mov = mov

    return mejor_mov
