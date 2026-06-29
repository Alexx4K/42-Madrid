*This project has been created as part of the 42 curriculum by aarellan.*

# get_next_line

## Description

**get_next_line** is a 42 project whose objective is to implement a function capable of reading from a file descriptor and returning one line at a time.

The function reads from a file or standard input (`stdin`) and returns the next available line, including the newline character (`\n`) when present. When the end of the file is reached or an error occurs, the function returns `NULL`.

This project introduces several important concepts in C programming, including:

* Dynamic memory allocation.
* Static variables.
* Buffer management.
* Persistent state between function calls.
* Efficient file reading.

The bonus part has also been implemented, allowing the function to handle multiple file descriptors simultaneously while preserving the reading state of each one independently.

---

## Function Prototype

```c
char *get_next_line(int fd);
```

### Parameters

| Parameter | Description                  |
| --------- | ---------------------------- |
| `fd`      | File descriptor to read from |

### Return Value

| Situation       | Return                       |
| --------------- | ---------------------------- |
| Successful read | Next line read from the file |
| End of file     | `NULL`                       |
| Error           | `NULL`                       |

---

## Algorithm Explanation

The implementation is based on maintaining a static memory area that stores data read from the file but not yet returned to the user.

For each call to `get_next_line`, the following steps are performed:

1. Read data from the file descriptor using `read()`.
2. Append the newly read data to the stored content.
3. Search for a newline character (`\n`).
4. Extract the next complete line.
5. Save any remaining characters for future calls.
6. Return the extracted line.

This approach ensures that the function only reads as much as necessary while preserving unread data between calls.

### Example

Given the following file:

```text
Hello
World
42
```

Successive calls produce:

```c
get_next_line(fd); // "Hello\n"
get_next_line(fd); // "World\n"
get_next_line(fd); // "42"
get_next_line(fd); // NULL
```

---

## Bonus Part

The bonus implementation extends the mandatory functionality by supporting multiple file descriptors simultaneously.

Example:

```c
fd1 = open("file1.txt", O_RDONLY);
fd2 = open("file2.txt", O_RDONLY);

get_next_line(fd1);
get_next_line(fd2);
get_next_line(fd1);
get_next_line(fd2);
```

Each file descriptor maintains its own reading state, allowing independent and interleaved reads without losing track of the remaining content associated with each descriptor.

---

## Project Structure

### Mandatory Part

```text
get_next_line.c
get_next_line_utils.c
get_next_line.h
```

### Bonus Part

```text
get_next_line_bonus.c
get_next_line_utils_bonus.c
get_next_line_bonus.h
```

---

## Instructions

### Compilation

Mandatory version:

```bash
cc -Wall -Wextra -Werror -D BUFFER_SIZE=42 \
get_next_line.c get_next_line_utils.c main.c
```

Bonus version:

```bash
cc -Wall -Wextra -Werror -D BUFFER_SIZE=42 \
get_next_line_bonus.c get_next_line_utils_bonus.c main.c
```

### Changing BUFFER_SIZE

The buffer size can be configured at compile time:

```bash
cc -D BUFFER_SIZE=100 ...
```

### Example Usage

```c
#include "get_next_line.h"
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(void)
{
	int		fd;
	char	*line;

	fd = open("example.txt", O_RDONLY);
	if (fd < 0)
		return (1);
	while ((line = get_next_line(fd)))
	{
		printf("%s", line);
		free(line);
	}
	close(fd);
	return (0);
}
```

---

## Technical Decisions

### Defensa

Doy sorbos con read() del tamaño de BUFFER_SIZE, los pego cpn ft_strjoin() y voy guardando en un buffer estático hasta que encuentre un salto de línea. Cuando lo encuentro, extraigo la línea completa y devuelvo el resto para la siguiente llamada.
Uso static para evitar perder el contenido no leído entre llamadas a la función.(las sobras)
La única diferencia que tiene el bonus es que en vez de tener un buffer estático, tengo un array de buffers estáticos, uno por cada fd. De esta manera puedo leer de varios ficheros a la vez sin perder el contenido no leído de cada uno.

### Static Storage

A static variable is used to preserve unread data between function calls.

### Incremental Reading

Instead of loading the entire file into memory, the function reads chunks of size `BUFFER_SIZE` until a complete line is available.

### Dynamic Memory Management

Memory is allocated dynamically using `malloc()` and released when it is no longer needed, minimizing memory usage while avoiding leaks.

### Multiple File Descriptor Support

The bonus implementation maintains an independent storage area for each file descriptor, allowing simultaneous reading from multiple sources.

---

## Resources

### Documentation

* https://man7.org/linux/man-pages/man2/read.2.html
* https://man7.org/linux/man-pages/man3/malloc.3.html
* https://man7.org/linux/man-pages/man3/free.3p.html
* https://man7.org/linux/man-pages/man2/open.2.html
* https://www.geeksforgeeks.org/dynamic-memory-allocation-in-c-using-malloc-calloc-free-and-realloc/
* https://www.geeksforgeeks.org/static-variables-in-c/

### AI Usage

Artificial Intelligence was used as a supporting tool for:

* Clarifying concepts related to file descriptors and the `read()` system call.
* Reviewing documentation.
* Understanding memory management strategies.
* Improving the writing and structure of this README.

The project design, implementation, debugging, testing, and validation were carried out by the author.

---
