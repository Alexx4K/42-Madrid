"""Command-line entry point for the A-Maze-ing project."""

from __future__ import annotations

import argparse
import os
import sys

from config_parser import ConfigError, MazeConfig, parse_config
from mazegen.generator import MazeGenerator
from output_writer import write_maze
from visualizer import run_interactive


def _run_interactive_mode(config: MazeConfig) -> int:
    """Run the interactive maze visualizer."""
    try:
        run_interactive(
            width=config.width,
            height=config.height,
            entry=config.entry,
            exit=config.exit,
            perfect=config.perfect,
            seed=config.seed,
        )
    except KeyboardInterrupt:
        pass
    except Exception as error:
        print(f"Interactive mode error: {error}", file=sys.stderr)
        return 1
    return 0


def _run_generation_mode(config: MazeConfig) -> int:
    """Run the standard maze generation mode."""
    lines = [
        "Configuration loaded:",
        f"Size: {config.width}x{config.height}",
        f"Entry: {config.entry[0]},{config.entry[1]}",
        f"Exit: {config.exit[0]},{config.exit[1]}",
        f"Perfect: {'yes' if config.perfect else 'no'}",
        f"Output file: {config.output_file}",
    ]
    if config.seed is not None:
        lines.append(f"Seed: {config.seed}")

    try:
        generator = MazeGenerator(seed=config.seed)
        if config.perfect:
            maze = generator.generate_perfect(
                config.width,
                config.height,
                config.entry,
                config.exit,
            )
        else:
            maze = generator.generate_imperfect(
                config.width,
                config.height,
                config.entry,
                config.exit,
            )
    except ValueError as error:
        print(
            f"Could not generate the maze: {error}",
            file=sys.stderr,
        )
        raise SystemExit(2)

    try:
        write_maze(maze, config.output_file)
    except (OSError, ValueError) as error:
        print(
            f"Could not write the output file: {error}",
            file=sys.stderr,
        )
        raise SystemExit(2)

    lines.append(f"Maze generated and written to: {config.output_file}")
    try:
        print("\n".join(lines), flush=True)
    except BrokenPipeError as error:
        with open(os.devnull, "w") as null_output:
            os.dup2(null_output.fileno(), sys.stdout.fileno())
        print(f"Could not display the output: {error}", file=sys.stderr)
        raise SystemExit(2)
    except UnicodeEncodeError as error:
        print(f"Could not display the output: {error}", file=sys.stderr)
        raise SystemExit(2)
    return 0


def _main() -> int:
    """Parse arguments and run the requested maze generation mode."""
    parser = argparse.ArgumentParser(
        description="A-Maze-ing maze generator",
    )
    parser.add_argument(
        "config",
        help="Path to the KEY=VALUE configuration file",
    )
    parser.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        help="Run the interactive terminal visualizer",
    )

    args = parser.parse_args()

    try:
        config = parse_config(args.config)
    except ConfigError as error:
        parser.error(str(error))

    if args.interactive:
        return _run_interactive_mode(config)
    return _run_generation_mode(config)


def main() -> int:
    """Run the CLI and report unexpected application errors cleanly."""
    try:
        return _main()
    except Exception as error:
        print(
            f"Unexpected {type(error).__name__}: {error}",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
