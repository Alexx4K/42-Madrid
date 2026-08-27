/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   linked_lists.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: crubio-p <crubio-p@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/02 12:22:01 by crubio-p          #+#    #+#             */
/*   Updated: 2026/08/07 19:03:24 by crubio-p         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

/// @brief Creates a new node for the stack with the given value
/// @param value The value to be stored in the new node
t_stack	*new_node(int value)
{
	t_stack	*node;

	node = malloc(sizeof(t_stack));
	if (!node)
		return (NULL);
	node->content = value;
	node->next = NULL;
	node->prev = NULL;
	return (node);
}

/// @brief Finds the last element in the list.
/// @param lst
/// @return A pointer to the last element.
t_stack	*ps_lstlast(t_stack *lst)
{
	if (lst == NULL)
		return (NULL);
	while (lst->next != NULL)
		lst = lst->next;
	return (lst);
}

/// @brief If the stack is NULL, it means that it's empty
/// @param stack
/// @return 1 if empty, 0 if not.
int	ft_is_empty(const t_stack *stack)
{
	return (stack == NULL);
}

/// @brief Counts the number of elements in the list.
/// @param lst
/// @return The size of the list.
int	ps_lstsize(t_stack *lst)
{
	int	size;

	size = 0;
	while (lst)
	{
		size++;
		lst = lst->next;
	}
	return (size);
}
