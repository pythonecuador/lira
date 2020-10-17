from pathlib import Path

from docutils.frontend import OptionParser
from docutils.nodes import Element
from docutils.parsers.rst import Directive, Parser, directives
from docutils.utils import new_document

from lira.parsers import BaseParser
from lira.parsers import nodes as booknodes


class DirectiveNode(Element):

    """
    Node representation of a directive.

    The attributes of this node are:

    - name
    - content
    - options
    """

    tagname = "directive"


def importable(value):
    # TODO: check if value can be imported
    return value


class TestDirective(Directive):

    """
    Test directive implementation.

    The first line of the directive is the description of it.
    Options:

    - help: Optional help text.
    - validator: A dotted path to a subclass of `lira.validators.Validator`.

    Example:

    .. test:: Escribe un comentario
       :help: Escribe un simple comentario :)
       :validator: lira.validators.CommentValidator
    """

    option_spec = {
        "help": str,
        "validator": importable,
    }
    has_content = True

    def run(self):
        """Returns a `DirectiveNode`, so it can be interpreted by the parser."""
        node = DirectiveNode(
            self.name,
            name=self.name,
            content=self.content,
            options=self.options,
        )
        return [node]


class RSTParser(BaseParser):

    """
    reStructuredText parser for lira.

    Powered by docutils.
    """

    terminal_nodes = {
        "#text": booknodes.Text,
        "literal": booknodes.Literal,
        "strong": booknodes.Strong,
        "emphasis": booknodes.Emphasis,
    }
    container_nodes = {
        "paragraph": booknodes.Paragraph,
    }

    def __init__(self, file: Path):
        super().__init__(file)
        self.document = self._parse_file(file)

    def _parse_file(self, file: Path):
        settings = OptionParser(components=(Parser,)).get_default_values()
        parser = Parser()
        document = new_document(str(file), settings)
        with file.open() as f:
            input = f.read()

        directives.register_directive("test", TestDirective)
        parser.parse(input, document)
        return document

    def parse_metadata(self):
        # TODO: set a spec for the metadata
        metadata = {}
        children = self.document.children
        if not children:
            return metadata
        firs_node = children[0]
        if firs_node.tagname == "field_list":
            for node in firs_node.children:
                name, value = (n.astext() for n in node.children)
                metadata[name] = value
        return metadata

    def parse_content(self):
        return self._parse_content(self.document)

    def _parse_content(self, node, start=0):
        nodes = []
        for child in node.children[start:]:
            tag = child.tagname
            if tag == "section":
                nodes.append(self._parse_section(child))
            if tag == "directive" and child.attributes.get("name") == "test":
                nodes.append(self._parse_test(child))
            if tag in self.terminal_nodes:
                nodes.append(self.terminal_nodes[tag](child.astext()))
            elif tag in self.container_nodes:
                nodes.append(self.container_nodes[tag](*self._parse_content(child)))
        return nodes

    def _parse_test(self, node):
        if node.tagname != "directive" or node.attributes.get("name") != "test":
            raise TypeError
        attrs = node.attributes
        description = attrs["content"][0]
        options = attrs["options"]
        help = options.get("help", "")
        validator = options["validator"]
        directive = booknodes.Test(
            validator=validator,
            description=description,
            help=help,
        )
        return directive

    def _parse_section(self, node):
        if node.tagname != "section":
            raise TypeError

        title = node.children[0].astext()
        section = booknodes.Section(
            *self._parse_content(node, start=1),
            title=title,
        )
        return section
