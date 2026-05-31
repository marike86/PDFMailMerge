import sys
import os

if getattr(sys, "frozen", False):
    os.chdir(os.path.dirname(sys.executable))

from src.interactive_cli import main

if __name__ == "__main__":
    main()
