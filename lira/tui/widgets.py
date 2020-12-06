import logging
from functools import partial

from prompt_toolkit.application import get_app
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.data_structures import Point
from prompt_toolkit.filters import Condition
from prompt_toolkit.formatted_text import (
    fragment_list_to_text,
    split_lines,
    to_formatted_text,
)
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous
from prompt_toolkit.keys import Keys
from prompt_toolkit.layout import (
    BufferControl,
    ConditionalMargin,
    Dimension,
    FormattedTextControl,
    HSplit,
    ScrollbarMargin,
    Window,
    WindowAlign,
)
from prompt_toolkit.layout.processors import (
    Document,
    HighlightSelectionProcessor,
    Processor,
    Transformation,
)
from prompt_toolkit.mouse_events import MouseEvent, MouseEventType
from prompt_toolkit.widgets import Box
from prompt_toolkit.widgets import Button as ToolkitButton

from lira.tui.utils import set_title

log = logging.getLogger(__name__)


class Button(ToolkitButton):

    """
    Override the default button to use a different style.

    By default buttons look like::

        < Button >

    Now they look like::

        [ Button ]
    """

    def _get_text_fragments(self):
        width = self.width - 2
        text = (f"{{:^{width}}}").format(self.text)

        def handler(mouse_event):
            if (
                self.handler is not None
                and mouse_event.event_type == MouseEventType.MOUSE_UP
            ):
                self.handler()

        return [
            ("class:button.arrow", "[", handler),
            ("[SetCursorPosition]", ""),
            ("class:button.text", text, handler),
            ("class:button.arrow", "]", handler),
        ]


class FormatTextProcessor(Processor):

    """
    Custom processor to represent formatted text.

    It makes use of :py:class:`FormattedBufferControl`.
    """

    def apply_transformation(self, transformation_input):
        formatted_lines = transformation_input.buffer_control.formatted_lines
        lineno = transformation_input.lineno
        max_lineno = len(formatted_lines) - 1
        if lineno > max_lineno:
            log.warning(
                "Index error when parsing document. max_lineno=%s lineno=%s",
                max_lineno,
                lineno,
            )
            lineno = max_lineno
        line = formatted_lines[lineno]
        return Transformation(to_formatted_text(line))


class FormattedBufferControl(BufferControl):

    """Control to support formatted_text and mouse events."""

    def __init__(self, formatted_text, **kwargs):
        self.formatted_lines = list(split_lines(formatted_text))
        super().__init__(**kwargs)

    def update_formatted_text(self, formatted_text):
        self.formatted_lines = list(split_lines(formatted_text))

    def mouse_handler(self, mouse_event):
        """
        Handle formatted text handlers.

        Taken from ``FormattedTextControl.mouse_handler``.
        """
        response = super().mouse_handler(mouse_event)

        if mouse_event.position.y >= len(self.formatted_lines):
            return response

        self.select(mouse_event)
        return response

    def select(self, mouse_event):
        fragments = self.formatted_lines[mouse_event.position.y]
        # Find position in the fragment list.
        xpos = mouse_event.position.x + 1

        # Find mouse handler for this character.
        count = 0
        for item in fragments:
            count += len(item[1])
            if count >= xpos:
                if len(item) >= 3:
                    handler = item[2]
                    return handler(mouse_event)
                break


class FormattedTextArea:

    """Just like text area, but it accepts formatted content."""

    def __init__(
        self,
        text="",
        focusable=False,
        wrap_lines=True,
        width=None,
        height=None,
        scrollbar=False,
        dont_extend_height=True,
        dont_extend_width=False,
        read_only=True,
        initial_position=0,
    ):
        self.read_only = read_only
        formatted_text = to_formatted_text(text)
        plain_text = fragment_list_to_text(formatted_text)
        self.buffer = Buffer(
            document=Document(plain_text, initial_position),
            read_only=Condition(lambda: self.read_only),
        )
        self.control = FormattedBufferControl(
            buffer=self.buffer,
            formatted_text=formatted_text,
            input_processors=[FormatTextProcessor(), HighlightSelectionProcessor()],
            key_bindings=self.get_key_bindings(),
            include_default_input_processors=False,
            focusable=focusable,
            focus_on_click=focusable,
        )
        self.scrollbar = scrollbar
        right_margins = [
            ConditionalMargin(
                ScrollbarMargin(display_arrows=True),
                filter=Condition(lambda: self.scrollbar),
            ),
        ]
        self.window = Window(
            content=self.control,
            width=width,
            height=height,
            wrap_lines=wrap_lines,
            right_margins=right_margins,
            dont_extend_height=dont_extend_height,
            dont_extend_width=dont_extend_width,
        )

    @property
    def document(self):
        return self.buffer.document

    @document.setter
    def document(self, value):
        self.buffer.set_document(value, bypass_readonly=True)

    @property
    def text(self):
        return self.buffer.text

    @text.setter
    def text(self, text):
        formatted_text = to_formatted_text(text)
        self.control.update_formatted_text(formatted_text)
        plain_text = fragment_list_to_text(formatted_text)
        current_position = min(self.document.cursor_position, len(plain_text))
        self.document = Document(plain_text, current_position)

    def get_key_bindings(self):
        keys = KeyBindings()

        @keys.add(" ")
        @keys.add(Keys.Enter)
        def _(event):
            row = self.document.cursor_position_row
            col = self.document.cursor_position_col
            mouse_event = MouseEvent(Point(col, row), MouseEventType.MOUSE_UP)
            self.control.select(mouse_event)

        return keys

    def __pt_container__(self):
        return self.window


class ListElement:

    """
    Element used by :py:class:`List`.

    :param text: Text to be displayed.
    :param on_select: Function to be call when the element is selected.
    :param on_focus: Function to be call when the element gains focus.
    """

    def __init__(self, text: str = "", on_select=None, on_focus=None):
        self.text = text
        self.on_select = on_select
        self.on_focus = on_focus


class List:

    """
    List widget.

    :param title: Any formatted text to be used as the title of the list.
    :param elements: List of :py:class:`ListElement`.
    :param get_bullet: A function (function(line)) to be called to get the
    bullet of the element in that line number.
    :param allow_select: If `True`, display an extra column indicating the
    current selected item. Util when you want to keep the list after the
    element is selected.
    """

    def __init__(
        self,
        title=None,
        elements=None,
        width=None,
        height=None,
        align=WindowAlign.LEFT,
        get_bullet=None,
        allow_select=True,
        scrollbar=True,
    ):
        self.index = 0
        self.get_bullet = get_bullet
        self.selected = -1
        self.elements = elements or []
        self.title = title
        self.allow_select = allow_select
        self.cursor = Point(0, 0)
        self.scrollbar = scrollbar
        self.control = FormattedTextControl(
            text=self._get_text,
            focusable=True,
            get_cursor_position=lambda: self.cursor,
            key_bindings=self.get_key_bindings(),
        )

        # TODO: figure out how to the make it look nicer
        right_margins = [
            ConditionalMargin(
                ScrollbarMargin(display_arrows=True),
                filter=Condition(lambda: self.scrollbar),
            ),
        ]
        self.title_window = FormattedTextArea(
            text=self.title,
            height=Dimension(min=1),
            width=Dimension(min=1),
        )
        self.list_window = Window(
            content=self.control,
            width=width,
            height=height,
            always_hide_cursor=False,
            style="class:list",
            wrap_lines=True,
            dont_extend_height=True,
            dont_extend_width=False,
            cursorline=False,
            right_margins=right_margins,
            allow_scroll_beyond_bottom=True,
            get_line_prefix=self._get_line_prefix,
        )
        self.window = HSplit(
            children=[
                Box(
                    self.title_window,
                    padding=Dimension.exact(1),
                ),
                Box(
                    self.list_window,
                    padding=Dimension.exact(1),
                    padding_top=Dimension.exact(0),
                ),
            ],
            height=Dimension(min=1),
            width=Dimension(min=1),
        )

    def _get_line_prefix(self, line, wrap_count):
        bullet = self.get_bullet(line) if self.get_bullet else " "
        if self.allow_select:
            if self.selected == line:
                bullet = "• " + bullet
            else:
                bullet = "  " + bullet
        if wrap_count:
            return " " * len(bullet)
        return bullet

    def _get_text(self):
        formatted_text = []
        for i, element in enumerate(self.elements):
            text = element.text.replace("\n", " ")
            style = ""
            if i < len(self.elements) - 1:
                text += "\n"
            if i == self.index:
                style = "class:list-item.focused"
            formatted_text.append(
                (
                    style,
                    text,
                    partial(self.mouse_select, i),
                )
            )
        return formatted_text

    @property
    def current_element(self):
        return self.elements[self.index]

    def mouse_select(self, index, mouse_event):
        if mouse_event.event_type == MouseEventType.MOUSE_UP:
            app = get_app()
            app.layout.focus(self)
            self.select(index)

    def select(self, index):
        self.index = index
        self.selected = self.index
        self.cursor = Point(0, self.index)
        element = self.current_element
        if element.on_select:
            element.on_select()

    def focus(self, index):
        self.index = index
        self.cursor = Point(0, self.index)
        element = self.current_element
        if element.on_focus:
            element.on_focus()

    def previous(self):
        index = max(self.index - 1, 0)
        self.focus(index)

    def next(self):
        index = min(self.index + 1, len(self.elements) - 1)
        self.focus(index)

    def get_key_bindings(self):
        keys = KeyBindings()

        @keys.add(Keys.Up)
        def _(event):
            self.previous()

        @keys.add(Keys.BackTab)
        def _(event):
            if self.index <= 0:
                focus_previous(event)
            else:
                self.previous()

        @keys.add(Keys.Down)
        def _(event):
            self.next()

        @keys.add(Keys.Tab)
        def _(event):
            if self.index >= len(self.elements) - 1:
                focus_next(event)
            else:
                self.next()

        @keys.add(" ")
        @keys.add(Keys.Enter)
        def _(event):
            self.select(self.index)

        return keys

    def __pt_container__(self):
        return self.window


class LiraList:

    """Wrapped around :py:class:`List`."""

    allow_select = False

    def __init__(self, tui):
        self.tui = tui
        self.lira = self.tui.lira
        self.container = List(
            title=self._get_title(),
            elements=self._get_elements(),
            get_bullet=self._get_bullet,
            allow_select=self.allow_select,
            width=Dimension(min=1),
            height=Dimension(min=1),
        )

    def _get_title(self):
        raise NotImplementedError

    def _get_elements(self):
        raise NotImplementedError

    def _get_bullet(self, line):
        return "• "

    def __pt_container__(self):
        return self.container


class BooksList(LiraList):

    """List of :py:class:`lira.book.Book`."""

    def _get_title(self):
        return to_formatted_text([("class:title", "Books")])

    def _get_elements(self):
        elements = []
        for i, book in enumerate(self.lira.books):
            book.parse()
            title = book.metadata["title"]
            elements.append(
                ListElement(
                    text=title,
                    on_select=partial(self._select, book, i),
                    on_focus=partial(self._focus, book, i),
                )
            )
        return elements

    def _select(self, book, index=0):
        widget = BookChaptersList(tui=self.tui, book=book)
        set_title(book.metadata["title"])
        self.tui.menu.push(widget)

    def _focus(self, book, index):
        title = book.metadata["title"]
        description = book.metadata["description"]
        language = book.metadata["language"]
        authors = ", ".join(book.metadata["authors"])
        published = book.metadata["published"]
        updated = book.metadata["updated"]
        formatted_text = [
            ("class:text.title", title),
            ("", "\n\n"),
        ]
        if description:
            formatted_text.extend(
                [
                    ("class:text.description", description),
                    ("", "\n\n"),
                ]
            )

        metadata = [
            ("Authors", authors),
            ("Language", language),
            ("Published", published),
            ("Updated", updated),
        ]
        for key, value in metadata:
            if not value:
                continue
            formatted_text.extend(
                [
                    ("class:text.key", key),
                    ("class:text.separator", ":"),
                    ("", " "),
                    ("class:text.value", value),
                    ("", "\n"),
                ]
            )
        text_area = FormattedTextArea(
            text=to_formatted_text(formatted_text),
            focusable=True,
            scrollbar=True,
        )
        self.tui.content.reset(text_area)


class BookChaptersList(LiraList):

    """List of :py:class:`lira.book.BookChapter`."""

    def __init__(self, tui, book):
        self.book = book
        super().__init__(tui)

    def _get_title(self):
        book_title = self.book.metadata["title"]
        return to_formatted_text([("class:title", book_title)])

    def _get_bullet(self, line):
        return f"{line + 1}. "

    def _get_elements(self):
        elements = []
        for i, chapter in enumerate(self.book.chapters):
            chapter.parse()
            elements.append(
                ListElement(
                    text=chapter.title,
                    on_select=partial(self._select, chapter, i),
                )
            )
        return elements

    def _select(self, chapter, index):
        widget = ChapterSectionsList(
            tui=self.tui,
            chapter=chapter,
            index=index,
        )
        self.tui.menu.push(widget)


class ChapterSectionsList(LiraList):

    """List of :py:class:`lira.parsers.nodes.Section`."""

    allow_select = True

    def __init__(self, tui, chapter, index):
        self.index = index
        self.chapter = chapter
        self.toc = self.chapter.toc(depth=1)
        super().__init__(tui)

        # Select first item automatically
        self.container.select(0)

    def _get_title(self):
        book_title = self.chapter.book.metadata["title"]
        return to_formatted_text(
            [
                ("class:title", book_title),
                ("", " "),
                ("class:seperator", ">"),
                ("", " "),
                ("class:title", self.chapter.title),
            ]
        )

    def _get_bullet(self, line):
        return f"{self.index + 1}.{line + 1}. "

    def _get_elements(self):
        elements = []
        for section, _ in self.toc:
            elements.append(
                ListElement(
                    text=section.options.title,
                    on_select=partial(self._select, section),
                )
            )
        return elements

    def _select(self, section):
        self.tui.content.render_section(section)
