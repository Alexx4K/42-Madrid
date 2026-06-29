/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstclear.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aarellan <aarellan@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/26 23:23:51 by aarellan          #+#    #+#             */
/*   Updated: 2026/05/26 23:23:51 by aarellan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*
	This function deletes a list.
	Like dynamite the entire train
*/
void	ft_lstclear(t_list **lst, void (*del)(void *))
{
	t_list	*tmp;

	if (!lst)
		return ;
	while (*lst)
	{
		tmp = (*lst)->next;
		ft_lstdelone(*lst, del);
		*lst = tmp;
	}
	*lst = NULL;
}

/*
#include <stdio.h>

void	del_content(void *content)
{
	(void)content;
}

int	main(void)
{
	t_list	*list = ft_lstnew("one");
	ft_lstadd_back(&list, ft_lstnew("two"));
	ft_lstadd_back(&list, ft_lstnew("three"));

	printf("Test 1: List size before clear: %d\n", ft_lstsize(list));
	ft_lstclear(&list, del_content);
	printf("Test 2: List after clear: %p\n", list);
	
	t_list *empty = NULL;
	ft_lstclear(&empty, del_content);
	printf("Test 3: Empty list clear: %p\n", empty);
	return (0);
}
*/
