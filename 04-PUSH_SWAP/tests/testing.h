/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   testing.h                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: crubio-p <crubio-p@student.42madrid.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/30 18:19:50 by crubio-p          #+#    #+#             */
/*   Updated: 2026/07/30 18:19:50 by crubio-p         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef TESTING_H
# define TESTING_H

# include "push_swap.h"

// testing_print.c
int		node_value(t_stack *node);
void	print_stack(char *name, t_stack *stack);
int		check_prev_links(t_stack *stack);
void	print_state(char *operation, t_stack *stack_a, t_stack *stack_b);

// testing_utils.c
void	append_node(t_stack **stack, t_stack *new_node);
void	free_stack(t_stack *stack);
int		init_stack_a(t_stack **stack_a, int *values, int size);

#endif
