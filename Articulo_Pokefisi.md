# Pokefisi: simulacion estrategica de combates por turnos con agentes inteligentes

## Nota para IA generativa

Este documento es el borrador fuente para construir el articulo final. La IA que lo use puede mejorar redaccion, cohesion, estilo academico y formato, pero no debe inventar resultados, metricas, referencias ni caracteristicas no implementadas.

Fuentes locales que deben respetarse:

- Codigo del simulador: `Batalla/`, `Modelos/`, `Datos/`, `IA/`, `Experimentos/`, `Interfaz/`.
- Resultados empiricos: `Resultados/comparacion_agentes.csv`, `Resultados/impacto_profundidad.csv`, `Resultados/comparacion_4v4.csv`, `Resultados/genetic_history.csv`, `Resultados/genetic_best_weights.json`.
- Insumos tabulados: `Resultados/insumos_articulo.md`.

Reglas para construir la version final:

- Mantener los valores numericos de las tablas tal como aparecen aqui o en `Resultados/`.
- No afirmar que un agente es superior si los resultados no lo respaldan.
- Mencionar que el sistema es una simplificacion academica inspirada en combates tipo Pokemon.
- No prometer efectos de estado, habilidades, objetos o reglas completas de Pokemon, porque no estan implementados.
- Si se agregan graficos, deben salir de los CSV de `Resultados/`.

## Resumen

Pokefisi es un simulador academico de combates por turnos inspirado en juegos de criaturas. El sistema modela batallas 3 vs 3 y 4 vs 4 con 30 criaturas seleccionadas desde un dataset curado, atributos de combate, movimientos con tipo, potencia y precision, cambios durante la batalla e interfaz grafica retro desarrollada en Pygame. Se implementaron agentes con distintos niveles de decision: aleatorio, heuristico basico, heuristico avanzado, Minimax con poda alfa-beta y un agente optimizado mediante algoritmo evolutivo.

La evaluacion experimental compara los agentes usando victorias, win rate, empates, turnos promedio y HP final promedio. En las comparaciones 3 vs 3, el agente heuristico basico obtuvo 89.0% de victorias contra el agente aleatorio, el agente avanzado manual obtuvo 80.0% contra el aleatorio y Minimax profundidad 2 obtuvo 85.0% contra el aleatorio. El agente optimizado supero al avanzado manual en la comparacion directa con 54.0% de victorias. En la verificacion 4 vs 4, el agente avanzado manual obtuvo 100.0% contra el agente aleatorio, mientras que Minimax profundidad 2 obtuvo 26.7% contra el heuristico basico. Estos resultados muestran que las estrategias informadas superan claramente al baseline aleatorio, aunque la busqueda Minimax no domina necesariamente a una heuristica directa basada en daño esperado en el modelo actual.

Palabras clave: inteligencia artificial, juegos por turnos, Minimax, poda alfa-beta, heuristicas, algoritmo evolutivo, simulacion.

## 1. Introduccion

Los juegos por turnos con adversario son un entorno adecuado para estudiar toma de decisiones, busqueda adversarial y funciones de evaluacion. En este tipo de problema, un agente debe elegir acciones considerando tanto el estado actual como las posibles respuestas del oponente. Pokefisi fue desarrollado como un sistema academico para experimentar con estrategias de decision en un combate simplificado inspirado en Pokemon.

El objetivo del proyecto es construir un simulador funcional que permita partidas humano contra maquina y maquina contra maquina. El sistema incorpora agentes de complejidad creciente: seleccion aleatoria, heuristica basica, heuristica avanzada con pesos configurables, Minimax con poda alfa-beta y optimizacion evolutiva de pesos. Ademas, se busca evaluar empiricamente como cambian los resultados al modificar la estrategia de decision, la profundidad de busqueda y el tamaño del equipo.

El proyecto no busca reproducir todas las reglas oficiales de Pokemon. En cambio, propone un modelo reducido y defendible para un curso de Inteligencia Artificial: atributos numericos, movimientos con potencia y precision, efectividad de tipos, seleccion de acciones, cambios de criatura, simulacion de partidas y comparacion experimental entre agentes.

## 2. Metodologia

### 2.1 Modelado del combate

Cada combate se realiza entre dos equipos de tres o cuatro criaturas. Cada criatura posee:

- HP maximo y HP actual.
- Ataque.
- Defensa.
- Velocidad.
- Tipo primario.
- Tipo secundario opcional.
- Lista de movimientos disponibles.
- Lista de cuatro movimientos usados durante la batalla.

El dataset fue curado a partir de `All_Pokemon.csv`. Se seleccionaron 30 criaturas y para cada una se definieron 8 movimientos disponibles. Al crear una instancia de combate, cada criatura recibe 4 movimientos seleccionados aleatoriamente desde su lista de 8 movimientos.

Cada movimiento posee:

- Nombre.
- Potencia.
- Precision.
- Tipo elemental.

En cada turno, ambos participantes eligen una accion:

- Atacar con uno de los movimientos disponibles.
- Cambiar a otra criatura viva del equipo.

Si ambos participantes atacan, actua primero la criatura con mayor velocidad. Si una criatura queda con HP menor o igual a cero, se considera debilitada y no puede seguir actuando. El combate termina cuando un equipo no tiene criaturas vivas. En los experimentos se usa un limite de 200 turnos; si se alcanza ese limite, la partida se registra como empate.

### 2.2 Funcion de daño

La funcion de daño esta centralizada en `Batalla/Danio.py`. La formula implementada usa la relacion entre ataque y defensa, la potencia del movimiento, un factor de escala y el modificador de efectividad de tipo:

```text
daño = (ataque / defensa_oponente) * potencia_movimiento * escala * modificador_tipo
```

El modificador de tipo considera los tipos defensivos de la criatura, incluyendo tipo secundario cuando existe. Esto permite representar debilidades, resistencias e inmunidades. Cuando el ataque acierta, el daño minimo aplicado es 1.

### 2.3 Representacion de acciones

Las acciones se representan con la clase `Accion`, que puede ser de tipo `atacar` o `cambiar`. Una accion de ataque almacena el indice del movimiento elegido; una accion de cambio almacena el indice de la criatura del equipo que ingresara al combate.

El conjunto de acciones disponibles se calcula a partir del estado actual:

- Si la criatura activa esta viva, se agregan sus movimientos como acciones de ataque.
- Si existen otras criaturas vivas, se agregan acciones de cambio validas.
- No se permite cambiar a una criatura debilitada ni a la misma criatura activa.

### 2.4 Agentes implementados

#### Agente aleatorio

Selecciona una accion valida sin evaluar el estado del combate. Se utiliza como baseline experimental.

#### Agente heuristico basico

Elige el movimiento que produce mayor daño esperado contra la criatura activa rival. El daño esperado se pondera por la precision del movimiento:

```text
score = daño_estimado * precision
```

Este agente es simple, pero resulta competitivo porque el modelo actual recompensa fuertemente el daño inmediato.

#### Agente heuristico avanzado

Evalua acciones simulando su efecto inmediato sobre una copia del estado y luego aplicando una funcion de evaluacion ponderada. Los factores estan normalizados aproximadamente entre -1 y 1.

Pesos manuales usados:

| Factor | Peso manual |
|---|---:|
| hp | 0.2800 |
| vivos | 0.2200 |
| tipo | 0.1200 |
| velocidad | 0.0800 |
| amenaza | 0.1200 |
| ko | 0.0800 |
| riesgo | 0.0600 |
| calidad_activo | 0.0400 |

Descripcion de factores:

- `hp`: diferencia relativa entre HP total propio y rival.
- `vivos`: diferencia proporcional entre criaturas vivas.
- `tipo`: ventaja de tipo del activo propio frente al activo rival.
- `velocidad`: ventaja relativa de velocidad entre activos.
- `amenaza`: diferencia de daño esperado maximo.
- `ko`: posibilidad inmediata de debilitar al rival frente a riesgo propio equivalente.
- `riesgo`: relacion entre presion ofensiva propia y amenaza recibida.
- `calidad_activo`: calidad general del activo considerando HP relativo, ofensiva y velocidad.

#### Minimax con poda alfa-beta

Se implemento Minimax con profundidad configurable y poda alfa-beta. El algoritmo simula turnos deterministas sobre copias del estado para no modificar la batalla real durante la busqueda. Los estados terminales se evaluan con puntajes extremos:

- Victoria: puntaje muy alto.
- Derrota: puntaje muy bajo.

Los estados no terminales se evaluan con la heuristica avanzada. Para controlar el costo de busqueda, el conjunto de acciones candidatas incluye ataques disponibles y un cambio candidato cuando existen cambios validos.

#### Agente optimizado

El agente optimizado usa pesos encontrados mediante algoritmo evolutivo. Cada individuo representa un conjunto de pesos normalizados para la heuristica avanzada.

Pesos optimizados usados por `AgenteOptimizado`:

| Factor | Peso optimizado inicial |
|---|---:|
| hp | 0.1414 |
| vivos | 0.2836 |
| tipo | 0.1675 |
| velocidad | 0.1068 |
| amenaza | 0.2507 |
| ko | 0.0200 |
| riesgo | 0.0200 |
| calidad_activo | 0.0100 |

### 2.5 Algoritmo evolutivo

El algoritmo evolutivo optimiza los pesos de la heuristica avanzada. Incluye:

- Poblacion inicial aleatoria.
- Normalizacion de pesos.
- Evaluacion por partidas simuladas.
- Fitness basado en win rate contra avanzado manual, heuristico basico y aleatorio, ademas de margen de HP.
- Seleccion de padres.
- Cruce.
- Mutacion.
- Elitismo.
- Historial por generacion.

Los resultados se guardan en:

- `Resultados/genetic_best_weights.json`.
- `Resultados/genetic_history.csv`.

## 3. Experimentos

### 3.1 Configuracion experimental

Configuracion usada:

- Dataset curado de 30 criaturas.
- Cada criatura dispone de 8 movimientos y usa 4 movimientos seleccionados aleatoriamente.
- Maximo de 200 turnos por partida.
- Comparaciones principales 3 vs 3: 100 partidas por enfrentamiento.
- Impacto de profundidad Minimax: 20 partidas por profundidad.
- Verificacion 4 vs 4: 30 partidas por enfrentamiento.
- Las series alternan el orden de los agentes para reducir sesgo por iniciativa.

### 3.2 Comparaciones realizadas

Se evaluaron cuatro grupos:

1. Comparacion general entre agentes.
2. Impacto de la profundidad de Minimax.
3. Optimizacion evolutiva de pesos.
4. Verificacion de batallas 4 vs 4.

### 3.3 Metricas

Las metricas registradas fueron:

- Numero de partidas.
- Victorias del agente 1.
- Victorias del agente 2.
- Empates.
- Win rate del agente 1.
- Win rate del agente 2.
- Turnos promedio.
- HP final promedio del agente 1.
- HP final promedio del agente 2.

## 4. Resultados

### 4.1 Comparacion entre agentes 3 vs 3

| Agente 1 | Agente 2 | Partidas | Win rate A1 | Win rate A2 | Empates | Turnos prom. | HP A1 | HP A2 |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Random A | Random B | 100 | 48.0% | 52.0% | 0 | 15.57 | 31.63 | 26.80 |
| Heuristico | Random | 100 | 89.0% | 11.0% | 0 | 9.58 | 122.39 | 6.33 |
| Avanzado manual | Random | 100 | 80.0% | 20.0% | 0 | 10.50 | 107.00 | 10.66 |
| Avanzado manual | Heuristico | 100 | 42.0% | 58.0% | 0 | 8.46 | 47.33 | 62.06 |
| Optimizado | Avanzado manual | 100 | 54.0% | 46.0% | 0 | 10.81 | 62.89 | 56.32 |
| Minimax p2 | Random | 100 | 85.0% | 15.0% | 0 | 11.33 | 112.30 | 11.32 |
| Minimax p2 | Heuristico | 100 | 33.0% | 67.0% | 0 | 9.04 | 28.09 | 82.38 |

### 4.2 Impacto de la profundidad de Minimax

| Agente 1 | Agente 2 | Partidas | Win rate A1 | Win rate A2 | Empates | Turnos prom. | HP A1 | HP A2 |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Minimax p1 | Random | 20 | 80.0% | 20.0% | 0 | 10.35 | 112.75 | 15.35 |
| Minimax p2 | Random | 20 | 80.0% | 20.0% | 0 | 10.25 | 129.45 | 12.90 |
| Minimax p3 | Random | 20 | 85.0% | 15.0% | 0 | 9.95 | 127.25 | 13.50 |

### 4.3 Verificacion 4 vs 4

| Agente 1 | Agente 2 | Partidas | Win rate A1 | Win rate A2 | Empates | Turnos prom. | HP A1 | HP A2 |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Avanzado manual 4v4 | Random 4v4 | 30 | 100.0% | 0.0% | 0 | 13.43 | 193.20 | 0.00 |
| Minimax p2 4v4 | Heuristico 4v4 | 30 | 26.7% | 73.3% | 0 | 12.23 | 28.47 | 108.93 |

### 4.4 Optimizacion evolutiva

Evolucion por generacion:

| Generacion | Fitness | Win rate vs manual | Win rate vs heuristico | Win rate vs random |
|---:|---:|---:|---:|---:|
| 1 | 0.4694 | 40.0% | 60.0% | 60.0% |
| 2 | 0.4706 | 40.0% | 60.0% | 60.0% |
| 3 | 0.4706 | 40.0% | 60.0% | 60.0% |

Mejores pesos encontrados en la corrida evolutiva:

| Factor | Peso encontrado |
|---|---:|
| hp | 0.2148 |
| vivos | 0.2115 |
| tipo | 0.0335 |
| velocidad | 0.0667 |
| amenaza | 0.1891 |
| ko | 0.1700 |
| riesgo | 0.0568 |
| calidad_activo | 0.0576 |

Evaluacion final del mejor individuo:

- Fitness final: 0.6429.
- Win rate vs avanzado manual: 73.3%.
- Win rate vs heuristico basico: 46.7%.
- Win rate vs random: 73.3%.

## 5. Discusion

El agente aleatorio funciona como baseline valido: en Random A contra Random B la distribucion fue cercana al equilibrio, con 48.0% y 52.0% de victorias. Esto indica que el sistema no favorece de forma extrema a una posicion cuando ambos agentes carecen de criterio.

Los agentes con decision informada superaron claramente al baseline aleatorio. El heuristico basico obtuvo 89.0% de victorias contra Random, el avanzado manual obtuvo 80.0% y Minimax profundidad 2 obtuvo 85.0%. Estos resultados muestran que evaluar daño esperado, HP, criaturas vivas y amenaza produce ventajas importantes frente a acciones aleatorias.

La heuristica basica supero al avanzado manual en la comparacion directa, con 58.0% de victorias para el heuristico basico. Esto sugiere que, en el modelo actual, el daño inmediato sigue siendo un factor dominante. Aunque la heuristica avanzada considera mas informacion del estado, los efectos secundarios, estados alterados, habilidades y objetos no estan modelados; por ello, factores estrategicos de largo plazo tienen menor impacto que en un sistema de combate completo.

Minimax tuvo buen rendimiento contra Random, pero no supero al heuristico basico. En 3 vs 3, Minimax profundidad 2 obtuvo 33.0% frente al heuristico basico. En 4 vs 4, Minimax profundidad 2 obtuvo 26.7% contra el mismo tipo de agente. Este resultado no invalida la busqueda adversarial; mas bien muestra que la calidad de la funcion de evaluacion, la reduccion de acciones candidatas y la simplificacion del modelo influyen fuertemente en el rendimiento.

La prueba de profundidad muestra una mejora moderada de profundidad 3 frente a profundidad 1 y 2 contra Random: 80.0%, 80.0% y 85.0%, respectivamente. Dado que solo se usaron 20 partidas por profundidad, esta diferencia debe interpretarse como indicio experimental y no como conclusion definitiva.

El algoritmo evolutivo encontro pesos distintos a los manuales, aumentando la importancia relativa de `amenaza` y `ko`. El mejor individuo alcanzo 73.3% contra la heuristica avanzada manual, 46.7% contra la heuristica basica y 73.3% contra Random. Esto indica que la optimizacion puede mejorar el agente frente a ciertos rivales, aunque no garantiza superioridad universal.

La verificacion 4 vs 4 confirma que el sistema extendido funciona. En esa modalidad, el avanzado manual obtuvo 100.0% contra Random. Sin embargo, Minimax profundidad 2 siguio por debajo del heuristico basico, lo que refuerza la necesidad de mejorar la evaluacion y seleccion de acciones candidatas si se desea que Minimax sea competitivo en escenarios mas grandes.

## 6. Limitaciones

El sistema implementa una version simplificada del combate. Las principales limitaciones son:

- No hay efectos secundarios de movimientos.
- No hay estados alterados como quemadura, paralisis o sueño.
- No hay habilidades, objetos ni condiciones de campo.
- La funcion de daño es simplificada respecto a Pokemon oficial.
- La seleccion de acciones en Minimax se reduce para controlar el costo computacional.
- El algoritmo evolutivo usa poblaciones y generaciones pequeñas para mantener tiempos razonables de ejecucion.
- La cantidad de partidas para profundidad y 4 vs 4 es menor que la comparacion principal.

Estas limitaciones son aceptables para el objetivo academico, pero deben considerarse al interpretar los resultados.

## 7. Conclusiones

Pokefisi cumple el objetivo de implementar un simulador funcional y defendible de combates por turnos con agentes inteligentes. El sistema incluye combate 3 vs 3 y 4 vs 4, seleccion de equipos, seleccion de movimientos, cambios de criatura, interfaz grafica, agentes de distinto nivel, Minimax con poda alfa-beta, algoritmo evolutivo y experimentos reproducibles.

Los resultados muestran que los agentes informados superan de forma clara al agente aleatorio. El heuristico basico fue especialmente competitivo por su enfoque directo en daño esperado. La heuristica avanzada aporta una evaluacion mas rica del estado, y la optimizacion evolutiva encontro pesos capaces de mejorar el rendimiento contra la version manual. Minimax demostro buen rendimiento contra Random, pero no supero al heuristico basico bajo la configuracion actual.

Como trabajo futuro se propone incorporar efectos de movimientos, estados alterados, habilidades, objetos, una funcion de daño mas completa, mas partidas experimentales, comparaciones 4 vs 4 mas amplias y una evaluacion Minimax mas eficiente.

## 8. Referencias

- Pokemon Showdown. Proyecto y datos de referencia para combates competitivos. https://github.com/Zarel/Pokemon-Showdown/
- PokeAPI Sprites. Repositorio de sprites utilizados como recursos visuales. https://github.com/PokeAPI/sprites/
- Russell, S. y Norvig, P. Artificial Intelligence: A Modern Approach. Pearson.
- Goldberg, D. Genetic Algorithms in Search, Optimization and Machine Learning. Addison-Wesley.
- Knuth, D. y Moore, R. An analysis of alpha-beta pruning. Artificial Intelligence, 1975.

## Anexo A. Archivos generados

Archivos de resultados:

- `Resultados/comparacion_agentes.csv`
- `Resultados/impacto_profundidad.csv`
- `Resultados/comparacion_4v4.csv`
- `Resultados/resultados_articulo.json`
- `Resultados/insumos_articulo.md`
- `Resultados/genetic_best_weights.json`
- `Resultados/genetic_history.csv`

Comandos relevantes:

```bash
python pantalla_batalla.py
python main.py
python experimentos.py
python optimizar_pesos.py
python Experimentos/generar_resultados_articulo.py
pytest
```
