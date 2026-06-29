/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_ calloc.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aarellan <aarellan@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/26 12:35:25 by aarellan          #+#    #+#             */
/*   Updated: 2026/05/26 14:55:58 by aarellan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*
 function allocates is like malloc but clears the allocated memory to zero.
*/
void	*ft_calloc(size_t count, size_t size)
{
	void	*ptr;

	if (count != 0 && size > (size_t)-1 / count)
		return (NULL);
	ptr = malloc(count * size);
	if (!ptr)
		return (NULL);
	ft_bzero(ptr, size * count);
	return (ptr);
}

/*
#include <stdio.h>

int	main(void)
{
	int	*arr;
	size_t	i;

	arr = (int *)ft_calloc(5, sizeof(int));
	printf("Test 1 (5 ints): ");
	i = 0;
	while (i < 5)
		printf("%d ", arr[i++]);
	printf("\n");
	free(arr);

	arr = (int *)ft_calloc(0, sizeof(int));
	printf("Test 2 (0 ints): %p\n", arr);
	free(arr);

	arr = (int *)ft_calloc(1, 0);
	printf("Test 3 (size 0): %p\n", arr);
	free(arr);
	return (0);
}
*/
