/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   testing_utils.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: crubio-p <crubio-p@student.42madrid.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/30 18:19:50 by crubio-p          #+#    #+#             */
/*   Updated: 2026/07/30 18:19:50 by crubio-p         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "testing.h"

void	append_node(t_stack **stack, t_stack *new_node)
{
	t_stack	*last;

	if (!stack || !new_node)
		return ;
	if (!*stack)
	{
		*stack = new_node;
		return ;
	}
	last = ps_lstlast(*stack);
	last->next = new_node;
	new_node->prev = last;
}

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

int	init_stack_a(t_stack **stack_a, int *values, int size)
{
	t_stack	*new_node;
	int		i;

	i = 0;
	while (i < size)
	{
		new_node = ps_lstnew(values[i]);
		if (!new_node)
			return (0);
		append_node(stack_a, new_node);
		i++;
	}
	return (1);
}
