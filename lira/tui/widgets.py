from functools import partial

from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.layout import Dimension, Window, WindowAlign
from prompt_toolkit.layout.containers import HSplit
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.widgets import Box, Button, Label

from lira.tui.utils import set_title


class FormattedTextArea:
    def __init__(
        self,
        text="",
        focusable=False,
        wrap_lines=True,
        width=None,
        height=None,
        align=WindowAlign.LEFT,
        style="",
    ):
        self.text = text
        self.formatted_text_control = FormattedTextControl(
            text=lambda: self.text,
            focusable=focusable,
        )
        self.window = Window(
            content=self.formatted_text_control,
            width=width,
            height=height,
            style="class:formatted-text-area " + style,
            wrap_lines=wrap_lines,
            dont_extend_height=True,
            dont_extend_width=False,
        )

    def __pt_container__(self):
        return self.window


class List:
    def __init__(self, tui, parent=None, index=0):
        self.tui = tui
        self.lira = self.tui.lira
        self.parent = parent
        self.index = index
        self.elements = self._get_elements()
        self.container = HSplit(
            children=self.elements,
            height=Dimension(min=1),
            width=Dimension(min=1),
        )

    def get_title(self, text):
        return Box(
            Label(text),
            padding=Dimension.exact(1),
        )

    def _get_elements(self):
        return []

    def select(self, element, index=0):
        raise NotImplementedError

    def __pt_container__(self):
        return self.container


class BooksList(List):
    def _get_elements(self):
        buttons = [self.get_title(HTML("<title>{}</title>").format("Books"))]
        for i, book in enumerate(self.lira.books):
            book.parse()
            title = book.metadata["title"]
            buttons.append(Button(f"{title}", handler=partial(self.select, book, i)))
        return buttons

    def select(self, book, index=0):
        widget = BookChaptersList(self.tui, book)
        set_title(book.metadata["title"])
        self.tui.menu.push(widget)


class BookChaptersList(List):
    def _get_elements(self):
        book = self.parent
        book_title = book.metadata["title"]
        buttons = [self.get_title(HTML("<title>{}</title>").format(book_title))]
        for i, chapter in enumerate(book.chapters):
            chapter.parse()
            buttons.append(
                Button(
                    f"{i + 1}. {chapter.title}",
                    handler=partial(self.select, chapter, i),
                )
            )
        return buttons

    def select(self, chapter, index):
        widget = ChapterSectionsList(self.tui, chapter, index)
        self.tui.menu.push(widget)


class ChapterSectionsList(List):
    def __init__(self, tui, parent, index):
        self.index = index
        self.toc = parent.toc(depth=1)
        super().__init__(tui, parent, index)

        # Change the window content to the first section
        if self.toc:
            self.select(self.toc[0][0])

    def _get_elements(self):
        chapter = self.parent
        book_title = chapter.book.metadata["title"]
        text = HTML(
            "<title>{}</title> <separator>></separator> <title>{}</title>"
        ).format(book_title, chapter.title)
        buttons = [self.get_title(text)]
        for i, element in enumerate(self.toc):
            section, _ = element
            buttons.append(
                Button(
                    f"{self.index + 1}.{i + 1}. {section.options.title}",
                    handler=partial(self.select, section),
                )
            )
        return buttons

    def select(self, section, index=0):
        self.tui.content.render_section(section)
