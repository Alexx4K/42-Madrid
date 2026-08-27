/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sorting_utils.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: crubio-p, aarellan <crubio-p, aarellan@stu +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/17 13:02:49 by crubio-p          #+#    #+#             */
/*   Updated: 2026/08/05 17:09:15 by crubio-p, aarell ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	list_is_sorted(t_stack *stack)
{
	int	expected_index;

	expected_index = 1;
	while (stack != NULL)
	{
		if (stack->content != expected_index)
			return (0);
		expected_index++;
		stack = stack->next;
	}
	return (1);
}

/// @brief Finds the position of a given value in the stack.
/// @param stack the stack to search for the value.
/// @param value the value to find in the stack.
/// @return the position of the value in the stack, or -1 if not found.
int	find_position(t_stack *stack, int value)
{
	int	pos;

	pos = 0;
	while (stack != NULL)
	{
		if (stack->content == value)
			return (pos);
		stack = stack->next;
		pos++;
	}
	return (-1);
}

/// @brief finds the minimum value in the given stack.
/// @param stack the stack to search for the minimum value.
/// @return the minimum value found in the stack.
int	find_min_value(t_stack *stack)
{
	int	min;

	min = stack->content;
	while (stack->next != NULL)
	{
		if (min > stack->next->content)
			min = stack->next->content;
		stack = stack->next;
	}
	return (min);
}

/// @brief Finds the position of an element from the interval.
/// @param stack the stack to search for the value.
/// @param chunk_min minimun value.
/// @param chunk_max maximun value.
/// @return the position of the value in the stack, or -1 if not found.
int	ft_find_first_chunk_pos(t_stack *stack, int chunk_min, int chunk_max)
{
	int	pos;

	pos = 0;
	while (stack != NULL)
	{
		if (stack->content >= chunk_min && stack->content <= chunk_max)
			return (pos);
		stack = stack->next;
		pos++;
	}
	return (-1);
}

/// @brief Rotates stack_a or stack_b (per op) so the element at pos ends up
/// on top, using whichever direction (ra/rra) needs fewer moves. Uses the
/// printing wrappers so every move is emitted as a Push_swap operation.
/// @param st_a Stack A.
/// @param st_b Stack B.
/// @param pos Position (0-indexed from the top) of the element to bring up.
/// @param op 'a' or 'b': which of the two stacks pos refers to.
void	ft_move_pos_to_top(t_stack **st_a, t_stack **st_b, int pos, char op)
{
	int	moves_remaining;
	int	size;

	if (op == 'a')
		size = ps_lstsize(*st_a);
	else
		size = ps_lstsize(*st_b);
	if (pos <= size / 2)
	{
		moves_remaining = pos;
		while (moves_remaining > 0)
		{
			ft_rotate(st_a, st_b, op);
			moves_remaining--;
		}
	}
	else
	{
		moves_remaining = size - pos;
		while (moves_remaining > 0)
		{
			ft_reverse_rotate(st_a, st_b, op);
			moves_remaining--;
		}
	}
}
