/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstsize.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aarellan <aarellan@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/26 23:17:10 by aarellan          #+#    #+#             */
/*   Updated: 2026/05/26 23:17:10 by aarellan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*
	This function counts the number of nodes in a list.
	Like counting the number of wagons in a train.
*/
int	ft_lstsize(t_list *lst)
{
	int	i;

	i = 0;
	while (lst)
	{
		lst = lst->next;
		i++;
	}
	return (i);
}

/*
#include <stdio.h>

int	main(void)
{
	t_list	*list = ft_lstnew("one");
	ft_lstadd_back(&list, ft_lstnew("two"));
	ft_lstadd_back(&list, ft_lstnew("three"));

	printf("Test 1: Size of 3: %d\n", ft_lstsize(list));
	printf("Test 2: Size of NULL: %d\n", ft_lstsize(NULL));
	t_list *one = ft_lstnew("only");
	printf("Test 3: Size of 1: %d\n", ft_lstsize(one));
	return (0);
}
*/
