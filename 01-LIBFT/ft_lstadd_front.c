/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstadd_front.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aarellan <aarellan@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/26 23:16:01 by aarellan          #+#    #+#             */
/*   Updated: 2026/05/26 23:16:01 by aarellan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*
	This function adds a new node to the front of a list.
	Like a new wagon to the front of a train.
*/
void	ft_lstadd_front(t_list **lst, t_list *new)
{
	if (!new || !lst)
		return ;
	if (!*lst)
	{
		*lst = new;
		return ;
	}
	new->next = *lst;
	*lst = new;
}

/*
#include <stdio.h>

int	main(void)
{
	t_list	*list = NULL;
	t_list	*elem1 = ft_lstnew("third");
	t_list	*elem2 = ft_lstnew("second");
	t_list	*elem3 = ft_lstnew("first");

	ft_lstadd_front(&list, elem1);
	printf("Test 1: %s\n", (char *)list->content);
	ft_lstadd_front(&list, elem2);
	printf("Test 2: %s\n", (char *)list->content);
	ft_lstadd_front(&list, elem3);
	printf("Test 3: %s\n", (char *)list->content);
	return (0);
}
*/
