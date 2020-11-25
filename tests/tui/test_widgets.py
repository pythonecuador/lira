from pathlib import Path
from textwrap import dedent
from unittest import mock

from prompt_toolkit.formatted_text import HTML, to_formatted_text
from prompt_toolkit.mouse_events import MouseEventType

from lira.app import LiraApp
from lira.tui.widgets import (
    BookChaptersList,
    BooksList,
    Button,
    ChapterSectionsList,
    FormattedTextArea,
    List,
    ListElement,
)

from .utils import to_text

data_dir = Path(__file__).parent / "../data"
config_file = data_dir / "books/config.yaml"


class TestButton:
    def test_button(self):
        button = Button("Hello")
        assert to_text(button) == "[  Hello   ]"

        button = Button("Exit", handler=lambda: print("Hi"))
        button.handler()
        assert to_text(button) == "[   Exit   ]"


class TestFormattedTextArea:
    def test_formatted_text_area(self):
        text = to_formatted_text("I'm a text area", style="bg:red")
        text_area = FormattedTextArea(text)
        assert text_area.text == "I'm a text area"

        formatted_text = dedent(
            """
            <title>I'm a title</title>

            I'm <strong>bold</strong>!

            <end>Do we end here?</end>
            """
        ).strip()
        formatted_text = HTML(formatted_text)
        plain_text = dedent(
            """
            I'm a title

            I'm bold!

            Do we end here?
            """
        ).strip()

        text_area = FormattedTextArea(formatted_text)
        assert text_area.text == plain_text

        formatted_text = dedent(
            """
            <title>I'm a title</title>

            I'm <strong>bold</strong>!

            <end>Do we end here?</end>

            No, here.

            """
        ).strip()
        formatted_text = HTML(formatted_text)
        plain_text = dedent(
            """
            I'm a title

            I'm bold!

            Do we end here?

            No, here.

            """
        ).strip()
        text_area.text = formatted_text
        assert text_area.text == plain_text


class TestList:
    def test_list(self):
        title = to_formatted_text("Title", style="bg:red")
        elements = [
            ListElement("One", on_select=lambda: print("Select")),
            ListElement("Two"),
            ListElement("Three", on_focus=lambda: print("Focus")),
        ]

        list = List(
            title=title,
            elements=elements,
        )

        assert list.title_window.text == "Title"

        expected = dedent(
            """
            One
            Two
            Three
            """
        ).strip()
        assert to_text(list.list_window) == expected

        list.next()
        assert list.current_element.text == "Two"
        assert to_text(list.list_window) == expected

        list.previous()
        assert list.current_element.text == "One"
        assert to_text(list.list_window) == expected

        list.focus(2)
        assert list.current_element.text == "Three"
        assert to_text(list.list_window) == expected

        list.select(0)
        assert list.current_element.text == "One"
        assert to_text(list.list_window) == expected

        list.select(1)
        assert list.current_element.text == "Two"
        assert to_text(list.list_window) == expected

        mouse_event = mock.MagicMock()
        mouse_event.event_type = MouseEventType.MOUSE_DOWN
        list.mouse_select(index=0, mouse_event=mouse_event)
        assert list.current_element.text == "Two"
        assert to_text(list.list_window) == expected

        mouse_event.event_type = MouseEventType.MOUSE_UP
        list.mouse_select(index=0, mouse_event=mouse_event)
        assert list.current_element.text == "One"
        assert to_text(list.list_window) == expected


class TestLiraLists:
    def setup_method(self):
        with mock.patch("lira.app.CONFIG_FILE", config_file):
            self.app = LiraApp()
            self.app.setup()

        self.tui = mock.MagicMock()
        self.tui.lira = self.app

    def test_book_list(self):
        books_list = BooksList(tui=self.tui)
        list = books_list.container

        assert list.title_window.text == "Books"
        expected = dedent(
            """
            Intro to Lira
            Basic Introduction to Python
            """
        ).strip()
        assert to_text(list.list_window) == expected

        assert books_list._get_bullet(0) == "• "

        # Changing focus updates the content window.
        list.next()
        self.tui.content.reset.assert_called_once()

        # Selecting an item updates the list.
        list.select(0)
        self.tui.menu.push.assert_called_once()

    def test_book_chapters_list(self):
        book = self.app.books[1]
        book.parse()
        chapters_list = BookChaptersList(tui=self.tui, book=book)
        list = chapters_list.container

        assert list.title_window.text == "Basic Introduction to Python"
        expected = dedent(
            """
            Introduction
            Nested Content
            """
        ).strip()
        assert to_text(list.list_window) == expected

        assert chapters_list._get_bullet(0) == "1. "

        # Selecting an item updates the list.
        list.select(0)
        self.tui.menu.push.assert_called_once()

    def test_chapter_sections_list(self):
        book = self.app.books[1]
        book.parse()
        chapter = book.chapters[0]
        chapter.parse()

        sections_list = ChapterSectionsList(tui=self.tui, chapter=chapter, index=0)
        list = sections_list.container

        # The first section is rendered by default.
        assert list.title_window.text == "Basic Introduction to Python > Introduction"
        expected = dedent(
            """
            Comments
            """
        ).strip()
        assert to_text(list.list_window) == expected
        self.tui.content.render_section.assert_called_once()

        assert sections_list._get_bullet(0) == "1.1. "
        assert sections_list._get_bullet(1) == "1.2. "

        # Selecting an item updates the content.
        self.tui.reset_mock()
        list.select(0)
        self.tui.content.render_section.assert_called_once()
