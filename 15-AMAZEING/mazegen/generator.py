"""Maze generation strategies and public facade."""

from collections.abc import Iterable
from random import Random
from typing import TypeAlias

from pydantic import BaseModel, ConfigDict

from mazegen.maze import Direction, Maze
from mazegen.pattern42 import Pattern42
from mazegen.types import Coordinate


Passage: TypeAlias = tuple[Coordinate, Direction]


class MazeGenerator(BaseModel):
    """Generate mazes with an optional reproducible random seed."""

    model_config = ConfigDict(frozen=True)

    seed: int | None = None

    @staticmethod
    def _validate_request(
        width: int,
        height: int,
        entry: Coordinate,
        exit: Coordinate,
    ) -> None:
        """Validate dimensions and endpoint coordinates for generation."""
        if width < 2 or height < 2:
            raise ValueError("Maze dimensions must be at least 2 by 2.")
        if entry == exit:
            raise ValueError("Entry and exit coordinates must be distinct.")

        for name, coordinate in (("Entry", entry), ("Exit", exit)):
            x, y = coordinate
            if not (0 <= x < width and 0 <= y < height):
                raise ValueError(
                    f"{name} coordinates must be inside the maze."
                )

    @staticmethod
    def _new_open_maze(width: int, height: int) -> Maze:
        """Create the open maze grid that generation will close."""
        return Maze.create_open(width, height)

    def _close_perfect_maze(
        self,
        maze: Maze,
        random_source: Random,
        required_open_passages: frozenset[Passage] = frozenset(),
        protected_closed_passages: frozenset[Passage] = frozenset(),
    ) -> None:
        """Close cycles while preserving one path between walkable cells."""
        parent = {
            (cell.x, cell.y): (cell.x, cell.y)
            for row in maze.cells
            for cell in row
            if not cell.blocked
        }
        for coordinate, direction in required_open_passages:
            neighbor = maze.neighbor_coordinates(*coordinate, direction)
            if neighbor is None:
                raise ValueError(
                    "Required passages cannot face outside the maze."
                )
            source_root = self._root(parent, coordinate)
            neighbor_root = self._root(parent, neighbor)
            if source_root == neighbor_root:
                raise ValueError("Required open passages form a cycle.")
            parent[source_root] = neighbor_root

        passages: list[tuple[Coordinate, Direction]] = []

        for row in maze.cells:
            for cell in row:
                coordinate = (cell.x, cell.y)
                if cell.blocked:
                    continue
                for direction in (Direction.EAST, Direction.SOUTH):
                    neighbor = maze.neighbor_coordinates(
                        *coordinate,
                        direction,
                    )
                    if neighbor is None or cell.has_wall(direction):
                        continue
                    if not maze.cell_at(neighbor).blocked:
                        passages.append((coordinate, direction))

        random_source.shuffle(passages)
        for coordinate, direction in passages:
            neighbor = maze.neighbor_coordinates(*coordinate, direction)
            if neighbor is None:
                continue
            passage = (coordinate, direction)
            if passage in required_open_passages:
                continue
            if passage in protected_closed_passages:
                maze.close_passage(*coordinate, direction)
                continue
            source_root = self._root(parent, coordinate)
            neighbor_root = self._root(parent, neighbor)
            if source_root == neighbor_root:
                maze.close_passage(*coordinate, direction)
                continue
            parent[source_root] = neighbor_root

        roots = {self._root(parent, coordinate) for coordinate in parent}
        if len(roots) != 1:
            raise ValueError("Protected closed passages disconnect the maze.")

    @staticmethod
    def _normalize_passages(
        maze: Maze,
        passages: Iterable[Passage],
        constraint_name: str,
    ) -> frozenset[Passage]:
        """Validate passages and give each shared wall one representation."""
        normalized: set[Passage] = set()
        for coordinate, direction in passages:
            if not isinstance(direction, Direction):
                raise ValueError(f"{constraint_name} must use a Direction.")
            try:
                neighbor = maze.neighbor_coordinates(*coordinate, direction)
            except (IndexError, TypeError):
                raise ValueError(
                    f"{constraint_name} must start inside the maze."
                ) from None
            if neighbor is None:
                raise ValueError(
                    f"{constraint_name} cannot face outside the maze."
                )
            source_cell = maze.cell_at(coordinate)
            neighbor_cell = maze.cell_at(neighbor)
            if source_cell.blocked or neighbor_cell.blocked:
                raise ValueError(
                    f"{constraint_name} cannot touch blocked cells."
                )
            if direction in (Direction.EAST, Direction.SOUTH):
                normalized.add((coordinate, direction))
            else:
                normalized.add((neighbor, direction.opposite))
        return frozenset(normalized)

    @staticmethod
    def _root(
        parent: dict[Coordinate, Coordinate],
        coordinate: Coordinate,
    ) -> Coordinate:
        """Return the root of a Union-Find component."""
        while parent[coordinate] != coordinate:
            coordinate = parent[coordinate]
        return coordinate

    def generate_perfect(
        self,
        width: int,
        height: int,
        entry: Coordinate,
        exit: Coordinate,
        required_open_passages: Iterable[Passage] = (),
        protected_closed_passages: Iterable[Passage] = (),
    ) -> Maze:
        """Generate a perfect maze while honoring explicit wall constraints.

        Pattern42 is centered when it fits; otherwise a warning is printed
        to stderr. A randomized Kruskal spanning tree connects every walkable
        cell with exactly one route between any two cells. The generator's
        seed reproduces the same layout for the same request.

        Args:
            width: Number of columns, at least two.
            height: Number of rows, at least two.
            entry: Walkable entry coordinates inside the maze.
            exit: Walkable exit coordinates, distinct from the entry.
            required_open_passages: Internal passages that must stay open.
            protected_closed_passages: Internal walls that must stay closed.

        Returns:
            A connected, acyclic maze with symmetric shared walls and closed
            external borders. Blocked pattern cells are excluded from paths.

        Raises:
            ValueError: If dimensions or endpoints are invalid, an endpoint
                overlaps Pattern42, passage constraints are invalid or
                conflicting, required passages form a cycle, or protected
                walls disconnect the walkable cells.
        """
        self._validate_request(width, height, entry, exit)
        random_source = Random(self.seed)
        open_maze = self._new_open_maze(width, height)
        maze = Maze(
            width=width,
            height=height,
            entry=entry,
            exit=exit,
            cells=open_maze.cells,
        )
        Pattern42.apply(maze, quiet=False)
        required_open = self._normalize_passages(
            maze,
            required_open_passages,
            "Required open passages",
        )
        protected_closed = self._normalize_passages(
            maze,
            protected_closed_passages,
            "Protected closed passages",
        )
        if required_open & protected_closed:
            raise ValueError(
                "A passage cannot be both required open and closed."
            )
        self._close_perfect_maze(
            maze,
            random_source,
            required_open,
            protected_closed,
        )
        return Maze(
            width=width,
            height=height,
            entry=entry,
            exit=exit,
            cells=maze.cells,
        )

    def generate_imperfect(
        self,
        width: int,
        height: int,
        entry: Coordinate,
        exit: Coordinate,
        required_open_passages: Iterable[Passage] = (),
        protected_closed_passages: Iterable[Passage] = (),
    ) -> Maze:
        """Generate a connected maze with deliberately retained cycles.

        Apply Pattern42, warning when the grid is too small, then build a
        randomized spanning tree around the required passages. Retain extra
        edges for loops and braid remaining dead ends using optional edges.
        Repair fully open 3x3 areas without introducing dead ends or breaking
        connectivity. Finally verify at least two independent cycles and at
        most two dead ends, excluding blocked pattern cells. The mask leaves
        all corners and the center walkable; connectivity keeps them usable.

        Args:
            width: Number of columns, at least two.
            height: Number of rows, at least two.
            entry: Walkable entry coordinates.
            exit: Walkable exit coordinates, distinct from the entry.
            required_open_passages: Internal passages that must stay open.
            protected_closed_passages: Internal walls that must stay closed.

        Returns:
            A connected maze honoring the supplied wall constraints.

        Raises:
            ValueError: If dimensions, endpoints, or constraints are invalid,
                two cycles are unavailable, protected walls force more than
                two dead ends, or a 3x3 area cannot be repaired safely while
                preserving required passages.
        """
        self._validate_request(width, height, entry, exit)
        random_source = Random(self.seed)
        open_maze = self._new_open_maze(width, height)
        maze = Maze(
            width=width,
            height=height,
            entry=entry,
            exit=exit,
            cells=open_maze.cells,
        )

        Pattern42.apply(maze, quiet=False)

        required_open = self._normalize_passages(
            maze,
            required_open_passages,
            "Required open passages",
        )
        protected_closed = self._normalize_passages(
            maze,
            protected_closed_passages,
            "Protected closed passages",
        )

        if required_open & protected_closed:
            raise ValueError(
                "A passage cannot be both required open and closed."
            )

        passages: list[Passage] = []
        for row in maze.cells:
            for cell in row:
                if cell.blocked:
                    continue
                for direction in (Direction.EAST, Direction.SOUTH):
                    coordinate = (cell.x, cell.y)
                    neighbor = maze.neighbor_coordinates(
                        *coordinate,
                        direction,
                    )
                    if neighbor is None or maze.cell_at(neighbor).blocked:
                        continue
                    passages.append((coordinate, direction))
        parent = {
            (cell.x, cell.y): (cell.x, cell.y)
            for row in maze.cells
            for cell in row
            if not cell.blocked
        }
        selected_passages = set(required_open)
        for coordinate, direction in required_open:
            neighbor = maze.neighbor_coordinates(*coordinate, direction)
            if neighbor is not None:
                source_root = self._root(parent, coordinate)
                neighbor_root = self._root(parent, neighbor)
                if source_root != neighbor_root:
                    parent[source_root] = neighbor_root

        candidates: list[Passage] = []
        for passage in passages:
            if passage in selected_passages or passage in protected_closed:
                continue
            candidates.append(passage)
        random_source.shuffle(candidates)

        for coordinate, direction in candidates:
            neighbor = maze.neighbor_coordinates(*coordinate, direction)
            if neighbor is None:
                continue
            source_root = self._root(parent, coordinate)
            neighbor_root = self._root(parent, neighbor)
            if source_root != neighbor_root:
                parent[source_root] = neighbor_root
                selected_passages.add((coordinate, direction))

        roots = {self._root(parent, coordinate) for coordinate in parent}
        if len(roots) != 1:
            raise ValueError("Protected closed passages disconnect the maze.")

        cycle_candidates = [
            passage
            for passage in candidates
            if passage not in selected_passages
        ]
        cycles_added = 0
        target_cycles = max(2, len(cycle_candidates) // 10)

        for passage in cycle_candidates:
            if cycles_added >= target_cycles:
                break
            selected_passages.add(passage)
            cycles_added += 1

        remaining = [p for p in cycle_candidates if p not in selected_passages]
        for passage in remaining:
            if random_source.random() < 0.5:
                selected_passages.add(passage)

        for coordinate, direction in passages:
            if (coordinate, direction) not in selected_passages:
                maze.close_passage(*coordinate, direction)

        # Opening an optional edge incident to a leaf removes that dead end
        # without threatening connectivity or any protected wall.
        for coordinate, direction in candidates:
            cell = maze.cell_at(coordinate)
            neighbor = maze.neighbor_coordinates(*coordinate, direction)
            if neighbor is None or not cell.has_wall(direction):
                continue
            neighbor_cell = maze.cell_at(neighbor)
            if len(cell.walls) == 3 or len(neighbor_cell.walls) == 3:
                maze.open_passage(*coordinate, direction)

        if self._has_3x3_open_area(maze):
            self._fix_3x3_open_areas(maze, random_source, required_open)

        walkable_count = sum(
            not cell.blocked for row in maze.cells for cell in row
        )
        open_count = sum(
            not maze.cell_at(coordinate).has_wall(direction)
            for coordinate, direction in passages
        )
        if open_count - walkable_count + 1 < 2:
            raise ValueError(
                "Imperfect mazes require at least two independent cycles."
            )
        dead_ends = sum(
            len(cell.walls) == 3
            for row in maze.cells for cell in row if not cell.blocked
        )
        if dead_ends > 2:
            raise ValueError(
                "Protected closed passages force more than two dead ends."
            )

        return Maze(
            width=width,
            height=height,
            entry=entry,
            exit=exit,
            cells=maze.cells,
        )

    def _has_3x3_open_area(self, maze: Maze) -> bool:
        """Check whether nine walkable cells form a fully open 3x3 area.

        Inspect each candidate square for blocked cells, then check both
        sides of every shared wall using east and south neighbor pairs.
        """
        for y in range(maze.height - 2):
            for x in range(maze.width - 2):
                all_open = True
                for dy in range(3):
                    for dx in range(3):
                        cell = maze.cell_at((x + dx, y + dy))
                        if cell.blocked:
                            all_open = False
                            break
                    if not all_open:
                        break
                if all_open:
                    internal_open = True
                    for dy in range(3):
                        for dx in range(3):
                            cx, cy = x + dx, y + dy
                            cell = maze.cell_at((cx, cy))
                            if dx < 2:
                                right = maze.cell_at((cx + 1, cy))
                                east_closed = cell.has_wall(
                                    Direction.EAST
                                ) or right.has_wall(Direction.WEST)
                                if east_closed:
                                    internal_open = False
                                    break
                            if dy < 2:
                                bottom = maze.cell_at((cx, cy + 1))
                                south_closed = cell.has_wall(
                                    Direction.SOUTH
                                ) or bottom.has_wall(Direction.NORTH)
                                if south_closed:
                                    internal_open = False
                                    break
                        if not internal_open:
                            break
                    if internal_open:
                        return True
        return False

    def _fix_3x3_open_areas(
        self,
        maze: Maze,
        random_source: Random,
        required_open_passages: frozenset[Passage],
    ) -> None:
        """Break fully open 3x3 areas without violating required passages.

        Skip squares containing blocked cells or fewer than twelve open
        internal passages. For each fully open square, close one optional
        passage whose endpoints both have degree at least three. Alternate
        paths within the square preserve connectivity, and the degree bound
        avoids introducing dead ends. A full 3x3 has four independent cycles,
        so this closure cannot reduce the maze below two cycles.

        Args:
            maze: Maze to modify in place.
            random_source: Random source used to choose optional passages.
            required_open_passages: Normalized passages that must stay open.

        Raises:
            ValueError: If required passages leave no optional internal edge
                that can be closed without introducing a dead end.
        """
        for y in range(maze.height - 2):
            for x in range(maze.width - 2):
                all_open = True
                for dy in range(3):
                    for dx in range(3):
                        if maze.cell_at((x + dx, y + dy)).blocked:
                            all_open = False
                            break
                    if not all_open:
                        break
                if not all_open:
                    continue

                internal_passages = []
                for dy in range(3):
                    for dx in range(3):
                        cx, cy = x + dx, y + dy
                        cell = maze.cell_at((cx, cy))
                        if dx < 2:
                            right = maze.cell_at((cx + 1, cy))
                            east_open = not cell.has_wall(
                                Direction.EAST
                            ) and not right.has_wall(Direction.WEST)
                            if east_open:
                                internal_passages.append(
                                    ((cx, cy), Direction.EAST)
                                )
                        if dy < 2:
                            bottom = maze.cell_at((cx, cy + 1))
                            south_open = not cell.has_wall(
                                Direction.SOUTH
                            ) and not bottom.has_wall(Direction.NORTH)
                            if south_open:
                                internal_passages.append(
                                    ((cx, cy), Direction.SOUTH)
                                )

                if len(internal_passages) != 12:
                    continue

                optional_passages = []
                for coordinate, direction in internal_passages:
                    if (coordinate, direction) in required_open_passages:
                        continue
                    dx, dy = direction.delta
                    neighbor = (coordinate[0] + dx, coordinate[1] + dy)
                    walls = max(
                        len(maze.cell_at(coordinate).walls),
                        len(maze.cell_at(neighbor).walls),
                    )
                    if walls <= 1:
                        optional_passages.append((coordinate, direction))
                if not optional_passages:
                    raise ValueError(
                        "Required open passages prevent repairing a 3x3 "
                        "open area without introducing dead ends."
                    )

                coordinate, direction = random_source.choice(optional_passages)
                maze.close_passage(*coordinate, direction)
