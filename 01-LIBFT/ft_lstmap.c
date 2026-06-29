/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstmap.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aarellan <aarellan@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/26 23:25:23 by aarellan          #+#    #+#             */
/*   Updated: 2026/05/26 23:25:23 by aarellan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*
	creates a new list by applying a function to each node of a list.
	Like a factory that makes copies of wagons but with modifications.
*/
t_list	*ft_lstmap(t_list *lst, void *(*f)(void *), void (*del)(void *))
{
	t_list	*newlst;
	t_list	*node;

	if (!lst || !f || !del)
		return (NULL);
	newlst = NULL;
	node = NULL;
	while (lst)
	{
		if (!f)
			node = ft_lstnew(lst->content);
		else
			node = ft_lstnew(f(lst->content));
		if (!node)
		{
			ft_lstclear(&newlst, del);
			return (NULL);
		}
		ft_lstadd_back(&newlst, node);
		lst = lst->next;
	}
	return (newlst);
}

/*
#include <stdio.h>

void	*map_f(void *content)
{
	(void)content;
	return ("mapped");
}

void	del_c(void *content)
{
	(void)content;
}

int	main(void)
{
	t_list	*list = ft_lstnew("one");
	ft_lstadd_back(&list, ft_lstnew("two"));
	
	t_list *new = ft_lstmap(list, map_f, del_c);
	printf("Test 1: First elem of mapped: %s\n", (char *)new->content);
	printf("Test 2: Second elem of mapped: %s\n", (char *)new->next->content);
	printf("Test 3: Mapping NULL: %p\n", ft_lstmap(NULL, map_f, del_c));
	return (0);
}
*/
