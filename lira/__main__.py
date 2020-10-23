from pathlib import Path

from lira.ui import TerminalUI

books_path = Path(__file__).parent / "../tests/data/books/example/"

ui = TerminalUI(books_path)
ui.run()
