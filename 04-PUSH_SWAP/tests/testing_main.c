/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   testing_main.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: crubio-p <crubio-p@student.42madrid.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/04 00:00:00 by crubio-p          #+#    #+#             */
/*   Updated: 2026/07/30 18:19:50 by crubio-p         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

/*
** Not part of the mandatory delivery: dev-only walkthrough of every
** operation (sa, sb, ss, pa, pb, ra, rb, rr, rra, rrb, rrr).
*/

#include "testing.h"

/// @brief Runs sa, pb, pb, sb, ss, ra, rb, rr, printing the state each time.
static void	run_ops_part1(t_stack **stack_a, t_stack **stack_b)
{
	ft_swap(stack_a, stack_b, 'a');
	print_state("sa", *stack_a, *stack_b);
	ft_push(stack_a, stack_b, 'b');
	print_state("pb", *stack_a, *stack_b);
	ft_push(stack_a, stack_b, 'b');
	print_state("pb", *stack_a, *stack_b);
	ft_swap(stack_a, stack_b, 'b');
	print_state("sb", *stack_a, *stack_b);
	ft_swap(stack_a, stack_b, 's');
	print_state("ss", *stack_a, *stack_b);
	ft_rotate(stack_a, stack_b, 'a');
	print_state("ra", *stack_a, *stack_b);
	ft_rotate(stack_a, stack_b, 'b');
	print_state("rb", *stack_a, *stack_b);
	ft_rotate(stack_a, stack_b, 'r');
	print_state("rr", *stack_a, *stack_b);
}

/// @brief Runs rra, rrb, rrr, pa, printing the state each time.
static void	run_ops_part2(t_stack **stack_a, t_stack **stack_b)
{
	ft_reverse_rotate(stack_a, stack_b, 'a');
	print_state("rra", *stack_a, *stack_b);
	ft_reverse_rotate(stack_a, stack_b, 'b');
	print_state("rrb", *stack_a, *stack_b);
	ft_reverse_rotate(stack_a, stack_b, 'r');
	print_state("rrr", *stack_a, *stack_b);
	ft_push(stack_a, stack_b, 'a');
	print_state("pa", *stack_a, *stack_b);
}

int	main(void)
{
	t_stack	*stack_a;
	t_stack	*stack_b;
	int		values[5];

	stack_a = NULL;
	stack_b = NULL;
	values[0] = 3;
	values[1] = 1;
	values[2] = 4;
	values[3] = 2;
	values[4] = 5;
	if (!init_stack_a(&stack_a, values, 5))
	{
		free_stack(stack_a);
		return (1);
	}
	print_state("initial", stack_a, stack_b);
	run_ops_part1(&stack_a, &stack_b);
	run_ops_part2(&stack_a, &stack_b);
	free_stack(stack_a);
	free_stack(stack_b);
	return (0);
}
