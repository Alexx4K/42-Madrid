/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_striteri.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aarellan <aarellan@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/26 22:51:14 by aarellan          #+#    #+#             */
/*   Updated: 2026/05/26 22:51:14 by aarellan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*
function iterates through a string and applies a function to each character.
*/
void	ft_striteri(char *s, void (*f)(unsigned int, char*))
{
	int	i;

	if (!s || !f)
		return ;
	i = 0;
	while (s[i])
	{
		(*f)(i, &s[i]);
		i++;
	}
}

/*
#include <stdio.h>

void	iteri_f(unsigned int i, char *c)
{
	if (i % 2 == 0)
		*c = *c - 32;
}

int	main(void)
{
	char str[] = "hello world";

	printf("Test 1: 'hello world' -> ");
	ft_striteri(str, iteri_f);
	printf("%s\n", str);
	printf("Test 2: NULL string handled\n");
	ft_striteri(NULL, iteri_f);
	printf("Test 3: NULL function handled\n");
	ft_striteri(str, NULL);
	return (0);
}
*/
