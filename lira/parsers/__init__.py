from pathlib import Path


class BaseParser:
    """
    Base class for a parser.

    The parser should parse the metadata from the file as a dictionary,
    and the content should be a list of nodes that subclass `lira.parsers.nodes.Node`.
    """

    def __init__(self, file: Path):
        self.file = file

    def parse_metadata(self):
        raise NotImplementedError

    def parse_content(self):
        raise NotImplementedError
