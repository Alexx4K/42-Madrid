/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memset.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aarellan <aarellan@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/23 15:35:49 by aarellan          #+#    #+#             */
/*   Updated: 2026/05/23 16:03:03 by aarellan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*
	This function sets a character to a string.
*/
void	*ft_memset(void *dest, int c, size_t count)
{
	size_t	i;
	char	*j;

	i = 0;
	j = (char *)dest;
	while (i < count)
	{
		j[i++] = ((char)c);
	}
	dest = (void *)j;
	return (dest);
}

/*
#include <stdio.h>
#include <string.h>

int	main(void)
{
	char str[10] = "Hello";

	ft_memset(str, 'A', 3);
	printf("Test 1: Set 3 'A's -> %s\n", str);
	ft_memset(str, 'B', 5);
	printf("Test 2: Set 5 'B's -> %s\n", str);
	ft_memset(str, 'C', 0);
	printf("Test 3: Set 0 'C's -> %s\n", str);
	return (0);
}
*/
