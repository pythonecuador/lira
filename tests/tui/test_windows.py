from unittest import mock

import pytest
from prompt_toolkit.layout.containers import to_container
from prompt_toolkit.widgets import Button, Label

from lira.tui.windows import SidebarMenu, StatusBar

from .utils import to_widget


class TestSidebarMenu:
    def setup_method(self):
        tui = mock.MagicMock()
        self.window = SidebarMenu(tui=tui)

    def test_default_menu(self):
        """The default menu has 2 buttons and a label."""
        children = to_container(self.window).get_children()
        assert len(children) == 3

        empty_label = children[0].get_container().content
        back_button = children[1]
        exit_button = to_widget(children[2])

        assert empty_label.text() == "Empty container"

        # Back button is not visible
        assert to_widget(back_button.content).text == "Back"
        assert not back_button.filter()

        # Exit button is visible
        assert isinstance(exit_button, Button)
        assert exit_button.text == "Exit"

    def test_toggle_back_button(self):
        """The back button is only visible if there are at least 2 pages."""
        first_label = Label("First")
        second_label = Label("Second")

        self.window.push(first_label)
        self.window.push(second_label)

        children = to_container(self.window).get_children()
        back_button = children[1]
        exit_button = to_widget(children[2])

        assert exit_button.text == "Exit"

        # Back button is visible
        assert to_widget(back_button.content).text == "Back"
        assert back_button.filter()

        label = children[0].get_container()
        assert label.text == "Second"

        self.window.pop()

        # Back button is't visible
        assert to_widget(back_button.content).text == "Back"
        assert not back_button.filter()

        label = children[0].get_container()
        assert label.text == "First"

    def test_pop_all_pages(self):
        first_label = Label("First")
        self.window.push(first_label)
        assert len(self.window.pages) == 1

        # We can't pop the last page.
        self.window.pop()
        self.window.pop()
        assert len(self.window.pages) == 1

        children = to_container(self.window).get_children()
        label = children[0].get_container()
        assert label.text == "First"

        # We can reset the pages to the default container.
        self.window.reset()
        assert len(self.window.pages) == 1
        children = to_container(self.window).get_children()
        label = children[0].get_container()
        assert label.content.text() == "Empty container"


class TestStatusBar:
    def _get_current_status(self, window):
        return to_container(window).get_children()[0].content.buffer.text

    def setup_method(self):
        tui = mock.MagicMock()
        self.window = StatusBar(tui=tui)

    def test_update_status(self):
        assert self._get_current_status(self.window) == ""

        msg = "Hello world!"
        self.window.update_status(msg)
        assert self._get_current_status(self.window) == msg

        assert len(self.window.history) == 1
        assert self.window.history[0] == msg

    @pytest.mark.asyncio
    async def test_notify(self):
        assert self._get_current_status(self.window) == ""

        msg = "Hello world!"
        await self.window.notify(msg, delay=0.1)

        assert len(self.window.history) == 2
        assert self.window.history[0] == msg
        assert self.window.history[1] == ""
        assert self._get_current_status(self.window) == ""
