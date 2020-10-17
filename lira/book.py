from pathlib import Path

from lira.parsers.rst import RSTParser


class Book:

    """
    Class representation of a lira book.

    The `parse` method should be called to initialize its attributes

    - `metadata`: dictionary with the metadata from the book.
    - `content`: list of nodes from `lira.parsers.nodes`.

    Currently, the RSTParser is used by default.
    """

    def __init__(self, file: Path):
        self.file = file
        self.parser = RSTParser(file)
        self.metadata = {}
        self.content = []

    def parse(self):
        self.metadata = self.parser.parse_metadata()
        self.content = self.parser.parse_content()
