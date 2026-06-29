/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstnew.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aarellan <aarellan@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/26 23:09:50 by aarellan          #+#    #+#             */
/*   Updated: 2026/05/26 23:09:50 by aarellan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*
	This function creates a new node.
	Like a new wagon for a train.
*/
t_list	*ft_lstnew(void *content)
{
	t_list	*list;

	list = malloc(sizeof(t_list));
	if (!list)
		return (NULL);
	list->content = content;
	list->next = NULL;
	return (list);
}

/*
#include <stdio.h>

int	main(void)
{
	t_list	*elem;

	elem = ft_lstnew("hello");
	printf("Test 1: Content: %s\n", (char *)elem->content);
	printf("Test 2: Next: %p\n", elem->next);
	elem = ft_lstnew(NULL);
	printf("Test 3: NULL content: %p\n", elem->content);
	return (0);
}
*/
