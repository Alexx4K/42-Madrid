/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstiter.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aarellan <aarellan@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/26 23:24:50 by aarellan          #+#    #+#             */
/*   Updated: 2026/05/26 23:24:50 by aarellan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*
	This function iterates through a list and applies a function to each node.
	Like a train conductor checking every wagon.
*/
void	ft_lstiter(t_list *lst, void (*f)(void *))
{
	if (!f || !lst)
		return ;
	while (lst)
	{
		f(lst->content);
		lst = lst->next;
	}
}

/*
#include <stdio.h>

void	print_content(void *content)
{
	printf("Content: %s\n", (char *)content);
}

int	main(void)
{
	t_list	*list = ft_lstnew("first");
	ft_lstadd_back(&list, ft_lstnew("second"));
	ft_lstadd_back(&list, ft_lstnew("third"));

	printf("Test 1: Iterating list:\n");
	ft_lstiter(list, print_content);
	printf("Test 2: Iterating NULL list:\n");
	ft_lstiter(NULL, print_content);
	printf("Test 3: Iterating list with NULL function:\n");
	ft_lstiter(list, NULL);
	return (0);
}
*/
