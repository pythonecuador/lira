#/usr/bin/env python
from prompt_toolkit.application import Application
from prompt_toolkit.document import Document
from prompt_toolkit.filters import has_focus
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, VSplit, Window
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import SearchToolbar, TextArea, Label


from prompt_toolkit.formatted_text import to_formatted_text, HTML, merge_formatted_text, FormattedText
from prompt_toolkit import print_formatted_text


from lira.book import Book
from pathlib import Path

path = Path('../tests/data/books/example/intro.rst')
book = Book(path)
book.parse()
print(book)


styles =  {
    'Text' :  '#ff0066 italic',
    'Strong' :  '#ff0066 italic',
    'Emphasis' :  '#ff0066 italic',
    'Literal' :  '#ff0066 italic',
    'Paragraph' :  '#ff0066 italic',
    'CodeBlock' :  '#ff0066 italic',
    'Prompt' :  '#ff0066 italic',
    'TestBlock' :  '#ff0066 italic',
    'Section' :  '#ff0066 italic',
}


def get_text(content):
    render = []
    for node in content.children:
        if node.is_terminal:
            text = node.text()
            style = node.tagname
            render.append(to_formatted_text(text, styles[style]))
        else:
            render += get_text(node)
    return render


render = get_text(book.content[0])


tutorial_label = Label(merge_formatted_text(render))


sections = {
    "menu": TextArea(
        height=40, width=20, style="class:output-field", text="Python-Tutorial\n"
    ),
    "status": TextArea(
        height=1,
        prompt=">>> ",
        style="class:input-field",
        multiline=False,
        wrap_lines=False,
    ),
    "text": TextArea(height=10, width=40, style="class:output-field", text='text'),
    "code": TextArea(height=10, width=40, style="class:output-field", text="code"),
    "prompt": TextArea(height=10, width=40, style="class:prompt", text="prompt"),
    "vseparator": Window(height=0, width=1, char="|", style="class:line"),
    "hseparator": Window(height=1, char="-", style="class:line"),
}


class TerminalUI:
    def __init__(self, tutorial_sections):
        sections_list = []
        for section in tutorial_sections:
            sections_list.append(sections[section])

        tutorial = HSplit(sections_list)

        self.container = HSplit([
            VSplit([
                sections["menu"],
                sections["vseparator"],
                HSplit([
                    tutorial_label,
                    sections["prompt"]
                ]),
            ]),
            sections["hseparator"],
            sections["status"],
        ])


def main():
    kb = KeyBindings()

    @kb.add("c-c")
    @kb.add("c-q")
    def _(event):
        " Pressing Ctrl-Q or Ctrl-C will exit the user interface. "
        event.app.exit()

    style = Style(
        [
            ("text", "bg:#000000 #ffffff"),
            ("prompt", "bg:#666666 #ffffff"),
            ("line", "#004400"),
        ]
    )

    terminal_ui = TerminalUI(["text", "prompt"])

    application = Application(
        layout=Layout(terminal_ui.container),
        key_bindings=kb,
        style=style,
        mouse_support=True,
        full_screen=True,
    )

    application.run()


if __name__ == "__main__":
    main()
