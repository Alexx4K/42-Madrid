"""Shortest-path solving with breadth-first search."""

from collections import deque
from typing import TypeAlias

from mazegen.maze import Direction, Maze
from mazegen.types import Coordinate

Route: TypeAlias = list[Direction]


def solve_shortest_path(maze: Maze) -> Route | None:
    """Return a shortest entry-to-exit route, or ``None`` when unreachable."""
    pending = deque([maze.entry])
    visited = {maze.entry}
    predecessors: dict[Coordinate, tuple[Coordinate, Direction]] = {}

    while pending:
        coordinate = pending.popleft()
        if coordinate == maze.exit:
            return _build_route(maze, predecessors)

        x, y = coordinate
        cell = maze.cell_at(coordinate)
        for direction in Direction:
            neighbor = maze.neighbor_coordinates(x, y, direction)
            if neighbor is None:
                continue
            if neighbor in visited:
                continue
            if cell.has_wall(direction):
                continue
            if maze.cell_at(neighbor).blocked:
                continue
            visited.add(neighbor)
            predecessors[neighbor] = (coordinate, direction)
            pending.append(neighbor)

    return None


def _build_route(
    maze: Maze,
    predecessors: dict[Coordinate, tuple[Coordinate, Direction]],
) -> Route:
    """Reconstruct the BFS route from the exit to the entry."""
    route: Route = []
    coordinate = maze.exit
    while coordinate != maze.entry:
        parent, direction = predecessors[coordinate]
        route.append(direction)
        coordinate = parent
    route.reverse()
    return route
