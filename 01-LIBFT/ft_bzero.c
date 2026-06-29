/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_bzero.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aarellan <aarellan@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/23 16:14:45 by aarellan          #+#    #+#             */
/*   Updated: 2026/05/23 16:19:13 by aarellan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*
	This function is like memset but it fills the memory with zeros.
*/
void	ft_bzero(void *s, size_t n)
{
	size_t	i;
	char	*j;

	i = 0;
	j = (char *)s;
	while (i < n)
	{
		j[i++] = 0;
	}
	s = (void *)j;
}

/*
#include <stdio.h>
#include <string.h>

int	main(void)
{
	char str1[10] = "Hello";
	char str2[10] = "World";
	char str3[10] = "Test";

	ft_bzero(str1, 2);
	printf("Test 1 (first 2 bytes zeroed): '%s' (hidden)\n", str1 + 2);
	ft_bzero(str2, 5);
	printf("Test 2 (full 5 bytes zeroed): '%s'\n", str2);
	ft_bzero(str3, 0);
	printf("Test 3 (0 bytes zeroed): '%s'\n", str3);
	return (0);
}
*/
