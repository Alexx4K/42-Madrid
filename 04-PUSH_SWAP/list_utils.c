/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   list_utils.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: crubio-p <crubio-p@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/28 15:15:55 by aarellan          #+#    #+#             */
/*   Updated: 2026/08/07 19:03:11 by crubio-p         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

/// @brief Builds a doubly linked list (stack) from an array of integers
/// in the same order as the array (index 0 is the top of the stack).
t_stack	*build_list(int *numbers, int count)
{
	t_stack	*list;
	t_stack	*node;
	t_stack	*last;
	int		i;

	list = NULL;
	last = NULL;
	i = 0;
	while (i < count)
	{
		node = new_node(numbers[i]);
		if (!node)
			return (free_stack(node), NULL);
		if (!list)
			list = node;
		else
		{
			last->next = node;
			node->prev = last;
		}
		last = node;
		i++;
	}
	return (list);
}

/// @brief Frees all nodes in a stack.
/// @param stack The stack to free.
void	free_stack(t_stack *stack)
{
	t_stack	*next;

	while (stack)
	{
		next = stack->next;
		free(stack);
		stack = next;
	}
}

/// @brief Converts an array of integers to their rank indices (1-based).
/// The smallest value gets index 1, second smallest gets 2, etc.
/// @param numbers Array of integers.
/// @param count Number of elements.
/// @return A newly allocated array with rank indices, or NULL on failure.
int	*psindex(int *numbers, int count)
{
	int	*indexed;
	int	i;
	int	j;
	int	rank;

	indexed = malloc(count * sizeof(int));
	if (!indexed)
		return (NULL);
	i = 0;
	while (i < count)
	{
		rank = 1;
		j = 0;
		while (j < count)
		{
			if (numbers[j] < numbers[i])
				rank++;
			j++;
		}
		indexed[i] = rank;
		i++;
	}
	return (indexed);
}
