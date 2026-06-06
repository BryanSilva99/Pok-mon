tabla_tipos = {
    "normal": {
        "roca": 0.5,
        "fantasma": 0.0,
        "acero": 0.5,
    },
    "fuego": {
        "fuego": 0.5,
        "agua": 0.5,
        "planta": 2.0,
        "hielo": 2.0,
        "bicho": 2.0,
        "roca": 0.5,
        "dragon": 0.5,
        "acero": 2.0,
    },
    "agua": {
        "fuego": 2.0,
        "agua": 0.5,
        "planta": 0.5,
        "tierra": 2.0,
        "roca": 2.0,
        "dragon": 0.5,
    },
    "electrico": {
        "agua": 2.0,
        "electrico": 0.5,
        "planta": 0.5,
        "tierra": 0.0,
        "volador": 2.0,
        "dragon": 0.5,
    },
    "planta": {
        "fuego": 0.5,
        "agua": 2.0,
        "planta": 0.5,
        "veneno": 0.5,
        "tierra": 2.0,
        "volador": 0.5,
        "bicho": 0.5,
        "roca": 2.0,
        "dragon": 0.5,
        "acero": 0.5,
    },
    "hielo": {
        "fuego": 0.5,
        "agua": 0.5,
        "planta": 2.0,
        "hielo": 0.5,
        "tierra": 2.0,
        "volador": 2.0,
        "dragon": 2.0,
        "acero": 0.5,
    },
    "lucha": {
        "normal": 2.0,
        "hielo": 2.0,
        "veneno": 0.5,
        "volador": 0.5,
        "psiquico": 0.5,
        "bicho": 0.5,
        "roca": 2.0,
        "fantasma": 0.0,
        "siniestro": 2.0,
        "acero": 2.0,
        "hada": 0.5,
    },
    "veneno": {
        "planta": 2.0,
        "veneno": 0.5,
        "tierra": 0.5,
        "roca": 0.5,
        "fantasma": 0.5,
        "acero": 0.0,
        "hada": 2.0,
    },
    "tierra": {
        "fuego": 2.0,
        "electrico": 2.0,
        "planta": 0.5,
        "veneno": 2.0,
        "volador": 0.0,
        "bicho": 0.5,
        "roca": 2.0,
        "acero": 2.0,
    },
    "volador": {
        "electrico": 0.5,
        "planta": 2.0,
        "lucha": 2.0,
        "bicho": 2.0,
        "roca": 0.5,
        "acero": 0.5,
    },
    "psiquico": {
        "lucha": 2.0,
        "veneno": 2.0,
        "psiquico": 0.5,
        "siniestro": 0.0,
        "acero": 0.5,
    },
    "bicho": {
        "fuego": 0.5,
        "planta": 2.0,
        "lucha": 0.5,
        "veneno": 0.5,
        "volador": 0.5,
        "psiquico": 2.0,
        "fantasma": 0.5,
        "siniestro": 2.0,
        "acero": 0.5,
        "hada": 0.5,
    },
    "roca": {
        "fuego": 2.0,
        "hielo": 2.0,
        "lucha": 0.5,
        "tierra": 0.5,
        "volador": 2.0,
        "bicho": 2.0,
        "acero": 0.5,
    },
    "fantasma": {
        "normal": 0.0,
        "psiquico": 2.0,
        "fantasma": 2.0,
        "siniestro": 0.5,
    },
    "dragon": {
        "dragon": 2.0,
        "acero": 0.5,
        "hada": 0.0,
    },
    "siniestro": {
        "lucha": 0.5,
        "psiquico": 2.0,
        "fantasma": 2.0,
        "siniestro": 0.5,
        "hada": 0.5,
    },
    "acero": {
        "fuego": 0.5,
        "agua": 0.5,
        "electrico": 0.5,
        "hielo": 2.0,
        "roca": 2.0,
        "acero": 0.5,
        "hada": 2.0,
    },
    "hada": {
        "fuego": 0.5,
        "lucha": 2.0,
        "veneno": 0.5,
        "dragon": 2.0,
        "siniestro": 2.0,
        "acero": 0.5,
    },
}


def obtener_modificador_tipo(tipo_ataque, tipo_defensor):
    return tabla_tipos.get(tipo_ataque, {}).get(tipo_defensor, 1.0)


def clasificar_efectividad(multiplicador):
    if multiplicador == 0:
        return "inefectivo"
    elif multiplicador > 1:
        return "super"
    elif multiplicador < 1:
        return "poco"
    return "normal"
