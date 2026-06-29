/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_isprint.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aarellan <aarellan@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/23 15:32:55 by aarellan          #+#    #+#             */
/*   Updated: 2026/05/25 13:59:39 by aarellan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

int	ft_isprint(int c)
{
	if (c >= 32 && c <= 126)
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
	printf("Test 1: 32 (space) -> %d\n", ft_isprint(32));
	printf("Test 2: 126 ('~') -> %d\n", ft_isprint(126));
	printf("Test 3: 31 (non-printable) -> %d\n", ft_isprint(31));
	return (0);
}
*/
