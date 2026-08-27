/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   flags.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: crubio-p, aarellan <crubio-p, aarellan@stu +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/22 13:59:09 by aarellan          #+#    #+#             */
/*   Updated: 2026/08/05 10:35:26 by crubio-p, aarell ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

/// @brief Gets the type of the flag.
/// @param str The flag to get the type of.
/// @return The type of the flag.
t_flag	get_flag_type(const char *str)
{
	if (str_equals(str, "--simple") == 0)
		return (FLAG_SIMPLE);
	if (str_equals(str, "--medium") == 0)
		return (FLAG_MEDIUM);
	if (str_equals(str, "--complex") == 0)
		return (FLAG_COMPLEX);
	if (str_equals(str, "--adaptive") == 0)
		return (FLAG_ADAPTIVE);
	if (str_equals(str, "--bench") == 0)
		return (FLAG_BENCH);
	return (FLAG_INVALID);
}

/// @brief Checks if there is a conflict between flags.
/// @param counts Array of flag counts.
/// @return 1 if there is a conflict, 0 otherwise.
int	has_conflict(int *counts)
{
	int	total;
	int	i;

	total = 0;
	i = FLAG_SIMPLE;
	while (i <= FLAG_ADAPTIVE)
	{
		if (counts[i] > 0)
			total++;
		i++;
	}
	return (total > 1);
}

/// @brief Checks if there are duplicated flags.
/// @param counts Array of flag counts.
/// @return 1 if there is a conflict, 0 otherwise.
int	has_duplicated_flags(int *counts)
{
	int	i;

	i = 0;
	while (i < FLAG_TOTAL)
	{
		if (counts[i] > 1)
			return (1);
		i++;
	}
	return (0);
}

/// @brief Initializes the flag counts.
/// @param flag_count Array of flag counts.
void	ft_init_flags(int *flag_count)
{
	int	i;

	i = 0;
	while (i < FLAG_TOTAL)
		flag_count[i++] = 0;
}
