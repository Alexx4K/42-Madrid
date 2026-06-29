/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_substr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aarellan <aarellan@student.42madrid.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/06 14:26:31 by aarellan         #+#    #+#             */
/*   Updated: 2026/06/06 14:26:45 by aarellan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_substr(char const *s, unsigned int start, size_t len)
{
	size_t	i;
	char	*str;

	if (!s)
		return (NULL);
	if (start + len > ft_strlen(s))
		len = ft_strlen(s) - start;
	if (start >= ft_strlen(s))
		return (ft_calloc(1, 1));
	i = 0;
	str = malloc(len + 1);
	if (!str)
		return (NULL);
	while (i < len)
	{
		str[i] = s[i + start];
		i++;
	}
	return (str[i] = '\0', str);
}
