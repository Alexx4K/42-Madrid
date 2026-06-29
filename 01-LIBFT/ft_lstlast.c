/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstlast.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aarellan <aarellan@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/26 23:20:32 by aarellan          #+#    #+#             */
/*   Updated: 2026/05/26 23:20:32 by aarellan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*
	This function returns the last node of a list.
	Like the last wagon of a train.
*/
t_list	*ft_lstlast(t_list *lst)
{
	if (!lst)
		return (NULL);
	while (lst != NULL && lst->next != NULL)
		lst = lst->next;
	return (lst);
}

/*
#include <stdio.h>

int	main(void)
{
	t_list	*list = ft_lstnew("first");
	ft_lstadd_back(&list, ft_lstnew("second"));
	ft_lstadd_back(&list, ft_lstnew("last"));
	printf("Test 1: Last elem: %s\n", (char *)ft_lstlast(list)->content);
	t_list *one = ft_lstnew("only");
	printf("Single elem list last: %s\n", (char *)ft_lstlast(one)->content);
	printf("Test 3: Empty list last: %p\n", ft_lstlast(NULL));
	return (0);
}
*/
