/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_iterative_factorial.c                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aarellan <aarellan@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/19 14:31:59 by aarellan          #+#    #+#             */
/*   Updated: 2026/05/22 19:40:46 by aarellan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

int	ft_iterative_factorial(int nb)
{
	int	result;

	result = 1;
	if ((nb < 0) || (nb > 12))
		return (0);
	while (nb > 1)
	{
		result = nb * result;
		nb--;
	}
	return (result);
}
