import importlib
import logging
from pathlib import Path

import yaml

from lira.book import Book
from lira.config import CONFIG_DIR, CONFIG_FILE, DATA_DIR, LOG_DIR

log = logging.getLogger(__name__)


class LiraApp:

    """
    Lira application.

    This class is used to interact with Lira.
    Before using this class you'll need to call to :py:method:`setup`.

    If you want to refresh the options with the latest configuration,
    call to :py:method:`load_config`.
    """

    default_config = {
        "books": ["lira.books.intro"],
    }

    def __init__(self):
        self.config = {}
        """Dictionary with the user configuration."""

        self.books = []
        """List of :py:class:`lira.book.Book`"""

    def _create_dirs(self):
        for dir in [CONFIG_DIR, DATA_DIR, LOG_DIR]:
            dir.mkdir(parents=True, exist_ok=True)

    def _setup_logger(self):
        logging.basicConfig(
            filename=LOG_DIR / "lira.log",
            format="%(asctime)s [%(levelname)s] [%(name)s:%(lineno)d]: %(message)s",
            datefmt="%d/%m/%Y %H:%M:%S",
            filemode="w",
            level=logging.WARNING,
        )

    def _read_config(self, file):
        if not file.exists():
            log.info("Config file not found")
            return self.default_config
        with file.open() as f:
            config = yaml.safe_load(f)
        return config

    def load_config(self):
        """
        Load the user configuration into the app.

        If called again, this method will refresh the configuration
        with the latest changes.
        """
        self.config = self._read_config(CONFIG_FILE)
        self.books = self._read_books(self.config)

    def _read_books(self, config):
        """
        Load all books from the Lira configuration file.

        Each book can be a dotted path to the module of the book,
        or a local path to the directory of the book
        (it can be a relative path to the config file).

        .. code-block:: yaml
           books:
             # A dotted path to the module
             - lira.books.intro

             # A local path
             - ~/local/path/to/book/

             # A relative path to the config file
             - relative/path

             # Install from a package (maybe in the future)
             - name: lira.book.basic
               package: git+https://gifhub.com/pythonecuador/pythones-lirabook
             - name: lira.book.basic
               package: pythones-lirabook
        """
        books_list = []
        for book_path in config.get("books", []):
            path = Path(book_path).expanduser()
            if not path.is_absolute():
                path = (CONFIG_FILE.parent / path).resolve()

            if path.exists() and path.is_dir():
                books_list.append(Book(root=path))
            else:
                try:
                    package = importlib.import_module(book_path)
                    path = Path(package.__file__).parent
                    books_list.append(Book(root=path))
                except ModuleNotFoundError:
                    log.warning("Unable to find book: %s", book_path)
                except Exception as e:
                    log.warning(
                        "Unable to load book. path=%s error=%s",
                        book_path,
                        str(e),
                    )
        return books_list

    def setup(self):
        self._create_dirs()
        self._setup_logger()
        self.load_config()
