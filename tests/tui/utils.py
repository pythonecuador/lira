from prompt_toolkit.formatted_text import fragment_list_to_text
from prompt_toolkit.layout import to_window


def to_widget(container):
    return container.content.text.__self__


def to_text(widget):
    control = to_window(widget).content
    return fragment_list_to_text(control.text())
