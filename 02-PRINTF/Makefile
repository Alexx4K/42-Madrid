# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: aarellan <aarellan@student.42madrid.com>   +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/06/06 14:26:31 by aarellan          #+#    #+#              #
#    Updated: 2026/06/06 14:26:45 by aarellan         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME = libftprintf.a
LIBFT = libft/libft.a
CC = cc
CFLAGS = -Wall -Wextra -Werror
AR = ar rcs
RM = rm -rf

SRC = ft_printf.c ft_print_numbers.c ft_print_words.c utils.c
OBJ = $(SRC:.c=.o)

all: $(NAME)

$(NAME): $(LIBFT) $(OBJ)
	cp $(LIBFT) $(NAME)
	$(AR) $(NAME) $(OBJ)

$(LIBFT):
	$(MAKE) -C libft

%.o: %.c
	$(CC) $(CFLAGS) -I. -Ilibft -c $< -o $@

clean:
	$(RM) $(OBJ)
	$(MAKE) -C libft clean

fclean: clean
	$(RM) $(NAME)
	$(MAKE) -C libft fclean

re: fclean all

.PHONY: all clean fclean re