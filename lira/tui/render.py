import logging
from functools import partial
from textwrap import indent

import click
import pygments
from prompt_toolkit.formatted_text import PygmentsTokens, to_formatted_text
from prompt_toolkit.mouse_events import MouseEventType
from prompt_toolkit.widgets.base import Border

from lira.parsers import State
from lira.tui.utils import copy_to_clipboard, get_lexer, notify_after_copy

log = logging.getLogger(__name__)


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

    def __init__(self, tui, section, width=60):
        self.tui = tui
        self.section = section
        self.width = width

    def render(self):
        return self._render([self.section])

    def _render(self, children):
        content = []
        for child in children:
            tag = child.tagname
            if tag == "Section":
                content.append(
                    to_formatted_text(child.options.title, "class:text.title")
                )
                content.extend(self._render(child.children))
            elif tag == "Paragraph":
                content.extend(self._render_separator())
                content.extend(self._render(child.children))
            elif tag == "CodeBlock":
                content.extend(self._render_separator())
                content.extend(self._render_code_block(child))
            elif tag == "TestBlock":
                content.extend(self._render_separator())
                content.extend(self._render_test_block(child))
            elif tag in ("Text", "Strong", "Emphasis", "Literal"):
                content.append(to_formatted_text(child.text(), self.styles[tag]))
            else:
                log.warning("Node not rendered. Unknown node: %s", tag)
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

    def _render_top_seperator(self, title=None):
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
        top_width = max(0, self.width - title_len - 2)
        formatted_text.append(
            ("class:border.inner", Border.HORIZONTAL * top_width),
        )
        return to_formatted_text(formatted_text)

    def _render_bottom_seperator(self):
        bottom_width = self.width - 1
        return to_formatted_text(
            [
                (
                    "class:border.inner",
                    Border.BOTTOM_LEFT + (Border.HORIZONTAL * bottom_width),
                ),
            ]
        )

    def _render_menu(self, items, state=None, top=False):
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

        menu_width = max(0, self.width - char_len)
        formatted_text.append(("class:border.inner", seperator * menu_width))
        return to_formatted_text(formatted_text)

    def _render_code_block(self, node):
        menu = self._render_menu(
            [("Copy", partial(self._copy_action, node))],
            top=True,
        )
        content = self._render_highlighted_block(
            content=node.text(),
            language=node.options.language,
        )
        bottom = self._render_bottom_seperator()
        seperator = to_formatted_text("\n\n")
        return [menu, seperator, content, seperator, bottom]

    def _render_test_block(self, node):
        top = self._render_top_seperator(
            title=node.options.description,
        )
        menu = self._render_menu(
            [
                ("Edit", partial(self._edit_action, node)),
                ("Reset", partial(self._reset_action, node)),
                ("Check", lambda x: None),
            ],
            state=node.options.state,
        )
        content = self._render_highlighted_block(
            content=node.text(),
            language=node.options.language,
        )
        bottom = self._render_bottom_seperator()
        seperator = to_formatted_text("\n\n")
        return [top, seperator, menu, seperator, content, seperator, bottom]

    def _copy_action(self, node, mouse_event):
        text = node.text()
        if text:
            copy_to_clipboard(text)
            notify_after_copy(self.tui, text)

    def _reset_action(self, node, mouse_event):
        if mouse_event.event_type == MouseEventType.MOUSE_UP:
            node.reset()
            self.tui.content.update_section(self.section)

    def _edit_action(self, node, mouse_event):
        if mouse_event.event_type == MouseEventType.MOUSE_UP:
            self._open_editor(node)
            self.tui.content.update_section(self.section)

    def _open_editor(self, node):
        """
        Open a editor to edit the content of the node.

        .. note::

           if a terminal editor is opened it will mess up with the terminal,
           we need to figure out how to refresh it.
           Users can trigger a refresh with ctrl+l.
        """
        try:
            extension = node.options.extension
            text = click.edit(text=node.text(), extension=extension)
            if text is not None:
                node.content = text.split("\n")
        except click.UsageError:
            log.warning("Editor not available")
