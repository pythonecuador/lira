from pathlib import Path

import yaml

from lira.parsers.rst import RSTParser


class BookChapter:

    """
    Class representation of a chapter.

    The `parse` method should be called to initialize its attributes

    - `metadata`: dictionary with the metadata from the book.
    - `contents`: list of nodes from `lira.parsers.nodes`.

    Currently, the RSTParser is used by default.


    .. code:: python

       from pathlib import Path
       from lira.book import BookChapter

       chapter = BookChapter(Path('intro.rst'))
       chapter.parse()
       print(chapter.metadata)
       print(chapter.contents)
       print(chapter.toc())
    """

    def __init__(self, *, file: Path, title: str = None):
        self.file = file
        self.title = title or file.name
        self.parser = RSTParser(file)
        self.metadata = {}
        self.contents = []

    def parse(self):
        """
        Parse the chapter content and initialize its attributes.

        This method should be called before accessing the
        `metadata` or `contents` attributes.
        """
        self.metadata = self.parser.parse_metadata()
        self.contents = self.parser.parse_content()

    def toc(self, depth=2):
        """
        A list of tuples representing the table of contents.

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
                title = node.options["title"]
                table.append((title, self._toc(node.children, depth=depth - 1)))
        return table

    def __repr__(self):
        return f"<BookChapter: {self.title}>"


class Book:

    """
    Class representation of a lira book.

    The `parse` method should be called to initialize its attributes

    - `metadata`: dictionary with the metadata from the book.
    - `chapters`: list of `BookChapter` instances.

    .. code:: python

       from pathlib import Path
       from lira.book import Book

       book = Book(Path('books/example/'))
       book.parse()
       print(chapter.metadata)
       print(chapter.chapters)
    """

    meta_spec = {
        "language",
        "authors",
        "title",
        "description",
        "created",
        "updated",
        "contents",
    }
    meta_file = "book.yaml"

    def __init__(self, *, module: str = None, path: Path = None):
        if (module and path) or (not module and not path):
            raise ValueError
        # TODO: handle a module too
        self.path = path
        self.root = path
        self.metadata = {}
        self.chapters = []

    def parse(self, all=False):
        self.metadata = self._parse_metadata()
        self.chapters = self._parse_chapters(
            self.metadata["contents"], parse_chapter=all
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
