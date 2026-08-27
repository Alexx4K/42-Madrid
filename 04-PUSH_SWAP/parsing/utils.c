/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   utils.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: crubio-p, aarellan <crubio-p, aarellan@stu +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/30 18:06:25 by crubio-p          #+#    #+#             */
/*   Updated: 2026/08/02 20:26:51 by crubio-p, aarell ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

/// @brief Prints "Error" to stderr and stops the program.
void	error_exit(void)
{
	write(2, "Error\n", 6);
	exit(1);
}

/// @brief Frees a NULL-terminated array of strings and the array itself.
/// @param arr The array to free.
void	free_split(char **arr)
{
	int	i;

	if (!arr)
		return ;
	i = 0;
	while (arr[i])
		free(arr[i++]);
	free(arr);
}

/// @brief Frees the token array and the numbers array used during parsing.
/// @param nbr_strs Token array to free.
/// @param numbers Numbers array to free.
void	free_all(char **nbr_strs, int *numbers)
{
	free_split(nbr_strs);
	free(numbers);
}

/// @brief Checks whether the given array of numbers has duplicate values.
/// @param numbers Array of integers.
/// @param count Number of elements.
/// @return 1 if a duplicate is found, 0 otherwise.
int	has_duplicates(int *numbers, int count)
{
	int	i;
	int	j;

	i = 0;
	while (i < count)
	{
		j = i + 1;
		while (j < count)
		{
			if (numbers[i] == numbers[j])
				return (1);
			j++;
		}
		i++;
	}
	return (0);
}

/// @brief Counts the total number of whitespace-separated tokens found
/// across every argv argument.
/// @param argc Number of program arguments.
/// @param argv Program argument array.
/// @return Total token count, or -1 on allocation failure.
int	compute_max_size(int argc, char **argv)
{
	int		i;
	int		j;
	int		count;
	char	**parts;

	count = 0;
	i = 1;
	while (i < argc)
	{
		parts = ft_split(argv[i], ' ');
		if (!parts)
			return (-1);
		j = 0;
		while (parts[j])
			j++;
		count += j;
		free_split(parts);
		i++;
	}
	return (count);
}
