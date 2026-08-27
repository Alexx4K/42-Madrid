/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: crubio-p <crubio-p@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/13 11:27:45 by crubio-p          #+#    #+#             */
/*   Updated: 2026/08/09 17:53:09 by crubio-p         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef PUSH_SWAP_H
# define PUSH_SWAP_H

# include <unistd.h>
# include <stdlib.h>
# include <stdio.h>
# include <limits.h>
# include <stdbool.h>
# include <stddef.h>
# include <stdint.h>
# include "libft.h"

// PHASE 2: Stacks and Sorting

typedef struct s_stack
{
	int				content;
	struct s_stack	*next;
	struct s_stack	*prev;
}	t_stack;

typedef enum e_op
{
	OP_SA,
	OP_SB,
	OP_SS,
	OP_PA,
	OP_PB,
	OP_RA,
	OP_RB,
	OP_RR,
	OP_RRA,
	OP_RRB,
	OP_RRR,
	OP_COUNT
}	t_op;

typedef enum e_output_mode
{
	OUTPUT_OPERATIONS,
	OUTPUT_MUTE
}	t_output_mode;

typedef enum e_flag
{
	FLAG_INVALID = -1,
	FLAG_SIMPLE,
	FLAG_MEDIUM,
	FLAG_COMPLEX,
	FLAG_ADAPTIVE,
	FLAG_BENCH,
	FLAG_TOTAL
}	t_flag;

typedef struct s_data
{
	t_stack	*a;
	t_stack	*b;
	int		flag_count[FLAG_TOTAL];
	int		count;
	int		forced_strat;
	float	disorder;
}	t_data;

// Linked list basic functions
t_stack		*new_node(int value);
t_stack		*ps_lstlast(t_stack *lst);
int			ft_is_empty(const t_stack *stack);
int			ps_lstsize(t_stack *lst);
void		free_stack(t_stack *stack);

// Double stack functions
void		ft_swap(t_stack **stack_a, t_stack **stack_b, char operation);
void		ft_push(t_stack **stack_a, t_stack **stack_b, char operation);
void		ft_list_rotate(t_stack **stack);
void		ft_rotate(t_stack **stack_a, t_stack **stack_b, char operation);
void		ft_list_reverse_rotate(t_stack **stack);
void		ft_reverse_rotate(t_stack **stack_a, t_stack **stack_b,
				char operation);

// list_utils.c
t_stack		*build_list(int *numbers, int count);
int			*psindex(int *numbers, int count);

// Sorting algos + utils
int			list_is_sorted(t_stack *stack);
int			find_position(t_stack *stack, int value);
int			find_min_value(t_stack *stack);
int			ft_find_first_chunk_pos(t_stack *stack, int chunk_min,
				int chunk_max);
void		sort_two(t_stack **stack_a, t_stack **stack_b);
void		sort_three(t_stack **stack_a, t_stack **stack_b);
void		sort_four(t_stack **stack_a, t_stack **stack_b);
void		sort_five(t_stack **stack_a, t_stack **stack_b);
void		sort_selection(t_stack **stack_a, t_stack **stack_b);
void		ft_move_pos_to_top(t_stack **st_a, t_stack **st_b, int pos,
				char op);
void		ft_prechunksort(t_stack **stack_a, t_stack **stack_b);
void		ft_radix_sort(t_stack **stack_a, t_stack **stack_b);
float		ft_compute_disorder(t_stack *stack);
void		ft_exec_strategy_dispatch(t_stack **stack_a, t_stack **stack_b,
				int forced_strat, float disorder);

// ft_operations.c
void		op_reset(void);
void		op_register(t_op op);
int			op_get_total(void);
int			op_get_count(t_op op);

// ft_op_output.c
void		op_set_output_mode(t_output_mode mode);
void		op_emit(t_op op);

void		bench_print(float disorder, int forced_strat);

// parser.c
int			str_equals(const char *a, const char *b);
void		parse_tokens(char **tokens, int *flag_count, int *numbers,
				int *count);

// utils.c
void		error_exit(void);
void		free_split(char **arr);
void		free_all(char **nbr_strs, int *numbers);
int			has_duplicates(int *numbers, int count);
int			compute_max_size(int argc, char **argv);

// tokenizer.c
int			*prepare_numbers(int argc, char **argv, int *flag_count,
				int *count);

// flags.c
t_flag		get_flag_type(const char *str);
int			has_conflict(int *counts);
int			has_duplicated_flags(int *counts);
void		ft_init_flags(int *flag_count);

// flags_comparing.c
int			is_simple(int *flag_count);
int			is_medium(int *flag_count);
int			is_complex(int *flag_count);
int			is_adaptive(int *flag_count);
int			is_bench(int *flag_count);

#endif
