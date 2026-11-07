"""Run with ``python -m unittest discover -s tests -p test_visualizer.py -v``.

For a colored sample preview, run ``python -m tests.test_visualizer --demo``
from the repository root. The public renderer can also be used directly:

    from mazegen.maze import Direction
    from visualizer import render_maze

    print(render_maze(maze, [Direction.EAST, Direction.SOUTH]))
"""

from collections import deque
import sys
import unittest

from mazegen.generator import MazeGenerator
from mazegen.maze import Direction, Maze
from mazegen.types import Coordinate
from visualizer import render_maze


class MazeRendererTests(unittest.TestCase):
    """Verify maze rendering, colors, and supplied route validation."""

    def test_renders_endpoints_walls_and_solution_without_ansi_colors(
        self,
    ) -> None:
        maze = Maze.create_open(width=2, height=2)

        rendered = render_maze(
            maze,
            [Direction.EAST, Direction.SOUTH],
            use_color=False,
        )

        lines = rendered.splitlines()
        self.assertEqual(len(lines), 2 * maze.height + 1)
        self.assertEqual(len(lines[0]), 4 * maze.width + 1)
        self.assertIn(" E ", lines[1])
        self.assertIn(" X ", lines[3])
        self.assertEqual(rendered.count(" * "), 1)
        self.assertNotIn("\033[", rendered)

    def test_can_hide_solution_and_enable_synthwave_colors(self) -> None:
        maze = Maze.create_open(width=2, height=2)
        solution = [Direction.EAST, Direction.SOUTH]

        hidden = render_maze(
            maze,
            solution,
            show_solution=False,
            use_color=False,
        )
        colored = render_maze(maze, solution)

        self.assertNotIn(" * ", hidden)
        self.assertIn("\033[38;5;51m", colored)
        self.assertIn("\033[38;5;198m", colored)
        self.assertIn("\033[38;5;226m", colored)
        self.assertIn("\033[38;5;201m", colored)

    def test_wall_color_is_configurable_without_changing_other_markers(
        self,
    ) -> None:
        maze = Maze.create_open(width=2, height=2)
        route = [Direction.EAST, Direction.SOUTH]
        default = render_maze(maze, route)
        custom = render_maze(maze, route, wall_color=208)

        self.assertEqual(
            custom, default.replace("\033[38;5;51m", "\033[38;5;208m")
        )
        for wall in ("---", "|"):
            self.assertIn(f"\033[38;5;208m{wall}\033[0m", custom)
        self.assertEqual(
            render_maze(maze, route, use_color=False, wall_color=208),
            render_maze(maze, route, use_color=False),
        )

    def test_renders_blocked_cells(self) -> None:
        maze = Maze.create_open(width=3, height=3)
        maze.block_cell(1, 1)

        rendered = render_maze(maze, use_color=False)

        self.assertIn("###", rendered)

    def test_rejects_routes_that_do_not_reach_the_exit(self) -> None:
        maze = Maze.create_open(width=2, height=2)

        with self.assertRaisesRegex(ValueError, "does not end"):
            render_maze(maze, [Direction.EAST], use_color=False)

    def test_rejects_routes_that_cross_a_wall(self) -> None:
        maze = Maze.create(2, 2)

        with self.assertRaisesRegex(ValueError, "closed wall"):
            render_maze(maze, [Direction.EAST], use_color=False)

    def test_rejects_routes_that_leave_the_maze(self) -> None:
        maze = Maze.create_open(width=2, height=2)

        with self.assertRaisesRegex(ValueError, "leaves the maze"):
            render_maze(maze, [Direction.NORTH], use_color=False)


def render_demo() -> None:
    """Print a colored sample maze for manual terminal inspection."""
    maze = MazeGenerator(seed=42).generate_perfect(
        width=9,
        height=5,
        entry=(0, 0),
        exit=(8, 4),
    )
    print(render_maze(maze, _find_solution(maze)))


def _find_solution(maze: Maze) -> list[Direction]:
    """Find a shortest route for the manual renderer preview."""
    pending = deque([maze.entry])
    previous: dict[Coordinate, tuple[Coordinate, Direction]] = {}
    visited = {maze.entry}

    while pending:
        coordinate = pending.popleft()
        if coordinate == maze.exit:
            break
        x, y = coordinate
        cell = maze.cell_at(coordinate)
        for direction in Direction:
            neighbor = maze.neighbor_coordinates(x, y, direction)
            if neighbor is None:
                continue
            if neighbor not in visited and not cell.has_wall(direction):
                visited.add(neighbor)
                previous[neighbor] = (coordinate, direction)
                pending.append(neighbor)

    if maze.exit not in visited:
        raise ValueError("The demo maze has no route to its exit.")

    route: list[Direction] = []
    current = maze.exit
    while current != maze.entry:
        parent, direction = previous[current]
        route.append(direction)
        current = parent
    route.reverse()
    return route


if __name__ == "__main__":
    if sys.argv[1:] == ["--demo"]:
        render_demo()
    else:
        unittest.main()
