from unittest import mock

from prompt_toolkit.layout.containers import to_container
from prompt_toolkit.widgets import Button, Label

from lira.tui.windows import SidebarMenu

from .utils import is_visible, to_widget


class TestSidebarMenu:
    def setup_method(self):
        tui = mock.MagicMock()
        self.window = SidebarMenu(tui=tui)

    def test_default_menu(self):
        children = to_container(self.window).get_children()
        assert len(children) == 3

        empty_label = children[0].get_container().content
        back_button = to_widget(children[1])
        exit_button = to_widget(children[2])

        assert empty_label.text() == "Empty container"

        assert isinstance(back_button, Button)
        assert back_button.text == "Back"
        assert not is_visible(back_button)

        assert isinstance(exit_button, Button)
        assert exit_button.text == "Exit"
        assert is_visible(exit_button)

    def test_toggle_back_button(self):
        first_label = Label("First")
        second_label = Label("Second")

        self.window.push(first_label)
        self.window.push(second_label)

        children = to_container(self.window).get_children()
        back_button = to_widget(children[1])
        exit_button = to_widget(children[2])

        # Back button is visible
        assert back_button.text == "Back"
        assert is_visible(back_button)

        assert exit_button.text == "Exit"
        assert is_visible(exit_button)

        label = children[0].get_container().content
        assert label.text() == "Second"

        self.window.pop()

        # Back button is't visible
        assert back_button.text == "Back"
        assert not is_visible(back_button)

        assert exit_button.text == "Exit"
        assert is_visible(exit_button)

        label = children[0].get_container().content
        assert label.text() == "First"
