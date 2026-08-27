/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_chunksort.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: crubio-p, aarellan <crubio-p, aarellan@stu +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/18 10:42:01 by cesar             #+#    #+#             */
/*   Updated: 2026/08/02 20:26:59 by crubio-p, aarell ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

/// @brief Calculates the nearest perfect square root.
/// @param n
/// @return The nearest perfect square.
/// @todo Move to a math utils
static int	ft_nearest_perfect_sqrt(int n)
{
	int	i;

	if (n < 1)
		return (0);
	i = 1;
	while (i * i <= n)
		i++;
	return (i - 1);
}

/// @brief Moves the elements of the chunk to the stack B.
/// @param stack_a
/// @param stack_b
/// @param chunk_size Size of the chunk.
/// @param act_chunk Actual chunk.
void	move_chunk_elem(t_stack **stack_a, t_stack **stack_b, int chunk_size,
	int act_chunk)
{
	int	pushed_elems;
	int	pos;
	int	first_index;
	int	last_index;

	pushed_elems = 0;
	while (!ft_is_empty(*stack_a) && pushed_elems < chunk_size)
	{
		first_index = (act_chunk * chunk_size) + 1;
		last_index = first_index + chunk_size - 1;
		pos = ft_find_first_chunk_pos(*stack_a, first_index, last_index);
		if (pos == -1)
			break ;
		ft_move_pos_to_top(stack_a, stack_b, pos, 'a');
		if ((*stack_a)->content < first_index + (chunk_size / 2))
		{
			ft_push(stack_a, stack_b, 'b');
			ft_rotate(stack_a, stack_b, 'b');
		}
		else
			ft_push(stack_a, stack_b, 'b');
		pushed_elems++;
	}
}

/// @brief Pushes the sorted elements from stack B to stack A.
/// @param stack_a
/// @param stack_b
/// @param max_index Maximum index to push.
void	ft_push_sorted_to_a(t_stack **stack_a, t_stack **stack_b, int max_index)
{
	int	pos;

	while (max_index > 0)
	{
		pos = find_position(*stack_b, max_index);
		ft_move_pos_to_top(stack_a, stack_b, pos, 'b');
		ft_push(stack_a, stack_b, 'a');
		max_index--;
	}
}

/// @brief Sorting algorithm that passes the elements chunk by chunk to the
/// stack B so they are more grouped.
/// @param stack_a
/// @param stack_b
/// @param n_elems Number of elements to sort.
void	ft_chunksort(t_stack **stack_a, t_stack **stack_b, int n_elems)
{
	int	chunk_size;
	int	act_chunk;

	chunk_size = ft_nearest_perfect_sqrt(n_elems);
	act_chunk = 0;
	while (!ft_is_empty(*stack_a))
	{
		move_chunk_elem(stack_a, stack_b, chunk_size, act_chunk);
		act_chunk++;
	}
	ft_push_sorted_to_a(stack_a, stack_b, n_elems);
}

/// @brief Previous function to prepare for the chunksort. For example, we
/// calculate the number of elements to save some lines.
/// @param stack_a
/// @param stack_b
void	ft_prechunksort(t_stack **stack_a, t_stack **stack_b)
{
	int	n_elems;

	n_elems = ps_lstsize(*stack_a);
	ft_chunksort(stack_a, stack_b, n_elems);
}
