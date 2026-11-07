"""Serialize mazes in the project hexadecimal interchange format."""

from pathlib import Path

from mazegen.maze import Direction, Maze
from mazegen.solver import Route, solve_shortest_path
from mazegen.types import Coordinate

_DIRECTION_LETTERS: dict[Direction, str] = {
    Direction.NORTH: "N",
    Direction.EAST: "E",
    Direction.SOUTH: "S",
    Direction.WEST: "W",
}


def serialize_maze(maze: Maze) -> str:
    """Return the maze grid, endpoints, and shortest route as text.

    Each grid cell is one uppercase hexadecimal digit whose wall bits follow
    :class:`mazegen.maze.Direction`.  The grid is followed by a blank line,
    entry coordinates, exit coordinates, and the cardinal-direction route.

    Raises:
        ValueError: If the maze is invalid or no route joins its endpoints.
    """
    validated_maze = Maze.model_validate(maze.model_dump())
    route = solve_shortest_path(validated_maze)
    if route is None:
        raise ValueError("The maze entry-to-exit route is unreachable.")

    grid = [
        "".join(f"{cell.wall_mask:X}" for cell in row)
        for row in validated_maze.cells
    ]
    return "\n".join(
        [
            *grid,
            "",
            _format_coordinate(validated_maze.entry),
            _format_coordinate(validated_maze.exit),
            _serialize_route(route),
            "",
        ]
    )


def write_maze(maze: Maze, output_file: str | Path) -> None:
    """Write the hexadecimal serialization of ``maze`` to ``output_file``."""
    Path(output_file).write_text(serialize_maze(maze), encoding="utf-8")


def _format_coordinate(coordinate: Coordinate) -> str:
    """Return a coordinate in the required comma-separated representation."""
    x, y = coordinate
    return f"{x},{y}"


def _serialize_route(route: Route) -> str:
    """Return cardinal directions as compact route letters."""
    return "".join(_DIRECTION_LETTERS[direction] for direction in route)
