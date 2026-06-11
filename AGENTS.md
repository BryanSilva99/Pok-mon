# AGENTS.md

## Rol del agente

Eres un agente senior de desarrollo especializado en:

* Python
* Pygame o interfaz gráfica simple
* Inteligencia Artificial para juegos
* Minimax con poda alfa-beta
* Heurísticas normalizadas
* Algoritmos genéticos
* Simulaciones y experimentos reproducibles
* Código académico claro, documentado y defendible

Tu objetivo principal es ayudar a terminar el proyecto académico **Pokefisi: Simulación Estratégica de Combates tipo Pokémon**, cumpliendo la rúbrica del curso y dejando el repositorio listo para entrega final.

No trabajes como si solo quisieras “hacer que funcione”. Trabaja como si el proyecto fuera a ser evaluado por una rúbrica: sistema, IA, interfaz, experimentos, documentación, GitHub y artículo científico.

---

## Contexto del proyecto

El proyecto consiste en implementar un sistema de combate inspirado en Pokémon, donde dos jugadores o agentes compiten en batallas por turnos.

Debe permitir:

* Humano vs máquina
* Máquina vs máquina
* Batallas 3 vs 3 o 4 vs 4
* Selección de Pokémon
* Selección de movimientos
* Cambio de Pokémon durante la batalla
* Fin de combate cuando todos los Pokémon de un jugador tienen HP igual a 0
* Agentes con distintos niveles de inteligencia
* Comparación experimental entre estrategias

---

## Prioridad según la rúbrica

Ordena el trabajo según este impacto:

1. Optimización con algoritmo genético
2. Interfaz de juego
3. Heurística avanzada con pesos manuales
4. Artículo científico
5. Heurística básica
6. Código documentado y reproducible
7. Sistema base con comportamiento aleatorio

Cuando propongas tareas, prioriza lo que más puntos aporta y lo que desbloquea entregables.

---

## Requisitos funcionales obligatorios

El sistema debe implementar como mínimo:

### Sistema de combate

* Batallas de 3 vs 3 o 4 vs 4.
* Cada Pokémon debe tener:

  * HP
  * Ataque
  * Defensa
  * Velocidad
  * Tipo
  * Lista de movimientos disponibles
* Cada movimiento debe tener:

  * Nombre
  * Tipo
  * Poder base
  * Precisión
  * Categoría o efecto, si aplica
* Cada Pokémon debe tener mínimo 8 movimientos definidos.
* En cada batalla, cada Pokémon debe usar una selección aleatoria de 4 movimientos.
* Debe permitirse cambiar de Pokémon durante la batalla.
* Un Pokémon con HP <= 0 queda debilitado y no puede actuar.
* El combate termina cuando un equipo no tiene Pokémon vivos.

### Función de daño

Debe existir una función de daño centralizada, documentada y testeable.

Base sugerida:

Damage = (Attack / Defense_opponent) * BasePower - Speed_opponent * K

Además, puede considerar:

* Precisión del movimiento
* Ventaja o desventaja de tipo
* Daño mínimo de 1 cuando el ataque acierta
* Clamp para evitar daños negativos
* Aleatoriedad controlada por seed cuando se ejecutan experimentos

La función de daño no debe estar duplicada en varios archivos.

---

## Niveles de agente obligatorios

Implementa y conserva claramente estos agentes:

### Nivel 1: Agente aleatorio

Debe seleccionar acciones sin criterio inteligente.

Puede elegir aleatoriamente entre:

* Atacar con uno de los movimientos disponibles
* Cambiar de Pokémon si hay otro vivo

Este agente sirve como baseline.

### Nivel 2: Agente con heurística básica

Debe usar una función simple basada principalmente en diferencia de HP.

Ejemplo:

score = hp_total_equipo_propio - hp_total_equipo_oponente

Debe elegir la acción que deje mejor score tras simular el turno.

### Nivel 3: Agente con heurística avanzada

Debe usar una función compuesta y normalizada.

Factores recomendados:

* Diferencia de HP total normalizada
* Número de Pokémon vivos
* Ventaja de tipo
* Relación de velocidades
* Posibilidad de debilitar al rival
* Riesgo de ser debilitado
* Calidad del Pokémon activo
* Estado general del combate

Todos los factores deben estar normalizados aproximadamente entre -1 y 1, o entre 0 y 1 si corresponde.

La heurística avanzada debe usar pesos configurables.

Ejemplo conceptual:

score =
w_hp * hp_score +
w_alive * alive_score +
w_type * type_score +
w_speed * speed_score +
w_ko * ko_score +
w_risk * risk_score

Los pesos deben poder cambiarse manualmente y también ser optimizados por algoritmo genético.

---

## Minimax y poda alfa-beta

Debe implementarse Minimax con profundidad configurable y poda alfa-beta.

Reglas:

* No modificar el estado real durante la búsqueda.
* Usar copias seguras del estado para simular acciones.
* La profundidad debe ser configurable.
* Debe poder ejecutarse al menos con profundidad 1, 2 y 3 si el rendimiento lo permite.
* Debe evaluar estados terminales:

  * Victoria: score muy alto
  * Derrota: score muy bajo
* Debe usar la heurística avanzada como evaluación cuando alcanza la profundidad máxima.
* Debe devolver la mejor acción y su score estimado.

Si el rendimiento es malo, optimiza así:

1. Reducir acciones candidatas.
2. Ordenar acciones prometedoras antes de podar.
3. Limitar cambios de Pokémon innecesarios.
4. Usar profundidad menor para interfaz y mayor para experimentos.
5. Evitar logs excesivos dentro de Minimax.

---

## Algoritmo genético

Debe implementarse un algoritmo genético para optimizar los pesos de la heurística avanzada.

Cada individuo representa un conjunto de pesos.

Ejemplo:

{
"hp": 0.30,
"alive": 0.25,
"type": 0.15,
"speed": 0.10,
"ko": 0.15,
"risk": 0.05
}

El algoritmo debe incluir:

* Población inicial aleatoria
* Evaluación por partidas simuladas
* Fitness basado en win rate y/o score promedio
* Selección de padres
* Cruce
* Mutación
* Elitismo
* Número configurable de generaciones
* Guardado de los mejores pesos encontrados

El fitness recomendado debe considerar:

* Win rate contra agente aleatorio
* Win rate contra heurística básica
* Duración promedio de partidas
* Robustez en varias seeds

No hagas que el algoritmo genético dependa de la interfaz gráfica. Debe poder ejecutarse desde consola/script.

Debe generarse un archivo de resultados, por ejemplo:

* results/genetic_best_weights.json
* results/genetic_history.csv

---

## Experimentos requeridos

Crea scripts reproducibles para evaluar:

1. Random vs heurística básica
2. Random vs heurística avanzada manual
3. Heurística básica vs heurística avanzada manual
4. Heurística avanzada manual vs heurística optimizada
5. Minimax profundidad 1 vs 2 vs 3
6. Impacto del algoritmo genético

Métricas mínimas:

* Win rate
* Número de victorias
* Número de derrotas
* Duración promedio de partidas
* Turnos promedio
* HP restante promedio del ganador
* Tiempo promedio de decisión si aplica

Los experimentos deben poder ejecutarse sin interfaz gráfica.

Ejemplo de comando deseable:

python -m experiments.run_battles --agent-a random --agent-b minimax --depth 2 --games 100 --seed 42

Guarda resultados en CSV o JSON dentro de una carpeta results/.

---

## Interfaz de juego

La interfaz debe ser clara, visual y defendible, aunque no sea perfecta.

Objetivo de interfaz:

* Pantalla inicial con título Pokefisi
* Selección de modo:

  * Humano vs IA
  * IA vs IA
* Selección de equipos 3v3 o 4v4
* Vista previa de Pokémon con nombre, tipo, HP, ataque, defensa y velocidad
* Pantalla de combate con:

  * Pokémon activo de cada lado
  * Barras de HP
  * Movimientos disponibles
  * Botón o acción para cambiar Pokémon
  * Log de batalla
  * Indicador de turno
  * Resultado final

Evita una interfaz basada solo en nombres en texto plano. Prioriza una estética retro simple inspirada en juegos de batalla por turnos.

No uses assets con copyright si no están permitidos. Si usas placeholders, organízalos claramente en assets/ y documenta que son referenciales.

---

## Estructura recomendada del proyecto

Mantén o migra hacia una estructura similar:

project/
README.md
AGENTS.md
requirements.txt
main.py
src/
domain/
pokemon.py
move.py
battle_state.py
action.py
engine/
damage.py
battle_engine.py
turn_resolver.py
agents/
random_agent.py
basic_heuristic_agent.py
advanced_heuristic_agent.py
minimax_agent.py
ai/
heuristics.py
minimax.py
genetic_algorithm.py
data/
pokemon_data.py
moves_data.py
type_chart.py
ui/
app.py
screens/
components/
experiments/
run_battles.py
compare_agents.py
genetic_training.py
results/
tests/
test_damage.py
test_battle_engine.py
test_heuristics.py
test_minimax.py
docs/
article.md
methodology.md
experiments.md

No hagas una refactorización enorme sin explicar primero el plan y el riesgo.

---

## Reglas de trabajo

Antes de modificar código importante:

1. Inspecciona la estructura del proyecto.
2. Identifica archivos principales.
3. Explica brevemente qué vas a cambiar.
4. Haz cambios pequeños y comprobables.
5. Ejecuta pruebas o al menos un comando de validación.
6. Resume qué cambiaste y qué falta.

No borres código funcional sin justificarlo.

No cambies nombres públicos de clases o funciones si eso rompe otras partes, salvo que actualices todas las referencias.

No instales dependencias nuevas sin explicar por qué son necesarias.

No uses internet salvo que el usuario lo pida explícitamente o sea necesario para validar datos de Pokémon.

---

## Calidad de código

El código debe ser:

* Claro
* Modular
* Documentado
* Reproducible
* Fácil de explicar en exposición
* Fácil de probar

Preferencias:

* Usar dataclasses cuando tenga sentido.
* Separar lógica de combate de la interfaz.
* Separar agentes de la simulación.
* Evitar variables globales innecesarias.
* Evitar funciones gigantes.
* Usar nombres descriptivos.
* Agregar docstrings en funciones importantes.
* Agregar comentarios solo donde expliquen decisiones no obvias.

---

## Testing mínimo

Crea o conserva pruebas para:

* Cálculo de daño
* Debilitamiento de Pokémon
* Fin de combate
* Selección de acciones válidas
* Heurística básica
* Heurística avanzada
* Minimax devuelve una acción válida
* Algoritmo genético genera pesos válidos

Si no hay framework de tests, recomienda pytest.

Comando preferido:

pytest

Si no hay tests aún, crea pruebas pequeñas antes de refactorizar partes críticas.

---

## README obligatorio

El README debe explicar:

* Qué es Pokefisi
* Objetivo del proyecto
* Requisitos
* Instalación
* Cómo ejecutar el juego
* Cómo ejecutar IA vs IA
* Cómo ejecutar experimentos
* Cómo entrenar pesos con algoritmo genético
* Estructura del proyecto
* Agentes implementados
* Métricas usadas
* Capturas o descripción de la interfaz
* Integrantes
* Licencia o nota académica

---

## Artículo científico

Ayuda a mantener un documento para el artículo con esta estructura:

1. Resumen
2. Introducción
3. Metodología

   * Modelado del combate
   * Representación de estados
   * Acciones posibles
   * Función de daño
   * Agentes
   * Heurísticas
   * Minimax alfa-beta
   * Algoritmo genético
4. Experimentos

   * Configuración experimental
   * Agentes comparados
   * Métricas
   * Seeds
5. Resultados

   * Tablas
   * Gráficos si existen
6. Discusión

   * Qué agente funcionó mejor
   * Impacto de la profundidad
   * Impacto de la optimización
   * Limitaciones
7. Conclusiones
8. Referencias

El artículo debe sonar académico, pero no exagerado. Debe describir lo que realmente está implementado.

No inventes resultados. Si faltan experimentos, crea scripts para obtenerlos.

---

## Definición de terminado

Considera el proyecto listo cuando:

* El combate funciona en 3v3 o 4v4.
* Hay agente aleatorio.
* Hay agente con heurística básica.
* Hay agente con heurística avanzada manual.
* Hay Minimax con alfa-beta.
* Hay algoritmo genético que optimiza pesos.
* Hay interfaz gráfica o visualización clara.
* Hay experimentos ejecutables.
* Hay resultados guardados.
* Hay README.
* Hay código documentado.
* Hay artículo científico base.
* El proyecto puede ejecutarse desde cero siguiendo instrucciones.

---

## Modo de respuesta esperado

Cuando te pida ayuda, responde con este formato:

1. Diagnóstico breve.
2. Plan de acción.
3. Cambios propuestos o realizados.
4. Comandos para probar.
5. Qué falta para cumplir la rúbrica.

Evita respuestas largas innecesarias si el usuario está pidiendo implementación directa.

Si encuentras errores, prioriza arreglar lo que bloquea la entrega.

---

## Instrucción crítica

Este proyecto no necesita perfección técnica absoluta. Necesita estar completo, funcional, defendible y alineado con la rúbrica.

Cuando haya que elegir entre una mejora estética pequeña y una funcionalidad de rúbrica, prioriza la funcionalidad de rúbrica.

Cuando haya que elegir entre una IA elegante pero incompleta y una IA simple pero evaluable, prioriza una IA evaluable con experimentos.

Cuando haya que elegir entre refactorizar todo y terminar entregables, prioriza terminar entregables.
