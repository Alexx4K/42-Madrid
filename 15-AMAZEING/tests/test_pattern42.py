"""Tests for the structural 42 pattern."""

from contextlib import redirect_stderr
from io import StringIO
import unittest

from mazegen.maze import Maze
from mazegen.pattern42 import Pattern42


class Pattern42Tests(unittest.TestCase):
    def test_apply_blocks_the_centered_mask(self) -> None:
        maze = Maze.create_open(width=10, height=9)

        Pattern42.apply(maze)

        blocked_coordinates = {
            (cell.x, cell.y)
            for row in maze.cells
            for cell in row
            if cell.blocked
        }
        self.assertEqual(
            blocked_coordinates,
            {
                (x + 1, y + 1)
                for y, row in enumerate((
                    "#..#.###", "#..#...#", "#..#...#", "####.###",
                    "...#.#..", "...#.#..", "...#.###",
                ))
                for x, marker in enumerate(row)
                if marker == "#"
            },
        )
        self.assertEqual(len(blocked_coordinates), 26)

    def test_mask_leaves_the_center_walkable_for_every_parity(self) -> None:
        for width in (10, 11, 12, 13):
            for height in (9, 10, 11, 12):
                with self.subTest(width=width, height=height):
                    maze = Maze.create_open(width, height)
                    self.assertTrue(Pattern42.apply(maze))
                    self.assertFalse(
                        maze.cell_at((width // 2, height // 2)).blocked
                    )
                    degrees = [
                        4 - len(cell.walls)
                        for row in maze.cells for cell in row
                        if not cell.blocked
                    ]
                    self.assertGreaterEqual(min(degrees), 2)

    def test_apply_omits_the_pattern_below_minimum_dimensions(self) -> None:
        for width, height in ((9, 9), (10, 8), (9, 8)):
            with self.subTest(width=width, height=height):
                maze = Maze.create_open(width=width, height=height)
                stderr = StringIO()

                with redirect_stderr(stderr):
                    applied = Pattern42.apply(maze)

                self.assertFalse(applied)
                self.assertEqual(
                    stderr.getvalue(),
                    "Warning: Maze too small for the 42 pattern "
                    f"({width}x{height} < 10x9). Pattern omitted.\n",
                )
                self.assertFalse(
                    any(cell.blocked for row in maze.cells for cell in row)
                )

    def test_apply_rejects_an_endpoint_inside_the_pattern(self) -> None:
        open_maze = Maze.create_open(width=10, height=9)
        maze = Maze(
            width=10,
            height=9,
            entry=(1, 1),
            exit=(9, 8),
            cells=open_maze.cells,
        )

        with self.assertRaisesRegex(
            ValueError,
            "Entry and exit coordinates cannot overlap Pattern42.",
        ):
            Pattern42.apply(maze)

        has_blocked_cells = any(
            cell.blocked for row in maze.cells for cell in row
        )
        self.assertFalse(has_blocked_cells)

    def test_quiet_remains_available_for_direct_pattern_application(
        self,
    ) -> None:
        maze = Maze.create_open(3, 3)
        stderr = StringIO()
        with redirect_stderr(stderr):
            self.assertFalse(Pattern42.apply(maze, quiet=True))
        self.assertEqual(stderr.getvalue(), "")


if __name__ == "__main__":
    unittest.main()
