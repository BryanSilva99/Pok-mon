from Modelos.Pokemon import Pokemon
from Modelos.Movimiento import Movimiento
from Batalla.Combate import turno
from Batalla.IA.Heuristicas import elegir_mejor_movimiento
import random

# crear movimientos
rayo_carga = Movimiento("Rayo Carga", 50, 0.95, "electrico")
placaje_electrico = Movimiento("Placaje Eléctrico", 90, 1.0, "electrico")
golpe_cuerpo = Movimiento("Golpe Cuerpo", 85, 1.0, "normal")
placaje = Movimiento("Placaje", 35, 1.0, "normal")
rayo_solar = Movimiento("Rayo Solar", 120, 0.8, "planta")
energibola = Movimiento("Energibola", 90, 0.9, "planta")

# crear pokémon
p1 = Pokemon("Pikachu", 60, 55, 40, 90, "electrico")
p2 = Pokemon("Bulbasaur", 60, 50, 45, 40, "planta")
p3 = Pokemon("Charmander", 60, 52, 43, 65, "fuego")
p4 = Pokemon("Squirtle", 60, 48, 65, 43, "agua")

# asignar movimientos
p1.aprender_movimiento(rayo_carga)
p1.aprender_movimiento(placaje)
# p1.aprender_movimiento(golpe_cuerpo)
p1.aprender_movimiento(placaje_electrico)


p2.aprender_movimiento(placaje)
p2.aprender_movimiento(rayo_solar)
p2.aprender_movimiento(energibola)
p2.aprender_movimiento(golpe_cuerpo)

# combate
while p1.esta_vivo() and p2.esta_vivo():
    mov1 = elegir_mejor_movimiento(p1, p2)
    mov2 = random.choice(p2.movimientos)

    print(f"\n--- TURNO ---")
    print(f"{p1.nombre}: {p1.hp_actual} HP")
    print(f"{p2.nombre}: {p2.hp_actual} HP")

    turno(p1, p2, mov1, mov2)

    print(f"{p1.nombre} usó {mov1.nombre}!")
    if p2.esta_vivo():
        print(f"{p2.nombre} usó {mov2.nombre}!")

    print(f"{p1.nombre}: {p1.hp_actual} HP")
    print(f"{p2.nombre}: {p2.hp_actual} HP")

print("\n=== RESULTADO ===")

if p1.esta_vivo():
    print(f"Gana {p1.nombre}")
else:
    print(f"Gana {p2.nombre}")
