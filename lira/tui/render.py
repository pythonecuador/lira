from textwrap import indent

import pygments
from prompt_toolkit.formatted_text import PygmentsTokens, to_formatted_text
from prompt_toolkit.widgets.base import Border

from lira.parsers import State
from lira.tui.utils import get_lexer


class Renderer:

    styles = {
        "Text": "class:text",
        "Strong": "class:strong",
        "Emphasis": "class:emphasis",
    }
    states = {
        State.UNKNOWN: "•",
        State.INVALID: "✗",
        State.VALID: "✓",
    }

    def render(self, section, width=60):
        return self._render([section], width=width)

    def _render(self, children, width):
        content = []
        for child in children:
            tag = child.tagname
            if tag == "Section":
                content.append(to_formatted_text(child.options.title, "class:title"))
                content.extend(self._render(child.children, width=width))
            elif tag == "Paragraph":
                content.extend(self._render_separator())
                content.extend(self._render(child.children, width=width))
            elif tag == "CodeBlock":
                content.extend(self._render_separator())
                content.extend(self._render_code_block(child))
            elif tag == "TestBlock":
                content.extend(self._render_separator())
                content.extend(self._render_test_block(child, width=width))
            elif tag in ("Text", "Strong", "Emphasis"):
                content.append(to_formatted_text(child.text(), self.styles[tag]))
        return content

    def _render_separator(self):
        return [to_formatted_text("\n\n")]

    def _render_highlighted_block(self, content, language):
        code = indent(content, " " * 2)
        lexer = get_lexer(language or "")
        if lexer:
            formatted_text = PygmentsTokens(pygments.lex(code=code, lexer=lexer))
        else:
            formatted_text = to_formatted_text(
                code,
                style="",
            )
        return formatted_text

    def _render_code_block(self, node):
        return [
            self._render_highlighted_block(
                content=node.text(), language=node.options.language
            )
        ]

    def _render_test_block(self, node, width=60):
        title = node.options.description
        top_width = max(0, width - len(title) - 4)
        top = to_formatted_text(
            [
                ("", f"{Border.TOP_LEFT}{Border.HORIZONTAL} "),
                ("class:text", title),
                ("", " " + (Border.HORIZONTAL * top_width)),
            ]
        )

        state = self.states[node.options.state]
        menu_width = max(0, width - 26)
        menu = to_formatted_text(
            [
                ("", "- "),
                ("", "[Edit]"),
                ("", " "),
                ("", "[Load]"),
                ("", " "),
                ("", "[Run]"),
                ("", f" ({state})"),
                ("", " " + ("-" * menu_width)),
            ]
        )
        formatted_content = self._render_highlighted_block(
            content=node.text(),
            language=node.options.language,
        )

        bottom_width = width - 1
        bottom = to_formatted_text(
            Border.BOTTOM_LEFT + (Border.HORIZONTAL * bottom_width)
        )

        seperator = to_formatted_text("\n\n")
        return [top, seperator, menu, seperator, formatted_content, seperator, bottom]
