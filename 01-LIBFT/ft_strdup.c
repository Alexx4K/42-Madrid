/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strdup.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aarellan <aarellan@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/20 17:54:25 by aarellan          #+#    #+#             */
/*   Updated: 2026/05/26 15:00:59 by aarellan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*
	This function duplicates a string.
*/
char	*ft_strdup(const char *src)
{
	int		i;
	char	*dest;

	i = 0;
	while (src[i])
		i++;
	dest = malloc((i + 1) * sizeof(char));
	if (!dest)
		return (NULL);
	i = 0;
	while (src[i])
	{
		dest[i] = src[i];
		i++;
	}
	dest[i] = '\0';
	return (dest);
}

/*
#include <stdio.h>

int	main(void)
{
	char *dup;

	dup = ft_strdup("Hello World");
	printf("Test 1: 'Hello World' -> %s\n", dup);
	free(dup);
	dup = ft_strdup("");
	printf("Test 2: '' -> '%s'\n", dup);
	free(dup);
	dup = ft_strdup("42");
	printf("Test 3: '42' -> %s\n", dup);
	free(dup);
	return (0);
}
*/
