/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_sqrt.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aarellan <aarellan@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/19 16:42:59 by aarellan          #+#    #+#             */
/*   Updated: 2026/05/22 20:13:04 by aarellan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

int	ft_sqrt(int nb)
{
	int	cont;

	cont = 1;
	while (cont <= nb / 2)
	{
		if (cont * cont == nb)
		{
			return (cont);
		}
		cont++;
	}
	return (0);
}
/*

int	main(void)
{
	ft_sqrt(25);
}*/
