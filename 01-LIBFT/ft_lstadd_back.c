/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstadd_back.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aarellan <aarellan@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/26 23:21:32 by aarellan          #+#    #+#             */
/*   Updated: 2026/05/26 23:21:32 by aarellan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*
	This function adds a new node to the end of a list.
	Like a new wagon to a train.
*/
void	ft_lstadd_back(t_list **lst, t_list *new)
{
	t_list	*tmp;

	if (!new || !lst)
		return ;
	if (!*lst)
	{
		*lst = new;
		return ;
	}
	tmp = ft_lstlast(*lst);
	tmp->next = new;
}

/*
#include <stdio.h>

int	main(void)
{
	t_list	*list = NULL;
	t_list	*elem1 = ft_lstnew("first");
	t_list	*elem2 = ft_lstnew("second");
	t_list	*elem3 = ft_lstnew("third");

	ft_lstadd_back(&list, elem1);
	printf("Test 1: %s\n", (char *)list->content);
	ft_lstadd_back(&list, elem2);
	printf("Test 2: %s\n", (char *)list->next->content);
	ft_lstadd_back(&list, elem3);
	printf("Test 3: %s\n", (char *)ft_lstlast(list)->content);
	return (0);
}
*/
