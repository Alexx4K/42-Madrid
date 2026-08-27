/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   test_indexed_print.c                               :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: crubio-p <crubio-p@student.42madrid.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/30 18:17:51 by crubio-p          #+#    #+#             */
/*   Updated: 2026/07/30 18:17:51 by crubio-p         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "tests.h"

/// @brief Prints an array of values as [a, b, c].
void	print_values(const int *values, int size)
{
	int	i;

	i = 0;
	printf("[");
	while (i < size)
	{
		printf("%d", values[i]);
		if (i + 1 < size)
			printf(", ");
		i++;
	}
	printf("]\n");
}

/// @brief Prints a stack from top to bottom.
void	print_stack(const char *name, t_stack *stack)
{
	printf("%s: top -> ", name);
	if (!stack)
	{
		printf("NULL\n");
		return ;
	}
	while (stack)
	{
		printf("%d", stack->content);
		if (stack->next)
			printf(" -> ");
		stack = stack->next;
	}
	printf(" -> NULL\n");
}
