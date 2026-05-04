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

    def esta_vivo(self):
        return self.hp_actual > 0

    def recibir_daño(self, daño):
        self.hp_actual = max(0, self.hp_actual - int(daño))
        return int(daño)

    def curar(self, cantidad):
        self.hp_actual = min(self.hp_max, self.hp_actual + cantidad)

    def aprender_movimiento(self, movimiento):
        if len(self.movimientos) < 4:
            self.movimientos.append(movimiento)
            return True
        return False

    def copiar(self):
        import copy
        return copy.deepcopy(self)

    def aplicar_estado_turno(self):
        pass
