"""Launch the desktop by default; keep explicit CLI workflows available."""
import sys
from pathlib import Path


def main():
    args = sys.argv[1:]
    if args and args[0] == "--self-test":
        from src.self_test import main as self_test
        return self_test(args[1:])
    if "--interactive" in args:
        from src.interactive_cli import main as interactive_main
        return interactive_main()
    if args or Path(sys.executable).stem.endswith("-CLI"):
        from src.cli import MailMergeCLI
        if args and args[0] == "--cli":
            args = args[1:]
        return MailMergeCLI().run(args)
    from src.gui import main as gui_main
    return gui_main()


if __name__ == "__main__":
    raise SystemExit(main())
