/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line_utils.c                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aarellan <aarellan@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/19 13:10:44 by aarellan          #+#    #+#             */
/*   Updated: 2026/06/28 14:00:59 by aarellan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"

size_t	ft_strlen(const char *str)
{
	size_t	i;

	i = 0;
	if (!str)
		return (0);
	while (str[i])
		i++;
	return (i);
}

char	*ft_strchr(const char *str, int c)
{
	size_t	i;

	i = 0;
	if (!str)
		return (NULL);
	while (str[i])
	{
		if (str[i] == (char)c)
			return ((char *)&str[i]);
		i++;
	}
	if ((char)c == '\0')
		return ((char *)&str[i]);
	return (NULL);
}

char	*ft_strjoin(char *buffer, char *content)
{
	size_t	i;
	size_t	j;
	char	*result;

	i = 0;
	result = (char *)malloc(sizeof(char) * (ft_strlen(buffer)
				+ ft_strlen(content)) + 1);
	if (!result)
		return (free_and_null(buffer, NULL));
	while (buffer && buffer[i])
	{
		result[i] = buffer[i];
		i++;
	}
	j = 0;
	while (content && content[j])
		result[i++] = content[j++];
	result[i] = '\0';
	free(buffer);
	return (result);
}

char	*extract_line(char **buffer)
{
	char	*line;

	line = read_the_line(*buffer);
	if (!line)
	{
		*buffer = free_and_null(*buffer, NULL);
		return (NULL);
	}
	*buffer = get_string(*buffer);
	return (line);
}

void	*ft_calloc(size_t size, size_t nmemb)
{
	void			*ptr;
	unsigned char	*to_char;
	size_t			i;
	size_t			n_bytes;

	if (nmemb != 0 && size > (size_t) - 1 / nmemb)
		return (NULL);
	n_bytes = nmemb * size;
	ptr = malloc(n_bytes);
	if (!ptr)
		return (NULL);
	to_char = (unsigned char *) ptr;
	i = 0;
	while (i < n_bytes)
	{
		to_char[i] = '\0';
		i++;
	}
	return (ptr);
}
