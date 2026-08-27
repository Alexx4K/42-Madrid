/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   testing_print.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: crubio-p <crubio-p@student.42madrid.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/30 18:19:50 by crubio-p          #+#    #+#             */
/*   Updated: 2026/07/30 18:19:50 by crubio-p         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "testing.h"

int	node_value(t_stack *node)
{
	return (node->content);
}

void	print_stack(char *name, t_stack *stack)
{
	printf("%s: top -> ", name);
	if (!stack)
	{
		printf("NULL\n");
		return ;
	}
	while (stack)
	{
		printf("%d", node_value(stack));
		if (stack->next)
			printf(" -> ");
		stack = stack->next;
	}
	printf(" -> NULL\n");
}

int	check_prev_links(t_stack *stack)
{
	t_stack	*prev;

	prev = NULL;
	while (stack)
	{
		if (stack->prev != prev)
			return (0);
		prev = stack;
		stack = stack->next;
	}
	return (1);
}

void	print_state(char *operation, t_stack *stack_a, t_stack *stack_b)
{
	printf("\n[%s]\n", operation);
	print_stack("A", stack_a);
	print_stack("B", stack_b);
	if (check_prev_links(stack_a))
		printf("prev links A: OK\n");
	else
		printf("prev links A: KO\n");
	if (check_prev_links(stack_b))
		printf("prev links B: OK\n");
	else
		printf("prev links B: KO\n");
}
