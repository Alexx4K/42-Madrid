/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_bench.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: crubio-p <crubio-p@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/20 19:10:00 by aarellan          #+#    #+#             */
/*   Updated: 2026/08/09 17:59:40 by crubio-p         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

/// @brief Names the strategy actually used, together with its complexity
/// class. When forced_strat is -1 (adaptive), the class shown is the one
/// picked for the measured disorder.
static const char	*strategy_label(int forced_strat, float disorder)
{
	if (forced_strat == 0)
		return ("Simple / O(n^2)");
	if (forced_strat == 1)
		return ("Medium / O(n\xE2\x88\x9An)");
	if (forced_strat == 2)
		return ("Complex / O(n log n)");
	if (disorder < 0.2f)
		return ("Adaptive / O(n^2)");
	if (disorder < 0.5f)
		return ("Adaptive / O(n\xE2\x88\x9An)");
	return ("Adaptive / O(n log n)");
}

/// @brief Prints the benchmark summary to stderr: disorder ratio, strategy
/// used, total operations and the breakdown per operation type.
/// @param disorder The disorder ratio of the original stack (0.0 - 1.0).
/// @param forced_strat The strategy used (-1 = adaptive, 0-2 = forced).
void	bench_print(float disorder, int forced_strat)
{
	fprintf(stderr, "[bench] disorder:   %.2f%%\n", disorder * 100);
	fprintf(stderr, "[bench] strategy:   %s\n",
		strategy_label(forced_strat, disorder));
	fprintf(stderr, "[bench] total_ops:  %d\n", op_get_total());
	fprintf(stderr, "[bench] sa: %d sb: %d ss: %d pa: %d pb: %d\n",
		op_get_count(OP_SA), op_get_count(OP_SB), op_get_count(OP_SS),
		op_get_count(OP_PA), op_get_count(OP_PB));
	fprintf(stderr, "[bench] ra: %d rb: %d rr: %d rra: %d rrb: %d rrr: %d\n",
		op_get_count(OP_RA), op_get_count(OP_RB), op_get_count(OP_RR),
		op_get_count(OP_RRA), op_get_count(OP_RRB), op_get_count(OP_RRR));
}
