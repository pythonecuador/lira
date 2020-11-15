from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous
from prompt_toolkit.keys import Keys
from prompt_toolkit.layout import Dimension, Layout
from prompt_toolkit.layout.containers import HSplit, VSplit

from lira.app import LiraApp
from lira.tui.themes import style, theme
from lira.tui.utils import exit_app
from lira.tui.widgets import BooksList
from lira.tui.windows import ContentArea, SidebarMenu, StatusBar


class TerminalUI:
    def __init__(self):
        self.lira = LiraApp()
        self.lira.setup()

        self.content = ContentArea(self)
        self.status = StatusBar(self)

        self.menu = SidebarMenu(self)
        self.menu.push(BooksList(self))

        self.container = HSplit(
            [
                VSplit(
                    [
                        self.menu,
                        self.content,
                    ],
                    padding=Dimension.exact(1),
                    padding_char="│",
                    padding_style=theme["separator"],
                ),
                self.status,
            ],
            padding=Dimension.exact(1),
            padding_char="─",
            padding_style=theme["separator"],
        )

    def get_key_bindings(self):
        keys = KeyBindings()

        @keys.add("tab")
        @keys.add("down")
        def _(event):
            focus_next(event)

        @keys.add("s-tab")
        @keys.add("up")
        def _(event):
            focus_previous(event)

        @keys.add(Keys.Backspace)
        def _(event):
            self.menu.pop()

        @keys.add("c-c")
        @keys.add("c-q")
        def _(event):
            """Pressing Ctrl-Q or Ctrl-C will exit the user interface."""
            exit_app()

        return keys

    def _ready(self, app):
        key = "__is_ready"
        if not hasattr(self, key):
            self.status.notify("Ready!")
            setattr(self, key, True)

    def run(self):
        self.app = Application(
            layout=Layout(self.container),
            key_bindings=self.get_key_bindings(),
            mouse_support=True,
            full_screen=True,
            style=style,
            after_render=self._ready,
        )
        self.app.run()
