from prompt_toolkit.styles import Style

themes = {
    "default": {
        # Node elements
        "text": "",
        "text.strong": "bold",
        "text.literal": "#fff",
        "text.emphasis": "italic",
        "text.title": "#fff bold",
        "text.description": "italic",
        "text.key": "bold",
        "text.value": "",
        # Inner widgets
        "separator.inner": "#aaa",
        "status": "bold",
        "status.unknown": "fg:#ebeb34",
        "status.valid": "fg:#14de17",
        "status.invalid": "fg:#de2514",
        "border.inner": "#aaa",
        "button.inner": "fg:#fff bg:#0055aa",
        "button.inner.border": "bold",
        # Custom widgets
        "separator": "#aaa",
        "title": "#fff bold",
        "list-item.focused": "bg:#0055aa #ffffff",
    }
}

theme = themes["default"]
style = Style.from_dict(theme)
