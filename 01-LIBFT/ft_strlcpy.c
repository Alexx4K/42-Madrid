/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strlcpy.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aarellan <aarellan@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/25 12:35:16 by aarellan          #+#    #+#             */
/*   Updated: 2026/05/25 15:13:18 by aarellan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*
	This function copies a string to a buffer
*/
size_t	ft_strlcpy(char *dst, const char *src, size_t dstsize)
{
	size_t	i;
	size_t	len;

	len = ft_strlen(src);
	if (dstsize < 1)
		return (len);
	i = 0;
	while (src[i] != '\0' && i < (dstsize - 1))
	{
		dst[i] = src[i];
		i++;
	}
	dst[i] = '\0';
	return (len);
}

/*
#include <stdio.h>
#include <string.h>

int	main(void)
{
	char dest[10];

	printf("'Hey'sz 10-> %zu, dest: %s\n", ft_strlcpy(dest, "Hey", 10), dest);
	printf("'World'sz 3> %zu, dest: %s\n", ft_strlcpy(dest, "World", 3), dest);
	printf("'42' (sz 0-> %zu\n", ft_strlcpy(dest, "42", 0));
	return (0);
}
*/
