from textwrap import indent

import pygments
from prompt_toolkit.formatted_text import PygmentsTokens, to_formatted_text
from prompt_toolkit.widgets.base import Border

from lira.parsers import State
from lira.tui.utils import get_lexer


class Renderer:

    styles = {
        "Text": "class:text",
        "Strong": "class:text.strong",
        "Emphasis": "class:text.emphasis",
        "Literal": "class:text.literal",
    }
    states = {
        State.UNKNOWN: ("•", "class:status.unknown"),
        State.INVALID: ("✗", "class:status.invalid"),
        State.VALID: ("✓", "class:status.valid"),
    }

    def render(self, section, width=60):
        return self._render([section], width=width)

    def _render(self, children, width):
        content = []
        for child in children:
            tag = child.tagname
            if tag == "Section":
                content.append(
                    to_formatted_text(child.options.title, "class:text.title")
                )
                content.extend(self._render(child.children, width=width))
            elif tag == "Paragraph":
                content.extend(self._render_separator())
                content.extend(self._render(child.children, width=width))
            elif tag == "CodeBlock":
                content.extend(self._render_separator())
                content.extend(self._render_code_block(child, width=width))
            elif tag == "TestBlock":
                content.extend(self._render_separator())
                content.extend(self._render_test_block(child, width=width))
            elif tag in ("Text", "Strong", "Emphasis", "Literal"):
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

    def _render_top_seperator(self, title=None, width=60):
        title = title or ""
        formatted_text = [
            ("class:border.inner", f"{Border.TOP_LEFT}{Border.HORIZONTAL}"),
        ]
        if title:
            formatted_text.extend(
                [
                    ("", " "),
                    ("class:text.title", title),
                    ("", " "),
                ]
            )
        title_len = len(title) + 2 if title else 0
        top_width = max(0, width - title_len - 2)
        formatted_text.append(
            ("class:border.inner", Border.HORIZONTAL * top_width),
        )
        return to_formatted_text(formatted_text)

    def _render_bottom_seperator(self, width=60):
        bottom_width = width - 1
        return to_formatted_text(
            [
                (
                    "class:border.inner",
                    Border.BOTTOM_LEFT + (Border.HORIZONTAL * bottom_width),
                ),
            ]
        )

    def _render_menu(self, items, state=None, width=60, top=False):
        seperator = "-"
        char_len = 0
        formatted_text = []
        if top:
            seperator = Border.HORIZONTAL
            formatted_text.extend(
                [
                    ("class:border.inner", Border.TOP_LEFT),
                    ("class:border.inner", seperator),
                    ("", " "),
                ]
            )
            char_len += 3
        else:
            formatted_text.extend(
                [
                    ("class:border.inner", seperator),
                    ("", " "),
                ]
            )
            char_len += 2
        for item, handler in items:
            formatted_text.extend(
                [
                    ("class:button.inner.border", "[", handler),
                    ("class:button.inner", f" {item} ", handler),
                    ("class:button.inner.border", "]", handler),
                    ("", " "),
                ]
            )
            char_len += len(item) + 5

        if state is not None:
            symbol, style = self.states[state]
            formatted_text.extend(
                [
                    (style, f"({symbol})"),
                    ("", " "),
                ]
            )
            char_len += len(symbol) + 3

        menu_width = max(0, width - char_len)
        formatted_text.append(("class:border.inner", seperator * menu_width))
        return to_formatted_text(formatted_text)

    def _render_code_block(self, node, width):
        menu = self._render_menu(
            [("Copy", lambda x: None)],
            width=width,
            top=True,
        )
        content = self._render_highlighted_block(
            content=node.text(),
            language=node.options.language,
        )
        bottom = self._render_bottom_seperator(width=width)
        seperator = to_formatted_text("\n\n")
        return [menu, seperator, content, seperator, bottom]

    def _render_test_block(self, node, width=60):
        top = self._render_top_seperator(
            title=node.options.description,
            width=width,
        )
        menu = self._render_menu(
            [
                ("Edit", lambda x: None),
                ("Load", lambda x: None),
                ("Run", lambda x: None),
            ],
            state=node.options.state,
            width=width,
        )
        content = self._render_highlighted_block(
            content=node.text(),
            language=node.options.language,
        )
        bottom = self._render_bottom_seperator(width=width)
        seperator = to_formatted_text("\n\n")
        return [top, seperator, menu, seperator, content, seperator, bottom]
