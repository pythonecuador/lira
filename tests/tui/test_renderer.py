from pathlib import Path
from unittest import mock

from prompt_toolkit.formatted_text import (
    fragment_list_to_text,
    merge_formatted_text,
    to_formatted_text,
)

from lira.book import Book
from lira.tui.windows import ContentArea

books_path = Path(__file__).parent / "../data/books"


class TestRenderer:
    def setup_method(self):
        book = Book(root=books_path / "renderer")
        book.parse(all=True)
        chapter = book.chapters[0]
        self.toc = chapter.toc()

        tui = mock.MagicMock()
        self.window = ContentArea(tui=tui)

    def test_code_block(self):
        expected = """
Python

This is a Python code block:

  for _ in range(3):
      print("Hello world")
"""
        expected = expected.lstrip()
        chapter = self.toc[0][0]
        content = self.window._get_content(chapter)
        result = fragment_list_to_text(to_formatted_text(merge_formatted_text(content)))
        assert result == expected

    def test_unknow_codeblock(self):
        expected = """
Unknown

This is an unknown or unsupported language:

  I don't exist."""
        expected = expected.lstrip()
        chapter = self.toc[1][0]
        content = self.window._get_content(chapter)
        result = fragment_list_to_text(to_formatted_text(merge_formatted_text(content)))
        assert result == expected
