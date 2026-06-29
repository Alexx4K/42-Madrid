/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strmapi.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aarellan <aarellan@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/26 22:49:58 by aarellan          #+#    #+#             */
/*   Updated: 2026/05/26 22:49:58 by aarellan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*
	it applies a function to each character of the string.
*/
char	*ft_strmapi(char *s, char (*f)(unsigned int, char))
{
	int		i;
	char	*str;
	int		len;

	i = 0;
	if (!s || !f)
		return (NULL);
	len = ft_strlen(s);
	str = malloc(sizeof(char) * (len + 1));
	if (!str)
		return (NULL);
	while (i < len)
	{
		str[i] = f(i, s[i]);
		i++;
	}
	str[len] = '\0';
	return (str);
}

/*
#include <stdio.h>

char	mapi_f(unsigned int i, char c)
{
	if (i % 2 == 0)
		return (c - 32);
	return (c);
}

int	main(void)
{
	char *res;

	res = ft_strmapi("hello", mapi_f);
	printf("Test 1: 'hello' -> %s\n", res);
	free(res);
	res = ft_strmapi("", mapi_f);
	printf("Test 2: '' -> '%s'\n", res);
	free(res);
	printf("Test 3: NULL string -> %p\n", ft_strmapi(NULL, mapi_f));
	return (0);
}
*/
