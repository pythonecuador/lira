from prompt_toolkit.styles import Style

themes = {
    "default": {
        # Basic elements
        "text": "#fff",
        "strong": "#fff bold",
        "literal": "#fff",
        "emphasis": "#fff italic",
        "title": "#fff bold",
        "description": "italic",
        "separator": "#aaa",
        "key": "bold",
        "value": "",
        # Custom widgets
        "list-item.focused": "bg:#0055aa #ffffff",
    }
}

theme = themes["default"]
style = Style.from_dict(theme)

theme["nodes"] = {
    "Text": theme["text"],
    "Strong": theme["strong"],
    "Emphasis": theme["emphasis"],
    "Literal": theme["literal"],
    "Section": theme["title"],
    # TODO: delete these
    "Paragraph": "#fff",
    "CodeBlock": "#fff",
    "Prompt": "bg:#999999 #fff",
    "TestBlock": "#fff",
}
