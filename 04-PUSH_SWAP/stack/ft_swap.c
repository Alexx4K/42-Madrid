/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_swap.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: crubio-p, aarellan <crubio-p, aarellan@stu +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/02 12:31:57 by crubio-p          #+#    #+#             */
/*   Updated: 2026/08/05 11:41:31 by crubio-p, aarell ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

/// @brief Swaps the first two elements of the given stack.
/// @param stack Pointer to the stack to operate on.
static void	ft_list_swap(t_stack **stack)
{
	t_stack	*first;
	t_stack	*second;

	if (!stack || !*stack || !(*stack)->next)
		return ;
	first = *stack;
	second = first->next;
	if (second->next)
		second->next->prev = first;
	first->next = second->next;
	first->prev = second;
	second->next = first;
	second->prev = NULL;
	*stack = second;
}

/// @brief Swaps in both stacks.
/// @param stack_a
/// @param stack_b
static void	ft_ss(t_stack **stack_a, t_stack **stack_b)
{
	ft_list_swap(stack_a);
	ft_list_swap(stack_b);
}

/// @brief Swaps the first two elements of the given stack(s) based on the
/// operation character.
/// @param stack_a Stack A
/// @param stack_b Stack B
/// @param operation Character indicating which stack(s) to operate on.
void	ft_swap(t_stack **stack_a, t_stack **stack_b, char operation)
{
	if (operation == 'a')
	{
		ft_list_swap(stack_a);
		op_register(OP_SA);
	}
	else if (operation == 'b')
	{
		ft_list_swap(stack_b);
		op_register(OP_SB);
	}
	else if (operation == 's')
	{
		ft_ss(stack_a, stack_b);
		op_register(OP_SS);
	}
}
