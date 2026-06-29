*Este proyecto ha sido creado como parte del currículo de 42 por aarellan.*

# Libft - Tu propia biblioteca de C

## Descripción
**Libft** es el primer proyecto del currículo de 42. El objetivo es recrear un subconjunto de funciones de la biblioteca estándar de C (libc), así como otras funciones de utilidad que nos servirán en futuros proyectos. Este proyecto ayuda a entender profundamente cómo funcionan las funciones básicas de manipulación de memoria, cadenas de texto y listas en C.

La biblioteca está diseñada para ser compilada como un archivo `.a` (archivo estático), el cual puede ser enlazado a otros proyectos de C.

## Instrucciones

### Compilación
El proyecto incluye un `Makefile` con las reglas estándar exigidas:
- `make`: Compila los archivos fuente y genera la biblioteca `libft.a`.
- `make bonus`: Compila las funciones de listas (bonus) y las añade a la biblioteca.
- `make clean`: Elimina los archivos objetos (`.o`) generados.
- `make fclean`: Elimina los archivos objetos y el archivo de la biblioteca `libft.a`.
- `make re`: Realiza un `fclean` seguido de un `make` (recompilación completa).

### Uso
Para utilizar esta biblioteca en tus propios proyectos, incluye el encabezado en tus archivos de C:
```c
#include "libft.h"
```
Y compila tu proyecto enlazando la biblioteca:
```bash
gcc main.c -L. -lft
```

## Recursos
- [Man de C](https://linux.die.net/man/3/) - Documentación oficial de las funciones de la libc.
- [42 Madrid](https://www.42madrid.com/) - Información sobre el campus y su metodología.
- [FlowStack](https://flowstack.io/) - Plataforma de aprendizaje de programación.

### Uso de IA
En este proyecto se ha utilizado IA para las siguientes tareas:
- **Creación de casos de prueba**: Generación de funciones `main` con diferentes intentos de romper el código.
- **Estructuración del README**: Organización parcial de la documentación del proyecto.

## Detalle de la librería

### Funciones de Libc
- `ft_isalpha`, `ft_isdigit`, `ft_isalnum`, `ft_isascii`, `ft_isprint`: Pruebas de tipo de carácter.
- `ft_strlen`, `ft_memset`, `ft_bzero`, `ft_memcpy`, `ft_memmove`, `ft_strlcpy`, `ft_strlcat`: Manipulación de memoria y cadenas.
- `ft_toupper`, `ft_tolower`: Conversión de mayúsculas/minúsculas.
- `ft_strchr`, `ft_strrchr`, `ft_strncmp`, `ft_memchr`, `ft_memcmp`, `ft_strnstr`: Búsqueda y comparación.
- `ft_atoi`, `ft_calloc`, `ft_strdup`: Conversión y gestión de memoria.

### Funciones adicionales
- `ft_substr`, `ft_strjoin`, `ft_strtrim`, `ft_split`, `ft_itoa`: Manipulación avanzada de cadenas.
- `ft_strmapi`, `ft_striteri`: Aplicación de funciones a cadenas.
- `ft_putchar_fd`, `ft_putstr_fd`, `ft_putendl_fd`, `ft_putnbr_fd`: Salida de datos a descriptores de archivo.

### Funciones de Listas (Bonus)
- `ft_lstnew`, `ft_lstadd_front`, `ft_lstsize`, `ft_lstlast`, `ft_lstadd_back`: Gestión de nodos y listas enlazadas.
- `ft_lstdelone`, `ft_lstclear`, `ft_lstiter`, `ft_lstmap`: Manipulación y limpieza de listas.
