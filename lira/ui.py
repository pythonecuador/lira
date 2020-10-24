from prompt_toolkit.application import Application
from prompt_toolkit.formatted_text import merge_formatted_text, to_formatted_text
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, VSplit, Window
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.widgets import Label, TextArea

from lira.book import Book


from prompt_toolkit.application import Application
from prompt_toolkit.application.current import get_app
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous
from prompt_toolkit.layout import HSplit, Layout, VSplit
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import Box, Button, Frame, Label, TextArea


def button1_clicked():
    text_area.text = "Python Tutorial"


def button2_clicked():
    text_area.text = "Clean Code"


def button3_clicked():
    text_area.text = "TDD"


def exit_clicked():
    get_app().exit()


button1 = Button("Python Tutorial", handler=button1_clicked)
button2 = Button("Clean Code", handler=button2_clicked)
button3 = Button("TDD", handler=button3_clicked)
button4 = Button("Exit", handler=exit_clicked)
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

    @keys.add("c-c")
    @keys.add("c-q")
    def _(event):
        "Pressing Ctrl-Q or Ctrl-C will exit the user interface."
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


class TerminalUI:
    def __init__(self, path):
        self.theme = "default"
        sections_list = []
        for section in ["text", "prompt"]:
            sections_list.append(sections[section])

        book = Book(root=path)
        book.parse()
        chapters = book.chapters[1]
        chapters.parse()

        contents = chapters.contents[0]
        render = self.get_label(contents)
        label = Label(merge_formatted_text(render))

        self.container = HSplit(
            [
                VSplit(
                    [
                        HSplit([button1, button2, button3, button4], padding=1),
                        sections["menu"],
                        sections["vseparator"],
                        HSplit([label, Box(height=20, width=80,  body=Frame(text_area), padding=1, style="class:right-pane")]),
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
        )

        self.app.run()
