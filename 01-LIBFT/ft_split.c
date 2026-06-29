/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   test.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aarellan <aarellan@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/26 20:25:09 by aarellan          #+#    #+#             */
/*   Updated: 2026/05/26 20:25:09 by aarellan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*
	This function counts the number of words in a string.
*/
static int	ft_cont_words(const char *s, char c)
{
	int	cont;
	int	i;

	cont = 0;
	i = 0;
	while (s[i])
	{
		if (s[i] != c && (i == 0 || s[i - 1] == c))
			cont++;
		i++;
	}
	return (cont);
}

/*
	This function frees the memory of a string array.
*/
static void	*ft_free(char **mem, size_t aux)
{
	size_t	i;

	i = 0;
	while (i < aux)
		free(mem[i]);
	free(mem);
	return (NULL);
}

/*
	This function splits a string into an array of strings.
*/
static void	ft_split_str(char **ptr, char *str, char c, int n)
{
	int		i;
	char	*start;

	i = 0;
	while (i < n)
	{
		while (*str && *str == c)
			str++;
		start = str;
		while (*str && *str != c)
			str++;
		ptr[i] = ft_substr(start, 0, str - start);
		if (!ptr[i])
		{
			ft_free(ptr, i);
			return ;
		}
		i++;
	}
}

/*
	This function does the same as split but it returns a string array.
*/
char	**ft_split(char const *s, char c)
{
	char	**ptr;
	int		n;

	if (!s)
		return (NULL);
	n = ft_cont_words(s, c);
	ptr = (char **)ft_calloc((n + 1), sizeof(char *));
	if (!ptr)
		return (NULL);
	ft_split_str(ptr, (char *)s, c, n);
	return (ptr);
}

/*
#include <stdio.h>

int	main(void)
{
	char **res;
	int i;

	printf("Test 1: 'hello world' split by ' '\n");
	res = ft_split("hello world", ' ');
	i = 0;
	while (res && res[i])
	{
		printf("res[%d]: %s\n", i, res[i]);
		free(res[i]);
		i++;
	}
	free(res);

	printf("Test 2: ',,,a,b,c,,,' split by ','\n");
	res = ft_split(",,,a,b,c,,,", ',');
	i = 0;
	while (res && res[i])
	{
		printf("res[%d]: %s\n", i, res[i]);
		free(res[i]);
		i++;
	}
	free(res);

	printf("Test 3: '' split by ' '\n");
	res = ft_split("", ' ');
	printf("res[0]: %p\n", res[0]);
	free(res);
	return (0);
}
*/
