/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memmove.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aarellan <aarellan@student.42madrid.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/06 14:26:31 by aarellan         #+#    #+#             */
/*   Updated: 2026/06/06 14:26:45 by aarellan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_memmove(void *dest, const void *src, size_t n)
{
	size_t				i;
	unsigned char		*dest1;
	const unsigned char	*src1;

	if (!dest && !src)
		return (NULL);
	dest1 = (unsigned char *)dest;
	src1 = (unsigned char *)src;
	if (src1 < dest1)
	{
		while (n--)
			dest1[n] = src1[n];
	}
	else
	{
		i = 0;
		while (i < n)
		{
			dest1[i] = src1[i];
			i++;
		}
	}
	return (dest);
}
