"""Tests for perfect and playable imperfect maze generation."""

from random import Random
from contextlib import redirect_stderr
from io import StringIO
import unittest

from pydantic import ValidationError

from mazegen.generator import MazeGenerator
from mazegen.maze import Direction, Maze


def count_open_internal_passages(maze: Maze) -> int:
    """Count internal passages once by looking east and south."""
    return sum(
        not cell.has_wall(direction)
        for row in maze.cells
        for cell in row
        for direction in (Direction.EAST, Direction.SOUTH)
    )


def wall_masks(maze: Maze) -> list[list[int]]:
    """Return a comparison-friendly representation of maze walls."""
    return [[cell.wall_mask for cell in row] for row in maze.cells]


class MazeGeneratorTests(unittest.TestCase):
    def test_generator_is_an_immutable_pydantic_model(self) -> None:
        generator = MazeGenerator(seed=42)

        with self.assertRaises(ValidationError):
            generator.seed = 7

    def test_initializes_an_open_maze(self) -> None:
        maze = MazeGenerator._new_open_maze(2, 2)

        self.assertFalse(maze.cell_at((0, 0)).has_wall(Direction.EAST))
        self.assertFalse(maze.cell_at((0, 0)).has_wall(Direction.SOUTH))
        self.assertTrue(maze.cell_at((0, 0)).has_wall(Direction.NORTH))
        self.assertTrue(maze.cell_at((0, 0)).has_wall(Direction.WEST))

    def test_closes_an_open_maze_to_a_perfect_maze(self) -> None:
        generator = MazeGenerator(seed=42)
        maze = generator._new_open_maze(3, 2)

        generator._close_perfect_maze(maze, Random(generator.seed))

        self.assertTrue(maze.has_coherent_walls())
        self.assertEqual(count_open_internal_passages(maze), 5)

    def test_generates_a_connected_acyclic_maze(self) -> None:
        maze = MazeGenerator(seed=42).generate_perfect(3, 2, (0, 0), (2, 1))

        self.assertEqual(maze.entry, (0, 0))
        self.assertEqual(maze.exit, (2, 1))
        self.assertTrue(maze.has_coherent_walls())
        self.assertEqual(
            count_open_internal_passages(maze),
            maze.width * maze.height - 1,
        )

    def test_generates_a_perfect_maze_around_pattern42(self) -> None:
        maze = MazeGenerator(seed=42).generate_perfect(10, 9, (0, 0), (9, 8))
        walkable_cells = sum(
            not cell.blocked for row in maze.cells for cell in row
        )
        open_passages = count_open_internal_passages(maze)

        self.assertEqual(
            sum(cell.blocked for row in maze.cells for cell in row),
            26,
        )
        self.assertEqual(open_passages, walkable_cells - 1)

    def test_preserves_explicit_open_and_closed_passages(self) -> None:
        maze = MazeGenerator(seed=42).generate_perfect(
            3,
            2,
            (0, 0),
            (2, 1),
            required_open_passages=[((0, 0), Direction.EAST)],
            protected_closed_passages=[((0, 0), Direction.SOUTH)],
        )

        self.assertFalse(maze.cell_at((0, 0)).has_wall(Direction.EAST))
        self.assertTrue(maze.cell_at((0, 0)).has_wall(Direction.SOUTH))
        self.assertEqual(count_open_internal_passages(maze), 5)

    def test_rejects_a_cycle_in_required_open_passages(self) -> None:
        generator = MazeGenerator()

        with self.assertRaisesRegex(
            ValueError,
            "Required open passages form a cycle.",
        ):
            generator.generate_perfect(
                2,
                2,
                (0, 0),
                (1, 1),
                required_open_passages=[
                    ((0, 0), Direction.EAST),
                    ((1, 0), Direction.SOUTH),
                    ((0, 1), Direction.EAST),
                    ((0, 0), Direction.SOUTH),
                ],
            )

    def test_rejects_one_passage_with_conflicting_constraints(self) -> None:
        generator = MazeGenerator()

        with self.assertRaisesRegex(
            ValueError,
            "A passage cannot be both required open and closed.",
        ):
            generator.generate_perfect(
                2,
                2,
                (0, 0),
                (1, 1),
                required_open_passages=[((1, 0), Direction.WEST)],
                protected_closed_passages=[((0, 0), Direction.EAST)],
            )

    def test_rejects_protected_passages_that_disconnect_the_maze(self) -> None:
        generator = MazeGenerator()

        with self.assertRaisesRegex(
            ValueError,
            "Protected closed passages disconnect the maze.",
        ):
            generator.generate_perfect(
                2,
                2,
                (0, 0),
                (1, 1),
                protected_closed_passages=[
                    ((0, 0), Direction.EAST),
                    ((0, 0), Direction.SOUTH),
                ],
            )

    def test_rejects_an_endpoint_overlapping_pattern42(self) -> None:
        generator = MazeGenerator()

        with self.assertRaisesRegex(
            ValueError,
            "Entry and exit coordinates cannot overlap Pattern42.",
        ):
            generator.generate_perfect(10, 9, (1, 1), (9, 8))

    def test_generates_a_loop_enabled_maze_with_a_cycle(self) -> None:
        maze = MazeGenerator(seed=42).generate_imperfect(3, 3, (0, 0), (2, 2))

        self.assertGreater(
            count_open_internal_passages(maze),
            maze.width * maze.height - 1,
        )

    def test_rejects_a_two_by_two_maze_with_only_one_possible_cycle(
        self,
    ) -> None:
        required_open = [
            ((0, 0), Direction.EAST),
            ((0, 0), Direction.SOUTH),
            ((1, 0), Direction.SOUTH),
            ((0, 1), Direction.EAST),
        ]

        for required in ([], required_open):
            with self.subTest(required=required):
                with self.assertRaisesRegex(ValueError, "two.*cycles"):
                    MazeGenerator(seed=42).generate_imperfect(
                        2, 2, (0, 0), (1, 1), required_open_passages=required
                    )

    def test_repairs_open_areas_without_closing_required_passages(
        self,
    ) -> None:
        required_open = [
            ((x, y), direction)
            for y in range(3)
            for x in range(3)
            for direction, index in ((Direction.EAST, x), (Direction.SOUTH, y))
            if index < 2
        ]
        optional = ((1, 1), Direction.EAST)
        required_open.remove(optional)

        generator = MazeGenerator(seed=42)
        maze = generator.generate_imperfect(
            3, 3, (0, 0), (2, 2), required_open_passages=required_open
        )

        for coordinate, direction in required_open:
            self.assertFalse(maze.cell_at(coordinate).has_wall(direction))
        self.assertTrue(maze.cell_at(optional[0]).has_wall(optional[1]))
        self.assertFalse(generator._has_3x3_open_area(maze))
        self.assertTrue(maze._has_full_connectivity())

    def test_rejects_required_passages_that_force_a_three_by_three_open_area(
        self,
    ) -> None:
        required_open = [
            ((x, y), direction)
            for y in range(3)
            for x in range(3)
            for direction, index in ((Direction.EAST, x), (Direction.SOUTH, y))
            if index < 2
        ]

        with self.assertRaisesRegex(ValueError, "Required.*3x3"):
            MazeGenerator(seed=42).generate_imperfect(
                3, 3, (0, 0), (2, 2), required_open_passages=required_open
            )

    def test_center_does_not_add_unrequested_required_passages(self) -> None:
        optional = ((1, 0), Direction.SOUTH)
        required_open = [
            ((x, y), direction)
            for y in range(3)
            for x in range(3)
            for direction, index in ((Direction.EAST, x), (Direction.SOUTH, y))
            if index < 2 and ((x, y), direction) != optional
        ]
        maze = MazeGenerator(seed=42).generate_imperfect(
            3, 3, (0, 0), (2, 2), required_open_passages=required_open
        )
        self.assertTrue(maze.cell_at(optional[0]).has_wall(optional[1]))
        self.assertLess(len(maze.cell_at((1, 1)).walls), 3)

    def test_preserves_cyclic_open_and_protected_closed_passages(self) -> None:
        required_open = [
            ((0, 0), Direction.EAST),
            ((1, 0), Direction.SOUTH),
            ((0, 1), Direction.EAST),
            ((0, 0), Direction.SOUTH),
        ]
        protected_closed = [((2, 1), Direction.SOUTH)]

        maze = MazeGenerator(seed=42).generate_imperfect(
            3,
            3,
            (0, 0),
            (2, 2),
            required_open_passages=required_open,
            protected_closed_passages=protected_closed,
        )

        for coordinate, direction in required_open:
            with self.subTest(passage=(coordinate, direction)):
                self.assertFalse(maze.cell_at(coordinate).has_wall(direction))
        for coordinate, direction in protected_closed:
            with self.subTest(passage=(coordinate, direction)):
                self.assertTrue(maze.cell_at(coordinate).has_wall(direction))

    def test_preserves_pattern42_connectivity_and_boundaries(self) -> None:
        maze = MazeGenerator(seed=42).generate_imperfect(10, 9, (0, 0), (9, 8))

        self.assertEqual(
            sum(cell.blocked for row in maze.cells for cell in row),
            26,
        )
        self.assertTrue(maze._has_full_connectivity())
        self.assertTrue(maze._has_symmetric_shared_walls())
        self.assertTrue(maze._has_closed_external_borders())

    def test_same_seed_produces_the_same_wall_layout(self) -> None:
        first = MazeGenerator(seed=42).generate_perfect(4, 3, (0, 0), (3, 2))
        second = MazeGenerator(seed=42).generate_perfect(4, 3, (0, 0), (3, 2))

        self.assertEqual(wall_masks(first), wall_masks(second))

    def test_both_modes_warn_when_the_pattern_is_omitted(self) -> None:
        generator = MazeGenerator(seed=42)
        for generate in (generator.generate_perfect,
                         generator.generate_imperfect):
            with self.subTest(mode=generate.__name__):
                stderr = StringIO()
                with redirect_stderr(stderr):
                    generate(3, 3, (0, 0), (2, 2))
                self.assertIn("Pattern omitted", stderr.getvalue())

    def test_unconstrained_imperfect_mazes_have_no_dead_ends(self) -> None:
        for width, height in ((2, 3), (3, 3), (10, 9), (11, 10), (20, 15)):
            for seed in range(12):
                with self.subTest(width=width, height=height, seed=seed):
                    with redirect_stderr(StringIO()):
                        maze = MazeGenerator(seed=seed).generate_imperfect(
                            width, height, (0, 0), (width - 1, height - 1)
                        )
                    dead_ends = [
                        (cell.x, cell.y)
                        for row in maze.cells for cell in row
                        if not cell.blocked and len(cell.walls) == 3
                    ]
                    self.assertEqual(dead_ends, [])
                    walkable_count = sum(
                        not cell.blocked
                        for row in maze.cells for cell in row
                    )
                    open_count = count_open_internal_passages(maze)
                    self.assertGreaterEqual(open_count - walkable_count + 1, 2)
                    self.assertFalse(
                        MazeGenerator()._has_3x3_open_area(maze)
                    )
                    self.assertTrue(maze.has_coherent_walls())
                    self.assertTrue(maze._has_full_connectivity())
                    for coordinate in (
                        (0, 0), (width - 1, 0), (0, height - 1),
                        (width - 1, height - 1), (width // 2, height // 2),
                    ):
                        cell = maze.cell_at(coordinate)
                        self.assertFalse(cell.blocked)
                        self.assertLess(len(cell.walls), 4)

    def test_constraints_are_normalized_in_both_modes(self) -> None:
        generator = MazeGenerator(seed=42)
        for generate in (generator.generate_perfect,
                         generator.generate_imperfect):
            with self.subTest(mode=generate.__name__):
                maze = generate(
                    4, 4, (0, 0), (3, 3),
                    required_open_passages=iter([
                        ((0, 0), Direction.EAST),
                        ((1, 0), Direction.WEST),
                    ]),
                    protected_closed_passages=iter([
                        ((2, 1), Direction.SOUTH),
                        ((2, 2), Direction.NORTH),
                    ]),
                )
                self.assertFalse(maze.cell_at((0, 0)).has_wall(Direction.EAST))
                self.assertTrue(maze.cell_at((2, 1)).has_wall(Direction.SOUTH))

    def test_imperfect_seed_reproduces_a_layout_without_shared_state(
        self,
    ) -> None:
        generator = MazeGenerator(seed=42)
        first = generator.generate_imperfect(20, 15, (0, 0), (19, 14))
        expected = wall_masks(first)
        first.close_passage(0, 0, Direction.EAST)
        second = generator.generate_imperfect(20, 15, (0, 0), (19, 14))
        different = MazeGenerator(seed=43).generate_imperfect(
            20, 15, (0, 0), (19, 14)
        )
        self.assertEqual(expected, wall_masks(second))
        self.assertNotEqual(expected, wall_masks(different))

    def test_both_modes_reject_invalid_passage_constraints(self) -> None:
        generator = MazeGenerator(seed=42)
        for generate in (generator.generate_perfect,
                         generator.generate_imperfect):
            for passage, message in (
                (((-1, 0), Direction.EAST), "start inside"),
                (((0, 0), Direction.NORTH), "outside"),
                (((1, 1), Direction.EAST), "blocked"),
            ):
                with self.subTest(mode=generate.__name__, passage=passage):
                    with self.assertRaisesRegex(ValueError, message):
                        generate(10, 9, (0, 0), (9, 8),
                                 required_open_passages=[passage])

    def test_protected_walls_cannot_reduce_imperfect_mode_to_one_cycle(
        self,
    ) -> None:
        with self.assertRaisesRegex(ValueError, "two independent cycles"):
            MazeGenerator(seed=42).generate_imperfect(
                2, 3, (0, 0), (1, 2),
                protected_closed_passages=[((0, 0), Direction.EAST)],
            )

    def test_rejects_constraints_forcing_more_than_two_dead_ends(self) -> None:
        protected = [
            ((0, 0), Direction.EAST),
            ((4, 0), Direction.WEST),
            ((0, 4), Direction.EAST),
        ]
        with self.assertRaisesRegex(ValueError, "two dead.ends"):
            MazeGenerator(seed=42).generate_imperfect(
                5, 5, (0, 0), (4, 4), protected_closed_passages=protected
            )

    def test_accepts_two_dead_ends_forced_by_protected_walls(self) -> None:
        protected = [
            ((0, 0), Direction.EAST),
            ((4, 0), Direction.WEST),
        ]
        maze = MazeGenerator(seed=42).generate_imperfect(
            5, 5, (0, 0), (4, 4), protected_closed_passages=protected
        )
        self.assertEqual(sum(
            len(cell.walls) == 3
            for row in maze.cells for cell in row if not cell.blocked
        ), 2)
        for coordinate, direction in protected:
            self.assertTrue(maze.cell_at(coordinate).has_wall(direction))

    def test_rejects_single_row_or_column_mazes(self) -> None:
        generator = MazeGenerator()

        for request in ((1, 3, (0, 0), (0, 2)), (3, 1, (0, 0), (2, 0))):
            with self.subTest(request=request):
                with self.assertRaisesRegex(
                    ValueError,
                    "Maze dimensions must be at least 2 by 2.",
                ):
                    generator.generate_perfect(*request)

    def test_rejects_invalid_generation_requests(self) -> None:
        generator = MazeGenerator()
        invalid_requests = (
            (0, 1, (0, 0), (0, 0)),
            (2, 1, (0, 0), (0, 0)),
            (2, 1, (-1, 0), (1, 0)),
            (2, 1, (0, 0), (2, 0)),
        )

        for request in invalid_requests:
            with self.subTest(request=request):
                with self.assertRaises(ValueError):
                    generator.generate_perfect(*request)


if __name__ == "__main__":
    unittest.main()
