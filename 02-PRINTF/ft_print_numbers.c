/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_print_numbers.c                                 :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aarellan <aarellan@student.42madrid.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/06 14:26:31 by aarellan         #+#    #+#             */
/*   Updated: 2026/06/06 14:26:45 by aarellan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

/*
** Prints a memory address in hexadecimal format.
** Metaphor: Like taking a picture of a house's GPS coordinates.
*/
int	print_pointer(void *ptr)
{
	int				len;
	unsigned long	new_ptr;

	len = 0;
	new_ptr = (unsigned long)ptr;
	if (new_ptr == 0)
	{
		write(1, "(nil)", 5);
		len = 5;
	}
	else
	{
		write(1, "0x", 2);
		len = 2 + print_hexapointer(new_ptr);
	}
	return (len);
}

/*
** Prints a signed integer using ft_itoa.
** Metaphor: Like writing down the balance 
   of a bank account, which could be negative.
*/
int	print_number(int nbr)
{
	int		len;
	char	*s;

	s = ft_itoa(nbr);
	len = print_string(s);
	free(s);
	return (len);
}

/*
** Prints an unsigned integer (always positive).
** Metaphor: Like counting steps taken; you can't walk negative steps.
*/
int	print_unsigned(unsigned int nbr)
{
	char	c;
	int		len;

	len = ft_unsignedintlen(nbr);
	if (nbr >= 10)
		print_unsigned(nbr / 10);
	c = (nbr % 10) + '0';
	write(1, &c, 1);
	return (len);
}

/*
** Prints a number in lowercase hexadecimal format.
** Metaphor: Like translating a
  number into an alien language that uses 16 symbols.
*/
int	print_hexalower(unsigned int nbr)
{
	char	word;
	int		len;

	len = 0;
	if (nbr >= 16)
		len = len + print_hexalower(nbr / 16);
	word = ft_hexalowercase(nbr % 16);
	write(1, &word, 1);
	len++;
	return (len);
}

/*
** Prints a number in uppercase hexadecimal format.
** Metaphor: Same alien language but shouting in CAPITAL letters.
*/
int	print_hexaupper(unsigned int nbr)
{
	char	word;
	int		len;

	len = 0;
	if (nbr >= 16)
		len = len + print_hexaupper(nbr / 16);
	word = ft_hexauppercase(nbr % 16);
	write(1, &word, 1);
	len++;
	return (len);
}

/*
int	main(void)
{
	int a = 42;
	ft_printf("Pointer: %p\n", &a);
	ft_printf("Unsigned: %u\n", 4294967295U);
	ft_printf("Hex: %x %X\n", 255, 255);
}
*/
