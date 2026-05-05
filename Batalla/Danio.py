# Este código define la función calcular_daño, que calcula el daño infligido por un movimiento de un Pokémon atacante a un Pokémon defensor. El daño se calcula utilizando una fórmula que toma en cuenta el ataque del atacante, la defensa del defensor y la potencia del movimiento. La función devuelve el daño como un número entero, asegurándose de que el daño mínimo sea al menos 1 para garantizar que siempre se inflija algún daño.
from Batalla.Tabla_tipos import obtener_modificador_tipo


def calcular_daño(atacante, defensor, movimiento):
    base = (atacante.ataque / defensor.defensa) * movimiento.potencia
    mult = obtener_modificador_tipo(movimiento.tipo, defensor.tipo)
    daño = base * mult
    return max(1, int(daño))
