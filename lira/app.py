import logging

from lira.config import CONFIG_DIR, DATA_DIR, LOG_DIR


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

    def setup(self):
        self._create_dirs()
        self._setup_logger()
