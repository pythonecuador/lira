import importlib
import logging
from pathlib import Path

import yaml

from lira.book import Book
from lira.config import CONFIG_DIR, CONFIG_FILE, DATA_DIR, LOG_DIR

log = logging.getLogger(__name__)


class LiraApp:
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

    def _read_config(self):
        if not CONFIG_FILE.exists():
            log.info("Config file not found")
            return {}
        with CONFIG_FILE.open() as f:
            config = yaml.safe_load(f)
        return config

    @property
    def books(self):
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
        cache_key = "__books"
        books_list = getattr(self, cache_key, [])
        if books_list:
            return books_list

        config = self._read_config()
        for book_path in config.get("books", ["lira.books.intro"]):
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
        setattr(self, cache_key, books_list)
        return books_list

    def setup(self):
        self._create_dirs()
        self._setup_logger()
