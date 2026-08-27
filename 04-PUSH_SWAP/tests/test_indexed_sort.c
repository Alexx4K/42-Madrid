/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   test_indexed_sort.c                                :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: crubio-p <crubio-p@student.42madrid.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/04 00:00:00 by crubio-p          #+#    #+#             */
/*   Updated: 2026/07/30 18:17:51 by crubio-p         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

/*
** Not part of the mandatory delivery: dev-only sanity check for the three
** base sorting algorithms, run through the Makefile's "tests" rule.
*/

#include "tests.h"

/// @brief Rank of values[position] (1 = smallest) among all values.
static int	get_index(const int *values, int size, int position)
{
	int	index;
	int	i;

	index = 1;
	i = 0;
	while (i < size)
	{
		if (values[i] < values[position])
			index++;
		i++;
	}
	return (index);
}

/// @brief Builds a stack of rank-indexes from an array of raw values.
static int	init_indexed_stack(t_stack **stack, const int *values, int size)
{
	int	i;
	int	index;

	if (test_has_duplicates(values, size))
		return (0);
	i = 0;
	while (i < size)
	{
		index = get_index(values, size, i);
		printf("  value %d -> index %d\n", values[i], index);
		if (!append_node(stack, index))
		{
			test_free_stack(*stack);
			*stack = NULL;
			return (0);
		}
		i++;
	}
	return (1);
}

/// @brief Validates the sorted result, reports OK/KO and frees the stacks.
static int	report_result(t_stack *stack_a, t_stack *stack_b, int size)
{
	int	ok;

	ok = is_sorted(stack_a) && stack_b == NULL
		&& ps_lstsize(stack_a) == size && has_valid_prev_links(stack_a);
	if (ok)
		printf("Result: OK\n");
	else
		printf("Result: KO\n");
	test_free_stack(stack_a);
	test_free_stack(stack_b);
	return (ok);
}

/// @brief Runs one sorting algorithm on the indexed values and reports OK/KO.
static int	test_algorithm(const char *name,
		void (*sort)(t_stack **, t_stack **), const int *values, int size)
{
	t_stack	*stack_a;
	t_stack	*stack_b;

	stack_a = NULL;
	stack_b = NULL;
	printf("\n=== %s ===\n", name);
	if (!init_indexed_stack(&stack_a, values, size))
	{
		fprintf(stderr, "Error: duplicate value or allocation failure\n");
		return (0);
	}
	print_stack("A", stack_a);
	print_stack("B", stack_b);
	sort(&stack_a, &stack_b);
	print_stack("A", stack_a);
	print_stack("B", stack_b);
	return (report_result(stack_a, stack_b, size));
}

int	main(void)
{
	int	values[7];
	int	size;
	int	ok;

	values[0] = 42;
	values[1] = -7;
	values[2] = 1000;
	values[3] = 3;
	values[4] = -25;
	values[5] = 81;
	values[6] = 0;
	size = 7;
	print_values(values, size);
	ok = test_algorithm("Selection sort", sort_selection, values, size);
	ok = ok & test_algorithm("Chunk sort", ft_prechunksort, values, size);
	ok = ok & test_algorithm("Radix sort", ft_radix_sort, values, size);
	if (ok)
		printf("\nOverall result: OK\n");
	else
		printf("\nOverall result: KO\n");
	return (!ok);
}
