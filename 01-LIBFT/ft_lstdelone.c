/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstdelone.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aarellan <aarellan@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/26 23:22:59 by aarellan          #+#    #+#             */
/*   Updated: 2026/05/26 23:22:59 by aarellan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*
	This function deletes a node.
	Like explode a wagon from a train.
*/
void	ft_lstdelone(t_list *lst, void (*del)(void *))
{
	if (!lst || !del)
		return ;
	(del)(lst->content);
	free(lst);
}

/*
#include <stdio.h>

void	del_content(void *content)
{
	(void)content;
}

int	main(void)
{
	t_list	*elem = ft_lstnew("content");

	printf("Test 1: Deleting element: %p\n", elem);
	ft_lstdelone(elem, del_content);
	printf("Test 2: Element deleted (manual verification)\n");
	ft_lstdelone(NULL, del_content);
	printf("Test 3: Deleting NULL element handled\n");
	return (0);
}
*/
