# Este código define la clase Movimiento, que representa un movimiento o ataque que un Pokémon puede aprender y usar en batalla. Cada movimiento tiene atributos como nombre, potencia, precisión y tipo. La clase se utiliza para crear objetos de movimiento que pueden ser asignados a los Pokémon para que los usen durante las batallas.
class Movimiento:
    def __init__(self, nombre, potencia, precision, tipo):
        self.nombre = nombre
        self.potencia = potencia
        self.precision = precision
        self.tipo = tipo
