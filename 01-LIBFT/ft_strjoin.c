/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strjoin.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aarellan <aarellan@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/26 17:58:00 by aarellan          #+#    #+#             */
/*   Updated: 2026/05/26 18:25:30 by aarellan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*
	This function is like a glue that sticks two strings together.
*/
char	*ft_strjoin(char const *s1, char const *s2)
{
	char	*str;
	int		i;
	int		j;

	if (!s1 || !s2)
		return (NULL);
	str = (char *)malloc(sizeof(char) * (ft_strlen(s1) + ft_strlen(s2) + 1));
	if (!str)
		return (NULL);
	i = 0;
	j = 0;
	while (s1[i])
	{
		str[i] = s1[i];
		i++;
	}
	while (s2[j])
	{
		str[i + j] = s2[j];
		j++;
	}
	str[i + j] = '\0';
	return (str);
}

/*
#include <stdio.h>

int	main(void)
{
	char *res;

	res = ft_strjoin("Hello ", "World");
	printf("Test 1: 'Hello ' + 'World' -> %s\n", res);
	free(res);
	res = ft_strjoin("", "42");
	printf("Test 2: '' + '42' -> %s\n", res);
	free(res);
	res = ft_strjoin("42", "");
	printf("Test 3: '42' + '' -> %s\n", res);
	free(res);
	return (0);
}
*/
