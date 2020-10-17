from pathlib import Path


class BaseParser:
    def __init__(self, file: Path):
        self.file = file

    def parse_metadata(self):
        raise NotImplementedError

    def parse_content(self):
        raise NotImplementedError
