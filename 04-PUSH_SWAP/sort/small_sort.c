/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   small_sort.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: crubio-p, aarellan <crubio-p, aarellan@stu +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/29 09:23:28 by crubio-p          #+#    #+#             */
/*   Updated: 2026/08/05 00:06:34 by crubio-p, aarell ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

/// @brief Sorts 2 elements in stack A.
/// @param stack_a The first stack.
/// @param stack_b The second stack.
void	sort_two(t_stack **stack_a, t_stack **stack_b)
{
	if ((*stack_a)->content > (*stack_a)->next->content)
		ft_swap(stack_a, stack_b, 'a');
}

/// @brief Sorts 3 elements in stack A.
/// @param stack_a The first stack.
/// @param stack_b The second stack.
void	sort_three(t_stack **stack_a, t_stack **stack_b)
{
	int	first;
	int	second;
	int	third;

	first = (*stack_a)->content;
	second = (*stack_a)->next->content;
	third = (*stack_a)->next->next->content;
	if (first > second && first < third && second < third)
		ft_swap(stack_a, stack_b, 'a');
	else if (first > second && first > third && second < third)
		ft_rotate(stack_a, stack_b, 'a');
	else if (first < second && first > third && second > third)
		ft_reverse_rotate(stack_a, stack_b, 'a');
	else if (first < second && first < third && second > third)
	{
		ft_swap(stack_a, stack_b, 'a');
		ft_rotate(stack_a, stack_b, 'a');
	}
	else if (first > second && first > third && second > third)
	{
		ft_swap(stack_a, stack_b, 'a');
		ft_reverse_rotate(stack_a, stack_b, 'a');
	}
}

/// @brief Sorts 4 elements in stack A.
/// @param stack_a The first stack.
/// @param stack_b The second stack.
void	sort_four(t_stack **stack_a, t_stack **stack_b)
{
	int	min_val;
	int	pos;

	min_val = find_min_value(*stack_a);
	pos = find_position(*stack_a, min_val);
	ft_move_pos_to_top(stack_a, stack_b, pos, 'a');
	if (!list_is_sorted(*stack_a))
	{
		ft_push(stack_a, stack_b, 'b');
		sort_three(stack_a, stack_b);
		ft_push(stack_a, stack_b, 'a');
	}
}

/// @brief Sorts 5 elements in stack A.
/// @param stack_a The first stack.
/// @param stack_b The second stack.
void	sort_five(t_stack **stack_a, t_stack **stack_b)
{
	int	min_val;
	int	pos;

	min_val = find_min_value(*stack_a);
	pos = find_position(*stack_a, min_val);
	ft_move_pos_to_top(stack_a, stack_b, pos, 'a');
	if (!list_is_sorted(*stack_a))
	{
		ft_push(stack_a, stack_b, 'b');
		sort_four(stack_a, stack_b);
		ft_push(stack_a, stack_b, 'a');
	}
}
