/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memcmp.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aarellan <aarellan@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/25 18:23:22 by aarellan          #+#    #+#             */
/*   Updated: 2026/05/25 19:17:06 by aarellan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*
	This function compares two strings.
*/
int	ft_memcmp(const void *s1, const void *s2, size_t n)
{
	size_t				i;
	unsigned const char	*str1;
	unsigned const char	*str2;

	i = 0;
	str1 = (unsigned const char *)s1;
	str2 = (unsigned const char *)s2;
	while (i < n)
	{
		if (*str1 != *str2)
			return ((int)(*str1 - *str2));
		str1++;
		str2++;
		i++;
	}
	return (0);
}

/*
#include <stdio.h>
#include <string.h>

int	main(void)
{
	printf(" 'abc' vs 'abc' (3 bytes) -> %d\n", ft_memcmp("abc", "abc", 3));
	printf(" 'abc' vs 'abd' (3 bytes) -> %d\n", ft_memcmp("abc", "abd", 3));
	printf("'abc' vs 'abd' (2 bytes) -> %d\n", ft_memcmp("abc", "abd", 2));
	return (0);
}
*/
