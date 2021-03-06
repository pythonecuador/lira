import asyncio
from functools import partial
from textwrap import dedent

from prompt_toolkit.application.current import get_app
from prompt_toolkit.filters import Condition
from prompt_toolkit.formatted_text import merge_formatted_text, to_formatted_text
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.layout import (
    ConditionalContainer,
    Dimension,
    DynamicContainer,
    HSplit,
    to_container,
)
from prompt_toolkit.widgets import Box, Label, TextArea

from lira import __version__
from lira.tui.render import Renderer
from lira.tui.utils import exit_app, notify_after_copy, set_title
from lira.tui.widgets import BooksList, Button, FormattedTextArea


class WindowContainer:

    inner_container = "container"

    def __init__(self, tui):
        self.tui = tui
        self.lira = self.tui.lira
        self.pages = [self._get_default_container()]
        self.container = DynamicContainer(self.get_container)

    def _get_default_container(self):
        return to_container(Label("Empty container"))

    def focus(self):
        layout = self.tui.app.layout
        window = next(layout.get_focusable_windows(), None)
        if window:
            layout.focus(window)

    def get_inner_container(self):
        return getattr(self, self.inner_container)

    def get_container(self):
        if self.pages:
            return self.pages[-1]
        return self._get_default_container()

    def push(self, widget):
        self.pages.append(widget)
        self.focus()

    def pop(self):
        if len(self.pages) <= 1:
            return
        self.pages.pop()
        self.focus()

    def reset(self, widget=None):
        widget = widget or self._get_default_container()
        self.pages = [widget]

    def __pt_container__(self):
        return self.container


class ContentArea(WindowContainer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text_area = self._get_default_container()

    def get_container(self):
        if self.pages:
            return self._box(self.pages[-1])
        return self._box(self._get_default_container())

    def _box(self, body):
        return Box(
            body=body,
            height=Dimension(min=1),
            width=Dimension(min=1, weight=4),
            padding=1,
        )

    def _get_default_container(self):
        text = dedent(
            f"""
            Welcome to Lira!

            - Press <Ctrl-q> to exit.
            - Change of window with <Tab>.
            - Move inside a widget with the arrow keys.
            - Copy a selection with <Ctrl-c>.

            Version: {__version__}.
            """
        )
        text_area = FormattedTextArea(
            to_formatted_text(text.strip()),
            scrollbar=True,
            focusable=True,
            after_copy=partial(notify_after_copy, self.tui),
        )
        return text_area

    def render_section(self, section):
        renderer = Renderer(tui=self.tui, section=section)
        self.text_area = FormattedTextArea(
            merge_formatted_text(renderer.render()),
            scrollbar=True,
            focusable=True,
            after_copy=partial(notify_after_copy, self.tui),
        )
        self.reset(self.text_area)

    def update_section(self, section):
        renderer = Renderer(tui=self.tui, section=section)
        self.text_area.text = merge_formatted_text(renderer.render())
        self.reset(self.text_area)


class SidebarMenu(WindowContainer):

    inner_container = "list"

    def __init__(self, tui):
        super().__init__(tui)
        self.list = DynamicContainer(self.get_container)
        self.back_button = ConditionalContainer(
            Button("Back", handler=self.pop),
            filter=Condition(lambda: len(self.pages) > 1),
        )
        self.exit_button = Button("Exit", handler=exit_app)
        self.container = HSplit(
            [
                self.list,
                self.back_button,
                self.exit_button,
            ],
            height=Dimension(min=1),
            width=Dimension(min=1),
            key_bindings=self.get_key_bindings(),
        )

    def _get_default_container(self):
        return BooksList(tui=self.tui)

    def get_key_bindings(self):
        keys = KeyBindings()

        @keys.add(Keys.Backspace)
        def _(event):
            self.pop()

        return keys

    def pop(self):
        super().pop()
        if len(self.pages) <= 1:
            set_title()


class StatusBar(WindowContainer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.history = []

    def _get_default_container(self):
        return to_container(self._get_status_area())

    def _get_status_area(self, status=""):
        return TextArea(
            text=status,
            height=Dimension.exact(1),
            prompt=">>> ",
            multiline=False,
            wrap_lines=False,
            focusable=False,
            read_only=True,
        )

    def update_status(self, status=""):
        self.history.append(status)
        self.reset(self._get_status_area(status))
        get_app().invalidate()

    def notify(self, text, delay=1.5):
        # TODO: create a queue, so notifications don't overlap.
        async def _main():
            await asyncio.sleep(0.1)
            self.update_status(text)
            await asyncio.sleep(delay)
            self.update_status()

        return asyncio.create_task(_main())
