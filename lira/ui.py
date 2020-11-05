from functools import partial

from prompt_toolkit.application import Application
from prompt_toolkit.application.current import get_app
from prompt_toolkit.formatted_text import merge_formatted_text, to_formatted_text
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous
from prompt_toolkit.layout.containers import HSplit, VSplit, Window, to_container
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import Box, Button, Label, TextArea

from lira.app import LiraApp


def get_key_bindings():
    keys = KeyBindings()

    @keys.add("tab")
    @keys.add("down")
    def _(event):
        focus_next(event)

    @keys.add("s-tab")
    @keys.add("up")
    def _(event):
        focus_previous(event)

    @keys.add("c-c")
    @keys.add("c-q")
    def _(event):
        """Pressing Ctrl-Q or Ctrl-C will exit the user interface."""
        event.app.exit()

    return keys


themes = {
    "default": {
        "Text": "#fff",
        "Strong": "#fff bold",
        "Emphasis": "#fff italic",
        "Literal": "#fff",
        "Paragraph": "#fff",
        "CodeBlock": "#fff",
        "Prompt": "bg:#999999 #fff",
        "TestBlock": "#fff",
        "Section": "#fff",
        "Separator": "#fff",
    }
}

styles = themes["default"]


style = Style(
    [
        ("left-pane", "bg:#888800 #000000"),
        ("right-pane", "bg:#00aa00 #000000"),
        ("button", "#000000"),
        ("button-arrow", "#000000"),
        ("button focused", "bg:#ff0000"),
        ("text-area focused", "bg:#ff0000"),
    ]
)


sections = {
    "menu": TextArea(height=40, width=20, style=styles["Text"], text=""),
    "status": TextArea(
        height=3,
        prompt=">>> ",
        style=styles["Text"],
        multiline=False,
        wrap_lines=False,
    ),
    "text": TextArea(height=10, width=40, style=styles["Text"], text="text"),
    "prompt": TextArea(height=10, width=40, style=styles["Prompt"], text=""),
    "vseparator": Window(height=0, width=1, char="│", style=styles["Separator"]),
    "hseparator": Window(height=1, char="─", style=styles["Separator"]),
}


class ContentArea:
    def __init__(self):
        self.text_area = TextArea(focusable=True)
        self.text_area.text = "Refresh"
        self.welcome = Label("Welcome to Lira! :)")
        self.container = Box(
            height=20, width=80, body=self.welcome, padding=1, style="class:right-pane"
        )

    def get_label(self, contents):
        formated_content = []
        for node in contents.children:
            text = node.text()
            style = node.tagname
            formated_content.append(to_formatted_text(text, styles[style]))
            if node.tagname == "Paragraph":
                formated_content.append(to_formatted_text("\n", ""))

        label = Label(merge_formatted_text(formated_content))

        return label

    def get_sections_list(self):
        sections_list = []
        for section in ["text", "prompt"]:
            sections_list.append(sections[section])

        return sections_list

    def render(self, section):
        app = get_app()
        vsplit = app.layout.container.get_children()[0]
        content = vsplit.get_children()[2]

        label = self.get_label(section)

        content.children = [
            to_container(
                Box(
                    height=20, width=80, body=label, padding=1, style="class:right-pane"
                )
            )
        ]


class SidebarMenu:
    def __init__(self, lira):
        self.lira = lira

        self.tutorial = ContentArea()

        self.items = self.get_nested_items()
        self.buttons = self.get_buttons()

        self.container = HSplit(
            self.buttons, padding=1, height=40, width=25, style=styles["Text"]
        )

    def get_top_items(self):
        """Return the list of items on top of the current menu item."""
        return ["PyTutorial", "Clean Code", "TDD", "top"]

    def get_nested_items(self):
        """Return the list of items nested on the current menu item."""
        nested_items = []

        self.lira.books[0].parse()
        chapter = self.lira.books[0].chapters[0]
        chapter.parse()
        self.contents = chapter.contents[1]
        self.toc = chapter.toc()

        for i in self.toc:
            nested_items.append(i[0].options.title)

        return nested_items

    def select_section(self, section):
        self.tutorial.render(section)

    def get_buttons(self):
        """Return a list of buttons from  a list of items."""
        buttons = []

        for i, item in enumerate(self.items):
            section = self.toc[i][0]
            buttons.append(
                Button(f"{i + 1}.{item}", handler=partial(self.select_section, section))
            )

        buttons.append(Button("Exit", handler=self.exit))
        return buttons

    def exit(self):
        get_app().exit()


class StatusBar:
    def __init__(self):
        self.container = sections["status"]


class TerminalUI:
    def __init__(self):
        self.theme = "default"

        self.lira = LiraApp()
        self.lira.setup()
        self.menu = SidebarMenu(self.lira)
        self.status = StatusBar()

        self.container = HSplit(
            [
                VSplit(
                    [
                        self.menu.container,
                        sections["vseparator"],
                        self.menu.tutorial.container,
                    ]
                ),
                sections["hseparator"],
                self.status.container,
            ]
        )

    def run(self):
        self.app = Application(
            layout=Layout(self.container),
            key_bindings=get_key_bindings(),
            mouse_support=True,
            full_screen=True,
        )

        self.app.run()
