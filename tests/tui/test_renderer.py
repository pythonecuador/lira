from pathlib import Path
from unittest import mock

from prompt_toolkit.data_structures import Point
from prompt_toolkit.formatted_text import (
    fragment_list_to_text,
    merge_formatted_text,
    to_formatted_text,
)
from prompt_toolkit.mouse_events import MouseEvent, MouseEventType

from lira.book import Book
from lira.tui.render import Renderer

books_path = Path(__file__).parent / "../data/books"


class TestRenderer:
    def setup_method(self):
        book = Book(root=books_path / "renderer")
        book.parse(all=True)
        self.tui = mock.MagicMock()
        self.chapters = book.chapters

    def _to_text(self, formatted_text_list):
        return fragment_list_to_text(
            to_formatted_text(merge_formatted_text(formatted_text_list))
        )

    def test_code_block(self):
        expected = """
Python

This is a Python code block:

┌─ [ Copy ] ─────────────────────────

  for _ in range(3):
      print("Hello world")


└────────────────────────────────────"""
        expected = expected.lstrip()
        toc = self.chapters[0].toc()
        section = toc[0][0]
        renderer = Renderer(tui=self.tui, section=section, width=37)
        content = renderer.render()
        assert self._to_text(content) == expected

    def test_unknow_codeblock(self):
        expected = """
Unknown

This is an unknown or unsupported language:

┌─ [ Copy ] ─────────────────────────

  I don't exist.

└────────────────────────────────────"""
        expected = expected.lstrip()
        toc = self.chapters[0].toc()
        section = toc[1][0]
        renderer = Renderer(tui=self.tui, section=section, width=37)
        content = renderer.render()
        assert self._to_text(content) == expected

    def test_test_block(self):
        expected = """
Python

This is a Python test block:

┌─ Write a comment ──────────────────

- [ Edit ] [ Reset ] [ Check ] (•) --

  # Put your comment below


└────────────────────────────────────"""
        expected = expected.lstrip()
        toc = self.chapters[1].toc()
        section = toc[0][0]
        renderer = Renderer(tui=self.tui, section=section, width=37)
        content = renderer.render()
        assert self._to_text(content) == expected

    def test_test_block_no_language(self):
        expected = """
Plain text

This is just plain text:

┌─ Who is Guido? ────────────────────

- [ Edit ] [ Reset ] [ Check ] (•) --

  He's the creator of something...

└────────────────────────────────────"""
        expected = expected.lstrip()
        toc = self.chapters[1].toc()
        section = toc[1][0]
        renderer = Renderer(tui=self.tui, section=section, width=37)
        content = renderer.render()
        assert self._to_text(content) == expected

    @mock.patch("lira.tui.render.click.edit")
    def test_test_block_edit_action(self, click_edit):
        toc = self.chapters[1].toc()
        section = toc[1][0]
        renderer = Renderer(tui=self.tui, section=section, width=37)
        renderer.render()
        text = "He's the creator of something..."
        new_text = "One\nTwo\nThree\n"
        node = section.children[1]
        assert node.tagname == "TestBlock"
        assert node.text() == text

        click_edit.return_value = new_text

        mouse_event = MouseEvent(Point(0, 0), MouseEventType.MOUSE_UP)
        renderer._edit_action(node, mouse_event)
        click_edit.assert_called_once_with(
            text=text,
            extension=".txt",
        )
        assert node.text() == new_text

        renderer._reset_action(node, mouse_event)
        assert node.text() == text

    @mock.patch("lira.tui.render.click.edit")
    def test_test_block_edit_action_none(self, click_edit):
        toc = self.chapters[1].toc()
        section = toc[1][0]
        renderer = Renderer(tui=self.tui, section=section, width=37)
        renderer.render()
        text = "He's the creator of something..."
        node = section.children[1]
        assert node.tagname == "TestBlock"
        assert node.text() == text

        click_edit.return_value = None

        mouse_event = MouseEvent(Point(0, 0), MouseEventType.MOUSE_UP)
        renderer._edit_action(node, mouse_event)
        click_edit.assert_called_once_with(
            text=text,
            extension=".txt",
        )
        assert node.text() == text
