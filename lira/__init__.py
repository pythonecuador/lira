#!/usr/bin/env python
from prompt_toolkit.application import Application
from prompt_toolkit.document import Document
from prompt_toolkit.filters import has_focus
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import VSplit, HSplit, Window
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import SearchToolbar, TextArea


sections = {
    'menu' : TextArea(
        height=0,
        width=20,
        style="class:output-field",
        text='Python-Tutorial\n'
        ),
    'status' : TextArea(
        height=1,
        prompt=">>> ",
        style="class:input-field",
        multiline=False,
        wrap_lines=False,
    ),
    'text' : TextArea(
        height=10,
        width=80,
        style="class:output-field",
        text='text'
    ),
    'code' : TextArea(
        height=10,
        width=80,
        style="class:output-field",
        text='code'
    ),
    'prompt' : TextArea(
        height=10,
        width=80,
        style="class:output-field",
        text='prompt'
    ),
    'vseparator' : Window(height=0, width=1, char="|", style="class:line"),
    'hseparator' : Window(height=1, char="-", style="class:line"),
}


class TerminalUI:
    def __init__(self, tutorial_sections):
        sections_list = []
        for section in tutorial_sections:
            sections_list.append(sections[section])

        tutorial  = HSplit(sections_list)

        self.container = HSplit(
            [
                VSplit(
                    [
                    sections['menu'],
                    sections['vseparator'],
                    tutorial,
                    ]
                ),
                sections['hseparator'],
                sections['status'],
            ]
        )


def main():
    kb = KeyBindings()

    @kb.add("c-c")
    @kb.add("c-q")
    def _(event):
        " Pressing Ctrl-Q or Ctrl-C will exit the user interface. "
        event.app.exit()

    style = Style(
        [
            ("output-field", "bg:#000000 #ffffff"),
            ("input-field", "bg:#000000 #ffffff"),
            ("line", "#004400"),
        ]
    )

    terminal_ui = TerminalUI(['text', 'text', 'text'])

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
