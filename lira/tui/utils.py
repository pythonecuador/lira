from prompt_toolkit.application import get_app
from prompt_toolkit.shortcuts import set_title as set_app_title
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound


def exit_app():
    """Exit the app and save any state."""
    get_app().exit()


def set_title(title=""):
    if not title:
        text = "Lira"
    else:
        text = f"{title} - Lira"
    set_app_title(text)


def get_lexer(language):
    try:
        return get_lexer_by_name(language.strip().lower())
    except ClassNotFound:
        return None


def copy_to_clipboard(text):
    get_app().clipboard.set_text(text)


def notify_after_copy(tui, text):
    lines = len(text.split("\n"))
    if lines <= 1:
        msg = "One line copied!"
    else:
        msg = f"{lines} lines copied!"
    tui.status.notify(msg)
