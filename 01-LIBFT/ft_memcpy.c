/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memcpy.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aarellan <aarellan@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/23 16:30:57 by aarellan          #+#    #+#             */
/*   Updated: 2026/05/25 17:22:06 by aarellan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*
	This function copies a string.
*/
void	*ft_memcpy(void *dest, const void *src, size_t n)
{
	size_t	i;
	char	*str;
	char	*pun;

	if (!dest && !src)
		return (NULL);
	i = 0;
	str = (char *)src;
	pun = (char *)dest;
	while (i < n)
	{
		pun[i] = str[i];
		i++;
	}
	return (dest);
}

/*
#include <stdio.h>
#include <string.h>

int	main(void)
{
	char src[] = "Hello";
	char dest[10];

	ft_memcpy(dest, src, 6);
	printf("Test 1: Copy 'Hello' -> %s\n", dest);
	ft_memcpy(dest, "World", 3);
	dest[3] = '\0';
	printf("Test 2: Copy 'Wor' -> %s\n", dest);
	printf("Test 3: NULL src/dest handled: %p\n", ft_memcpy(NULL, NULL, 5));
	return (0);
}
*/
