"""Domain models for maze cells and structure."""

from collections import deque
from enum import IntEnum

from pydantic import BaseModel, ConfigDict, Field, model_validator

from mazegen.types import Coordinate


class Direction(IntEnum):
    """Cardinal directions and their hexadecimal output bits."""

    NORTH = 0b0001
    EAST = 0b0010
    SOUTH = 0b0100
    WEST = 0b1000

    @property
    def opposite(self) -> "Direction":
        """Return the direction of the adjacent cell that faces this one."""
        return {
            Direction.NORTH: Direction.SOUTH,
            Direction.EAST: Direction.WEST,
            Direction.SOUTH: Direction.NORTH,
            Direction.WEST: Direction.EAST,
        }[self]

    @property
    def delta(self) -> Coordinate:
        """Return the coordinate offset associated with this direction."""
        return {
            Direction.NORTH: (0, -1),
            Direction.EAST: (1, 0),
            Direction.SOUTH: (0, 1),
            Direction.WEST: (-1, 0),
        }[self]


class Cell(BaseModel):
    """A cell identified by coordinates and bounded by four walls."""

    model_config = ConfigDict(validate_assignment=True)

    x: int = Field(ge=0)
    y: int = Field(ge=0)
    walls: set[Direction] = Field(default_factory=lambda: set(Direction))
    blocked: bool = False

    @property
    def wall_mask(self) -> int:
        """Return wall flags packed into the hexadecimal output mask."""
        return sum(direction.value for direction in self.walls)

    def has_wall(self, direction: Direction) -> bool:
        """Return whether this cell is closed in ``direction``."""
        return direction in self.walls


class Maze(BaseModel):
    """Mutable cell grid indexed by ``(x, y)`` coordinates."""

    model_config = ConfigDict(validate_assignment=True)

    width: int = Field(gt=0)
    height: int = Field(gt=0)
    entry: Coordinate
    exit: Coordinate
    cells: list[list[Cell]]

    @model_validator(mode="after")
    def validate_grid(self) -> "Maze":
        """Ensure that the stored cells form the declared rectangular grid."""
        if len(self.cells) != self.height:
            raise ValueError("The number of cell rows must match height.")

        if not self._is_in_bounds(self.entry):
            raise ValueError(
                "Entry coordinates must be inside the maze bounds."
            )
        if not self._is_in_bounds(self.exit):
            raise ValueError(
                "Exit coordinates must be inside the maze bounds."
            )
        if self.entry == self.exit:
            raise ValueError("Entry and exit coordinates must be distinct.")

        for y, row in enumerate(self.cells):
            if len(row) != self.width:
                raise ValueError("Every cell row must match width.")
            for x, cell in enumerate(row):
                if (cell.x, cell.y) != (x, y):
                    raise ValueError(
                        "Cell coordinates must match their grid position."
                    )

        entry_cell = self.cell_at(self.entry)
        exit_cell = self.cell_at(self.exit)
        if entry_cell.blocked or exit_cell.blocked:
            raise ValueError("Entry and exit coordinates must be walkable.")

        if not self._has_closed_blocked_cells():
            raise ValueError("Blocked cells must keep all four walls closed.")
        if not self._has_closed_external_borders():
            raise ValueError("External maze borders must remain closed.")
        if not self._has_symmetric_shared_walls():
            raise ValueError("Shared walls must agree between adjacent cells.")
        if not self._has_full_connectivity():
            raise ValueError(
                "Every maze cell must be reachable through open passages."
            )
        return self

    def _is_in_bounds(self, coordinate: Coordinate) -> bool:
        """Return whether a coordinate belongs to this maze."""
        x, y = coordinate
        return 0 <= x < self.width and 0 <= y < self.height

    def _has_closed_external_borders(self) -> bool:
        """Return whether all walls that face outside the grid are closed."""
        for y, row in enumerate(self.cells):
            for x, cell in enumerate(row):
                for direction in Direction:
                    if self.neighbor_coordinates(x, y, direction) is None:
                        if not cell.has_wall(direction):
                            return False
        return True

    def _has_closed_blocked_cells(self) -> bool:
        """Return whether every blocked cell has all four walls closed."""
        for row in self.cells:
            for cell in row:
                if cell.blocked and cell.walls != set(Direction):
                    return False
        return True

    def _has_symmetric_shared_walls(self) -> bool:
        """Return whether internal walls agree from both adjacent cells."""
        for y, row in enumerate(self.cells):
            for x, cell in enumerate(row):
                for direction in Direction:
                    neighbor = self.neighbor_coordinates(x, y, direction)
                    if neighbor is not None:
                        neighbor_cell = self.cell_at(neighbor)
                        if cell.has_wall(direction) != neighbor_cell.has_wall(
                            direction.opposite
                        ):
                            return False
        return True

    def _has_full_connectivity(self) -> bool:
        """Return whether every walkable cell can be reached by passages."""
        reachable = {self.entry}
        pending = deque([self.entry])
        while pending:
            x, y = pending.popleft()
            cell = self.cell_at((x, y))
            for direction in Direction:
                neighbor = self.neighbor_coordinates(x, y, direction)
                if neighbor is None or cell.has_wall(direction):
                    continue
                neighbor_cell = self.cell_at(neighbor)
                if not neighbor_cell.blocked and neighbor not in reachable:
                    reachable.add(neighbor)
                    pending.append(neighbor)
        walkable_cells = sum(
            not cell.blocked for row in self.cells for cell in row
        )
        return len(reachable) == walkable_cells

    @classmethod
    def create(cls, width: int, height: int) -> "Maze":
        """Create a rectangular maze whose cells start fully closed."""
        return cls.model_construct(
            width=width,
            height=height,
            entry=(0, 0),
            exit=(width - 1, height - 1),
            cells=[
                [Cell(x=x, y=y) for x in range(width)]
                for y in range(height)
            ],
        )

    @classmethod
    def create_open(cls, width: int, height: int) -> "Maze":
        """Create a maze with open internal passages and closed borders."""
        if width < 2 or height < 2:
            raise ValueError(
                "Open mazes require at least two rows and columns."
            )
        return cls.model_construct(
            width=width,
            height=height,
            entry=(0, 0),
            exit=(width - 1, height - 1),
            cells=[
                [
                    Cell(
                        x=x,
                        y=y,
                        walls={
                            direction
                            for direction in Direction
                            if not all(
                                0 <= coordinate < size
                                for coordinate, size in (
                                    (x + direction.delta[0], width),
                                    (y + direction.delta[1], height),
                                )
                            )
                        },
                    )
                    for x in range(width)
                ]
                for y in range(height)
            ],
        )

    def cell_at(self, coordinate: Coordinate) -> Cell:
        """Return the cell stored at ``coordinate``."""
        x, y = coordinate
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise IndexError(f"Cell ({x}, {y}) is outside the maze bounds.")
        return self.cells[y][x]

    def neighbor_coordinates(
        self,
        x: int,
        y: int,
        direction: Direction,
    ) -> Coordinate | None:
        """Return adjacent coordinates, or ``None`` at an external border."""
        self.cell_at((x, y))
        delta_x, delta_y = direction.delta
        neighbor_x, neighbor_y = x + delta_x, y + delta_y
        if 0 <= neighbor_x < self.width and 0 <= neighbor_y < self.height:
            return neighbor_x, neighbor_y
        return None

    def open_passage(self, x: int, y: int, direction: Direction) -> None:
        """Open the shared wall between a cell and its neighbor."""
        neighbor = self.neighbor_coordinates(x, y, direction)
        if neighbor is None:
            raise ValueError("An external maze border cannot be opened.")

        cell = self.cell_at((x, y))
        neighbor_cell = self.cell_at(neighbor)
        if cell.blocked or neighbor_cell.blocked:
            raise ValueError("Blocked cells cannot have open passages.")
        cell.walls.discard(direction)
        neighbor_cell.walls.discard(direction.opposite)

    def close_passage(self, x: int, y: int, direction: Direction) -> None:
        """Close the shared wall between a cell and its neighbor."""
        neighbor = self.neighbor_coordinates(x, y, direction)
        if neighbor is None:
            raise ValueError("An external maze border cannot be closed.")

        cell = self.cell_at((x, y))
        neighbor_cell = self.cell_at(neighbor)
        cell.walls.add(direction)
        neighbor_cell.walls.add(direction.opposite)

    def block_cell(self, x: int, y: int) -> None:
        """Make one cell unreachable while preserving wall symmetry."""
        if (x, y) == self.entry or (x, y) == self.exit:
            raise ValueError("Entry and exit cells cannot be blocked.")
        cell = self.cell_at((x, y))
        previous_blocked = cell.blocked
        previous_walls = set(cell.walls)
        neighboring_walls: dict[Coordinate, set[Direction]] = {}
        for direction in Direction:
            neighbor = self.neighbor_coordinates(x, y, direction)
            if neighbor is not None:
                neighboring_walls[neighbor] = set(self.cell_at(neighbor).walls)

        cell.blocked = True
        cell.walls.update(Direction)
        for direction in Direction:
            neighbor = self.neighbor_coordinates(x, y, direction)
            if neighbor is not None:
                self.cell_at(neighbor).walls.add(direction.opposite)
        if self._has_full_connectivity():
            return

        cell.blocked = previous_blocked
        cell.walls = previous_walls
        for neighbor, walls in neighboring_walls.items():
            self.cell_at(neighbor).walls = walls
        raise ValueError("Blocking this cell disconnects walkable cells.")

    def has_coherent_walls(self) -> bool:
        """Check shared-wall symmetry and closed external borders."""
        return self._has_closed_external_borders() and (
            self._has_symmetric_shared_walls()
        )
