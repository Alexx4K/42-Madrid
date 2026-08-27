/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   tokenizer.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: crubio-p <crubio-p@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/30 18:06:25 by crubio-p          #+#    #+#             */
/*   Updated: 2026/08/07 18:01:19 by crubio-p         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

/// @brief Splits one argv argument by space and appends the resulting
/// tokens to all_tokens, starting at idx.
/// @return The updated idx, or -1 on allocation failure.
static int	append_tokens(char **all_tokens, char *arg, int idx)
{
	char	**parts;
	int		j;

	parts = ft_split(arg, ' ');
	if (!parts)
		return (-1);
	j = 0;
	while (parts[j])
		all_tokens[idx++] = parts[j++];
	free(parts);
	return (idx);
}

/// @brief Splits every argv argument by space and stores the resulting
/// tokens in a single NULL-terminated array.
/// @param total Total token count, as returned by compute_max_size.
/// @return A newly allocated array of tokens, or NULL on failure.
static char	**build_tokens(int argc, char **argv, int total)
{
	char	**all_tokens;
	int		idx;
	int		i;

	all_tokens = malloc((total + 1) * sizeof(char *));
	if (!all_tokens)
		return (NULL);
	idx = 0;
	i = 1;
	while (i < argc)
	{
		idx = append_tokens(all_tokens, argv[i], idx);
		if (idx == -1)
		{
			free(all_tokens);
			return (NULL);
		}
		i++;
	}
	all_tokens[idx] = NULL;
	return (all_tokens);
}

/// @brief Parses the tokens into flags/numbers, validates them and converts
/// the numbers into their rank-index representation.
/// @param tokens Token array, consumed (freed) by this function.
/// @param total Number of numeric slots to allocate.
/// @return A newly allocated array of rank indexes, or NULL on failure.
static int	*parse_and_index(char **tokens, int *flag_count, int *count,
		int total)
{
	int	*numbers;
	int	*indexed;

	numbers = malloc(total * sizeof(int));
	if (!numbers)
	{
		free_split(tokens);
		return (NULL);
	}
	parse_tokens(tokens, flag_count, numbers, count);
	if (has_conflict(flag_count) || has_duplicates(numbers, *count)
		|| has_duplicated_flags(flag_count))
	{
		free_all(tokens, numbers);
		error_exit();
	}
	indexed = psindex(numbers, *count);
	free_all(tokens, numbers);
	return (indexed);
}

/// @brief Tokenizes the program arguments and produces the rank-index
/// array ready to build the initial stack a.
/// @param flag_count Output array of flag counters.
/// @param count Output number of parsed integers.
/// @return A newly allocated array of rank indexes, or NULL if there was
/// nothing to sort.
int	*prepare_numbers(int argc, char **argv, int *flag_count, int *count)
{
	int		total;
	char	**tokens;

	total = compute_max_size(argc, argv);
	if (total <= 0)
		return (NULL);
	tokens = build_tokens(argc, argv, total);
	if (!tokens)
		return (NULL);
	return (parse_and_index(tokens, flag_count, count, total));
}
