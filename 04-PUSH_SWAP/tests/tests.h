/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   tests.h                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: crubio-p <crubio-p@student.42madrid.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/30 18:17:51 by crubio-p          #+#    #+#             */
/*   Updated: 2026/07/30 18:17:51 by crubio-p         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef TESTS_H
# define TESTS_H

# include "push_swap.h"

// test_indexed_print.c
void	print_values(const int *values, int size);
void	print_stack(const char *name, t_stack *stack);

// test_indexed_checks.c
void	test_free_stack(t_stack *stack);
int		append_node(t_stack **stack, int content);
int		test_has_duplicates(const int *values, int size);
int		is_sorted(t_stack *stack);
int		has_valid_prev_links(t_stack *stack);

#endif
