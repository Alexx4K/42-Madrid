/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   utils.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aarellan <aarellan@student.42madrid.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/06 14:26:31 by aarellan         #+#    #+#             */
/*   Updated: 2026/06/06 14:26:45 by aarellan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

/*
** Calculates the length of a signed integer.
** Metaphor: Like measuring the length
 of a line on a ruler, including the minus sign.
*/
int	ft_intlen(int nbr)
{
	int		len;
	long	num;

	len = 0;
	num = nbr;
	if (num == 0)
		return (1);
	if (num < 0)
	{
		num = -num;
		len++;
	}
	while (num > 0)
	{
		num = num / 10;
		len++;
	}
	return (len);
}

/*
** Calculates the length of an unsigned integer.
** Metaphor: Like counting the number of digits in a positive phone number.
*/
int	ft_unsignedintlen(unsigned int nbr)
{
	unsigned int	len;

	len = 0;
	if (nbr == 0)
		return (1);
	while (nbr > 0)
	{
		nbr = nbr / 10;
		len++;
	}
	return (len);
}

/*
** Returns the lowercase hex character for a value.
** Metaphor: Like a decoder ring that turns 10 into 'a' and 15 into 'f'.
*/
char	ft_hexalowercase(unsigned int nbr)
{
	char	*lower;

	lower = "0123456789abcdef";
	return (lower[nbr]);
}

/*
** Returns the uppercase hex character for a value.
** Metaphor: Same decoder ring but it screams in ALL CAPS.
*/
char	ft_hexauppercase(unsigned int nbr)
{
	char	*upper;

	upper = "0123456789ABCDEF";
	return (upper[nbr]);
}

/*
** Recursive function to print a pointer's hex address.
** Metaphor: Like a descending escalator where each step uncovers 
** another part of the secret code.
*/
int	print_hexapointer(unsigned long nbr)
{
	char	word;
	int		len;

	len = 0;
	if (nbr >= 16)
		len = len + print_hexapointer(nbr / 16);
	word = ft_hexalowercase(nbr % 16);
	write(1, &word, 1);
	len++;
	return (len);
}

/*
int	main(void)
{
	ft_printf("Int Len 42: %d\n", ft_intlen(42));
	ft_printf("Uint Len 42: %d\n", ft_unsignedintlen(42));
	ft_printf("Hex map for 15: %c\n", ft_hexauppercase(15));
}
*/
