*This project has been created as part of the 42 curriculum by aarellan, crubio-p.*

# A-Maze-ing



Generador y visualizador de laberintos en Python.

Este proyecto propone una estructura modular para crear, configurar y representar laberintos de forma reutilizable, con un ejecutable principal, un módulo de generación y una capa de visualización.

## Description

La idea principal es separar claramente la lógica del laberinto, la configuración del programa y la salida visual o textual para mantener el proyecto escalable y fácil de mantener.

- Generación del laberinto
- Validación de configuración con Pydantic
- Escritura del resultado final
- Visualización ASCII interactiva en terminal
- Estructura reutilizable como paquete Python

## Estructura del proyecto

```text
a_maze_ing/
├── a_maze_ing.py              # Archivo ejecutable principal
│                              # Ejemplo: python3 a_maze_ing.py config.txt
├── config.txt                 # Configuración por defecto del proyecto
├── Makefile                   # Comandos obligatorios: install, run, debug, clean, lint
├── LICENSE.md                 # Licencia de reutilización
├── README.md                  # Documentación del proyecto
├── pyproject.toml             # Configuración del paquete reutilizable
├── .gitignore                 # Archivos y artefactos generados por Python
│
├── mazegen/                   # Módulo reutilizable (compilable como mazegen-*.whl)
│   ├── __init__.py            # Expone la clase MazeGenerator
│   ├── generator.py           # Kruskal aleatorizado y generación con ciclos
│   ├── maze.py                # Estructura del laberinto
│   ├── pattern42.py           # Patrón estructural 42
│   ├── solver.py              # Ruta mínima por BFS
│   └── types.py               # Tipos compartidos
│
├── visualizer/                # Módulo de visualización
│   ├── __init__.py
│   ├── ascii_display.py       # Renderizado en terminal ASCII (interactivo)
│   └── interactive.py         # Lectura de teclas y estado de la interfaz
│
├── config_parser.py           # Parser KEY=VALUE y validación con Pydantic
├── output_writer.py           # Generador del resultado final en formato hexadecimal + coordenadas + ruta
├── tests/                     # Pruebas con unittest
└──
```

La distribución instalable `mazegen-*.whl` se entrega en la raíz. Incluye
la biblioteca y esta documentación, no la CLI ni el visualizador.

## Módulos principales

### `mazegen/`
Contiene la lógica central para generar y manipular el laberinto. Está pensado para ser reutilizable y exportable como paquete.

### `visualizer/`
Representa paredes, entrada, salida, patrón 42 y solución mediante ASCII y
colores ANSI. No utiliza MiniLibX.

### `config_parser.py`
Se encarga de validar y procesar la configuración del archivo `config.txt`.

### `output_writer.py`
Genera la salida final del proyecto en un formato legible y útil para análisis o visualización posterior.

## Flujo esperado

1. El usuario ejecuta el programa principal.
2. Se carga la configuración desde `config.txt`.
3. Se genera el laberinto con la estrategia deseada.
4. Se calcula la ruta mínima si corresponde.
5. Se imprime o escribe el resultado final.

## Instructions

```bash
make install
.venv/bin/python a_maze_ing.py config.txt
.venv/bin/python a_maze_ing.py config.txt --interactive
```

## Comandos recomendados

```bash
make install
make run
make debug
make clean
make lint
make test
make check
make package
```

## Objetivo del proyecto

Crear una base sólida para un sistema de generación y resolución de laberintos, con una arquitectura limpia, documentación útil y posibilidad de reutilización del módulo principal.

---

Requiere Python 3.10 o posterior. `make install` crea `.venv` e instala
Pydantic y las herramientas de desarrollo declaradas en `pyproject.toml`.
Las rutas relativas se interpretan desde el directorio de ejecución.
Los detalles de uso también están en [TUTORIAL.md](TUTORIAL.md).

## Configuración (`config_parser.py`)

El módulo `config_parser.py` procesa y valida el archivo de configuración en formato `KEY=VALUE`, garantizando la integridad de los datos de entrada antes de inicializar la lógica de generación.

### Arquitectura y Funcionamiento

1. **Modelo de Datos e Inmutabilidad (`MazeConfig`)**:
   Se utiliza un modelo de Pydantic (`BaseModel`) configurado con `ConfigDict(frozen=True)` que almacena la configuración validada. Pydantic es una dependencia de ejecución declarada en `pyproject.toml` (`pydantic>=2,<3`) y previene modificaciones accidentales de los parámetros durante el ciclo de vida del programa.

2. **Control de Errores Exhaustivo (`ConfigError`)**:
   Cualquier anomalía (archivos inexistentes, errores de sintaxis, coordenadas inválidas o tipos incompatibles) se captura y relanza bajo la excepción personalizada `ConfigError`. Esto evita fallos inesperados y asegura mensajes claros por consola.

3. **Validaciones**:
   - Descarta comentarios iniciados por `#` y líneas vacías.
   - Verifica la presencia obligatoria de las claves `WIDTH`, `HEIGHT`, `ENTRY`, `EXIT`, `OUTPUT_FILE` y `PERFECT`.
   - Valida que `ENTRY` y `EXIT` estén dentro de los límites ($0 \le x < \text{WIDTH}$, $0 \le y < \text{HEIGHT}$) y no coincidan en la misma celda.
   - Parsea opcionalmente el parámetro `SEED` para ejecuciones reproducibles.

El archivo UTF-8 contiene un par `KEY=VALUE` por línea. Se ignoran líneas
vacías y las que empiezan por `#`, tras quitar espacios iniciales. Un `#`
dentro de un valor se conserva: `OUTPUT_FILE=maze#1.txt` es válido. No se
admiten comentarios al final de una asignación. Los espacios alrededor de
claves y valores se ignoran; las claves no distinguen mayúsculas.

Ejemplo completo, independiente de cambios locales de `config.txt`:

```ini
# Tablero con rutas alternativas
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=False
SEED=42
```

| Clave | Obligatoria | Formato y significado |
| --- | --- | --- |
| `WIDTH` | Sí | Entero: número de columnas, mínimo 2. |
| `HEIGHT` | Sí | Entero: número de filas, mínimo 2. |
| `ENTRY` | Sí | Coordenadas `x,y` de entrada, con enteros desde cero. |
| `EXIT` | Sí | Coordenadas `x,y` de salida, distintas de la entrada. |
| `OUTPUT_FILE` | Sí | Ruta de salida; su directorio debe existir. |
| `PERFECT` | Sí | `True` genera un árbol; `False`, un tablero con ciclos. |
| `SEED` | No | Entero; omitido, usa aleatoriedad del sistema. |

Los booleanos aceptan `true`, `1`, `yes`, `false`, `0` y `no`, sin distinguir
mayúsculas. Las coordenadas deben estar dentro del tablero y no ocupar el 42.
`x` crece hacia la derecha e `y` hacia abajo. Las claves adicionales se ignoran;
si se repite una clave, se utiliza su última asignación.

El modo imperfecto rechaza parámetros o restricciones que impidan cumplir
conectividad, al menos dos ciclos independientes o un máximo de dos
callejones sin salida. Un tablero 2×2 no puede cumplir el mínimo de ciclos.
La semilla reproduce la estructura para la misma configuración y versión
del generador; no promete compatibilidad entre versiones del algoritmo.

## Algoritmos y decisiones técnicas

El modo perfecto utiliza Kruskal aleatorizado: mezcla las conexiones de la
cuadrícula y Union-Find decide cuáles unen componentes diferentes. Las demás
se cierran. El resultado es un árbol sobre las celdas transitables: está
conectado y no tiene ciclos. Las celdas del 42 quedan fuera del grafo.

Este enfoque permite controlar los ciclos explícitamente, respetar conexiones
obligatorias y paredes protegidas, y reproducir resultados con una semilla.
Estas son las razones técnicas de su elección. No pretende generar
uniformemente todos los árboles posibles.

El modo imperfecto conserva conexiones adicionales y reduce callejones sin
salida. Comprueba las propiedades finales y repara las áreas 3×3 totalmente
abiertas sin romper las restricciones. Los cuatro vértices y la celda
`(WIDTH // 2, HEIGHT // 2)` permanecen transitables.

BFS calcula una ruta mínima porque cada paso tiene el mismo coste.
La salida guarda filas hexadecimales, una línea vacía, entrada, salida y
la ruta `N`, `E`, `S`, `W`; todas las líneas terminan con un salto de línea.
Los bits de pared cerrada son norte=1, este=2, sur=4 y oeste=8.

## Visualización

El modo `--interactive` necesita una terminal real. `E` indica entrada, `X`
salida, `*` solución y `###` celdas del 42. Las teclas no necesitan Enter:

| Tecla | Acción |
| --- | --- |
| `R` | Regenerar con las mismas opciones y una nueva semilla aleatoria. |
| `S` | Mostrar u ocultar la ruta mínima. |
| `C` | Cambiar el color de las paredes. |
| `N` | Activar o desactivar colores ANSI. |
| `Q`, `Esc`, `Ctrl+C` | Salir. |

La generación normal escribe `OUTPUT_FILE`; el modo interactivo visualiza
pero no actualiza ese archivo. Para comparar ambas ejecuciones, usa una
semilla fija antes de regenerar. El patrón solo se omite cuando no cabe y
esa omisión se anuncia por consola en ambos modos.

## Biblioteca reutilizable

La API pública de `mazegen` expone `MazeGenerator`, `Maze`, `Cell`, `Direction`,
`Pattern42` y `solve_shortest_path`. Ejemplo ejecutable:

```python
from mazegen import Direction, MazeGenerator, solve_shortest_path

generator = MazeGenerator(seed=42)
maze = generator.generate_perfect(
    width=20, height=15, entry=(0, 0), exit=(19, 14)
)
cell = maze.cell_at((0, 0))
print(maze.width, maze.height, cell.has_wall(Direction.NORTH))
print([[cell.wall_mask for cell in row] for row in maze.cells])
solution = solve_shortest_path(maze)
assert solution is not None
print([direction.name for direction in solution])

board = generator.generate_imperfect(
    width=20, height=15, entry=(0, 0), exit=(19, 14)
)
assert solve_shortest_path(board) is not None
```

Ambos métodos aceptan `required_open_passages` y `protected_closed_passages`:
iterables de `((x, y), Direction)`. Las restricciones incompatibles producen
`ValueError`; la biblioteca no oculta esas excepciones al programa importador.
Las celdas son mutables: si se modifican directamente, el consumidor debe
mantener la coherencia de paredes y conectividad.

Para reconstruir desde las fuentes e instalar en otro entorno:

```bash
make install
make package
python3 -m pip install ./mazegen-0.1.0-py3-none-any.whl
```

La construcción estándar equivalente es
`.venv/bin/python -m build --no-isolation --outdir .`; crea wheel y tarball
en la raíz. La licencia MIT de `LICENSE.md` permite reutilizar y distribuir
el módulo conservando el aviso de licencia. `make clean` elimina cachés y
el directorio temporal `build/`, pero conserva las distribuciones entregables.

## Equipo y gestión del proyecto

Reparto registrado en la bitácora original:

- César: modelos `Maze` y `Cell`, estructura inicial, generador y pruebas.
- Alex: parser, Makefile, exploración de MLX y transición a ASCII, mypy y flake8.

El plan registrado comenzó separando modelos y configuración; después pasó
a generación, pruebas y visualización. La alternativa MLX se sustituyó por
ASCII. La fase de cierre añadió la auditoría del subject, correcciones de
conformidad, documentación y comprobación de distribuciones. No se conservan
estimaciones iniciales de fechas, por lo que no se presenta un calendario
retrospectivo inventado.

Qué funcionó: la separación entre modelo, generador, solver e interfaz
permite comprobar e instalar la biblioteca de manera independiente. Las
pruebas de regresión hacen repetibles los fallos encontrados.

Qué mejorar: mantener la documentación sincronizada desde el principio y
convertir cada obligación del subject en una comprobación explícita. Una
suite verde no detectaba por sí sola todos los requisitos Pac-Man.

Herramientas: Python, Pydantic, Git, Make, venv/pip, unittest, flake8, mypy,
pdb y build/setuptools/wheel. La bitácora siguiente conserva las notas
originales, no una atribución completa de cada cambio posterior.

## Resources

- [Documentación de Python](https://docs.python.org/3/): excepciones,
  `random`, `collections.deque`, `unittest`, `venv` y `pdb`.
- [Pydantic](https://docs.pydantic.dev/latest/): modelos y validadores.
- [Kruskal](https://en.wikipedia.org/wiki/Kruskal%27s_algorithm) y
  [Union-Find](https://en.wikipedia.org/wiki/Disjoint-set_data_structure):
  árboles de expansión y componentes conexas.
- [BFS](https://en.wikipedia.org/wiki/Breadth-first_search): ruta mínima.
- [Python Packaging User Guide](https://packaging.python.org/en/latest/):
  construcción e instalación de distribuciones.
- [flake8](https://flake8.pycqa.org/en/latest/) y
  [mypy](https://mypy.readthedocs.io/en/stable/): estilo y tipos.

Uso de IA registrado en la revisión final: Hermes ayudó a contrastar el
subject con el código, reproducir errores, diseñar y ejecutar pruebas y
corregir CLI, parser, generación, patrón 42 y controles de color. También
ayudó a actualizar esta documentación y verificar el empaquetado. Estas
contribuciones no sustituyen la revisión y comprensión del equipo ni una
defensa con compañeros. La bitácora original no documenta otros usos de IA.

## Cuaderno de bitácora

### Día 1

División de trabajo y empezamos fuerte:

```text
CÉSAR:      Clases Maze y Cell

ALEX:       Parseo (Que lea del config.txt y devuelva un objeto con todos los settings)
```

### Día 3

```text
CÉSAR:      Clase Maze, tests y esqueleto del proyecto

ALEX:       Revisar parseo, Makefile y aprender MLX
```

### Día 6

```text
CÉSAR:      Maze Generator + tests del generator

ALEX:       Cambio de MLX a ASCII y gestión de mypy, flake8 y caché
```
