/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   display_file.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aarellan <aarellan@student.42madrid.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/22 18:30:22 by aarellan          #+#    #+#             */
/*   Updated: 2026/05/22 20:46:13 by aarellan         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>
#include <fcntl.h>

void	printfi(char const *name)
{
	int		fd;
	char	buffer[1];

	fd = open(name, O_RDONLY);
	if (fd < 0)
		write(2, "Cannot read file.\n", 18);
	else
	{
		while (read(fd, buffer, sizeof(buffer)))
		{
			write(1, buffer, sizeof(buffer));
		}
		close(fd);
	}
}

int	main(int argc, char **argv)
{
	if (argc == 2)
		printfi(argv[1]);
	else if (argc < 2)
		write(2, "File name missing.\n", 19);
	else
		write(2, "Too many arguments.\n", 20);
	return (0);
}
