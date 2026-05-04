def calcular_daño(atacante, defensor, movimiento):
    daño = (atacante.ataque / defensor.defensa) * movimiento.potencia
    return max(1, int(daño))
