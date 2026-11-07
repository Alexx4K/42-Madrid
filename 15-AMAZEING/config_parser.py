"""Parse KEY=VALUE files into validated, immutable maze configurations."""

from pathlib import Path

from pydantic import BaseModel, ConfigDict

from mazegen.types import Coordinate


class MazeConfig(BaseModel):
    """Stores the validated maze configuration parameters.

    Attributes:
        width: Number of horizontal cells in the maze.
        height: Number of vertical cells in the maze.
        entry: Coordinates (x, y) for the maze entry point.
        exit: Coordinates (x, y) for the maze exit point.
        output_file: Target path for the output maze file.
        perfect: True if the maze is a spanning tree (single solution path),
            False if it is a loop-enabled board.
        seed: Optional integer seed for reproducible generation.
    """

    model_config = ConfigDict(frozen=True)

    width: int
    height: int
    entry: Coordinate
    exit: Coordinate
    output_file: str
    perfect: bool
    seed: int | None = None


class ConfigError(Exception):
    """Custom exception for configuration parsing or validation failures."""

    pass


def _parse_bool(value: str) -> bool:
    """Convert a string representation into a boolean value.

    Args:
        value: The string to convert ('true', 'false', '1', '0', etc.).

    Returns:
        The evaluated boolean.

    Raises:
        ConfigError: If the string cannot be parsed as a boolean.
    """
    val = value.strip().lower()
    if val in ("true", "1", "yes"):
        return True
    if val in ("false", "0", "no"):
        return False
    raise ConfigError(f"Invalid boolean value: '{value}'")


def _parse_coords(value: str) -> Coordinate:
    """Parse a 'x,y' string into a pair of integer coordinates.

    Args:
        value: Comma-separated string containing two integers.

    Returns:
        A tuple of (x, y) integers.

    Raises:
        ConfigError: If the format is invalid or values are not integers.
    """
    parts = value.split(",")
    if len(parts) != 2:
        raise ConfigError(
            f"Invalid coordinate format '{value}'. Expected 'x,y'."
        )
    try:
        x, y = int(parts[0].strip()), int(parts[1].strip())
        return x, y
    except ValueError as err:
        raise ConfigError(
            f"Coordinates must be integers, got '{value}'."
        ) from err


def parse_config(filepath: str | Path) -> MazeConfig:
    """Parse and validate a KEY=VALUE maze configuration file.

    Args:
        filepath: Path to the configuration file on disk.

    Returns:
        A frozen MazeConfig instance containing validated settings.

    Raises:
        ConfigError: If the file is unreadable, malformed, missing mandatory
            keys, or contains out-of-bounds coordinates.
    """
    path = Path(filepath)
    if not path.is_file():
        raise ConfigError(f"Configuration file not found: '{filepath}'")

    raw_data: dict[str, str] = {}

    try:
        with path.open("r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                clean_line = line.strip()
                if not clean_line or clean_line.startswith("#"):
                    continue

                if "=" not in clean_line:
                    raise ConfigError(
                        f"Line {line_num}: Invalid syntax '{line.strip()}'."
                    )

                key, value = clean_line.split("=", 1)
                raw_data[key.strip().upper()] = value.strip()
    except Exception as err:
        if isinstance(err, ConfigError):
            raise
        raise ConfigError(f"Failed to read file '{filepath}': {err}") from err

    required_keys = {
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT",
    }
    missing = required_keys - raw_data.keys()
    if missing:
        raise ConfigError(
            f"Missing required configuration keys: {', '.join(missing)}"
        )

    try:
        width = int(raw_data["WIDTH"])
        height = int(raw_data["HEIGHT"])
        entry = _parse_coords(raw_data["ENTRY"])
        exit_coord = _parse_coords(raw_data["EXIT"])
        output_file = raw_data["OUTPUT_FILE"]
        perfect = _parse_bool(raw_data["PERFECT"])
        seed = int(raw_data["SEED"]) if "SEED" in raw_data else None
    except ValueError as err:
        raise ConfigError(f"Data type conversion error: {err}") from err

    if width < 2 or height < 2:
        raise ConfigError("WIDTH and HEIGHT must be at least 2.")

    if not (0 <= entry[0] < width and 0 <= entry[1] < height):
        raise ConfigError(
            f"ENTRY {entry} is out of maze bounds ({width}x{height})."
        )

    if not (0 <= exit_coord[0] < width and 0 <= exit_coord[1] < height):
        raise ConfigError(
            f"EXIT {exit_coord} is out of maze bounds ({width}x{height})."
        )

    if entry == exit_coord:
        raise ConfigError("ENTRY and EXIT coordinates must be different.")

    return MazeConfig(
        width=width,
        height=height,
        entry=entry,
        exit=exit_coord,
        output_file=output_file,
        perfect=perfect,
        seed=seed,
    )
