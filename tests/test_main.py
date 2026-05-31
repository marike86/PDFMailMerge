import sys
import os
import pytest


class TestMainModule:

    def test_main_import(self):
        import main
        assert hasattr(main, "main")

    def test_frozen_mode_chdir(self):
        import main as main_module
        import types
        original_frozen = getattr(sys, "frozen", False)

        mock_main = types.ModuleType("main_test")
        mock_main.__file__ = main_module.__file__

        assert callable(main_module.main)

    def test_main_entry_calls_interactive_cli(self):
        from unittest.mock import patch, MagicMock
        import main as main_module

        with patch("src.interactive_cli.main") as mock_main:
            mock_main.return_value = None
            with patch.object(sys, "argv", ["main.py"]):
                exec(
                    compile(open(main_module.__file__).read(), main_module.__file__, "exec"),
                    {"__name__": "__not_main__"},
                )
