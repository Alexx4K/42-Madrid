/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_isascii.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aarellan <aarellan@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/23 15:30:04 by aarellan          #+#    #+#             */
/*   Updated: 2026/05/23 15:33:50 by aarellan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

int	ft_isascii(int c)
{
	if (c >= 0 && c <= 127)
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
	printf("Test 1: 65 ('A') -> %d\n", ft_isascii(65));
	printf("Test 2: 127 -> %d\n", ft_isascii(127));
	printf("Test 3: 128 -> %d\n", ft_isascii(128));
	return (0);
}
*/
