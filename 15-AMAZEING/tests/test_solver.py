"""Tests for shortest-path maze solving."""

import unittest

from mazegen.maze import Direction, Maze
from mazegen.solver import solve_shortest_path


class ShortestPathSolverTests(unittest.TestCase):
    def test_returns_the_shortest_route_through_an_open_maze(self) -> None:
        maze = Maze.create_open(width=3, height=3)

        route = solve_shortest_path(maze)

        self.assertEqual(
            route,
            [
                Direction.EAST,
                Direction.EAST,
                Direction.SOUTH,
                Direction.SOUTH,
            ],
        )

    def test_returns_none_when_the_exit_is_unreachable(self) -> None:
        maze = Maze.create(width=2, height=2)

        route = solve_shortest_path(maze)

        self.assertIsNone(route)

    def test_uses_the_maze_entry_and_exit_as_route_endpoints(self) -> None:
        open_maze = Maze.create_open(width=3, height=3)
        maze = Maze(
            width=3,
            height=3,
            entry=(2, 0),
            exit=(1, 2),
            cells=open_maze.cells,
        )

        route = solve_shortest_path(maze)

        self.assertEqual(
            route,
            [Direction.SOUTH, Direction.SOUTH, Direction.WEST],
        )


if __name__ == "__main__":
    unittest.main()
