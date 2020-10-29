from pathlib import Path

import yaml

from lira.parsers.rst import RSTParser


class BookChapter:

    """
    Class representation of a chapter.

    The :py:meth:`parse` method should be called to initialize the :py:attr:`metadata`
    and :py:attr:`contents` attributes.

    Currently, the :py:class:`lira.parsers.rst.RSTParser` parser is used by default.

    .. code:: python

       from pathlib import Path
       from lira.book import BookChapter

       chapter = BookChapter(Path('intro.rst'))
       chapter.parse()
       print(chapter.metadata)
       print(chapter.contents)
       print(chapter.toc())

    :param file: File of the chapter
    :param title: Title of the chapter (defaults to the name of the file)
    """

    def __init__(self, *, file: Path, title: str = None):
        self.file = file
        self.title = title or file.name

        self.metadata = {}
        """Dictionary with the metadata from the book"""

        self.contents = []
        """List of nodes from :py:mod:`lira.parsers.nodes`"""

    def parse(self):
        """Parse the chapter content and initialize its attributes."""
        with self.file.open() as f:
            content = f.read()
        parser = RSTParser(content=content, source=self.file)
        self.metadata = parser.parse_metadata()
        self.contents = parser.parse_content()

    def toc(self, depth=2):
        """
        Return a list of tuples representing the table of contents.

        The first element of the tuple is the title,
        and the second is list of sub-sections
        (it can be empty if it doesn't have subsections).

        :param depth: Depth of the table of contents.
        """
        return self._toc(self.contents, depth)

    def _toc(self, nodes, depth):
        if depth <= 0:
            return []
        table = []
        for node in nodes:
            if node.tagname == "Section":
                title = node.options.title
                table.append((title, self._toc(node.children, depth=depth - 1)))
        return table

    def __repr__(self):
        return f"<BookChapter: {self.title}>"


class Book:

    """
    Class representation of a lira book.

    The :py:meth:`parse` method should be called to initialize the :py:attr:`metadata`
    and :py:attr:`chapters` attributes.

    .. code:: python

       from pathlib import Path
       from lira.book import Book

       book = Book(Path('books/example/'))
       book.parse()
       print(chapter.metadata)
       print(chapter.chapters)

    :param root: Path to the root directory of the book
    """

    meta_spec = {
        "language",
        "authors",
        "title",
        "description",
        "created",
        "updated",
        "chapters",
    }
    meta_file = "book.yaml"

    def __init__(self, root: Path):
        self.root = root

        self.metadata = {}
        """Dictionary with the metadata from the book"""

        self.chapters = []
        """List of :py:class:`lira.book.BookChapter` instances"""

    def parse(self, all: bool = False):
        """
        Parse the book metadata.

        :param all: If `True` all chapters are parsed as well
        """
        self.metadata = self._parse_metadata()
        self.chapters = self._parse_chapters(
            self.metadata["chapters"], parse_chapter=all
        )

    def _parse_metadata(self):
        meta_file = self.root / self.meta_file
        with meta_file.open() as f:
            yaml_data = yaml.safe_load(f)
        metadata = {}
        for key, val in yaml_data.items():
            if key in self.meta_spec:
                metadata[key] = val
        return metadata

    def _parse_chapters(self, contents, parse_chapter=False):
        chapters = []
        for title, file in contents.items():
            if isinstance(file, dict):
                # TODO: support sub-chapters?
                pass
            else:
                chapter = BookChapter(
                    file=self.root / file,
                    title=title,
                )
                if parse_chapter:
                    chapter.parse()
                chapters.append(chapter)
        return chapters

    def __repr__(self):
        title = self.metadata.get("title", "")
        return f"<Book: {title} -> {self.root.name}/>"
