/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_tolower.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aarellan <aarellan@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/25 13:14:13 by aarellan          #+#    #+#             */
/*   Updated: 2026/05/25 13:15:34 by aarellan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

int	ft_tolower(int c)
{
	if (c >= 'A' && c <= 'Z')
		return (c + 32);
	return (c);
}

/*
#include <stdio.h>
#include <ctype.h>

int	main(void)
{
	printf("Test 1: 'A' -> %c\n", ft_tolower('A'));
	printf("Test 2: 'z' -> %c\n", ft_tolower('z'));
	printf("Test 3: '1' -> %c\n", ft_tolower('1'));
	return (0);
}
*/
