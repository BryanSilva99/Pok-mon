# Pygame GUI Skill

Cuando trabajes con pygame:

## Arquitectura

- Separar:
  - main.py
  - scenes/
  - ui/
  - entities/
  - assets/

## UI

- Crear clases reutilizables:
  - Button
  - Panel
  - Label
  - HealthBar
  - DialogBox

## Estilo

- Preferir estética retro tipo GBA/Pokémon
- Usar escalado entero
- Mantener pixel-perfect rendering

## Código

- Evitar lógica gigante en main loop
- Usar SceneManager
- Separar update() y draw()

## Sprites

- Soportar spritesheets
- Usar convert_alpha()

## Rendimiento

- Evitar recrear fuentes cada frame
- Cachear imágenes

## Input

- Manejar hover/click correctamente
- Soportar teclado y mouse
