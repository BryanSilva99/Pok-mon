# Este código define la clase Pokemon, que representa a un Pokémon en el juego. Cada Pokémon tiene atributos como nombre, puntos de salud (HP), ataque, defensa, velocidad, tipo y estado. La clase incluye métodos para verificar si el Pokémon está vivo, recibir daño, curar, aprender movimientos y copiarse a sí mismo. También hay un método para aplicar efectos de estado al inicio de cada turno, aunque su implementación está pendiente.
class Pokemon:
    def __init__(self, nombre, hp, ataque, defensa, velocidad, tipo):
        self.nombre = nombre
        self.hp_max = hp
        self.hp_actual = hp
        self.ataque = ataque
        self.defensa = defensa
        self.velocidad = velocidad
        self.tipo = tipo
        self.estado = None
        self.movimientos = []

    # Métodos para manejar el estado del Pokémon
    # El método esta_vivo verifica si el Pokémon tiene HP actual mayor que 0, lo que indica que está vivo.
    def esta_vivo(self):
        return self.hp_actual > 0

    # El método recibir_daño toma un valor de daño, lo convierte a un entero y lo resta del HP actual del Pokémon. Si el HP actual cae por debajo de 0, se establece en 0 para evitar valores negativos. El método devuelve el daño recibido como un entero.

    def recibir_daño(self, daño):
        self.hp_actual = max(0, self.hp_actual - int(daño))
        return int(daño)

    # El método curar toma una cantidad de curación y la suma al HP actual del Pokémon, asegurándose de que no exceda el HP máximo. Esto permite que el Pokémon recupere salud durante la batalla o después de ella.
    #  # def curar(self, cantidad):
    #    self.hp_actual = min(self.hp_max, self.hp_actual + cantidad)

    # El método aprender_movimiento permite que el Pokémon aprenda un nuevo movimiento, siempre y cuando no tenga más de 4 movimientos en su lista. Si el Pokémon ya tiene 4 movimientos, el método devuelve False, indicando que no se puede aprender un nuevo movimiento. Si el movimiento se agrega con éxito, el método devuelve True.
    def aprender_movimiento(self, movimiento):
        if len(self.movimientos) < 4:
            self.movimientos.append(movimiento)
            return True
        return False

    # El método copiar utiliza la función deepcopy del módulo copy para crear una copia completa del objeto Pokémon, incluyendo todos sus atributos y estados. Esto es útil para simular batallas o situaciones donde se necesita un duplicado del Pokémon sin afectar al original.
    def copiar(self):
        import copy
        return copy.deepcopy(self)

    # El método aplicar_estado_turno es un espacio reservado para implementar efectos de estado que se aplican al inicio de cada turno. Esto podría incluir efectos como envenenamiento, parálisis, quemaduras, entre otros, que afectan al Pokémon durante la batalla. Actualmente, el método no tiene una implementación específica y simplemente pasa sin hacer nada.
    def aplicar_estado_turno(self):
        pass
