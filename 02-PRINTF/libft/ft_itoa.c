/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_itoa.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aarellan <aarellan@student.42madrid.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/06 14:26:31 by aarellan         #+#    #+#             */
/*   Updated: 2026/06/06 14:26:45 by aarellan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static int	ft_len_int(long n)
{
	int	len;

	len = 0;
	if (n == 0)
		return (1);
	if (n < 0)
	{
		n = -n;
		len++;
	}
	while (n > 0)
	{
		n = n / 10;
		len++;
	}
	return (len);
}

char	*ft_itoa(int n)
{
	char	*number;
	size_t	len;
	long	new_nb;

	new_nb = n;
	len = ft_len_int(new_nb);
	number = malloc(len + 1);
	if (number == 0)
		return (0);
	number[len] = '\0';
	if (new_nb == 0)
		number[0] = '0';
	if (new_nb < 0)
	{
		number[0] = '-';
		new_nb = -new_nb;
	}
	while (new_nb > 0)
	{
		len--;
		number[len] = new_nb % 10 + '0';
		new_nb = new_nb / 10;
	}
	return (number);
}
