class Equipo:
    def __init__(self, nombre, pokemons):
        self.nombre = nombre
        self.pokemons = pokemons
        self.indice_activo = 0

    def pokemon_activo(self):
        return self.pokemons[self.indice_activo]

    def tiene_pokemon_vivos(self):
        return any(pokemon.esta_vivo() for pokemon in self.pokemons)

    def pokemons_vivos(self):
        return [pokemon for pokemon in self.pokemons if pokemon.esta_vivo()]

    def indices_pokemons_vivos(self):
        indices = []

        for indice, pokemon in enumerate(self.pokemons):
            if pokemon.esta_vivo():
                indices.append(indice)

        return indices

    def indices_cambios_validos(self):
        indices = []

        for indice in range(len(self.pokemons)):
            if self.puede_cambiar_a(indice):
                indices.append(indice)

        return indices

    def puede_cambiar_a(self, nuevo_indice):
        if nuevo_indice < 0 or nuevo_indice >= len(self.pokemons):
            return False

        if nuevo_indice == self.indice_activo:
            return False

        return self.pokemons[nuevo_indice].esta_vivo()

    def cambiar_a(self, nuevo_indice):
        if not self.puede_cambiar_a(nuevo_indice):
            return False

        self.indice_activo = nuevo_indice
        return True

    def seleccionar_siguiente_vivo(self):
        for indice, pokemon in enumerate(self.pokemons):
            if pokemon.esta_vivo():
                self.indice_activo = indice
                return pokemon

        return None

    def copiar(self):
        import copy
        return copy.deepcopy(self)
