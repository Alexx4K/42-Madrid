/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strtrim.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aarellan <aarellan@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/26 18:26:22 by aarellan          #+#    #+#             */
/*   Updated: 2026/05/26 18:41:56 by aarellan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*
	removes the characters in 'set' from the beginning and end of 's1'
	It returns a new string with the characters removed.
*/
char	*ft_strtrim(char const *s1, char const *set)
{
	size_t	start;
	size_t	end;
	char	*str;

	str = 0;
	if (s1 != 0 && set != 0)
	{
		start = 0;
		end = ft_strlen(s1);
		while (s1[start] && ft_strchr(set, s1[start]))
			start++;
		while (end > start && ft_strchr(set, s1[end - 1]))
			end--;
		str = (char *)malloc(sizeof(char) * (end - start + 1));
		if (str)
			ft_strlcpy(str, &s1[start], end - start + 1);
	}
	return (str);
}

/*
#include <stdio.h>

int	main(void)
{
	char *res;

	res = ft_strtrim("  hello world  ", " ");
	printf("Test 1: '  hello world  ' trim ' ' -> '%s'\n", res);
	free(res);
	res = ft_strtrim("123hello123", "123");
	printf("Test 2: '123hello123' trim '123' -> '%s'\n", res);
	free(res);
	res = ft_strtrim("   ", " ");
	printf("Test 3: '   ' trim ' ' -> '%s'\n", res);
	free(res);
	return (0);
}
*/
