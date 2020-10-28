import pytest

from lira.parsers import nodes


class TestNodes:
    def test_text_node(self):
        node = nodes.Text("Hello")
        assert node.tagname == "Text"
        assert node.text() == "Hello"
        assert str(node) == '<Text: "Hello">'

    def test_strong_node(self):
        node = nodes.Strong("hello")
        assert node.tagname == "Strong"
        assert node.text() == "hello"
        assert str(node) == '<Strong: "hello">'

    def test_emphasis_node(self):
        node = nodes.Emphasis("hello")
        assert node.tagname == "Emphasis"
        assert node.text() == "hello"
        assert str(node) == '<Emphasis: "hello">'

    def test_literal_node(self):
        node = nodes.Literal("hello")
        assert node.tagname == "Literal"
        assert node.text() == "hello"
        assert str(node) == '<Literal: "hello">'

    def test_paragraph_node(self):
        node = nodes.Paragraph(nodes.Text("Hello "), nodes.Strong("world!"))
        assert node.tagname == "Paragraph"
        assert node.text() == "Hello world!"
        assert str(node) == '<Paragraph: [<Text: "Hello ">, <Strong: "world!">]>'

    def test_code_block_node(self):
        node = nodes.CodeBlock(
            [
                "import os",
                "",
                "print('Hello world')",
            ],
            language="python",
        )
        assert node.tagname == "CodeBlock"
        assert node.text() == "import os\n\nprint('Hello world')"
        assert str(node) == "<CodeBlock python: import os...>"

    def test_test_block_node(self):
        node = nodes.TestBlock(
            validator="lira.validators.Validator",
            help="Validate me",
            description="I'm a validator",
        )
        assert node.tagname == "TestBlock"
        assert node.options.validator == "lira.validators.Validator"
        assert node.options.help == "Validate me"
        assert node.options.description == "I'm a validator"
        assert node.text() == "I'm a validator"
        assert str(node) == "<TestBlock lira.validators.Validator: I'm a validator>"

    @pytest.mark.parametrize(
        "type",
        ["note", "warning", "tip"],
    )
    def test_admonition_node(self, type):
        paragraph = nodes.Paragraph(nodes.Text("Hello "), nodes.Strong("world!"))
        node = nodes.Admonition(
            paragraph,
            title="Hey!",
            type=type,
        )
        assert node.tagname == "Admonition"
        assert node.options.title == "Hey!"
        assert node.options.type == type
        assert node.text() == "Hello world!"
        repr = (
            '<Admonition Hey!: [<Paragraph: [<Text: "Hello ">, <Strong: "world!">]>]>'
        )
        assert str(node) == repr

    def test_section_node(self):
        paragraph = nodes.Paragraph(nodes.Text("Hello "), nodes.Strong("world!"))
        paragraph2 = nodes.Paragraph(nodes.Text("Hello again"))
        node = nodes.Section(
            paragraph,
            paragraph2,
            title="I'm a section",
        )
        assert node.tagname == "Section"
        assert node.options.title == "I'm a section"
        assert node.text() == "Hello world!\n\nHello again"
        repr = (
            "<Section I'm a section: "
            '[<Paragraph: [<Text: "Hello ">, <Strong: "world!">]>, '
            '<Paragraph: [<Text: "Hello again">]>]>'
        )
        assert str(node) == repr
