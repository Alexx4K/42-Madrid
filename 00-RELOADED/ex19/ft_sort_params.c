/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_sort_params.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aarellan <aarellan@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/20 10:38:43 by aarellan          #+#    #+#             */
/*   Updated: 2026/05/20 13:32:44 by aarellan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

/*#include <unistd.h>

void	ft_putchar(char c)
{
	write(1, &c, 1);
}*/
void	ft_putchar(char c);

int	ft_strcmp(char *s1, char *s2)
{
	while (*s1 && *s2)
	{
		if (*s1 != *s2)
		{
			return (*s1 - *s2);
		}
		s1++;
		s2++;
	}
	return (*s1 - *s2);
}

void	ft_swap(char **a, char **b)
{
	char	*temp;

	temp = *a;
	*a = *b;
	*b = temp;
}

void	ft_print_params(int numpar, char **params)
{
	int	i;
	int	j;

	j = 0;
	while (j < numpar)
	{
		i = 0;
		while (params[j][i] != 0)
		{
			ft_putchar(params[j][i]);
			i++;
		}
		ft_putchar('\n');
		j++;
	}
}

void	ft_sort_params(int argc, char **argv)
{
	int	i;
	int	orden;

	i = 0;
	orden = 0;
	while (orden < argc)
	{
		i = 0;
		while (i < (argc - orden) && (i + 1) < argc)
		{
			if (ft_strcmp(argv[i], argv[i + 1]) > 0)
				ft_swap(&argv[i], &argv[i + 1]);
			i++;
		}
		orden++;
	}
}

int	main(int ac, char **av)
{
	int		i;

	i = 1;
	ft_sort_params(ac - 1, &av[1]);
	ft_print_params(ac - 1, &av[1]);
	return (0);
}
