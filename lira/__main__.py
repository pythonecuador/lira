from pathlib import Path

from lira.ui import TerminalUI

books_path = Path(__file__).parent / "../tests/data/books/example/"

ui = TerminalUI(books_path)
ui.run()

def get_menu():
    book = Book(root=path)
    book.parse()
    chapters = book.chapters[1]
    chapters.parse()
    breakpoint()

