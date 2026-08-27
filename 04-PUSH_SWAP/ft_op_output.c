/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_op_output.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: crubio-p, aarellan <crubio-p, aarellan@stu +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/05 12:21:38 by crubio-p, aarell  #+#    #+#             */
/*   Updated: 2026/08/05 12:23:43 by crubio-p, aarell ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static t_output_mode	*get_output_mode(void)
{
	static t_output_mode	mode = OUTPUT_OPERATIONS;

	return (&mode);
}

void	op_set_output_mode(t_output_mode mode)
{
	*get_output_mode() = mode;
}

static const char	*op_name(t_op op)
{
	static const char	*names[OP_COUNT] = {
		"sa\n",
		"sb\n",
		"ss\n",
		"pa\n",
		"pb\n",
		"ra\n",
		"rb\n",
		"rr\n",
		"rra\n",
		"rrb\n",
		"rrr\n"
	};

	if (op < OP_SA || op >= OP_COUNT)
		return (NULL);
	return (names[op]);
}

void	op_emit(t_op op)
{
	const char	*name;

	if (*get_output_mode() != OUTPUT_OPERATIONS)
		return ;
	name = op_name(op);
	if (name)
		write(1, name, ft_strlen(name));
}
