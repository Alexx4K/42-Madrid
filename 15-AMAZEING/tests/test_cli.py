"""Tests for the command-line entry point."""

from contextlib import redirect_stderr, redirect_stdout
from io import BytesIO, StringIO, TextIOWrapper
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from a_maze_ing import main
from mazegen import Pattern42


class CommandLineTests(unittest.TestCase):
    def test_reports_unexpected_errors_without_a_traceback(self) -> None:
        """Keep unexpected application failures inside the CLI boundary."""
        for error_type in (RuntimeError, MemoryError, OSError):
            with self.subTest(error_type=error_type.__name__):
                stderr = StringIO()
                with (
                    patch("sys.argv", ["a_maze_ing.py", "unused.conf"]),
                    patch(
                        "a_maze_ing.parse_config",
                        side_effect=error_type("unexpected failure"),
                    ),
                    redirect_stderr(stderr),
                ):
                    exit_code = main()

                self.assertEqual(exit_code, 1)
                self.assertIn(error_type.__name__, stderr.getvalue())
                self.assertIn("unexpected failure", stderr.getvalue())
                self.assertNotIn("Traceback", stderr.getvalue())

    def test_help_describes_both_modes_in_english(self) -> None:
        stdout = StringIO()
        with (
            patch("sys.argv", ["a_maze_ing.py", "--help"]),
            redirect_stdout(stdout),
            self.assertRaises(SystemExit) as raised,
        ):
            main()

        self.assertEqual(raised.exception.code, 0)
        self.assertIn("A-Maze-ing maze generator", stdout.getvalue())
        self.assertIn(
            "Path to the KEY=VALUE configuration file", stdout.getvalue()
        )
        self.assertIn(
            "Run the interactive terminal visualizer", stdout.getvalue()
        )

    def test_rejects_single_row_or_column_without_a_traceback(self) -> None:
        for width, height in ((1, 2), (2, 1)):
            for perfect in ("true", "false"):
                for interactive in (False, True):
                    with self.subTest(
                        size=(width, height),
                        perfect=perfect,
                        interactive=interactive,
                    ), TemporaryDirectory() as temporary_directory:
                        directory = Path(temporary_directory)
                        output_file = directory / "maze.txt"
                        config_file = directory / "maze.conf"
                        config_file.write_text(
                            "\n".join(
                                (
                                    f"WIDTH={width}",
                                    f"HEIGHT={height}",
                                    "ENTRY=0,0",
                                    f"EXIT={width - 1},{height - 1}",
                                    f"OUTPUT_FILE={output_file}",
                                    f"PERFECT={perfect}",
                                )
                            ),
                            encoding="utf-8",
                        )
                        argv = ["a_maze_ing.py", str(config_file)]
                        if interactive:
                            argv.append("--interactive")
                        stderr = StringIO()
                        with (
                            patch("sys.argv", argv),
                            redirect_stderr(stderr),
                            self.assertRaises(SystemExit) as raised,
                        ):
                            main()

                        self.assertEqual(raised.exception.code, 2)
                        self.assertIn("at least 2", stderr.getvalue())
                        self.assertNotIn("Traceback", stderr.getvalue())
                        self.assertFalse(output_file.exists())

    def test_reports_an_endpoint_overlapping_pattern42(self) -> None:
        """Report incompatible endpoints without creating an output file."""
        width = len(Pattern42.MASK[0]) + 2
        height = len(Pattern42.MASK) + 2
        for perfect in ("true", "false"):
            with self.subTest(perfect=perfect), TemporaryDirectory() as tmp:
                directory = Path(tmp)
                output_file = directory / "maze.txt"
                config_file = directory / "maze.conf"
                config_file.write_text(
                    "\n".join(
                        (
                            f"WIDTH={width}",
                            f"HEIGHT={height}",
                            "ENTRY=1,1",
                            f"EXIT={width - 1},{height - 1}",
                            f"OUTPUT_FILE={output_file}",
                            f"PERFECT={perfect}",
                            "SEED=42",
                        )
                    ),
                    encoding="utf-8",
                )
                stderr = StringIO()
                stdout = StringIO()
                with (
                    patch("sys.argv", ["a_maze_ing.py", str(config_file)]),
                    redirect_stderr(stderr),
                    redirect_stdout(stdout),
                    self.assertRaises(SystemExit) as raised,
                ):
                    main()

                self.assertEqual(raised.exception.code, 2)
                self.assertIn("cannot overlap Pattern42", stderr.getvalue())
                self.assertNotIn("Traceback", stderr.getvalue())
                self.assertEqual(stdout.getvalue(), "")
                self.assertFalse(output_file.exists())

    def test_prints_the_parsed_configuration_summary(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            directory = Path(temporary_directory)
            output_file = directory / "maze.txt"
            config_file = directory / "maze.conf"
            config_file.write_text(
                "\n".join(
                    (
                        "WIDTH=3",
                        "HEIGHT=2",
                        "ENTRY=0,0",
                        "EXIT=2,1",
                        f"OUTPUT_FILE={output_file}",
                        "PERFECT=true",
                        "SEED=42",
                    )
                ),
                encoding="utf-8",
            )
            stdout = StringIO()

            with (
                patch("sys.argv", ["a_maze_ing.py", str(config_file)]),
                redirect_stdout(stdout),
            ):
                exit_code = main()

        self.assertEqual(exit_code, 0)
        self.assertEqual(
            stdout.getvalue(),
            "\n".join(
                (
                    "Configuration loaded:",
                    "Size: 3x2",
                    "Entry: 0,0",
                    "Exit: 2,1",
                    "Perfect: yes",
                    f"Output file: {output_file}",
                    "Seed: 42",
                    f"Maze generated and written to: {output_file}",
                    "",
                )
            ),
        )

    def test_generates_and_writes_an_imperfect_maze(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            directory = Path(temporary_directory)
            output_file = directory / "maze.txt"
            config_file = directory / "maze.conf"
            config_file.write_text(
                "\n".join(
                    (
                        "WIDTH=3",
                        "HEIGHT=3",
                        "ENTRY=0,0",
                        "EXIT=2,2",
                        f"OUTPUT_FILE={output_file}",
                        "PERFECT=false",
                        "SEED=42",
                    )
                ),
                encoding="utf-8",
            )
            stdout = StringIO()

            with (
                patch("sys.argv", ["a_maze_ing.py", str(config_file)]),
                redirect_stdout(stdout),
            ):
                exit_code = main()

            self.assertEqual(exit_code, 0)
            self.assertTrue(output_file.is_file())
            serialized_maze = output_file.read_text(encoding="utf-8")
            self.assertIn(
                f"Maze generated and written to: {output_file}",
                stdout.getvalue(),
            )
            self.assertIn("0,0\n2,2\n", serialized_maze)

    def test_generates_and_writes_a_perfect_maze(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            directory = Path(temporary_directory)
            output_file = directory / "maze.txt"
            config_file = directory / "maze.conf"
            config_file.write_text(
                "\n".join(
                    (
                        "WIDTH=3",
                        "HEIGHT=3",
                        "ENTRY=0,0",
                        "EXIT=2,2",
                        f"OUTPUT_FILE={output_file}",
                        "PERFECT=true",
                        "SEED=42",
                    )
                ),
                encoding="utf-8",
            )
            stdout = StringIO()

            with (
                patch("sys.argv", ["a_maze_ing.py", str(config_file)]),
                redirect_stdout(stdout),
            ):
                exit_code = main()

            self.assertEqual(exit_code, 0)
            self.assertTrue(output_file.is_file())
            serialized_maze = output_file.read_text(encoding="utf-8")
            self.assertIn(
                f"Maze generated and written to: {output_file}",
                stdout.getvalue(),
            )
            self.assertIn("0,0\n2,2\n", serialized_maze)

    def test_reports_a_null_byte_in_the_output_filename(self) -> None:
        """Report an invalid output path without an unhandled ValueError."""
        with TemporaryDirectory() as tmp:
            directory = Path(tmp)
            output_file = directory / "maze\x00.txt"
            config_file = directory / "maze.conf"
            config_file.write_text(
                "\n".join(
                    (
                        "WIDTH=3",
                        "HEIGHT=3",
                        "ENTRY=0,0",
                        "EXIT=2,2",
                        f"OUTPUT_FILE={output_file}",
                        "PERFECT=true",
                        "SEED=42",
                    )
                ),
                encoding="utf-8",
            )
            stderr = StringIO()
            stdout = StringIO()
            with (
                patch("sys.argv", ["a_maze_ing.py", str(config_file)]),
                redirect_stderr(stderr),
                redirect_stdout(stdout),
                self.assertRaises(SystemExit) as raised,
            ):
                main()

            self.assertEqual(raised.exception.code, 2)
            self.assertIn("Could not write the output file", stderr.getvalue())
            self.assertIn("null byte", stderr.getvalue())
            self.assertNotIn("Traceback", stderr.getvalue())
            self.assertEqual(stdout.getvalue(), "")
            self.assertEqual(list(directory.iterdir()), [config_file])

    def test_reports_a_stdout_encoding_failure(self) -> None:
        """Report an ASCII output error while keeping the saved maze."""
        with TemporaryDirectory() as tmp:
            directory = Path(tmp)
            output_file = directory / "salida_ñ.txt"
            config_file = directory / "maze.conf"
            config_file.write_text(
                "\n".join(
                    (
                        "WIDTH=3",
                        "HEIGHT=3",
                        "ENTRY=0,0",
                        "EXIT=2,2",
                        f"OUTPUT_FILE={output_file}",
                        "PERFECT=true",
                        "SEED=42",
                    )
                ),
                encoding="utf-8",
            )
            stderr = StringIO()
            with (
                TextIOWrapper(BytesIO(), encoding="ascii") as stdout,
                patch("sys.argv", ["a_maze_ing.py", str(config_file)]),
                redirect_stdout(stdout),
                redirect_stderr(stderr),
                self.assertRaises(SystemExit) as raised,
            ):
                main()

            self.assertEqual(raised.exception.code, 2)
            self.assertIn("Could not display the output", stderr.getvalue())
            self.assertNotIn("Traceback", stderr.getvalue())
            self.assertTrue(output_file.is_file())
            self.assertIn(
                "0,0\n2,2\n", output_file.read_text(encoding="utf-8")
            )

    def test_reports_a_closed_stdout_pipe(self) -> None:
        """Exit cleanly when the stdout reader has already closed its pipe."""
        with TemporaryDirectory() as tmp:
            directory = Path(tmp)
            output_file = directory / "maze.txt"
            config_file = directory / "maze.conf"
            config_file.write_text(
                "\n".join(
                    (
                        "WIDTH=3",
                        "HEIGHT=3",
                        "ENTRY=0,0",
                        "EXIT=2,2",
                        f"OUTPUT_FILE={output_file}",
                        "PERFECT=true",
                        "SEED=42",
                    )
                ),
                encoding="utf-8",
            )
            script = Path(__file__).resolve().parents[1] / "a_maze_ing.py"
            read_fd, write_fd = os.pipe()
            os.close(read_fd)
            try:
                result = subprocess.run(
                    [sys.executable, "-B", str(script), str(config_file)],
                    stdout=write_fd,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=10,
                )
            finally:
                os.close(write_fd)

            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertIn("Could not display the output", result.stderr)
            self.assertNotIn("Traceback", result.stderr)
            self.assertNotIn("Exception ignored", result.stderr)
            self.assertTrue(output_file.is_file())

    def test_reports_an_output_write_failure_without_a_traceback(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            directory = Path(temporary_directory)
            output_file = directory / "missing" / "maze.txt"
            config_file = directory / "maze.conf"
            config_file.write_text(
                "\n".join(
                    (
                        "WIDTH=3",
                        "HEIGHT=3",
                        "ENTRY=0,0",
                        "EXIT=2,2",
                        f"OUTPUT_FILE={output_file}",
                        "PERFECT=false",
                    )
                ),
                encoding="utf-8",
            )
            stderr = StringIO()

            try:
                with (
                    patch("sys.argv", ["a_maze_ing.py", str(config_file)]),
                    redirect_stderr(stderr),
                    self.assertRaises(SystemExit) as raised,
                ):
                    main()
            except OSError as error:
                self.fail(f"CLI raised an unhandled write error: {error}")

        self.assertEqual(raised.exception.code, 2)
        self.assertIn(
            "Could not write the output file",
            stderr.getvalue(),
        )


if __name__ == "__main__":
    unittest.main()
