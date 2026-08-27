/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   test_indexed_checks.c                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: crubio-p <crubio-p@student.42madrid.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/30 18:17:51 by crubio-p          #+#    #+#             */
/*   Updated: 2026/07/30 18:17:51 by crubio-p         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "tests.h"

/// @brief Frees every node in a stack.
void	test_free_stack(t_stack *stack)
{
	t_stack	*next;

	while (stack)
	{
		next = stack->next;
		free(stack);
		stack = next;
	}
}

/// @brief Appends a new node holding content at the back of the stack.
/// @return 1 on success, 0 on allocation failure.
int	append_node(t_stack **stack, int content)
{
	t_stack	*new_node;
	t_stack	*last;

	new_node = ps_lstnew(content);
	if (!new_node)
		return (0);
	if (!*stack)
	{
		*stack = new_node;
		return (1);
	}
	last = ps_lstlast(*stack);
	last->next = new_node;
	new_node->prev = last;
	return (1);
}

/// @brief Checks whether the given array of values has duplicate values.
int	test_has_duplicates(const int *values, int size)
{
	int	i;
	int	j;

	i = 0;
	while (i < size)
	{
		j = i + 1;
		while (j < size)
		{
			if (values[i] == values[j])
				return (1);
			j++;
		}
		i++;
	}
	return (0);
}

/// @brief Checks that the stack is sorted in strictly ascending order.
int	is_sorted(t_stack *stack)
{
	while (stack && stack->next)
	{
		if (stack->content >= stack->next->content)
			return (0);
		stack = stack->next;
	}
	return (1);
}

/// @brief Checks that every node's prev pointer matches its predecessor.
int	has_valid_prev_links(t_stack *stack)
{
	t_stack	*previous;

	previous = NULL;
	while (stack)
	{
		if (stack->prev != previous)
			return (0);
		previous = stack;
		stack = stack->next;
	}
	return (1);
}
