/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memchr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aarellan <aarellan@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/25 17:53:55 by aarellan          #+#    #+#             */
/*   Updated: 2026/05/25 18:19:50 by aarellan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*
	This function searches for a character in a string.
	Like a detective searching for a clue in a crime scene.
*/
void	*ft_memchr(const void *s, int c, size_t n)
{
	size_t			i;
	unsigned char	*str;
	unsigned char	find;

	i = 0;
	str = (unsigned char *)s;
	find = (unsigned char)c;
	while (i < n)
	{
		if (str[i] == find)
			return (&str[i]);
		i++;
	}
	return (NULL);
}

/*
#include <stdio.h>
#include <string.h>

int	main(void)
{
	char str[] = "Hello World";
	printf("'W' in 'Hello World' -> %s\n", (char *)ft_memchr(str, 'W', 11));
	printf("o' in 'Hello' (first 4 bytes) -> %p\n", ft_memchr(str, 'o', 4));
	printf("'z' in 'Hello' -> %p\n", ft_memchr(str, 'z', 5));
	return (0);
}
*/
