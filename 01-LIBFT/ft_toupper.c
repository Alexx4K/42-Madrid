/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_toupper.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aarellan <aarellan@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/25 13:04:01 by aarellan          #+#    #+#             */
/*   Updated: 2026/05/25 13:12:43 by aarellan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

int	ft_toupper(int c)
{
	if (c >= 'a' && c <= 'z')
		return (c - 32);
	return (c);
}

/*
#include <stdio.h>
#include <ctype.h>

int	main(void)
{
	printf("Test 1: 'a' -> %c\n", ft_toupper('a'));
	printf("Test 2: 'Z' -> %c\n", ft_toupper('Z'));
	printf("Test 3: '1' -> %c\n", ft_toupper('1'));
	return (0);
}
*/
