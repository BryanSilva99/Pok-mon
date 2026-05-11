class Accion:
    def __init__(self, tipo, indice):
        self.tipo = tipo
        self.indice = indice

    @staticmethod
    def atacar(indice_movimiento):
        return Accion("atacar", indice_movimiento)

    @staticmethod
    def cambiar(indice_pokemon):
        return Accion("cambiar", indice_pokemon)
