"""Render mazes in the terminal with optional Synthwave colors."""

from collections.abc import Iterable

from mazegen.maze import Direction, Maze
from mazegen.types import Coordinate

_RESET = "\033[0m"
_WALL_COLOR = 51
_PATH_COLOR = "\033[38;5;198m"
_ENTRY_COLOR = "\033[38;5;226m"
_EXIT_COLOR = "\033[38;5;201m"
_BLOCKED_COLOR = "\033[38;5;141m"


def render_maze(
    maze: Maze,
    solution: Iterable[Direction] | None = None,
    *,
    show_solution: bool = True,
    use_color: bool = True,
    wall_color: int = _WALL_COLOR,
) -> str:
    """Render a maze with its endpoints, blocked cells, and optional route.

    Args:
        maze: Maze to render.
        solution: Directions from the maze entry to its exit.
        show_solution: Whether to mark the supplied route.
        use_color: Whether to apply the Synthwave ANSI color palette.
        wall_color: ANSI 256-color code for walls (cyan by default).

    Returns:
        A multiline ASCII representation of the maze.

    Raises:
        ValueError: If the supplied solution leaves the maze, crosses a wall
            or blocked cell, or does not end at the maze exit.
    """
    path_cells = _solution_cells(maze, solution)
    wall_ansi = f"\033[38;5;{wall_color}m"

    def paint(text: str, color: str) -> str:
        """Apply an ANSI foreground color when color output is enabled."""
        if not use_color:
            return text
        return f"{color}{text}{_RESET}"

    lines: list[str] = []
    for y, row in enumerate(maze.cells):
        north_walls = ["+"]
        for cell in row:
            segment = "---" if cell.has_wall(Direction.NORTH) else "   "
            north_walls.append(paint(segment, wall_ansi))
            north_walls.append("+")
        lines.append("".join(north_walls))

        interior: list[str] = []
        for x, cell in enumerate(row):
            west_wall = "|" if cell.has_wall(Direction.WEST) else " "
            interior.append(paint(west_wall, wall_ansi))

            coordinate = (x, y)
            if coordinate == maze.entry:
                marker = paint(" E ", _ENTRY_COLOR)
            elif coordinate == maze.exit:
                marker = paint(" X ", _EXIT_COLOR)
            elif cell.blocked:
                marker = paint("###", _BLOCKED_COLOR)
            elif show_solution and coordinate in path_cells:
                marker = paint(" * ", _PATH_COLOR)
            else:
                marker = "   "
            interior.append(marker)

        east_wall = "|" if row[-1].has_wall(Direction.EAST) else " "
        interior.append(paint(east_wall, wall_ansi))
        lines.append("".join(interior))

    south_walls = ["+"]
    for cell in maze.cells[-1]:
        segment = "---" if cell.has_wall(Direction.SOUTH) else "   "
        south_walls.append(paint(segment, wall_ansi))
        south_walls.append("+")
    lines.append("".join(south_walls))
    return "\n".join(lines)


def _solution_cells(
    maze: Maze,
    solution: Iterable[Direction] | None,
) -> set[Coordinate]:
    """Validate a route and return the coordinates it visits."""
    visited = {maze.entry}
    if solution is None:
        return visited

    coordinate = maze.entry
    for direction in solution:
        if not isinstance(direction, Direction):
            raise ValueError(f"Invalid route direction: {direction!r}.")

        x, y = coordinate
        cell = maze.cell_at(coordinate)
        neighbor = maze.neighbor_coordinates(x, y, direction)
        if neighbor is None:
            raise ValueError("The route leaves the maze bounds.")
        if cell.has_wall(direction):
            raise ValueError("The route crosses a closed wall.")
        if maze.cell_at(neighbor).blocked:
            raise ValueError("The route crosses a blocked cell.")

        coordinate = neighbor
        visited.add(coordinate)

    if coordinate != maze.exit:
        raise ValueError("The route does not end at the maze exit.")
    return visited
