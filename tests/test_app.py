from pathlib import Path
from unittest import mock

from lira.app import LiraApp

data_dir = Path(__file__).parent / "data"
config_file = data_dir / "books/config.yaml"
non_existing_config = data_dir / "books/config-not-found.yaml"


class TestApp:
    @mock.patch("lira.app.CONFIG_FILE", non_existing_config)
    def test_load_default_config(self):
        app = LiraApp()
        app.setup()

        assert not non_existing_config.exists()
        assert app.config is app.default_config

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

        assert book_b.metadata["title"] == "Basic Introduction to Python"
        book_path = data_dir / "books/example"
        assert book_b.root == book_path

    @mock.patch.object(LiraApp, "_read_config")
    def test_ignore_invalid_books(self, read_config):
        read_config.return_value = {
            "books": [
                "lira.not.found.module",
                "/lira/not/found/path",
                "lira/not/found/path",
                "lira.books.intro",
            ],
        }

        app = LiraApp()
        app.setup()

        books = app.books
        assert len(books) == 1
        book = books[0]
        book.parse()
        assert book.metadata["title"] == "Intro to Lira"
