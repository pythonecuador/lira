from pathlib import Path
from unittest import mock

from lira.app import LiraApp

data_dir = Path(__file__).parent / "data"
config_file = data_dir / "books/config.yaml"


class TestApp:
    @mock.patch("lira.app.CONFIG_FILE", config_file)
    def test_load_books(self):
        app = LiraApp()
        app.setup()

        books = app.books
        assert len(books) == 2

        book_a, book_b = books
        book_a.parse()
        book_b.parse()

        assert book_a.metadata["title"] == "Intro to Lira"
        book_path = data_dir / "../../lira/books/intro"
        assert book_a.root == book_path.resolve()

        assert book_b.metadata["title"] == "Basic Introducction to Python"
        book_path = data_dir / "books/example"
        assert book_b.root == book_path

    @mock.patch("lira.app.CONFIG_FILE", config_file)
    def test_cached_property(self):
        app = LiraApp()
        app.setup()
        books = app.books
        assert books == app.books
