"""Tests for hexadecimal maze serialization."""

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from mazegen.maze import Direction, Maze
from output_writer import serialize_maze, write_maze


class OutputWriterTests(unittest.TestCase):
    def test_serializes_hex_grid_endpoints_and_shortest_route(self) -> None:
        maze = Maze.create_open(width=2, height=2)

        serialized = serialize_maze(maze)

        self.assertEqual(serialized, "93\nC6\n\n0,0\n1,1\nES\n")

    def test_writes_the_serialized_output_to_the_target_file(self) -> None:
        maze = Maze.create_open(width=2, height=2)

        with TemporaryDirectory() as directory:
            output_file = Path(directory) / "maze.txt"
            write_maze(maze, output_file)

            self.assertEqual(
                output_file.read_text(encoding="utf-8"),
                "93\nC6\n\n0,0\n1,1\nES\n",
            )

    def test_rejects_a_maze_with_disconnected_cells(self) -> None:
        maze = Maze.create(width=2, height=2)

        with self.assertRaisesRegex(ValueError, "reachable"):
            serialize_maze(maze)

    def test_rejects_a_maze_with_asymmetric_shared_walls(self) -> None:
        maze = Maze.create_open(width=2, height=2)
        maze.cell_at((0, 0)).walls.add(Direction.EAST)

        with self.assertRaisesRegex(ValueError, "Shared walls"):
            serialize_maze(maze)


if __name__ == "__main__":
    unittest.main()
