/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_substr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aarellan <aarellan@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/26 15:07:33 by aarellan          #+#    #+#             */
/*   Updated: 2026/05/26 17:50:57 by aarellan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*
	This function creates a substring from a string.
	It returns a new string with the characters from 'start' to 'start + len'.
*/
char	*ft_substr(char const *s, unsigned int start, size_t len)
{
	char	*str;
	size_t	i;
	size_t	slen;

	if (!s)
		return (NULL);
	slen = ft_strlen(s);
	if (start >= slen)
		return (ft_strdup(""));
	if (len > slen - start)
		len = slen - start;
	str = (char *)malloc(sizeof(char) * (len + 1));
	if (!str)
		return (NULL);
	i = 0;
	while (i < len && s[start + i])
	{
		str[i] = s[start + i];
		i++;
	}
	str[i] = '\0';
	return (str);
}

/*
#include <stdio.h>

int	main(void)
{
	char *res;

	res = ft_substr("hello world", 6, 5);
	printf("Test 1: 'hello world' [6, 5] -> %s\n", res);
	free(res);
	res = ft_substr("hello world", 0, 5);
	printf("Test 2: 'hello world' [0, 5] -> %s\n", res);
	free(res);
	res = ft_substr("hello world", 20, 5);
	printf("Test 3: 'hello world' [20, 5] -> '%s'\n", res);
	free(res);
	return (0);
}
*/
