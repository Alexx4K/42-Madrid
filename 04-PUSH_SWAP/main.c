/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: crubio-p <crubio-p@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/28 14:49:18 by aarellan          #+#    #+#             */
/*   Updated: 2026/08/10 09:41:56 by crubio-p         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

/// @brief Determines which strategy was explicitly forced through the
/// program's selector flags.
/// @param flag_count Array of flag counters.
/// @return 0 (simple), 1 (medium), 2 (complex) or -1 (adaptive / default).
static int	get_forced_strat(int *flag_count)
{
	if (is_simple(flag_count))
		return (0);
	if (is_medium(flag_count))
		return (1);
	if (is_complex(flag_count))
		return (2);
	return (-1);
}

/// @brief Runs the sorting strategy matching the amount of elements to sort.
/// @param data Program state (stacks, flags, disorder index).
static void	run_sort(t_data *data)
{
	op_reset();
	if (data->count == 0 || data->count == 1)
		return ;
	else if (data->count == 2)
		sort_two(&data->a, &data->b);
	else if (data->count == 3)
		sort_three(&data->a, &data->b);
	else if (data->count == 4)
		sort_four(&data->a, &data->b);
	else if (data->count == 5)
		sort_five(&data->a, &data->b);
	else if (data->count > 5)
		ft_exec_strategy_dispatch(&data->a, &data->b, data->forced_strat,
			data->disorder);
}

int	main(int argc, char **argv)
{
	t_data	data;
	int		*indexed;

	if (argc < 2)
		return (0);
	ft_init_flags(data.flag_count);
	indexed = prepare_numbers(argc, argv, data.flag_count, &data.count);
	if (!indexed)
		return (0);
	data.a = build_list(indexed, data.count);
	free(indexed);
	if (list_is_sorted(data.a))
	{
		return (free_stack(data.a), 0);
	}
	data.b = NULL;
	data.forced_strat = get_forced_strat(data.flag_count);
	data.disorder = ft_compute_disorder(data.a);
	op_set_output_mode(OUTPUT_OPERATIONS);
	run_sort(&data);
	if (is_bench(data.flag_count))
		bench_print(data.disorder, data.forced_strat);
	return (free_stack(data.a), free_stack(data.b), 0);
}
