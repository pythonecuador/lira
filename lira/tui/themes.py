from prompt_toolkit.styles import Style

themes = {
    "default": {
        "text": "#fff",
        "strong": "#fff bold",
        "literal": "#fff",
        "emphasis": "#fff italic",
        "title": "#55f bold",
        "separator": "#aaa",
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
