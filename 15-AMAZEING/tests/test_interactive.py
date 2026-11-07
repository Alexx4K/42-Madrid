"""Regression tests for interactive controls and Linux terminal input."""

from contextlib import redirect_stdout
from dataclasses import replace
from io import StringIO
import os
from pathlib import Path
import subprocess
import sys
from textwrap import dedent
import time
import unittest
from unittest.mock import patch

from mazegen.generator import MazeGenerator
from mazegen.maze import Direction, Maze
from mazegen.solver import solve_shortest_path
from visualizer import interactive


_CLEAR = "\033[2J\033[H"
_GETCH_CHILD = dedent(
    """\
    import sys
    from unittest.mock import patch
    from visualizer.interactive import Getch

    reader = Getch()
    with reader as entered:
        assert entered is reader
        if sys.argv[1] == "error":
            with patch.object(sys.stdin, "read", side_effect=RuntimeError):
                try:
                    reader()
                except RuntimeError:
                    print("read failed", flush=True)
                else:
                    raise AssertionError("Expected the read to fail")
        else:
            print(reader().hex(), flush=True)
    """
)


def make_state() -> interactive.VisualizerState:
    """Use an open, deterministic maze with an interior route marker."""
    return interactive.VisualizerState(
        maze=Maze.create_open(2, 2),
        solution=[Direction.EAST, Direction.SOUTH],
        show_solution=True,
        use_color=False,
        generator=MazeGenerator(seed=42),
        config_width=2,
        config_height=2,
        config_entry=(0, 0),
        config_exit=(1, 1),
        config_perfect=False,
        config_seed=42,
    )


class InteractiveControlTests(unittest.TestCase):
    """Exercise real state transitions, generation, and ASCII rendering."""

    def test_initial_state_generates_and_solves_both_modes(self) -> None:
        for perfect in (True, False):
            with self.subTest(perfect=perfect):
                generator = MazeGenerator(seed=42)
                state = interactive._build_initial_state(
                    generator, 3, 2, (0, 1), (2, 0), perfect, 42
                )

                self.assertIs(state.generator, generator)
                self.assertEqual((state.maze.width, state.maze.height), (3, 2))
                self.assertEqual(state.maze.entry, (0, 1))
                self.assertEqual(state.maze.exit, (2, 0))
                self.assertEqual(state.config_perfect, perfect)
                self.assertEqual(state.config_seed, 42)
                self.assertEqual(
                    state.solution, solve_shortest_path(state.maze)
                )
                self.assertTrue(state.show_solution)
                self.assertTrue(state.use_color)
                self.assertEqual(state.last_action, "")

    def test_s_toggles_route_rendering_without_mutating_original(self) -> None:
        original = make_state()
        self.assertIn(" * ", interactive._render_state(original))

        hidden = interactive._handle_key(original, b"s")
        assert hidden is not None
        self.assertFalse(hidden.show_solution)
        self.assertEqual(hidden.last_action, "Solution hidden")
        self.assertNotIn(" * ", interactive._render_state(hidden))
        self.assertIs(hidden.maze, original.maze)
        self.assertIs(hidden.solution, original.solution)
        self.assertTrue(original.show_solution)
        self.assertEqual(original.last_action, "")

        shown = interactive._handle_key(hidden, b"S")
        assert shown is not None
        self.assertTrue(shown.show_solution)
        self.assertEqual(shown.last_action, "Solution shown")
        self.assertIn(" * ", interactive._render_state(shown))
        self.assertEqual(replace(shown, last_action=""), original)

    def test_c_cycles_actual_wall_codes_and_preserves_maze_and_route(
        self,
    ) -> None:
        original = replace(make_state(), use_color=True)
        state = original
        for index in range(1, len(interactive.COLOR_OPTIONS) + 1):
            key = b"c" if index % 2 else b"C"
            updated = interactive._handle_key(state, key)
            assert updated is not None
            expected = index % len(interactive.COLOR_OPTIONS)
            self.assertEqual(updated.wall_color_index, expected)
            color = interactive.COLOR_OPTIONS[expected]
            rendered = interactive._render_state(updated)
            self.assertIn(f"\033[38;5;{color}m---\033[0m", rendered)
            self.assertIn(f"\033[38;5;{color}m|\033[0m", rendered)
            if index == 1:
                self.assertNotIn("\033[38;5;51m---", rendered)
            self.assertTrue(updated.use_color)
            self.assertIs(updated.maze, original.maze)
            self.assertIs(updated.solution, original.solution)
            self.assertEqual(updated.show_solution, original.show_solution)
            self.assertIs(updated.generator, original.generator)
            self.assertEqual(updated.config_seed, original.config_seed)
            self.assertIn(" * ", rendered)
            state = updated

        self.assertEqual(original.wall_color_index, 0)
        self.assertEqual(replace(state, last_action=""), original)

    def test_color_index_wraps_defensively_when_rendering_and_cycling(
        self,
    ) -> None:
        for index in (-1, len(interactive.COLOR_OPTIONS) + 2):
            with self.subTest(index=index):
                state = replace(
                    make_state(), use_color=True, wall_color_index=index
                )
                color = interactive.COLOR_OPTIONS[
                    index % len(interactive.COLOR_OPTIONS)
                ]
                self.assertIn(
                    f"\033[38;5;{color}m---", interactive._render_state(state)
                )
                updated = interactive._handle_key(state, b"c")
                assert updated is not None
                self.assertEqual(
                    updated.wall_color_index,
                    (index + 1) % len(interactive.COLOR_OPTIONS),
                )

    def test_n_toggles_colors_without_losing_selected_wall_color(self) -> None:
        original = replace(
            make_state(), use_color=True, wall_color_index=5
        )
        plain = interactive._handle_key(original, b"n")
        assert plain is not None
        self.assertFalse(plain.use_color)
        self.assertEqual(plain.last_action, "Colors disabled")
        self.assertNotIn("\033[", interactive._render_state(plain))
        self.assertEqual(plain.wall_color_index, original.wall_color_index)

        colored = interactive._handle_key(plain, b"N")
        assert colored is not None
        self.assertTrue(colored.use_color)
        self.assertEqual(colored.last_action, "Colors enabled")
        color = interactive.COLOR_OPTIONS[original.wall_color_index]
        self.assertIn(
            f"\033[38;5;{color}m---", interactive._render_state(colored)
        )
        self.assertEqual(replace(colored, last_action=""), original)

    def test_r_preserves_configuration_and_recalculates_route(self) -> None:
        for perfect in (True, False):
            for key in (b"r", b"R"):
                with self.subTest(perfect=perfect, key=key):
                    original = interactive._build_initial_state(
                        MazeGenerator(seed=42),
                        3, 2, (0, 1), (2, 0), perfect, 42,
                    )
                    original = replace(
                        original, solution=[],
                        show_solution=False, use_color=False,
                        wall_color_index=5,
                    )
                    # Fix the replacement seed, not a random layout assertion.
                    replacement = MazeGenerator(seed=7)
                    with (
                        patch.object(
                            interactive, "MazeGenerator",
                            return_value=replacement,
                        ) as factory,
                        patch.object(
                            interactive, "solve_shortest_path",
                            wraps=solve_shortest_path,
                        ) as solver,
                    ):
                        updated = interactive._handle_key(original, key)

                    assert updated is not None
                    factory.assert_called_once_with(seed=None)
                    solver.assert_called_once_with(updated.maze)
                    self.assertIs(updated.generator, replacement)
                    self.assertIsNot(updated.maze, original.maze)
                    self.assertIsNot(updated.solution, original.solution)
                    self.assertEqual(
                        updated.solution, solve_shortest_path(updated.maze)
                    )
                    generate = (
                        replacement.generate_perfect if perfect
                        else replacement.generate_imperfect
                    )
                    self.assertEqual(
                        updated.maze, generate(3, 2, (0, 1), (2, 0))
                    )
                    self.assertEqual(
                        replace(
                            updated, maze=original.maze,
                            solution=original.solution,
                            generator=original.generator, last_action="",
                        ),
                        original,
                    )
                    self.assertEqual(
                        updated.last_action, "New maze generated"
                    )
                    self.assertEqual(original.solution, [])
                    self.assertEqual(original.last_action, "")

    def test_q_escape_and_raw_ctrl_c_request_exit(self) -> None:
        state = make_state()
        for key in (b"q", b"Q", b"\x1b", b"\x03"):
            with self.subTest(key=key):
                self.assertIsNone(interactive._handle_key(state, key))

    def test_unknown_empty_and_invalid_bytes_preserve_state(self) -> None:
        state = make_state()
        for key in (b"?", b"", b"\xff", b"\n"):
            with self.subTest(key=key):
                self.assertIs(interactive._handle_key(state, key), state)

    def test_render_includes_configuration_help_and_last_action(self) -> None:
        state = replace(make_state(), last_action="Test action")
        rendered = interactive._render_state(state)
        self.assertIn("Mode: Imperfect | Size: 2x2 | Seed: 42", rendered)
        self.assertIn("-> Test action", rendered)
        self.assertTrue(rendered.isascii())
        self.assertIn("Controls:", rendered)
        for label in (
            "R - Regenerate maze (new seed)",
            "S - Show/Hide solution",
            "C - Cycle wall color",
            "N - Toggle colors ON/OFF",
            "Q / Esc / Ctrl-C - Quit",
        ):
            self.assertIn(label, rendered)
        perfect = replace(state, config_perfect=True)
        self.assertIn("Mode: Perfect", interactive._render_state(perfect))

    def test_render_labels_random_seed_in_english(self) -> None:
        state = replace(make_state(), generator=MazeGenerator(seed=None))

        self.assertIn("Seed: random", interactive._render_state(state))

    def test_render_labels_zero_seed_as_zero_not_random(self) -> None:
        state = replace(
            make_state(), generator=MazeGenerator(seed=0), config_seed=0
        )

        rendered = interactive._render_state(state)

        self.assertIn("Seed: 0", rendered)
        self.assertNotIn("Seed: random", rendered)


class InteractiveLoopTests(unittest.TestCase):
    """Simulate only input; keep generation, dispatch, and rendering real."""

    def test_loop_c_changes_wall_ansi_codes_between_frames(self) -> None:
        stdout = StringIO()
        with (
            patch.object(interactive, "Getch") as getch,
            redirect_stdout(stdout),
        ):
            getch.return_value.side_effect = [b"c", b"C", b"q"]
            interactive.run_interactive(3, 2, (0, 0), (2, 1), False, 0)

        frames = stdout.getvalue().split(_CLEAR)[1:]
        for index, frame in enumerate(frames[:-1]):
            color = interactive.COLOR_OPTIONS[index]
            self.assertIn(f"\033[38;5;{color}m---\033[0m", frame)
            self.assertIn("Seed: 0", frame)
            self.assertIn(" * ", frame)
        self.assertNotEqual(frames[0], frames[1])
        self.assertNotEqual(frames[1], frames[2])
        self.assertEqual(frames[-1], "Goodbye!\n")

    def test_loop_renders_each_toggle_and_ignores_unknown_key(self) -> None:
        stdout = StringIO()
        keys = [b"s", b"n", b"?", b"S", b"N", b"q"]
        with (
            patch.object(interactive, "Getch") as getch,
            redirect_stdout(stdout),
        ):
            getch.return_value.side_effect = keys
            interactive.run_interactive(3, 2, (0, 0), (2, 1), False, 42)

        getch.assert_called_once_with()
        self.assertEqual(getch.return_value.call_count, len(keys))
        frames = stdout.getvalue().split(_CLEAR)[1:]
        self.assertEqual(len(frames), len(keys) + 1)
        self.assertIn(" * ", frames[0])
        self.assertIn("\033[38;5;", frames[0])
        self.assertNotIn(" * ", frames[1])
        self.assertIn("Solution hidden", frames[1])
        self.assertNotIn("\033[", frames[2])
        self.assertEqual(frames[2], frames[3])
        self.assertIn(" * ", frames[4])
        self.assertIn("Solution shown", frames[4])
        self.assertIn("\033[38;5;", frames[5])
        self.assertIn("Colors enabled", frames[5])
        self.assertEqual(frames[-1], "Goodbye!\n")

    def test_loop_exits_on_q_escape_or_raw_ctrl_c_after_one_read(self) -> None:
        for key in (b"q", b"Q", b"\x1b", b"\x03"):
            with self.subTest(key=key):
                stdout = StringIO()
                with (
                    patch.object(interactive, "Getch") as getch,
                    redirect_stdout(stdout),
                ):
                    # Any extra read fails immediately rather than hanging.
                    getch.return_value.side_effect = [key]
                    interactive.run_interactive(
                        3, 2, (0, 0), (2, 1), False, 42
                    )
                self.assertEqual(getch.return_value.call_count, 1)
                self.assertEqual(stdout.getvalue().count(_CLEAR), 2)
                self.assertTrue(stdout.getvalue().endswith("Goodbye!\n"))

    def test_keyboard_interrupt_still_clears_screen_and_says_goodbye(
        self,
    ) -> None:
        stdout = StringIO()
        with (
            patch.object(interactive, "Getch") as getch,
            redirect_stdout(stdout),
        ):
            getch.return_value.side_effect = KeyboardInterrupt
            interactive.run_interactive(3, 2, (0, 0), (2, 1), False, 42)
        self.assertEqual(getch.return_value.call_count, 1)
        self.assertTrue(stdout.getvalue().endswith(_CLEAR + "Goodbye!\n"))

    def test_read_failure_propagates_after_final_screen_cleanup(self) -> None:
        stdout = StringIO()
        with (
            patch.object(interactive, "Getch") as getch,
            redirect_stdout(stdout),
            self.assertRaisesRegex(OSError, "input failed"),
        ):
            getch.return_value.side_effect = OSError("input failed")
            interactive.run_interactive(3, 2, (0, 0), (2, 1), False, 42)
        self.assertTrue(stdout.getvalue().endswith(_CLEAR + "Goodbye!\n"))


@unittest.skipUnless(sys.platform.startswith("linux"), "Requires Linux PTY")
class GetchTerminalTests(unittest.TestCase):
    """Use isolated PTYs; never change the test runner's own terminal."""

    def run_getch_in_pty(
        self, key: bytes | None, child_script: str = _GETCH_CHILD
    ) -> str:
        """Bound every wait and always reap the child and restore the PTY."""
        import pty
        import termios

        master, slave = pty.openpty()
        process: subprocess.Popen[str] | None = None
        original = termios.tcgetattr(slave)
        try:
            environment = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
            process = subprocess.Popen(
                [
                    sys.executable, "-B", "-c", child_script,
                    "error" if key is None else "read",
                ],
                stdin=slave,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=Path(__file__).resolve().parents[1],
                env=environment,
            )
            if key is not None:
                # setraw flushes input: send only after ICANON is disabled.
                deadline = time.monotonic() + 5.0
                while termios.tcgetattr(slave)[3] & termios.ICANON:
                    if process.poll() is not None:
                        output, errors = process.communicate(timeout=2)
                        self.fail(f"Getch exited before raw mode: {output}")
                    if time.monotonic() >= deadline:
                        self.fail("Getch did not enter raw mode within 5s")
                    time.sleep(0.005)
                self.assertEqual(os.write(master, key), len(key))

            output, errors = process.communicate(timeout=5)
            self.assertEqual(process.returncode, 0, errors)
            self.assertEqual(errors, "")
            self.assertEqual(termios.tcgetattr(slave), original)
            return output.strip()
        finally:
            try:
                if process is not None:
                    if process.poll() is None:
                        process.kill()
                    process.communicate(timeout=2)
            finally:
                try:
                    termios.tcsetattr(slave, termios.TCSANOW, original)
                finally:
                    os.close(slave)
                    os.close(master)

    def test_real_getch_reads_bytes_and_restores_terminal(self) -> None:
        for key in (b"s", b"\x1b", b"\x03"):
            with self.subTest(key=key):
                self.assertEqual(self.run_getch_in_pty(key), key.hex())

    def test_getch_restores_terminal_when_read_raises(self) -> None:
        self.assertEqual(self.run_getch_in_pty(None), "read failed")

    def test_real_loop_raw_ctrl_c_exits_and_restores_terminal_on_ascii(
        self,
    ) -> None:
        script = dedent(
            """\
            import sys
            from visualizer.interactive import run_interactive

            sys.stdout.reconfigure(encoding="ascii", errors="strict")
            run_interactive(20, 15, (0, 0), (19, 14), True, 0)
            """
        )

        output = self.run_getch_in_pty(b"\x03", script)

        self.assertIn("Seed: 0", output)
        self.assertTrue(output.endswith(_CLEAR + "Goodbye!"))
        self.assertTrue(output.isascii())


if __name__ == "__main__":
    unittest.main()
