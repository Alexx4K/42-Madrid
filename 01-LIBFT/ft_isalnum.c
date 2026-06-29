/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_isalnum.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aarellan <aarellan@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/23 15:19:11 by aarellan          #+#    #+#             */
/*   Updated: 2026/05/23 15:29:03 by aarellan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

int	ft_isalnum(int c)
{
	return (ft_isalpha(c) || ft_isdigit(c));
}

/*
#include <stdio.h>
#include <ctype.h>

int	main(void)
{
	printf("Test 1: 'a' -> %d\n", ft_isalnum('a'));
	printf("Test 2: '1' -> %d\n", ft_isalnum('1'));
	printf("Test 3: '@' -> %d\n", ft_isalnum('@'));
	return (0);
}
*/
