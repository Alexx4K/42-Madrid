/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_isdigit.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aarellan <aarellan@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/23 15:06:30 by aarellan          #+#    #+#             */
/*   Updated: 2026/05/23 15:10:06 by aarellan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

int	ft_isdigit(int n)
{
	if (n >= '0' && n <= '9')
	{
		return (1);
	}
	return (0);
}

/*
#include <stdio.h>
#include <ctype.h>

int	main(void)
{
	printf("Test 1: '1' -> %d\n", ft_isdigit('1'));
	printf("Test 2: 'a' -> %d\n", ft_isdigit('a'));
	printf("Test 3: '0' -> %d\n", ft_isdigit('0'));
	return (0);
}
*/
