import asyncio
from textwrap import dedent

from prompt_toolkit.application.current import get_app
from prompt_toolkit.formatted_text import merge_formatted_text, to_formatted_text
from prompt_toolkit.layout import Dimension
from prompt_toolkit.layout.containers import DynamicContainer, HSplit, to_container
from prompt_toolkit.widgets import Box, Button, Label, TextArea

from lira import __version__
from lira.tui.themes import theme
from lira.tui.utils import exit_app


class WindowContainer:

    inner_container = "container"

    def __init__(self, tui):
        self.tui = tui
        self.lira = self.tui.lira
        self.pages = []
        self.container = DynamicContainer(self._get_default_container)

    def _get_default_container(self):
        return to_container(Label("Empty container"))

    def focus(self):
        if not hasattr(self.tui, "app"):
            return

        layout = self.tui.app.layout
        window = next(layout.get_focusable_windows(), None)
        if window:
            layout.focus(window)

    def get_inner_container(self):
        return getattr(self, self.inner_container)

    def render(self, widget):
        container = self.get_inner_container()
        container.get_container = lambda: to_container(widget)
        self.focus()

    def push(self, widget):
        self.pages.append(widget)
        self.render(widget)

    def pop(self):
        if len(self.pages) <= 1:
            return
        self.pages.pop()
        prev_window = self.pages[-1]
        self.render(prev_window)

    def reset(self, widget=None):
        widget = widget or self._get_default_container()
        self.pages = [widget]
        self.render(widget)

    def __pt_container__(self):
        return self.container


class ContentArea(WindowContainer):
    def _get_default_container(self):
        text = dedent(
            f"""
            Welcome to Lira!

            - Press <C-c> or <C-q> to exit.
            - Navivate with <Tab> and the navigation keys.

            Version: {__version__}
            """
        )
        text_area = TextArea(
            text=text.strip(),
            style=theme["text"],
            focusable=False,
            read_only=True,
        )
        return to_container(
            Box(
                height=Dimension(min=1),
                width=Dimension(min=1, weight=4),
                body=text_area,
                padding=1,
                style=theme["text"],
            )
        )

    def _get_content(self, node):
        # TODO: parse and render individual nodes
        formated_content = []
        for child in node.children:
            text = child.text()
            formated_content.append(
                to_formatted_text(text, theme["nodes"][child.tagname])
            )
            if child.tagname == "Paragraph":
                formated_content.append(to_formatted_text("\n", ""))

        label = Label(merge_formatted_text(formated_content))

        return label

    def render_section(self, section):
        content = self.tui.content
        content.reset(
            Box(
                height=Dimension(min=1),
                width=Dimension(min=1, weight=4),
                body=self._get_content(section),
                padding=1,
                style=theme["text"],
            )
        )


class SidebarMenu(WindowContainer):

    inner_container = "list"

    def __init__(self, tui):
        super().__init__(tui)
        self.list = DynamicContainer(self._get_default_container)
        self.back_button = to_container(
            Button("Back", handler=self.pop),
        )
        self.container = HSplit(
            [
                self.list,
                self.back_button,
                Button("Exit", handler=exit_app),
            ],
            height=Dimension(min=1),
            width=Dimension(min=1),
        )
        self.toggle_back_button()

    def toggle_back_button(self):
        dimension = 1 if len(self.pages) > 1 else 0
        self.back_button.height = Dimension.exact(dimension)

    def push(self, widget):
        super().push(widget)
        self.toggle_back_button()

    def pop(self):
        super().pop()
        self.toggle_back_button()


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
            style=theme["text"],
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
