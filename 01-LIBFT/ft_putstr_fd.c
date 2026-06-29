/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putstr_fd.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aarellan <aarellan@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/26 23:04:39 by aarellan          #+#    #+#             */
/*   Updated: 2026/05/26 23:04:39 by aarellan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*
	This function prints a string to a file descriptor.
*/
void	ft_putstr_fd(char *s, int fd)
{
	if (!s)
		return ;
	while (*s != '\0')
	{
		ft_putchar_fd(*s, fd);
		s++;
	}
}

/*
int	main(void)
{
	ft_putstr_fd("Hello ", 1);
	ft_putstr_fd("World", 1);
	ft_putstr_fd("!", 1);
	ft_putchar_fd('\n', 1);
	return (0);
}
*/
