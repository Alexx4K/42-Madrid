/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   flags_comparing.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: crubio-p, aarellan <crubio-p, aarellan@stu +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/30 14:30:33 by crubio-p          #+#    #+#             */
/*   Updated: 2026/08/05 10:27:49 by crubio-p, aarell ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

/// @brief Checks if the flag is set.
/// @param flag_count Array of flag counts.
/// @return 1 if the flag is set, 0 otherwise.
int	is_simple(int *flag_count)
{
	return (flag_count[FLAG_SIMPLE] > 0);
}

int	is_medium(int *flag_count)
{
	return (flag_count[FLAG_MEDIUM] > 0);
}

int	is_complex(int *flag_count)
{
	return (flag_count[FLAG_COMPLEX] > 0);
}

int	is_adaptive(int *flag_count)
{
	return (flag_count[FLAG_ADAPTIVE] > 0);
}

int	is_bench(int *flag_count)
{
	return (flag_count[FLAG_BENCH] > 0);
}
