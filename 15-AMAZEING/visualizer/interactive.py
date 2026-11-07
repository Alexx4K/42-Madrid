"""Display and interact with mazes in a terminal on Linux or Windows.

Attributes:
    COLOR_PALETTE: Named Synthwave colors expressed as ANSI 256-color codes.
    COLOR_OPTIONS: Ordered colors available for interactive wall cycling.

Running this module directly starts a demonstration maze.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, replace

from mazegen.generator import MazeGenerator
from mazegen.maze import Direction, Maze
from mazegen.solver import solve_shortest_path
from mazegen.types import Coordinate
from visualizer.ascii_display import render_maze


class Getch:
    """Read a single character using the platform's terminal facilities."""

    def __init__(self) -> None:
        """Select Windows input or save the current POSIX terminal settings."""
        if sys.platform == "win32":
            import msvcrt

            self._getch = msvcrt.getch
        else:
            import termios

            self._fd = sys.stdin.fileno()
            self._old_settings = termios.tcgetattr(self._fd)

    def __call__(self) -> bytes:
        """Read one character and restore POSIX terminal settings afterward."""
        if sys.platform == "win32":
            return self._getch()
        import termios
        import tty

        try:
            tty.setraw(self._fd)
            return sys.stdin.read(1).encode()
        finally:
            termios.tcsetattr(
                self._fd,
                termios.TCSADRAIN,
                self._old_settings,
            )

    def __enter__(self) -> "Getch":
        """Return this reader for use as a context manager."""
        return self

    def __exit__(self, *args: object) -> None:
        """Leave the context; each read already restores terminal settings."""
        pass


@dataclass(frozen=True)
class VisualizerState:
    """Immutable state for the interactive visualizer."""

    maze: Maze
    solution: list[Direction] | None
    show_solution: bool
    use_color: bool
    generator: MazeGenerator
    config_width: int
    config_height: int
    config_entry: Coordinate
    config_exit: Coordinate
    config_perfect: bool
    config_seed: int | None
    last_action: str = ""
    wall_color_index: int = 0


COLOR_PALETTE = {
    "synthwave_cyan": 51,
    "synthwave_magenta": 198,
    "synthwave_yellow": 226,
    "synthwave_pink": 201,
    "synthwave_purple": 141,
    "synthwave_orange": 208,
    "synthwave_green": 82,
    "synthwave_blue": 75,
    "white": 15,
    "gray": 244,
    "dark_gray": 238,
    "red": 196,
    "green": 46,
    "blue": 39,
    "yellow": 226,
    "magenta": 201,
    "cyan": 51,
}

COLOR_OPTIONS = [
    COLOR_PALETTE["synthwave_cyan"],
    COLOR_PALETTE["synthwave_magenta"],
    COLOR_PALETTE["synthwave_yellow"],
    COLOR_PALETTE["synthwave_pink"],
    COLOR_PALETTE["synthwave_purple"],
    COLOR_PALETTE["synthwave_orange"],
    COLOR_PALETTE["synthwave_green"],
    COLOR_PALETTE["synthwave_blue"],
    COLOR_PALETTE["white"],
    COLOR_PALETTE["gray"],
    COLOR_PALETTE["red"],
    COLOR_PALETTE["green"],
    COLOR_PALETTE["blue"],
    COLOR_PALETTE["cyan"],
    COLOR_PALETTE["magenta"],
    COLOR_PALETTE["yellow"],
]


def _cycle_wall_color(state: VisualizerState) -> VisualizerState:
    """Advance the state's wall palette without changing its maze or route."""
    index = (state.wall_color_index + 1) % len(COLOR_OPTIONS)
    return replace(
        state,
        wall_color_index=index,
        last_action=f"Wall color: {COLOR_OPTIONS[index]}",
    )


def _build_initial_state(
    generator: MazeGenerator,
    width: int,
    height: int,
    entry: Coordinate,
    exit: Coordinate,
    perfect: bool,
    seed: int | None,
) -> VisualizerState:
    """Generate initial maze and build state."""
    if perfect:
        maze = generator.generate_perfect(width, height, entry, exit)
    else:
        maze = generator.generate_imperfect(width, height, entry, exit)
    solution = solve_shortest_path(maze)
    return VisualizerState(
        maze=maze,
        solution=solution,
        show_solution=True,
        use_color=True,
        generator=generator,
        config_width=width,
        config_height=height,
        config_entry=entry,
        config_exit=exit,
        config_perfect=perfect,
        config_seed=seed,
    )


def _regenerate_maze(state: VisualizerState) -> VisualizerState:
    """Generate a new maze with the same configuration and no fixed seed.

    A seed of None uses system randomness instead of the configured seed.
    """
    new_generator = MazeGenerator(seed=None)
    if state.config_perfect:
        maze = new_generator.generate_perfect(
            state.config_width,
            state.config_height,
            state.config_entry,
            state.config_exit,
        )
    else:
        maze = new_generator.generate_imperfect(
            state.config_width,
            state.config_height,
            state.config_entry,
            state.config_exit,
        )
    solution = solve_shortest_path(maze)
    return replace(
        state,
        maze=maze,
        solution=solution,
        generator=new_generator,
        last_action="New maze generated",
    )


def _toggle_solution(state: VisualizerState) -> VisualizerState:
    """Toggle solution visibility."""
    action = "shown" if not state.show_solution else "hidden"
    return replace(
        state,
        show_solution=not state.show_solution,
        last_action=f"Solution {action}",
    )


def _toggle_color_mode(state: VisualizerState) -> VisualizerState:
    """Toggle color mode on/off."""
    action = "enabled" if not state.use_color else "disabled"
    return replace(
        state,
        use_color=not state.use_color,
        last_action=f"Colors {action}",
    )


def _clear_screen() -> None:
    """Clear the terminal screen."""
    print("\033[2J\033[H", end="")


def _render_state(state: VisualizerState) -> str:
    """Render the current state to a string."""
    maze_str = render_maze(
        maze=state.maze,
        solution=state.solution if state.show_solution else None,
        show_solution=state.show_solution,
        use_color=state.use_color,
        wall_color=COLOR_OPTIONS[state.wall_color_index % len(COLOR_OPTIONS)],
    )

    mode_str = "Perfect" if state.config_perfect else "Imperfect"
    gen_seed = state.generator.seed
    seed_str = str(gen_seed) if gen_seed is not None else "random"

    help_lines = [
        "",
        f"Mode: {mode_str} | Size: "
        f"{state.config_width}x{state.config_height} | Seed: {seed_str}",
        "",
        "Controls:",
        "  R - Regenerate maze (new seed)",
        "  S - Show/Hide solution",
        "  C - Cycle wall color",
        "  N - Toggle colors ON/OFF",
        "  Q / Esc / Ctrl-C - Quit",
        "",
    ]

    if state.last_action:
        help_lines.insert(0, f"-> {state.last_action}")
        help_lines.insert(1, "")

    return maze_str + "\n" + "\n".join(help_lines)


def _handle_key(state: VisualizerState, key: bytes) -> VisualizerState | None:
    """Handle a case-insensitive keyboard command.

    R regenerates the maze, S toggles the solution, C cycles wall colors,
    and N toggles color output.
    Q, Escape, and raw Ctrl-C return None to quit; other keys do nothing.
    """
    key_str = key.decode("utf-8", errors="ignore").lower()

    if key_str in ("q", "\x1b", "\x03"):
        return None
    if key_str == "r":
        return _regenerate_maze(state)
    if key_str == "s":
        return _toggle_solution(state)
    if key_str == "c":
        return _cycle_wall_color(state)
    if key_str == "n":
        return _toggle_color_mode(state)
    return state


def run_interactive(
    width: int,
    height: int,
    entry: Coordinate,
    exit: Coordinate,
    perfect: bool,
    seed: int | None = None,
) -> None:
    """Generate the initial maze and run the terminal interaction loop.

    Render the current state, read a key, and apply the resulting action
    until the user quits. Clear the terminal and print a farewell on exit.
    """
    getch = Getch()

    generator = MazeGenerator(seed=seed)
    state = _build_initial_state(
        generator, width, height, entry, exit, perfect, seed
    )

    try:
        while True:
            _clear_screen()
            output = _render_state(state)
            print(output, end="")
            sys.stdout.flush()

            key = getch()
            new_state = _handle_key(state, key)
            if new_state is None:
                break
            state = new_state
    except KeyboardInterrupt:
        pass
    finally:
        _clear_screen()
        print("Goodbye!")


if __name__ == "__main__":
    run_interactive(
        width=20,
        height=10,
        entry=(0, 0),
        exit=(19, 9),
        perfect=False,
        seed=42,
    )
