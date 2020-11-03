from pathlib import Path

from lira.book import Book, BookChapter

books_path = Path(__file__).parent / "data/books"


class TestBook:
    def setup_method(self):
        self.book = Book(root=books_path / "example")

    def test_book_metadata(self):
        self.book.parse()
        metadata = {
            "language": "en",
            "title": "Basic Introduction to Python",
            "description": "Basic introduction to Python",
            "created": "16/10/2020",
            "updated": "16/10/2020",
            "authors": ["Santos Gallegos"],
            "chapters": {
                "Introduction": "intro.rst",
                "Nested Content": "nested.rst",
            },
        }
        assert self.book.metadata == metadata
        assert str(self.book) == "<Book: Basic Introduction to Python -> example/>"

    def test_book_chapters(self):
        self.book.parse()

        chapters = self.book.chapters
        assert len(chapters) == 2

        chapter_one = chapters[0]
        assert isinstance(chapter_one, BookChapter)
        assert chapter_one.title == "Introduction"
        assert chapter_one.file.name == "intro.rst"

        chapter_two = chapters[1]
        assert isinstance(chapter_two, BookChapter)
        assert chapter_two.title == "Nested Content"
        assert chapter_two.file.name == "nested.rst"


class TestBookChapter:
    def setup_method(self):
        self.book = Book(root=books_path / "example")
        self.book.parse(all=True)
        self.chapter_one = self.book.chapters[0]
        self.chapter_two = self.book.chapters[1]

    def assert_toc(self, toc, expected_toc):
        """Recursively check that `toc` has the same hierarchy as `expected`."""
        if isinstance(expected_toc, list):
            assert isinstance(toc, list)
            assert len(toc) == len(expected_toc)
            for element, expected_element in zip(toc, expected_toc):
                self.assert_toc(element, expected_element)
        else:
            section = toc[0]
            content = toc[1]
            assert section.options.title == expected_toc[0]
            self.assert_toc(content, expected_toc[1])

    def test_chapter_metadata(self):
        metadata = {
            "tags": "comments",
            "level": "easy",
        }
        assert self.chapter_one.metadata == metadata

        metadata = {
            "tags": "nested content, toc",
            "level": "medium",
        }
        assert self.chapter_two.metadata == metadata

    def test_chapter_toc(self):
        toc = [
            ("Comments", []),
        ]
        self.assert_toc(
            self.chapter_one.toc(),
            toc,
        )

        toc = [
            (
                "I'm a title",
                [
                    ("I'm a subtitle", []),
                    ("I'm another subtitle", []),
                ],
            )
        ]
        self.assert_toc(
            self.chapter_two.toc(),
            toc,
        )

    def test_chapter_toc_custom_min_depth(self):
        toc = [("I'm a title", [])]
        self.assert_toc(
            self.chapter_two.toc(depth=1),
            toc,
        )

    def test_chapter_toc_custom_max_depth(self):
        toc = [
            (
                "I'm a title",
                [
                    ("I'm a subtitle", []),
                    (
                        "I'm another subtitle",
                        [("Another one", [])],
                    ),
                ],
            )
        ]
        self.assert_toc(
            self.chapter_two.toc(depth=99),
            toc,
        )
