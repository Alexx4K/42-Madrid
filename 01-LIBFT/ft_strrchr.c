/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strrchr.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aarellan <aarellan@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/25 13:27:16 by aarellan          #+#    #+#             */
/*   Updated: 2026/05/25 17:20:40 by aarellan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*
	This function searches for a character in a string, but it only 
	looks in the last 'len' characters of the string.
*/
char	*ft_strrchr(const char *s, int c)
{
	size_t	len;

	len = ft_strlen(s);
	while (len > 0)
	{
		if ((unsigned char)s[len] == (char)c)
			return ((char *)&s[len]);
		len--;
	}
	if (s[len] == (char)c)
		return ((char *)&s[len]);
	return (0);
}

/*
#include <stdio.h>
#include <string.h>

int	main(void)
{
	char *str = "Hello World";

	printf("last 'o' in 'Hello World' -> %s\n", ft_strrchr(str, 'o'));
	printf("last 'l' in 'Hello' -> %s\n", ft_strrchr(str, 'l'));
	printf("last 'z' in 'Hello' -> %p\n", ft_strrchr(str, 'z'));
	return (0);
}
*/
