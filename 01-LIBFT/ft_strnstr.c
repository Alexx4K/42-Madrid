/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strnstr.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aarellan <aarellan@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/25 19:23:30 by aarellan          #+#    #+#             */
/*   Updated: 2026/05/25 21:03:06 by aarellan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*
	This function searches for a string in another string, but it only 
	looks in the first 'len' characters of the string.
*/
char	*ft_strnstr(const char *big, const char *little, size_t len)
{
	size_t	i;
	size_t	j;

	i = 0;
	if (little[i] == '\0')
		return ((char *)big);
	if (len == 0)
		return (NULL);
	while (big[i] != '\0' && i < len)
	{
		j = 0;
		while ((i + j) < len && big[i + j] == little[j])
		{
			j++;
			if (little[j] == '\0')
				return ((char *)big + i);
		}
		i++;
	}
	return (0);
}

/*
#include <stdio.h>
#include <string.h>

int	main(void)
{
	char *big = "Hello World";
	printf("'World' in 'Hello World'n11-> %s\n", ft_strnstr(big, "World", 11));
	printf("'World' in 'Hello' (n=5) -> %p\n", ft_strnstr(big, "World", 5));
	printf("Test 3: Find '' in 'Hello' -> %s\n", ft_strnstr(big, "", 11));
	return (0);
}
*/
