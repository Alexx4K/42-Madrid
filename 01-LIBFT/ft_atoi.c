/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_atoi.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aarellan <aarellan@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/26 12:04:51 by aarellan          #+#    #+#             */
/*   Updated: 2026/05/26 12:31:55 by aarellan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*
	This function converts a string to an integer.
	It skips all whitespace characters at the beginning of the string.
	It then checks for a sign character ('-' or '+').
	Finally, it converts the digits to an integer.
*/
int	ft_atoi(const char *str)
{
	int	result;
	int	sign;

	result = 0;
	sign = 1;
	if (*str)
	{
		while (*str == 32 || (*str >= 9 && *str <= 13))
			str++;
		if (*str == '-' || *str == '+')
		{
			if (*str == '-')
				sign = sign * (-1);
			str++;
		}
		while (*str >= '0' && *str <= '9')
		{
			result = result * 10 + *str - '0';
			str ++;
		}
		return (result * sign);
	}
	return (0);
}

/*
#include <stdio.h>
#include <stdlib.h>

int	main(void)
{
	printf("Test 1: '42' -> %d\n", ft_atoi("42"));
	printf("Test 2: '   -123' -> %d\n", ft_atoi("   -123"));
	printf("Test 3: '2147483647' -> %d\n", ft_atoi("2147483647"));
	return (0);
}
*/
