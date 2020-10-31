from prompt_toolkit.application import Application
from prompt_toolkit.formatted_text import merge_formatted_text, to_formatted_text
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, VSplit, Window
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.widgets import Label, TextArea

from lira.app import LiraApp
from lira.book import Book
from lira.parsers.nodes import Section


from prompt_toolkit.application.current import get_app
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous
from prompt_toolkit.layout import HSplit, Layout, VSplit
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import Box, Button, Frame, Label, TextArea


class Tutorial:
    def __init__(self):
        self.text_area = TextArea(focusable=True)
        self.text_area.text = "Refresh"
        self.label = Label('Welcome to Lira! :)')
        self.label.text = ' to Lira! :)'

    def refresh(self, text):
        self.text_area.text = text
        self.label.text = text

    def get_label(self, contents):
        render = []
        for node in contents.children:
            if node.is_terminal:
                text = node.text()
                style = node.tagname
                render.append(to_formatted_text(text, styles[style]))
            else:
                render.extend(self.get_label(node))
        render.append(to_formatted_text("\n", ""))

        return render


class Menu:
    def __init__(self, lira):
        self.tutorial = Tutorial()

        self.selection =  lira
        self.items = self.get_nested_items()

        self.buttons = self.get_buttons()


    def get_top_items(self):
        """Return the list of items on top of the current menu item"""
        return ['PyTutorial', 'Clean Code', 'TDD', 'top']


    def get_nested_items(self):
        """Return the list of items nested on the current menu item"""
        nested_items = []

        self.selection.books[0].parse()
        chapter = self.selection.books[0].chapters[0]
        chapter.parse()
        self.contents = chapter.contents[1]

        toc = chapter.toc()

        for i in toc:
            nested_items.append(i[0])

        return nested_items


    def refresh_buttons(self):
        render = self.tutorial.get_label(self.contents)
        label = Label(merge_formatted_text(render))
        self.tutorial.label = label

        self.tutorial.refresh(str(self.tutorial.label))

        self.items = self.get_nested_items()
        self.buttons = self.get_buttons()


    def get_buttons(self):
        """Return a list of buttons from  a list of items"""
        buttons = []

        for item in self.items:
            buttons.append(Button(item, handler=self.refresh_buttons))

        buttons.append(Button("Exit", handler=exit))
        return buttons


def exit():
    get_app().exit()


text_area = TextArea(focusable=True)


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

    @keys.add("right")
    def _(event):
        c2 = HSplit(
            [
                Box(height=20, width=80,  body=Frame(Label('asdasdasd')), padding=1, style="class:right-pane"),
            ]
        )
        event.app.layout = Layout(c2)
        event.app.reset()

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


sections = {
    "menu": TextArea(
        height=40, width=20, style=styles["Text"], text=""
    ),
    "status": TextArea(
        height=3,
        prompt=">>> ",
        style=styles["Text"],
        multiline=False,
        wrap_lines=False,
    ),
    "text": TextArea(height=10, width=40, style=styles["Text"], text="text"),
    "prompt": TextArea(height=10, width=40, style=styles["Prompt"], text=""),
    "vseparator": Window(height=0, width=1, char="|", style=styles["Separator"]),
    "hseparator": Window(height=1, char="-", style=styles["Separator"]),
}


class TerminalUI():
    def __init__(self, root):
        self.theme = "default"

        self.lira = LiraApp()
        self.lira.setup()

        self.menu = Menu(self.lira)

        self.tutorial = self.menu.tutorial

        sections_list = []
        for section in ["text", "prompt"]:
            sections_list.append(sections[section])

        book = Book(root=root)
        book.parse()
        chapters = book.chapters[1]
        chapters.parse()

        contents = chapters.contents[0]
        render = self.get_label(contents)


        self.container = HSplit(
            [
                VSplit(
                    [
                        HSplit(self.menu.buttons, padding=1, height=40, width=25, style=styles["Text"]),
                        sections["vseparator"],
                        HSplit([Frame(self.menu.tutorial.label), 
                                Box(height=20, width=80,  body=Frame(self.tutorial.label), padding=1, style="class:right-pane"),
                                Box(height=20, width=80,  body=Frame(self.tutorial.text_area), padding=1, style="class:right-pane")]),
                    ]
                ),
                sections["hseparator"],
                sections["status"],
            ]
        )

    def get_label(self, contents):
        render = []
        for node in contents.children:
            if node.is_terminal:
                text = node.text()
                style = node.tagname
                render.append(to_formatted_text(text, styles[style]))
            else:
                render.extend(self.get_label(node))
        render.append(to_formatted_text("\n", ""))

        return render

    def run(self):
        self.app = Application(
            layout=Layout(self.container),
            key_bindings=get_key_bindings(),
            mouse_support=True,
            full_screen=True,
            min_redraw_interval=0.1,
        )

        self.app.run()
