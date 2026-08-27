/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_operations.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: crubio-p, aarellan <crubio-p, aarellan@stu +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/05 12:18:27 by crubio-p, aarell  #+#    #+#             */
/*   Updated: 2026/08/05 12:18:33 by crubio-p, aarell ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static int	*get_counts(void)
{
	static int	counts[OP_COUNT];

	return (counts);
}

void	op_reset(void)
{
	int	*counts;
	int	i;

	counts = get_counts();
	i = 0;
	while (i < OP_COUNT)
		counts[i++] = 0;
}

void	op_register(t_op op)
{
	if (op < OP_SA || op >= OP_COUNT)
		return ;
	get_counts()[op]++;
	op_emit(op);
}

int	op_get_total(void)
{
	int	*counts;
	int	total;
	int	i;

	counts = get_counts();
	total = 0;
	i = 0;
	while (i < OP_COUNT)
		total += counts[i++];
	return (total);
}

int	op_get_count(t_op op)
{
	if (op < OP_SA || op >= OP_COUNT)
		return (0);
	return (get_counts()[op]);
}
