# Entry point. Run from the project root: python main.py

import sys

sys.path.insert(0, "src")

from emporio_agent.cli import main  # noqa: E402

main()
