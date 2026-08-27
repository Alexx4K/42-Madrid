/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_adaptive.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: crubio-p, aarellan <crubio-p, aarellan@stu +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/20 19:16:00 by aarellan          #+#    #+#             */
/*   Updated: 2026/08/02 20:26:56 by crubio-p, aarell ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

/// @brief Computes the disorder of the stack.
/// @param stack The stack to compute the disorder of.
/// @return The disorder of the stack.
float	ft_compute_disorder(t_stack *stack)
{
	t_stack	*i;
	t_stack	*j;
	int		total_pairs;
	int		mistakes;

	if (!stack || !stack->next)
		return (0.0);
	total_pairs = 0;
	mistakes = 0;
	i = stack;
	while (i)
	{
		j = i->next;
		while (j)
		{
			total_pairs++;
			if (i->content > j->content)
				mistakes++;
			j = j->next;
		}
		i = i->next;
	}
	return ((float)mistakes / total_pairs);
}

/// @brief Executes the strategy dispatch.
/// @param stack_a The first stack.
/// @param stack_b The second stack.
/// @param forced_strat The forced strategy.
/// @param disorder The disorder of the stack.
void	ft_exec_strategy_dispatch(t_stack **stack_a, t_stack **stack_b,
			int forced_strat, float disorder)
{
	if (forced_strat == 0)
		sort_selection(stack_a, stack_b);
	else if (forced_strat == 1)
		ft_prechunksort(stack_a, stack_b);
	else if (forced_strat == 2)
		ft_radix_sort(stack_a, stack_b);
	else
	{
		if (disorder >= 0.5)
			ft_radix_sort(stack_a, stack_b);
		else if (disorder >= 0.2)
			ft_prechunksort(stack_a, stack_b);
		else
			sort_selection(stack_a, stack_b);
	}
}
