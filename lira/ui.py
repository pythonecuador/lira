#/usr/bin/env python
from prompt_toolkit.application import Application
from prompt_toolkit.document import Document
from prompt_toolkit.filters import has_focus
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, VSplit, Window
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import SearchToolbar, TextArea, Label
from prompt_toolkit.formatted_text import to_formatted_text, merge_formatted_text, FormattedText
from prompt_toolkit import print_formatted_text


from lira.book import Book
from pathlib import Path


themes = {
    'default' : {
        'Text' :  '#fff',
        'Strong' :  '#fff bold',
        'Emphasis' :  '#fff italic',
        'Literal' :  '#fff',
        'Paragraph' :  '#fff',
        'CodeBlock' :  '#fff',
        'Prompt' :  '#fff',
        'TestBlock' :  '#fff',
        'Section' :  '#fff',
        'Separator' :  '#00ff00',
    }
}


styles = themes['default']


sections = {
    "menu": TextArea(
        height=40, width=25, style=styles['Text'], text="Python-Tutorial\n"
    ),
    "status": TextArea(
        height=3,
        prompt=">>> ",
        style=styles['Text'],
        multiline=False,
        wrap_lines=False,
    ),
    "text": TextArea(height=10, width=40, style=styles['Text'], text='text'),
    "prompt": TextArea(height=10, width=40, style=styles['Text'], text="prompt"),
    "vseparator": Window(height=0, width=1, char="|", style=styles['Separator']),
    "hseparator": Window(height=1, char="-", style=styles['Separator']),
}


class TerminalUI:
    path = Path('../tests/data/books/example/')
    book = Book(path=path)
    book.parse()

    chapters = book.chapters[1]
    chapters.parse()

    kb = KeyBindings()

    @kb.add("c-c")
    @kb.add("c-q")
    def _(self, event):
        " Pressing Ctrl-Q or Ctrl-C will exit the user interface."
        event.app.exit()


    def __init__(self):
        sections_list = []
        for section in ["text", "prompt"]:
            sections_list.append(sections[section])

        tutorial = HSplit(sections_list)

        contents  = self.chapters.contents[0]
        render = self.get_label(contents)
        label = Label(merge_formatted_text(render))


        self.container = HSplit([
            VSplit([
                sections["menu"],
                sections["vseparator"],
                HSplit([
                    label,
                    sections["prompt"]
                ]),
            ]),
            sections["hseparator"],
            sections["status"],
        ])


    def get_label(self, contents):

        render = []
        for node in contents.children:
            if node.is_terminal:
                text = node.text()
                style = node.tagname
                render.append(to_formatted_text(text, styles[style]))
            else:
                render += self.get_label(node)
        render.append(to_formatted_text('\n', ''))

        return render


    def run(self):
        self.app = Application(
            layout=Layout(self.container),
            key_bindings=self.kb,
            mouse_support=True,
            full_screen=True,
        )

        self.app.run()



if __name__ == "__main__":
    ui = TerminalUI()
    ui.theme = 'default'
    ui.run()
