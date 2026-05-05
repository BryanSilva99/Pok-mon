# diccionarios para las tablas de tipos (elementales) : fuego , agua , planta , electrico , normal ... por el momento.
tabla_tipos = {
    ("electrico", "agua"): 2.0,
    ("electrico", "planta"): 0.5,
    ("fuego", "planta"): 2.0,
    ("fuego", "agua"): 0.5,
    ("planta", "agua"): 2.0,
    ("planta", "fuego"): 0.5
}


def obtener_modificador_tipo(tipo_ataque, tipo_defensor):
    return tabla_tipos.get((tipo_ataque, tipo_defensor), 1.0)


def clasificar_efectividad(multiplicador):
    if multiplicador == 0:
        return "inefectivo"
    elif multiplicador > 1:
        return "super"
    elif multiplicador < 1:
        return "poco"
    return "normal"
