from pathlib import Path

from lira.ui import TerminalUI


def main():
    books_path = Path(__file__).parent / "../tests/data/books/example/"
    ui = TerminalUI(books_path)
    ui.run()


main()
