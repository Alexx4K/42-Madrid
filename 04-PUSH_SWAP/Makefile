# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: crubio-p, aarellan <crubio-p, aarellan@stu +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/08/02 20:29:10 by crubio-p, aarell  #+#    #+#              #
#    Updated: 2026/08/05 13:41:03 by crubio-p, aarell ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


NAME		=	push_swap

CC			=	cc
CFLAGS		=	-Wall -Wextra -Werror -g
RM			=	rm -f

LIBFT_DIR	=	include
LIBFT		=	$(LIBFT_DIR)/libft.a

INCLUDES	=	-Iinclude -I.

SRCS		=	main.c \
				ft_bench.c \
				ft_op_output.c \
				ft_operations.c \
				linked_lists.c \
				list_utils.c \
				push_swap.c \
				parsing/flags_comparing.c \
				parsing/flags.c \
				parsing/parser.c \
				parsing/tokenizer.c \
				parsing/utils.c \
				sort/ft_adaptive.c \
				sort/ft_chunksort.c \
				sort/ft_radix.c \
				sort/selection_sort.c \
				sort/small_sort.c \
				sort/sorting_utils.c \
				stack/ft_push.c \
				stack/ft_rotate.c \
				stack/ft_swap.c

OBJS		=	$(SRCS:.c=.o)

%.o:		%.c push_swap.h
			$(CC) $(CFLAGS) $(INCLUDES) -c $< -o $@

$(NAME):	$(LIBFT) $(OBJS)
			$(CC) $(CFLAGS) $(OBJS) $(LIBFT) -o $(NAME)

all:		$(NAME)

bonus:		all

clean:
			$(RM) $(OBJS)

fclean:		clean
			$(RM) $(NAME)
			$(RM) *.txt


re:			fclean all

.PHONY:		all bonus clean fclean re
