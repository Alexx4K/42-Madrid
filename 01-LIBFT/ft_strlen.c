/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strlen.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aarellan <aarellan@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/19 18:29:00 by aarellan          #+#    #+#             */
/*   Updated: 2026/05/25 15:21:04 by aarellan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*
	This function counts the length of a string.
*/
size_t	ft_strlen(const char *str)
{
	size_t	i;

	i = 0;
	while (str[i])
		i++;
	return (i);
}

/*
#include <stdio.h>
#include <string.h>

int	main(void)
{
	printf("Test 1: 'Hello' -> %zu\n", ft_strlen("Hello"));
	printf("Test 2: '' -> %zu\n", ft_strlen(""));
	printf("Test 3: '42' -> %zu\n", ft_strlen("42"));
	return (0);
}
*/
