"""Tests for the maze domain model."""

import unittest

from pydantic import ValidationError

from mazegen.maze import Cell, Direction, Maze


def connected_row_cells() -> list[Cell]:
    """Build the smallest valid connected maze grid."""
    left = Cell(x=0, y=0)
    right = Cell(x=1, y=0)
    left.walls.remove(Direction.EAST)
    right.walls.remove(Direction.WEST)
    return [left, right]


class CellTests(unittest.TestCase):
    def test_new_cell_starts_with_all_four_walls_closed(self) -> None:
        cell = Cell(x=2, y=3)

        self.assertEqual(cell.walls, set(Direction))
        self.assertEqual(cell.wall_mask, 0b1111)


class MazeTests(unittest.TestCase):
    def test_requires_endpoints_for_validated_construction(self) -> None:
        with self.assertRaises(ValidationError):
            Maze.model_validate(
                {"width": 2, "height": 1, "cells": [connected_row_cells()]}
            )

    def test_rejects_negative_entry_coordinates(self) -> None:
        with self.assertRaises(ValidationError):
            Maze(
                width=2,
                height=1,
                entry=(-1, 0),
                exit=(1, 0),
                cells=[connected_row_cells()],
            )

    def test_rejects_a_grid_with_a_wrong_row_count(self) -> None:
        with self.assertRaises(ValidationError):
            Maze(
                width=2,
                height=2,
                entry=(0, 0),
                exit=(1, 1),
                cells=[connected_row_cells()],
            )

    def test_rejects_cell_coordinates_that_do_not_match_the_grid(self) -> None:
        cells = connected_row_cells()
        cells[0].x = 1

        with self.assertRaises(ValidationError):
            Maze(
                width=2,
                height=1,
                entry=(0, 0),
                exit=(1, 0),
                cells=[cells],
            )

    def test_rejects_non_positive_dimensions(self) -> None:
        invalid_dimensions = ((0, 1), (-1, 1), (1, 0), (1, -1))
        for width, height in invalid_dimensions:
            with self.subTest(width=width, height=height):
                with self.assertRaises(ValidationError):
                    Maze(
                        width=width,
                        height=height,
                        entry=(0, 0),
                        exit=(1, 0),
                        cells=[],
                    )

    def test_rejects_a_grid_with_unreachable_cells(self) -> None:
        with self.assertRaises(ValidationError):
            Maze(
                width=2,
                height=1,
                entry=(0, 0),
                exit=(1, 0),
                cells=[[Cell(x=0, y=0), Cell(x=1, y=0)]],
            )

    def test_rejects_asymmetric_shared_walls(self) -> None:
        cells = connected_row_cells()
        cells[1].walls.add(Direction.WEST)

        with self.assertRaises(ValidationError):
            Maze(
                width=2,
                height=1,
                entry=(0, 0),
                exit=(1, 0),
                cells=[cells],
            )

    def test_rejects_an_open_external_border(self) -> None:
        cells = connected_row_cells()
        cells[0].walls.remove(Direction.NORTH)

        with self.assertRaises(ValidationError):
            Maze(
                width=2,
                height=1,
                entry=(0, 0),
                exit=(1, 0),
                cells=[cells],
            )

    def test_rejects_identical_entry_and_exit_coordinates(self) -> None:
        with self.assertRaises(ValidationError):
            Maze(
                width=2,
                height=1,
                entry=(0, 0),
                exit=(0, 0),
                cells=[connected_row_cells()],
            )

    def test_rejects_an_out_of_bounds_exit_coordinate(self) -> None:
        with self.assertRaises(ValidationError):
            Maze(
                width=2,
                height=1,
                entry=(0, 0),
                exit=(2, 0),
                cells=[connected_row_cells()],
            )

    def test_rejects_an_out_of_bounds_entry_coordinate(self) -> None:
        with self.assertRaises(ValidationError):
            Maze(
                width=2,
                height=1,
                entry=(2, 0),
                exit=(1, 0),
                cells=[connected_row_cells()],
            )

    def test_records_explicit_entry_and_exit_coordinates(self) -> None:
        left = Cell(x=0, y=0)
        right = Cell(x=1, y=0)
        left.walls.remove(Direction.EAST)
        right.walls.remove(Direction.WEST)

        maze = Maze(
            width=2,
            height=1,
            entry=(0, 0),
            exit=(1, 0),
            cells=[[left, right]],
        )

        self.assertEqual(maze.entry, (0, 0))
        self.assertEqual(maze.exit, (1, 0))

    def test_create_builds_a_rectangular_grid_of_closed_cells(self) -> None:
        maze = Maze.create(width=3, height=2)

        self.assertEqual(maze.width, 3)
        self.assertEqual(maze.height, 2)
        self.assertEqual(maze.entry, (0, 0))
        self.assertEqual(maze.exit, (2, 1))
        self.assertEqual(maze.cell_at((2, 1)).model_dump(), {
            "x": 2,
            "y": 1,
            "walls": set(Direction),
            "blocked": False,
        })

    def test_create_open_opens_internal_passages_and_keeps_borders_closed(
        self,
    ) -> None:
        maze = Maze.create_open(width=2, height=2)

        self.assertTrue(maze.cell_at((0, 0)).has_wall(Direction.NORTH))
        self.assertTrue(maze.cell_at((0, 0)).has_wall(Direction.WEST))
        self.assertTrue(maze.cell_at((1, 1)).has_wall(Direction.EAST))
        self.assertTrue(maze.cell_at((1, 1)).has_wall(Direction.SOUTH))
        self.assertFalse(maze.cell_at((0, 0)).has_wall(Direction.EAST))
        self.assertFalse(maze.cell_at((0, 0)).has_wall(Direction.SOUTH))
        self.assertTrue(maze.has_coherent_walls())

    def test_create_open_requires_at_least_two_rows_and_columns(self) -> None:
        invalid_dimensions = ((1, 1), (1, 2), (2, 1), (0, 2), (2, 0))

        for width, height in invalid_dimensions:
            with self.subTest(width=width, height=height):
                with self.assertRaisesRegex(
                    ValueError,
                    "Open mazes require at least two rows and columns.",
                ):
                    Maze.create_open(width=width, height=height)

    def test_block_cell_closes_it_and_all_facing_neighbour_walls(
        self,
    ) -> None:
        maze = Maze.create_open(width=3, height=3)

        maze.block_cell(1, 1)

        self.assertTrue(maze.cell_at((1, 1)).blocked)
        self.assertEqual(maze.cell_at((1, 1)).walls, set(Direction))
        self.assertTrue(maze.cell_at((1, 0)).has_wall(Direction.SOUTH))
        self.assertTrue(maze.cell_at((2, 1)).has_wall(Direction.WEST))
        self.assertTrue(maze.cell_at((1, 2)).has_wall(Direction.NORTH))
        self.assertTrue(maze.cell_at((0, 1)).has_wall(Direction.EAST))
        self.assertTrue(maze.has_coherent_walls())

    def test_block_cell_rejects_entry_or_exit(self) -> None:
        for coordinate in ((0, 0), (2, 2)):
            with self.subTest(coordinate=coordinate):
                maze = Maze.create_open(width=3, height=3)

                with self.assertRaisesRegex(
                    ValueError,
                    "Entry and exit cells cannot be blocked.",
                ):
                    maze.block_cell(*coordinate)

    def test_block_cell_rejects_a_disconnecting_block(self) -> None:
        maze = Maze.create_open(width=3, height=2)
        maze.block_cell(1, 0)

        with self.assertRaisesRegex(
            ValueError,
            "Blocking this cell disconnects walkable cells.",
        ):
            maze.block_cell(1, 1)

        self.assertFalse(maze.cell_at((1, 1)).blocked)

    def test_open_passage_rejects_blocked_cells(self) -> None:
        maze = Maze.create_open(width=3, height=3)
        maze.block_cell(1, 1)

        with self.assertRaisesRegex(
            ValueError,
            "Blocked cells cannot have open passages.",
        ):
            maze.open_passage(1, 1, Direction.NORTH)

        with self.assertRaisesRegex(
            ValueError,
            "Blocked cells cannot have open passages.",
        ):
            maze.open_passage(1, 0, Direction.SOUTH)

    def test_validation_ignores_blocked_cells_for_connectivity(self) -> None:
        maze = Maze.create_open(width=3, height=3)
        maze.block_cell(1, 1)

        validated = Maze(
            width=3,
            height=3,
            entry=(0, 0),
            exit=(2, 2),
            cells=maze.cells,
        )

        self.assertTrue(validated.cell_at((1, 1)).blocked)

    def test_rejects_entry_or_exit_on_a_blocked_cell(self) -> None:
        for blocked_coordinate in ((0, 0), (2, 2)):
            with self.subTest(blocked_coordinate=blocked_coordinate):
                maze = Maze.create_open(width=3, height=3)
                blocked_cell = maze.cell_at(blocked_coordinate)
                blocked_cell.blocked = True
                blocked_cell.walls.update(Direction)
                for direction in Direction:
                    neighbor = maze.neighbor_coordinates(
                        *blocked_coordinate,
                        direction,
                    )
                    if neighbor is not None:
                        maze.cell_at(neighbor).walls.add(direction.opposite)

                with self.assertRaisesRegex(
                    ValidationError,
                    "Entry and exit coordinates must be walkable.",
                ):
                    Maze(
                        width=3,
                        height=3,
                        entry=(0, 0),
                        exit=(2, 2),
                        cells=maze.cells,
                    )

    def test_rejects_blocked_cell_without_four_closed_walls(self) -> None:
        maze = Maze.create_open(width=3, height=3)
        maze.cell_at((1, 1)).blocked = True

        with self.assertRaisesRegex(
            ValidationError,
            "Blocked cells must keep all four walls closed.",
        ):
            Maze(
                width=3,
                height=3,
                entry=(0, 0),
                exit=(2, 2),
                cells=maze.cells,
            )

    def test_open_passage_removes_the_two_facing_walls(self) -> None:
        maze = Maze.create(width=2, height=1)

        maze.open_passage(0, 0, Direction.EAST)

        self.assertFalse(maze.cell_at((0, 0)).has_wall(Direction.EAST))
        self.assertFalse(maze.cell_at((1, 0)).has_wall(Direction.WEST))

    def test_close_passage_adds_the_two_facing_walls(self) -> None:
        maze = Maze.create_open(width=2, height=2)

        maze.close_passage(0, 0, Direction.EAST)

        self.assertTrue(maze.cell_at((0, 0)).has_wall(Direction.EAST))
        self.assertTrue(maze.cell_at((1, 0)).has_wall(Direction.WEST))
        self.assertTrue(maze.has_coherent_walls())

    def test_rejects_a_grid_that_does_not_match_its_dimensions(self) -> None:
        with self.assertRaises(ValidationError):
            Maze(
                width=2,
                height=1,
                entry=(0, 0),
                exit=(1, 0),
                cells=[[Cell(x=0, y=0)]],
            )

    def test_detects_incoherent_shared_walls(self) -> None:
        maze = Maze.create(width=2, height=1)
        maze.open_passage(0, 0, Direction.EAST)

        self.assertTrue(maze.has_coherent_walls())

        maze.cell_at((1, 0)).walls.add(Direction.WEST)

        self.assertFalse(maze.has_coherent_walls())


if __name__ == "__main__":
    unittest.main()
