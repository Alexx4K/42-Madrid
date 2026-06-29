/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strncmp.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aarellan <aarellan@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/19 18:34:50 by aarellan          #+#    #+#             */
/*   Updated: 2026/05/25 17:50:53 by aarellan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*
	compares two strings, while it doesn't find the same character, 
	it returns the difference between the two characters.
	If the strings are equal, it returns 0.
*/
int	ft_strncmp(const char *s1, const char *s2, size_t n)
{
	size_t	i;

	i = 0;
	while (i < n && (s1[i] || s2[i]))
	{
		if (s1[i] != s2[i])
			return ((unsigned char)s1[i] - (unsigned char)s2[i]);
		else if (s1[i] == '\0')
			return (0);
		i++;
	}
	return (0);
}

/*
#include <stdio.h>
#include <string.h>

int	main(void)
{
	printf("'abc' vs 'abd' (n=2) -> %d\n", ft_strncmp("abc", "abd", 2));
	printf("'abc' vs 'abd' (n=3) -> %d\n", ft_strncmp("abc", "abd", 3));
	printf("'test' vs 'test' (n=10) -> %d\n", ft_strncmp("test", "test", 10));
	return (0);
}
*/
