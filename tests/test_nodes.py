import pytest

from lira.parsers import State, nodes


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
        node = nodes.Paragraph(children=[nodes.Text("Hello "), nodes.Strong("world!")])
        assert node.tagname == "Paragraph"
        assert node.text() == "Hello world!"
        assert str(node) == '<Paragraph: [<Text: "Hello ">, <Strong: "world!">]>'

        for child in node.children:
            assert child.parent is node

    def test_code_block_node(self):
        node = nodes.CodeBlock(
            content=[
                "import os",
                "",
                "print('Hello world')",
            ],
            attributes=dict(
                language="python",
            ),
        )
        assert node.tagname == "CodeBlock"
        assert node.text() == "import os\n\nprint('Hello world')"
        assert str(node) == "<CodeBlock python: import os...>"

    def test_test_block_node(self):
        node = nodes.TestBlock(
            content=["# Write a comment"],
            attributes=dict(
                validator="lira.validators.TestBlockValidator",
                language="python",
                state=State.UNKNOWN,
                description="I'm a validator",
                extension=".txt",
            ),
        )
        assert node.tagname == "TestBlock"
        assert node.attributes.validator == "lira.validators.TestBlockValidator"
        assert node.attributes.language == "python"
        assert node.attributes.description == "I'm a validator"
        assert node.attributes.state == State.UNKNOWN
        assert node.text() == "# Write a comment"
        assert (
            str(node)
            == "<TestBlock lira.validators.TestBlockValidator: I'm a validator>"
        )

    def test_block_node_reset(self):
        node = nodes.TestBlock(
            content=["# Write a comment"],
            attributes=dict(
                validator="lira.validators.TestBlockValidator",
                language="python",
                state=State.UNKNOWN,
                description="I'm a validator",
                extension=".txt",
            ),
        )
        node.attributes.language = "python"
        node.attributes.state = State.VALID
        node.attributes.description = "Please revert me!"
        node.content = ["One", "Two"]

        node.reset()

        assert node.tagname == "TestBlock"
        assert node.attributes.validator == "lira.validators.TestBlockValidator"
        assert node.attributes.language == "python"
        assert node.attributes.description == "I'm a validator"
        assert node.attributes.state == State.UNKNOWN
        assert node.text() == "# Write a comment"

    @pytest.mark.parametrize(
        "type",
        ["note", "warning", "tip"],
    )
    def test_admonition_node(self, type):
        paragraph = nodes.Paragraph(
            children=[nodes.Text("Hello "), nodes.Strong("world!")]
        )
        node = nodes.Admonition(
            children=[paragraph],
            attributes=dict(
                title="Hey!",
                type=type,
            ),
        )
        assert node.tagname == "Admonition"
        assert node.attributes.title == "Hey!"
        assert node.attributes.type == type
        assert node.text() == "Hello world!"
        repr = (
            '<Admonition Hey!: [<Paragraph: [<Text: "Hello ">, <Strong: "world!">]>]>'
        )
        assert str(node) == repr

    def test_section_node(self):
        paragraph = nodes.Paragraph(
            children=[nodes.Text("Hello "), nodes.Strong("world!")]
        )
        paragraph2 = nodes.Paragraph(children=[nodes.Text("Hello again")])
        node = nodes.Section(
            children=[
                paragraph,
                paragraph2,
            ],
            attributes=dict(title="I'm a section"),
        )
        assert node.tagname == "Section"
        assert node.attributes.title == "I'm a section"
        assert node.text() == "Hello world!\n\nHello again"
        repr = (
            "<Section I'm a section: "
            '[<Paragraph: [<Text: "Hello ">, <Strong: "world!">]>, '
            '<Paragraph: [<Text: "Hello again">]>]>'
        )
        assert str(node) == repr

        for child in node.children:
            assert child.parent is node
