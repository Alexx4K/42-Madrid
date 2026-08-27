/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   selection_sort.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: crubio-p, aarellan <crubio-p, aarellan@stu +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/17 13:03:22 by crubio-p          #+#    #+#             */
/*   Updated: 2026/08/02 20:27:06 by crubio-p, aarell ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

/// @brief Sorts the elements in stack_a using the selection sort algorithm and
/// moves them to stack_b, then moves them back to stack_a in sorted order.
/// @param stack_a
/// @param stack_b
/// @todo change so it goes index by index.
void	sort_selection(t_stack **stack_a, t_stack **stack_b)
{
	int	value;
	int	pos;

	while (!ft_is_empty(*stack_a))
	{
		value = find_min_value(*stack_a);
		pos = find_position(*stack_a, value);
		ft_move_pos_to_top(stack_a, stack_b, pos, 'a');
		ft_push(stack_a, stack_b, 'b');
	}
	while (!ft_is_empty(*stack_b))
		ft_push(stack_a, stack_b, 'a');
}
