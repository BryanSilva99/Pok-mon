from Modelos.Pokemon import Pokemon
from Modelos.Movimiento import Movimiento
from Batalla.Combate import turno
from Batalla.Danio import calcular_daño
import random

# crear movimientos
impactrueno = Movimiento("Impactrueno", 40, 0.9, "electrico")
placaje = Movimiento("Placaje", 35, 1.0, "normal")
rayo_solar = Movimiento("Rayo Solar", 120, 0.8, "planta")

# crear pokémon
p1 = Pokemon("Pikachu", 100, 55, 40, 90, "electrico")
p2 = Pokemon("Bulbasaur", 100, 49, 49, 45, "planta")

# asignar movimientos
p1.aprender_movimiento(impactrueno)
p1.aprender_movimiento(placaje)

p2.aprender_movimiento(placaje)
p2.aprender_movimiento(rayo_solar)


def evaluar(p1, p2):
    return p1.hp_actual - p2.hp_actual


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


# combate
while p1.esta_vivo() and p2.esta_vivo():
    mov1 = elegir_mejor_movimiento(p1, p2)
    mov2 = random.choice(p2.movimientos)

    print(f"{p1.nombre}: {p1.hp_actual} HP")
    print(f"{p2.nombre}: {p2.hp_actual} HP")

    print(f"-------------")

    turno(p1, p2, mov1, mov2)
    print(f"{p1.nombre} usó {mov1.nombre}!")
    print(f"{p2.nombre} usó {mov2.nombre}!")
    print(f"{p1.nombre}: {p1.hp_actual} HP")
    print(f"{p2.nombre}: {p2.hp_actual} HP")
    print("------")

# resultado
if p1.esta_vivo():
    print(f"Gana {p1.nombre}")
else:
    print(f"Gana {p2.nombre}")
