/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strchr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aarellan <aarellan@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/25 13:19:47 by aarellan          #+#    #+#             */
/*   Updated: 2026/05/25 13:24:13 by aarellan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*
	This function searches for a character in a string.
*/
char	*ft_strchr(const char *s, int c)
{
	char	a;

	a = (char)c;
	while (*s)
	{
		if (*s == a)
			return ((char *)s);
		s++;
	}
	if (a == '\0')
		return ((char *)s);
	return (0);
}

/*
#include <stdio.h>
#include <string.h>

int	main(void)
{
	char *str = "Hello World";

	printf("Test 1: Find 'W' in 'Hello World' -> %s\n", ft_strchr(str, 'W'));
	printf("Test 2: Find '\\0' in 'Hello' -> '%s'\n", ft_strchr(str, '\0'));
	printf("Test 3: Find 'z' in 'Hello' -> %s\n", ft_strchr(str, 'z'));
	return (0);
}
*/
