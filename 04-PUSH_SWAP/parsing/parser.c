/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   parser.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: crubio-p <crubio-p@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/22 14:22:16 by aarellan          #+#    #+#             */
/*   Updated: 2026/08/07 14:32:30 by crubio-p         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

/// @brief Checks if the string is a valid number.
/// @param str The string to check.
/// @return 1 if the string is a valid number, 0 otherwise.
static int	is_valid_number(const char *str)
{
	int	i;

	i = 0;
	if (str[i] == '+' || str[i] == '-')
		i++;
	if (str[i] == '\0')
		return (0);
	while (str[i])
	{
		if (str[i] < '0' || str[i] > '9')
			return (0);
		i++;
	}
	return (1);
}

/// @brief Checks if the strings are equal.
/// @param a The first string.
/// @param b The second string.
/// @return 1 if the strings are equal, 0 otherwise.
int	str_equals(const char *a, const char *b)
{
	int	i;

	i = 0;
	while (a[i] && b[i] && a[i] == b[i])
		i++;
	return (a[i] - b[i]);
}

/// @brief Converts a string to a long.
/// @param str The string to convert.
/// @return The long value.
long	str_to_long(const char *str)
{
	long	num;
	int		sign;
	int		i;

	num = 0;
	sign = 1;
	i = 0;
	if (str[i] == '+' || str[i] == '-')
	{
		if (str[i] == '-')
			sign = -1;
		i++;
	}
	while (str[i])
		num = num * 10 + (str[i++] - '0');
	return (num * sign);
}

/// @brief Stores n from arguments if its valid
/// @param str argument to convert in number
/// @param numbers
/// @param count counts the numbers stored.
/// @param nbr_strs This is used to free the memory in case of error
void	store_number(char *str, int *numbers, int *count, char **nbr_strs)
{
	long	value;

	if (!is_valid_number(str))
	{
		free_all(nbr_strs, numbers);
		error_exit();
	}
	value = str_to_long(str);
	if (value > INT_MAX || value < INT_MIN)
	{
		free_all(nbr_strs, numbers);
		error_exit();
	}
	numbers[*count] = (int)value;
	(*count)++;
}

/// @brief Parses arguments and stores the numbers and flags in their arrays
/// @param nbr_strs Arguments passed by the user (everything but the program
/// name).
/// @param flag_count list of flags (0 if not appeared, 1 if present,
/// controls duplicate).
/// @param numbers array of numbers after atol.
void	parse_tokens(char **nbr_strs, int *flag_count, int *numbers, int *count)
{
	int		j;
	t_flag	type;
	int		flag_section;

	j = 0;
	*count = 0;
	flag_section = 1;
	while (flag_section && nbr_strs[j] != NULL)
	{
		type = get_flag_type(nbr_strs[j]);
		if (type != FLAG_INVALID)
		{
			flag_count[type]++;
			j++;
		}
		else
			flag_section = 0;
	}
	while (nbr_strs[j] != NULL)
	{
		store_number(nbr_strs[j], numbers, count, nbr_strs);
		j++;
	}
}
