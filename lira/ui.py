from prompt_toolkit.application import Application
from prompt_toolkit.formatted_text import merge_formatted_text, to_formatted_text
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, VSplit, Window
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.widgets import Label, TextArea

from lira.app import LiraApp
from lira.book import Book


def get_key_bindings():
    keys = KeyBindings()

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
        "Prompt": "#fff",
        "TestBlock": "#fff",
        "Section": "#fff",
        "Separator": "#00ff00",
    }
}

styles = themes["default"]


sections = {
    "menu": TextArea(
        height=40, width=25, style=styles["Text"], text="Python-Tutorial\n"
    ),
    "status": TextArea(
        height=3,
        prompt=">>> ",
        style=styles["Text"],
        multiline=False,
        wrap_lines=False,
    ),
    "text": TextArea(height=10, width=40, style=styles["Text"], text="text"),
    "prompt": TextArea(height=10, width=40, style=styles["Text"], text="prompt"),
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
                        sections["menu"],
                        sections["vseparator"],
                        HSplit([label, sections["prompt"]]),
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
        lira = LiraApp()
        lira.setup()

        self.app = Application(
            layout=Layout(self.container),
            key_bindings=get_key_bindings(),
            mouse_support=True,
            full_screen=True,
        )

        self.app.run()
