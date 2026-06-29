/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_print_words.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aarellan <aarellan@student.42madrid.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/06 14:26:31 by aarellan         #+#    #+#             */
/*   Updated: 2026/06/06 14:26:45 by aarellan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

/*
** Prints a single character.
** Metaphor: Like picking up a single lego piece and placing it on a board.
*/
int	print_character(char c)
{
	ft_putchar_fd(c, 1);
	return (1);
}

/*
** Prints a string of characters.
** Metaphor: Like taking a string
 of lego pieces already connected and placing them.
*/
int	print_string(char *str)
{
	if (!str)
	{
		ft_putstr_fd("(null)", 1);
		return (6);
	}
	ft_putstr_fd(str, 1);
	return (ft_strlen(str));
}

/*
int	main(void)
{
	ft_printf("Char: %c\n", 'z');
	ft_printf("String: %s\n", "Testing strings");
	ft_printf("NULL: %s\n", (char *)0);
}
*/
