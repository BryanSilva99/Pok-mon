# Insumos para el articulo cientifico - Pokefisi

Este archivo contiene los resultados empiricos generados para redactar el articulo final.

## Configuracion experimental

- Combates 3 vs 3 y verificacion experimental 4 vs 4.
- Dataset curado de 30 Pokemon.
- Cada Pokemon dispone de 8 movimientos y usa 4 movimientos seleccionados aleatoriamente.
- Maximo de 200 turnos por partida; si se alcanza ese limite se registra empate.
- Comparaciones principales: 100 partidas por enfrentamiento.
- Prueba de profundidad Minimax: 20 partidas por profundidad.
- Prueba 4 vs 4: 30 partidas por enfrentamiento.
- Las series alternan el orden de los agentes para reducir sesgo por iniciativa.

## Pesos manuales de la heuristica avanzada

| Factor | Peso |
|---|---:|
| hp | 0.2800 |
| vivos | 0.2200 |
| tipo | 0.1200 |
| velocidad | 0.0800 |
| amenaza | 0.1200 |
| ko | 0.0800 |
| riesgo | 0.0600 |
| calidad_activo | 0.0400 |

## Pesos optimizados usados por AgenteOptimizado

| Factor | Peso |
|---|---:|
| hp | 0.1414 |
| vivos | 0.2836 |
| tipo | 0.1675 |
| velocidad | 0.1068 |
| amenaza | 0.2507 |
| ko | 0.0200 |
| riesgo | 0.0200 |
| calidad_activo | 0.0100 |

## Comparacion entre agentes

| Agente 1 | Agente 2 | Partidas | Win rate A1 | Win rate A2 | Empates | Turnos prom. | HP A1 | HP A2 |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Random A | Random B | 100 | 48.0% | 52.0% | 0 | 15.57 | 31.63 | 26.80 |
| Heuristico | Random | 100 | 89.0% | 11.0% | 0 | 9.58 | 122.39 | 6.33 |
| Avanzado manual | Random | 100 | 80.0% | 20.0% | 0 | 10.50 | 107.00 | 10.66 |
| Avanzado manual | Heuristico | 100 | 42.0% | 58.0% | 0 | 8.46 | 47.33 | 62.06 |
| Optimizado | Avanzado manual | 100 | 54.0% | 46.0% | 0 | 10.81 | 62.89 | 56.32 |
| Minimax p2 | Random | 100 | 85.0% | 15.0% | 0 | 11.33 | 112.30 | 11.32 |
| Minimax p2 | Heuristico | 100 | 33.0% | 67.0% | 0 | 9.04 | 28.09 | 82.38 |

## Impacto de la profundidad de Minimax

| Agente 1 | Agente 2 | Partidas | Win rate A1 | Win rate A2 | Empates | Turnos prom. | HP A1 | HP A2 |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Minimax p1 | Random | 20 | 80.0% | 20.0% | 0 | 10.35 | 112.75 | 15.35 |
| Minimax p2 | Random | 20 | 80.0% | 20.0% | 0 | 10.25 | 129.45 | 12.90 |
| Minimax p3 | Random | 20 | 85.0% | 15.0% | 0 | 9.95 | 127.25 | 13.50 |

## Verificacion 4 vs 4

| Agente 1 | Agente 2 | Partidas | Win rate A1 | Win rate A2 | Empates | Turnos prom. | HP A1 | HP A2 |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Avanzado manual 4v4 | Random 4v4 | 30 | 100.0% | 0.0% | 0 | 13.43 | 193.20 | 0.00 |
| Minimax p2 4v4 | Heuristico 4v4 | 30 | 26.7% | 73.3% | 0 | 12.23 | 28.47 | 108.93 |

## Optimizacion evolutiva

### Evolucion por generacion

| Generacion | Fitness | Win rate vs manual | Win rate vs heuristico | Win rate vs random |
|---:|---:|---:|---:|---:|
| 1 | 0.4694 | 40.0% | 60.0% | 60.0% |
| 2 | 0.4706 | 40.0% | 60.0% | 60.0% |
| 3 | 0.4706 | 40.0% | 60.0% | 60.0% |

### Mejores pesos encontrados en la corrida evolutiva

| Factor | Peso |
|---|---:|
| hp | 0.2148 |
| vivos | 0.2115 |
| tipo | 0.0335 |
| velocidad | 0.0667 |
| amenaza | 0.1891 |
| ko | 0.1700 |
| riesgo | 0.0568 |
| calidad_activo | 0.0576 |

### Evaluacion final del mejor individuo

- Fitness final: 0.6429
- Win rate vs avanzado manual: 73.3%
- Win rate vs heuristico basico: 46.7%
- Win rate vs random: 73.3%

## Estructura recomendada del articulo

1. Resumen: objetivo, agentes evaluados, metodologia experimental y hallazgos principales.
2. Introduccion: juegos por turnos, toma de decisiones adversarial y motivacion del simulador.
3. Metodologia: modelado de Pokemon, movimientos, formula de dano, agentes y optimizacion.
4. Experimentos: escenarios, numero de partidas, metricas y configuracion de semillas.
5. Resultados: insertar las tablas anteriores.
6. Discusion: interpretar rendimiento, costo de Minimax, ventajas y limites de la optimizacion.
7. Conclusiones: aprendizajes, agente mas competitivo y mejoras futuras.
8. Referencias: Pokemon Showdown, PokeAPI sprites y material teorico de Minimax/algoritmos geneticos.
