/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aarellan <aarellan@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/12 10:47:48 by aarellan          #+#    #+#             */
/*   Updated: 2026/06/28 13:58:42 by aarellan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"

/// @brief Standardized function to search the positions of the first '\n' 
/// beginning in 'i'.
/// @param str The string to search in.
/// @param i The first position where to look.
/// @return Position + 1 where the '\n' has been found.
size_t	find_line_ending(char *str, size_t i)
{
	while (str[i] && str[i] != '\n')
		i++;
	if (str[i] == '\n')
		i++;
	return (i);
}

/// @brief Given a string, creates a copy of everything but the first line of 
/// the string. So first it detects where the first line ends, and copies from
/// there.
/// @param str String given
/// @return A copy of the first line of 'str'
char	*get_string(char *str)
{
	char	*new_str;
	size_t	line_end;
	size_t	i;

	if (!str || str[0] == '\0')
		return (free_and_null(str, NULL));
	line_end = find_line_ending(str, 0);
	if (str[line_end] == '\0')
		return (free_and_null(str, NULL));
	new_str = ft_calloc(ft_strlen(str) - line_end + 1, sizeof(char));
	if (!new_str)
		return (free_and_null(str, NULL));
	i = 0;
	while (str[line_end])
		new_str[i++] = str[line_end++];
	free(str);
	return (new_str);
}

/// @brief Reads the first line from the 'str'.
/// @param str string to search in.
/// @return A copy of the first line of the 'str'.
char	*read_the_line(char *str)
{
	char	*line;
	size_t	line_end;
	size_t	i;

	line_end = 0;
	if (!str || str[0] == '\0')
		return (NULL);
	line_end = find_line_ending(str, line_end);
	line = (char *)ft_calloc(sizeof(char), line_end + 1);
	if (!line)
		return (NULL);
	i = 0;
	while (i < line_end)
	{
		line[i] = str[i];
		i++;
	}
	return (line);
}

/// @brief This function permits the release of to blocks of memory in one call.
/// @param buff1 One buffer
/// @param buff2 Other buffer
/// @return Returns 0 so the static variable can have a 
char	*free_and_null(char *buff1, char *buff2)
{
	if (buff1)
	{
		free(buff1);
		buff1 = NULL;
	}
	if (buff2)
	{
		free(buff2);
		buff2 = NULL;
	}
	return (NULL);
}

/// @brief Reads a line until the '\n'.
/// @param fd file descriptor from where to read.
/// @return The next line of fd.
char	*get_next_line(int fd)
{
	static char	*read_buffer;
	char		*read_content;
	int			read_bytes;

	read_bytes = 1;
	if ((fd < 0 || BUFFER_SIZE <= 0 || BUFFER_SIZE > INT_MAX))
		return (NULL);
	read_content = (char *)ft_calloc(sizeof(char), BUFFER_SIZE + 1);
	if (!read_content)
		return (read_buffer = free_and_null(read_buffer, NULL), NULL);
	while (!(ft_strchr(read_buffer, '\n')) && read_bytes != 0)
	{
		read_bytes = read(fd, read_content, BUFFER_SIZE);
		if (read_bytes == -1)
			return (read_buffer = free_and_null(read_content, read_buffer));
		read_content[read_bytes] = '\0';
		read_buffer = ft_strjoin(read_buffer, read_content);
		if (!read_buffer)
			return (free_and_null(read_content, NULL));
	}
	free(read_content);
	return (extract_line(&read_buffer));
}
