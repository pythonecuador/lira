from textwrap import dedent

from prompt_toolkit.formatted_text import to_formatted_text

from lira.tui.widgets import Button, FormattedTextArea, List, ListElement

from .utils import to_text


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
        assert to_text(text_area) == "I'm a text area"


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

        assert to_text(list.title_window) == "Title"

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
