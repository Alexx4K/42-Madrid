/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strnstr.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aarellan <aarellan@student.42madrid.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/06 14:26:31 by aarellan         #+#    #+#             */
/*   Updated: 2026/06/06 14:26:45 by aarellan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strnstr(const char *big, const char *little, size_t len)
{
	size_t	i;
	size_t	j;

	if (little[0] == '\0')
		return ((char *)big);
	if (big[0] == '\0')
		return (0);
	i = 0;
	while (big[i] != '\0' && i < len)
	{
		if (big[i] == little[0])
		{
			j = 0;
			while (big[i + j] == little[j] && little[j] != '\0'
				&& (i + j) < len)
				j++;
			if (little[j] == '\0')
				return ((char *)big + i);
		}
		i++;
	}
	return (0);
}
