*Este proyecto ha sido creado como parte del currículo de 42 por aarellan.*

# ft_printf

## Descripción
El proyecto **ft_printf** es una recreación de la famosa función `printf` de la biblioteca estándar de C (`stdio.h`). El objetivo principal es profundizar en el funcionamiento de las funciones variádicas en C, así como en la manipulación de diferentes tipos de datos (enteros, cadenas, caracteres, punteros y hexadecimales) para su salida por pantalla.

Este proyecto es fundamental en el currículo de 42, ya que proporciona una herramienta de depuración personalizada que se utilizará en proyectos futuros del cursus.

## Instrucciones

### Compilación
El proyecto incluye un `Makefile` compatible con los estándares de la escuela. Para compilar la biblioteca, simplemente ejecuta:

```bash
make
```

Esto generará el archivo `libftprintf.a`.

### Limpieza
Para eliminar los archivos objeto `.o`:
```bash
make clean
```

Para eliminar los objetos y la biblioteca final:
```bash
make fclean
```

Para recompilar todo desde cero:
```bash
make re
```

### Uso
Para utilizar esta biblioteca en tu propio proyecto, inclúyela en tu código y enlaza el archivo `.a` al compilar:

```c
#include "ft_printf.h"

int main() {
    ft_printf("Hola %s!\n", "Mundo");
    return 0;
}
```

```bash
gcc main.c libftprintf.a -o mi_programa
```

## Recursos

### Documentación y Referencias
- [Documentación oficial de printf (man printf)](https://linux.die.net/man/3/printf)
- [Variadic Functions in C - GeeksforGeeks](https://www.geeksforgeeks.org/variadic-functions-in-c/)
- [Tutorial sobre el manejo de va_list](https://www.learn-c.org)

### Uso de Inteligencia Artificial (IA)
En este proyecto se ha utilizado asistencia de IA para las siguientes tareas:

- **Documentación**: Añadir metáforas a los comentarios que hay sobre las funciones para facilitar la comprensión del código.
- **Estructuración del README**: Refinar la estructura del README para que sea más claro.

## Decisiones Técnicas y Algoritmos

### Algoritmo de Conversión (Recursividad)
Para la impresión de números (decimales, sin signo y hexadecimales), se ha optado por un **algoritmo recursivo**. Esta decisión se justifica por:
1.  **Simplicidad**: Permite procesar los dígitos de un número de izquierda a derecha de forma natural, aprovechando la pila de llamadas para el orden de impresión.
2.  **Mantenibilidad**: El código es mucho más corto y fácil de leer que un bucle iterativo que requiere el uso de buffers temporales o la inversión de cadenas.

### Estructura de Datos
El proyecto utiliza principalmente:
-   **va_list**: La estructura de datos fundamental para manejar una cantidad desconocida de argumentos. Es óptima para esta tarea ya que permite el acceso secuencial a los parámetros pasados a la función.
-   **Strings (char *)**: Utilizados para el manejo de los especificadores y el parseo de la cadena de formato.

### Robustez
El código ha sido verificado para manejar casos borde como:
-   Punteros `NULL` (mostrando `(nil)`).
-   Cadenas `NULL` (mostrando `(null)`).
-   Valores máximos y mínimos de enteros (`INT_MAX` e `INT_MIN`).
-   Símbolos de porcentaje consecutivos (`%%`).
