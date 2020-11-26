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
