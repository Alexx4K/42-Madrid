/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_split.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aarellan <aarellan@student.42madrid.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/06 14:26:31 by aarellan         #+#    #+#             */
/*   Updated: 2026/06/06 14:26:45 by aarellan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static int	count_words(char const *str, char c)
{
	int	i;
	int	words;

	i = 0;
	words = 0;
	while (str[i] != '\0')
	{
		while (str[i] == c)
			i++;
		if (str[i] != '\0')
		{
			words++;
			while (str[i] && str[i] != c)
				i++;
		}
	}
	return (words);
}

static int	len_word_array(char const *str, char c)
{
	int	i;

	i = 0;
	while (str[i] != '\0' && str[i] != c)
		i++;
	return (i);
}

static void	free_mem(char **s, int i)
{
	while (i >= 0)
	{
		free(s[i]);
		i--;
	}
	free(s);
}

static int	create_words(char **array, const char *str, char c)
{
	int	i;
	int	j;
	int	len;

	i = 0;
	j = 0;
	while (str[i] != '\0')
	{
		while (str[i] == c)
			i++;
		if (str[i] != '\0')
		{
			len = len_word_array(str + i, c);
			array[j] = ft_substr(str, i, len);
			if (array[j] == NULL)
			{
				free_mem(array, j - 1);
				return (0);
			}
			i = i + len;
			j++;
		}
	}
	array[j] = NULL;
	return (1);
}

char	**ft_split(char const *s, char c)
{
	char	**array;

	if (!s)
		return (NULL);
	array = malloc((count_words(s, c) + 1) * sizeof(char *));
	if (!array)
		return (NULL);
	if (!create_words(array, s, c))
		return (NULL);
	return (array);
}
