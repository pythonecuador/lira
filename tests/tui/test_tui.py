from prompt_toolkit.application import create_app_session
from prompt_toolkit.input import create_pipe_input
from prompt_toolkit.output import DummyOutput

from lira.tui import TerminalUI


class TestTUI:
    def test_layout(self):
        input = create_pipe_input()
        with create_app_session(input=input, output=DummyOutput()):
            tui = TerminalUI()
            layout = tui.app.layout
            assert len(list(layout.find_all_windows())) > 1

            children = layout.container.get_children()
            assert len(children) == 2
            assert len(children[0].get_children()) == 2
