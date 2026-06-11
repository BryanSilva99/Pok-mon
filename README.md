# Pokefisi

Pokefisi es un simulador academico de combates por turnos inspirado en Pokemon. El proyecto compara agentes de inteligencia artificial en batallas 3 vs 3 y 4 vs 4, con seleccion de movimientos, cambios de Pokemon, heuristicas, Minimax con poda alfa-beta y optimizacion de pesos mediante algoritmo genetico.

## Objetivo

El objetivo es evaluar estrategias de decision en un entorno adversarial simple y reproducible. El sistema permite jugar humano vs IA, observar IA vs IA y ejecutar experimentos por consola para comparar agentes.

## Requisitos

- Python 3.10 o superior.
- `pygame` para la interfaz grafica.
- `Pillow` para cargar sprites GIF/PNG.
- `pytest` para ejecutar pruebas.

Instalacion recomendada:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Como ejecutar

Interfaz grafica:

```bash
python pantalla_batalla.py
```

Demo por consola:

```bash
python main.py
```

Experimentos comparativos:

```bash
python experimentos.py
```

Optimizacion de pesos:

```bash
python optimizar_pesos.py
```

Generar resultados para el articulo:

```bash
python Experimentos/generar_resultados_articulo.py
```

## Agentes implementados

- `AgenteAleatorio`: elige acciones validas al azar.
- `AgenteHeuristico`: prioriza el movimiento con mayor dano esperado.
- `AgenteHeuristicoAvanzado`: evalua acciones con factores normalizados y pesos configurables, incluyendo HP, vivos, tipo, velocidad, amenaza, KO, riesgo y calidad del activo.
- `AgenteMinimax`: usa busqueda Minimax con poda alfa-beta, profundidad configurable y evaluacion basada en la heuristica avanzada.
- `AgenteOptimizado`: usa pesos obtenidos por el algoritmo evolutivo.

## Modelo de combate

Cada Pokemon tiene HP, ataque, defensa, velocidad, tipo primario, tipo secundario opcional y movimientos. Cada Pokemon dispone de 8 movimientos definidos en el dataset curado y recibe 4 movimientos aleatorios al iniciar una batalla.

En cada turno ambos participantes eligen una accion:

- Atacar con uno de los movimientos disponibles.
- Cambiar a otro Pokemon vivo.

El combate termina cuando un equipo no tiene Pokemon vivos. En experimentos se usa un limite de 200 turnos para evitar ciclos largos.

## Funcion de dano

La funcion central esta en `Batalla/Danio.py`:

```text
dano = (ataque / defensa_oponente) * potencia_movimiento * escala * modificador_tipo
```

El modificador de tipo considera resistencias, debilidades e inmunidades. Cuando un ataque acierta, el dano minimo es 1.

## Experimentos y metricas

Los scripts de `Experimentos/` comparan:

- Random vs Random.
- Heuristico vs Random.
- Avanzado manual vs Random.
- Avanzado manual vs Heuristico.
- Optimizado vs Avanzado manual.
- Minimax profundidad 2 vs Random y Heuristico.
- Minimax profundidad 1, 2 y 3 contra Random.
- Verificacion 4v4 con agentes informados.

Metricas registradas:

- Victorias por agente.
- Win rate.
- Empates.
- Turnos promedio.
- HP final promedio.

Los resultados se guardan en `Resultados/` como CSV, JSON y Markdown.

## Articulo cientifico

El documento base esta en `Articulo_Pokefisi.md`. Los insumos generados automaticamente para tablas y resultados se guardan en `Resultados/insumos_articulo.md`.

## Estructura del proyecto

```text
Batalla/        Motor de combate, dano y tabla de tipos.
Datos/          Carga del dataset y creacion de equipos.
IA/             Agentes, heuristicas, Minimax y algoritmo evolutivo.
Interfaz/       Interfaz grafica retro en Pygame.
Modelos/        Clases base: Pokemon, Movimiento, Equipo y Accion.
Experimentos/   Simulacion, comparaciones y generacion de resultados.
Resultados/     Archivos CSV/JSON/Markdown producidos por experimentos.
Assets/         Sprites usados por la interfaz.
tests/          Pruebas automatizadas.
```

## Pruebas

```bash
pytest
```

## Estado actual frente a la rubrica

El proyecto ya implementa combate por turnos, agentes inteligentes, Minimax, algoritmo genetico, interfaz con seleccion 3v3/4v4, resultados experimentales y pruebas automatizadas. Las mejoras pendientes principales son ampliar la bateria de pruebas y regenerar resultados finales antes de la entrega.

## Nota academica

Este repositorio es un proyecto academico de Inteligencia Artificial. Los nombres y sprites de Pokemon se usan como referencia educativa.
