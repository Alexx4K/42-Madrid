*Este proyecto ha sido creado como parte del currículo de 42 por crubio-p y aarellan.*

# push_swap

## Descripción

`push_swap` es un proyecto de algoritmia escrito en C cuyo objetivo es ordenar
una secuencia de enteros utilizando dos stacks, `a` y `b`, y un conjunto muy
limitado de operaciones.

Al comenzar, `a` contiene todos los valores recibidos y `b` está vacío. El
programa no muestra la lista ordenada: escribe en la salida estándar la
secuencia de instrucciones de Push_swap que permite ordenar `a` de menor a
mayor. El reto consiste en producir una secuencia correcta y lo más corta
posible.

Esta implementación normaliza primero los valores a índices de rango `1..n`.
Así conserva el orden relativo de enteros negativos, positivos o muy grandes y
permite que todas las estrategias trabajen sobre el mismo dominio.

Además de algoritmos específicos para entradas de hasta cinco elementos, el
proyecto integra cuatro modos de ordenación:

- **Simple:** selection sort adaptado.
- **Medium:** chunk sort con chunks de tamaño aproximado `√n`.
- **Complex:** radix sort LSD binario.
- **Adaptive:** selecciona automáticamente una de las tres estrategias
  anteriores según el desorden inicial. Es el modo predeterminado.

## Reglas y operaciones disponibles

Solo se pueden modificar los stacks mediante estas once operaciones:

| Operación | Efecto |
|---|---|
| `sa` | Intercambia los dos primeros elementos de `a`. |
| `sb` | Intercambia los dos primeros elementos de `b`. |
| `ss` | Ejecuta `sa` y `sb` simultáneamente. |
| `pa` | Mueve el primer elemento de `b` a la cima de `a`. |
| `pb` | Mueve el primer elemento de `a` a la cima de `b`. |
| `ra` | Rota `a` hacia arriba: el primer elemento pasa al final. |
| `rb` | Rota `b` hacia arriba: el primer elemento pasa al final. |
| `rr` | Ejecuta `ra` y `rb` simultáneamente. |
| `rra` | Rota `a` hacia abajo: el último elemento pasa al principio. |
| `rrb` | Rota `b` hacia abajo: el último elemento pasa al principio. |
| `rrr` | Ejecuta `rra` y `rrb` simultáneamente. |

Una operación que no pueda aplicarse por falta de elementos no modifica el
stack correspondiente.

## Instrucciones

### Requisitos

- Un sistema Unix o compatible.
- Un compilador de C, como `cc` o `clang`.
- `make`.

### Compilación

```sh
make
```

Esto genera el ejecutable `push_swap`. También están disponibles las reglas
habituales:

```sh
make clean    # elimina los objetos
make fclean   # elimina los objetos y el ejecutable
make re       # recompila el proyecto desde cero
```

### Ejecución

Los enteros pueden pasarse como argumentos separados o dentro de una cadena:

```sh
./push_swap 4 2 1 3
./push_swap "4 2 1 3"
```

Ejemplo de salida:

```text
pb
sa
ra
pa
```

La salida real depende de la entrada y de la estrategia escogida. Si no se
indica un selector, se utiliza el modo adaptativo:

```sh
./push_swap --adaptive 8 3 6 1 5
./push_swap --simple 8 3 6 1 5
./push_swap --medium 8 3 6 1 5
./push_swap --complex 8 3 6 1 5
```

Los selectores de estrategia son mutuamente excluyentes, deben aparecer antes
de los números y no pueden repetirse. `--bench` sí puede combinarse con uno de
ellos:

```sh
./push_swap --bench --complex 8 3 6 1 5 > operations.txt
```

La secuencia de operaciones se escribe en `stdout`; el informe de benchmark se
escribe en `stderr` e incluye el desorden, la estrategia, el total de
operaciones y el desglose por instrucción.

Para contar las operaciones generadas:

```sh
ARG="8 3 6 1 5"
./push_swap $ARG | wc -l
```

#### Uso checker oficial
Si se dispone del checker oficial, se puede validar el resultado con:

```sh
ARG="8 3 6 1 5"
./push_swap $ARG | ./checker_linux $ARG
```

El programa rechaza valores que no sean enteros, números fuera del rango de
`int`, duplicados, flags desconocidos y combinaciones de estrategia
incompatibles. En esos casos escribe `Error` en la salida de error.


#### Comandos útiles para testing

```shell
shuf -i 0-9999 -n 500 > prueba_500_elems.txt ; ./push_swap $(cat prueba_500_elems.txt) | wc -l

shuf -i 0-9999 -n 100 > prueba_500_elems.txt ; ./push_swap $(cat prueba_500_elems.txt) | wc -l

```



## Índice de desorden

El desorden mide lo lejos que se encuentra el stack inicial de estar ordenado.
Su valor está comprendido entre `0` y `1`:

- `0`: todos los pares están en el orden correcto.
- `1`: todos los pares están invertidos.
- Un valor intermedio representa una entrada parcialmente ordenada.

Para calcularlo se examinan todos los pares `(i, j)` con `i < j`. Existe una
inversión cuando `a[i] > a[j]`:

```text
desorden = número de inversiones / número total de pares
```

Pseudocódigo:

```c
function compute_disorder(stack a):
	mistakes = 0
	total_pairs = 0
	for i from 0 to size(a) - 1:
		for j from i + 1 to size(a) - 1:
			total_pairs += 1
			if a[i] > a[j]:
				mistakes += 1
	return mistakes / total_pairs
```

El cálculo realiza `O(n²)` comparaciones en C, pero no genera ninguna
operación Push_swap. Por ello no aumenta la longitud de la solución producida.

## Algoritmos seleccionados

La complejidad indicada a continuación se expresa principalmente en **número
de operaciones Push_swap emitidas**, tal como exige el proyecto, y no solo en
operaciones internas sobre arrays o listas.

### Casos pequeños: de 2 a 5 elementos

Antes de aplicar cualquier estrategia general, las entradas de hasta cinco
elementos se resuelven mediante casos especializados. Dos y tres valores se
ordenan con combinaciones directas de `sa`, `ra` y `rra`; para cuatro y cinco
se extrae el mínimo, se ordena el resto y se vuelve a insertar. Esto evita el
coste fijo de un algoritmo general en entradas pequeñas.

### Simple: selection sort adaptado

En cada iteración se localiza el menor valor de `a`, se lleva a la cima por el
camino más corto (`ra` o `rra`) y se envía a `b` con `pb`. Cuando `a` queda
vacío, todos los elementos regresan mediante `pa`.

La estrategia es sencilla, determinista y adecuada cuando hay poco desorden.
En el peor caso puede requerir `O(n²)` operaciones, porque para cada uno de los
`n` elementos puede ser necesario recorrer mediante rotaciones una parte
lineal del stack. Utiliza `O(1)` espacio auxiliar durante la ordenación.

### Medium: chunk sort

Los índices se dividen en intervalos de tamaño `⌊√n⌋`. Cada chunk se
traslada de `a` a `b`; los valores de su mitad inferior se rotan en `b` para
agruparlos y reducir movimientos posteriores. Finalmente se busca en `b` el
índice máximo restante, se lleva a la cima por el camino más corto y se
devuelve a `a`. La reinserción descendente deja `a` ordenado de forma
ascendente.

El uso de chunks reduce la distancia media de las rotaciones frente al método
de selección. Su objetivo de rendimiento es `O(n·√n)` operaciones en entradas
distribuidas de forma habitual; una distribución adversa puede elevar el peor
caso a `O(n²)`. El espacio auxiliar de la fase de ordenación es `O(1)`.

### Complex: radix sort LSD binario

Radix opera sobre los índices de rango, nunca sobre los valores originales.
Por cada bit, de menos a más significativo, recorre los `n` elementos de `a`:

```c
if (((index >> current_bit) & 1) == 0)
	pb();
else
	ra();
```

Los elementos cuyo bit vale `0` pasan a `b`; los que tienen un `1` rotan y
permanecen en `a`. Al terminar cada pasada, todos los valores de `b` vuelven a
`a`. La estabilidad de este reparto conserva el orden obtenido en los bits
anteriores.

Se necesitan `⌈log₂ n⌉` pasadas y cada una produce `O(n)` instrucciones,
por lo que la complejidad es `O(n·log n)` operaciones Push_swap, con `O(1)`
espacio auxiliar durante la ordenación. Su rendimiento no depende del número
inicial de inversiones, lo que lo hace apropiado para entradas muy
desordenadas.

### Adaptive: selección según el desorden

El modo predeterminado calcula el desorden antes de mover ningún elemento y
aplica estos umbrales:

| Desorden inicial | Estrategia elegida | Complejidad esperada en operaciones |
|---|---|---|
| `< 0.2` | Selection sort adaptado | `O(n²)` en el peor caso |
| `[0.2, 0.5)` | Chunk sort | `O(n·√n)` objetivo; `O(n²)` peor caso |
| `>= 0.5` | Radix sort LSD | `O(n·log n)` |

El umbral `0.2` reserva selection sort para entradas con pocas inversiones,
donde suele necesitar pocas rotaciones pese a su cota cuadrática. El valor
`0.5` coincide con el desorden esperado de una permutación aleatoria: en
promedio, la mitad de sus pares están invertidos. A partir de ahí se elige
radix, cuya cantidad de pasadas depende de los bits de `n` y no del orden
inicial.

El coste en operaciones del modo adaptativo es el de la estrategia elegida. La
selección previa requiere `O(n²)` comparaciones internas para medir el desorden,
pero no emite instrucciones Push_swap.

## Complejidad espacial

Las estrategias trabajan directamente sobre las dos listas doblemente
enlazadas y no reservan memoria proporcional a `n` durante la ordenación, por
lo que usan `O(1)` espacio auxiliar en esa fase. La preparación inicial sí usa
`O(n)` memoria para tokenizar, validar, indexar los argumentos y construir el
stack `a`.

## Estructura del proyecto

```text
.
├── main.c                 # entrada, selección y ejecución de estrategia
├── ft_bench.c             # contadores e informe de operaciones
├── parsing/               # flags, tokenización y validación
├── sort/                  # algoritmos y utilidades de ordenación
├── stack/                 # implementación de las 11 operaciones
├── include/               # libft y cabeceras asociadas
├── push_swap.h            # tipos y prototipos del proyecto
└── Makefile
```

## Recursos

- [Inversion (discrete mathematics)](https://en.wikipedia.org/wiki/Inversion_(discrete_mathematics)):
  definición de inversiones usada para calcular el desorden.
- [Selection sort](https://en.wikipedia.org/wiki/Selection_sort): base del
  algoritmo simple, adaptada aquí a las operaciones de dos stacks.
- [Radix sort](https://en.wikipedia.org/wiki/Radix_sort): fundamentos del
  procesamiento estable por dígitos o bits.
- [Big O notation](https://en.wikipedia.org/wiki/Big_O_notation): referencia
  para expresar y comparar las cotas de complejidad.
- Peer2peer con compañeros estudiantes.

### Uso de inteligencia artificial

Se ha utilizado IA generativa como apoyo para estructurar y redactar este
README, convertir las reglas del subject en explicaciones accesibles y
contrastar los ejemplos, flags y descripciones algorítmicas con el código del
repositorio. La revisión de la implementación, la validación de su
comportamiento y la responsabilidad sobre el contenido final corresponden a
los autores.

## Contribuciones

El proyecto se ha desarrollado conjuntamente por `crubio-p` y `aarellan`, con
trabajo compartido en la estructura de stacks, el parsing, las operaciones, la
integración de algoritmos, el benchmark, las pruebas y la documentación.

Concretamente, hemos separado el desarrollo del proyecto en dos secciones muy diferenciadas:

- `aarellan`: toda la parte del parseo, lectura de argumentos, inicialización de los stacks.
- `crubio-p`: la implementación de los algoritmos de ordenación.

Y los demás puntos se han hecho en común.
