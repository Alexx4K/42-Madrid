/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aarellan <aarellan@student.42madrid.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/06 14:26:31 by aarellan         #+#    #+#             */
/*   Updated: 2026/06/06 14:26:45 by aarellan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef FT_PRINTF_H
# define FT_PRINTF_H

# include "libft/libft.h"
# include <stdarg.h>
# include <stdint.h>

int		ft_printf(char const *format, ...);
int		print_character(char c);
int		print_string(char *str);
int		print_pointer(void *ptr);
int		print_number(int nbr);
int		ft_intlen(int nbr);
int		ft_unsignedintlen(unsigned int nbr);
int		print_unsigned(unsigned int nbr);
int		print_hexalower(unsigned int nbr);
int		print_hexaupper(unsigned int nbr);
char	ft_hexalowercase(unsigned int nbr);
char	ft_hexauppercase(unsigned int nbr);
int		print_hexapointer(unsigned long nbr);

#endif