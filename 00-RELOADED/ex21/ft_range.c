/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_range.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aarellan <aarellan@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/20 18:22:12 by aarellan          #+#    #+#             */
/*   Updated: 2026/05/22 14:59:36 by aarellan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdlib.h>

int	*ft_range(int min, int max)
{
	int	i;
	int	j;
	int	*rango;

	if (min < max)
	{
		rango = (int *)malloc(sizeof(int) * (max - min));
		i = 0;
		j = min;
		while (i < max - min)
		{
			rango[i] = j;
			j++;
			i++;
		}
		return (rango);
	}
	return (0);
}
