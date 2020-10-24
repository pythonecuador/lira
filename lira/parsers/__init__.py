from pathlib import Path


class BaseParser:
    """
    Base class for a parser.

    The parser should parse the metadata from the file as a dictionary,
    and the content should be a list of nodes that subclass
    :py:class:`lira.parsers.nodes.Node`.

    :param content: Content to parse
    :param source: Source file of the content
    """

    def __init__(self, content: str, source: Path = None):
        self.content = content
        self.source = source

    def parse_metadata(self):
        raise NotImplementedError

    def parse_content(self):
        raise NotImplementedError
