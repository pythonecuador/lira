from prompt_toolkit.application.current import get_app


def exit_app():
    """Exit the app and save any state."""
    get_app().exit()
