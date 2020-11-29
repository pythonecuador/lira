from pathlib import Path

from prompt_toolkit.formatted_text import (
    fragment_list_to_text,
    merge_formatted_text,
    to_formatted_text,
)

from lira.book import Book
from lira.tui.render import Renderer

books_path = Path(__file__).parent / "../data/books"


class TestRenderer:
    def setup_method(self):
        book = Book(root=books_path / "renderer")
        book.parse(all=True)
        self.chapters = book.chapters
        self.renderer = Renderer()

    def _to_text(self, formatted_text_list):
        return fragment_list_to_text(
            to_formatted_text(merge_formatted_text(formatted_text_list))
        )

    def test_code_block(self):
        expected = """
Python

This is a Python code block:

  for _ in range(3):
      print("Hello world")
"""
        expected = expected.lstrip()
        toc = self.chapters[0].toc()
        section = toc[0][0]
        content = self.renderer.render(section)
        assert self._to_text(content) == expected

    def test_unknow_codeblock(self):
        expected = """
Unknown

This is an unknown or unsupported language:

  I don't exist."""
        expected = expected.lstrip()
        toc = self.chapters[0].toc()
        section = toc[1][0]
        content = self.renderer.render(section)
        assert self._to_text(content) == expected

    def test_test_block(self):
        expected = """
Python

This is a Python test block:

┌─ Write a comment ───────────────

- [ Edit ] [ Load ] [ Run ] (•) --

  # Put your comment below


└─────────────────────────────────"""
        expected = expected.lstrip()
        toc = self.chapters[1].toc()
        section = toc[0][0]
        content = self.renderer.render(section, width=34)
        assert self._to_text(content) == expected

    def test_test_block_no_language(self):
        expected = """
Plain text

This is just plain text:

┌─ Who is Guido? ─────────────────

- [ Edit ] [ Load ] [ Run ] (•) --

  He's the creator of something...

└─────────────────────────────────"""
        expected = expected.lstrip()
        toc = self.chapters[1].toc()
        section = toc[1][0]
        content = self.renderer.render(section, width=34)
        assert self._to_text(content) == expected
