/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memmove.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aarellan <aarellan@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/25 11:57:54 by aarellan          #+#    #+#             */
/*   Updated: 2026/05/27 16:42:56 by aarellan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*
	This function is like memcpy but it can handle overlapping memory regions.
*/
void	*ft_memmove(void *dst, const void *src, size_t len)
{
	unsigned char	*d;
	unsigned char	*s;

	if (src == NULL && dst == NULL)
		return (NULL);
	d = (unsigned char *)dst;
	s = (unsigned char *)src;
	if (d > s)
	{
		while (len > 0)
		{
			len--;
			d[len] = s[len];
		}
	}
	else
		ft_memcpy(d, s, len);
	return (dst);
}

/*
#include <stdio.h>
#include <string.h>

int	main(void)
{
	char str1[] = "Hello World";
	char str2[] = "Hello World";

	ft_memmove(str1 + 2, str1, 5);
	printf("Test 1 (overlap dst > src): %s\n", str1);
	ft_memmove(str2, str2 + 2, 5);
	printf("Test 2 (overlap src > dst): %s\n", str2);
	char dest[10];
	ft_memmove(dest, "Test", 5);
	printf("Test 3 (no overlap): %s\n", dest);
	return (0);
}
*/
