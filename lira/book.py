from pathlib import Path

from lira.parsers.rst import RSTParser


class Book:
    def __init__(self, file: Path):
        self.file = file
        self.parser = RSTParser(file)
        self.metadata = {}
        self.content = []

    def parse(self):
        self.metadata = self.parser.parse_metadata()
        self.content = self.parser.parse_content()
