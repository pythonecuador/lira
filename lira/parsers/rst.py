import logging

from docutils.frontend import OptionParser
from docutils.nodes import Element
from docutils.parsers.rst import Directive, Parser, directives
from docutils.utils import new_document

from lira.parsers import BaseParser, State
from lira.parsers import nodes as booknodes

logger = logging.getLogger(__name__)


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


class BaseDirective(Directive):
    def run(self):
        """Return a `DirectiveNode`, so it can be interpreted by the parser."""
        node = DirectiveNode(
            self.name,
            name=self.name,
            arguments=self.arguments,
            content=self.content,
            options=self.options,
        )
        return [node]


class CodeBlockDirective(BaseDirective):

    """Override the code directive to return a Directive node."""

    has_content = True
    required_arguments = 1


def validate_state(value):
    value = value.lower().strip()
    if not value:
        return State.UNKNOWN
    for state in State:
        if value == state.value:
            return state
    raise ValueError("Invalid state")


class TestBlockDirective(BaseDirective):

    """
    Test directive implementation.

    The first line of the directive is the description of it.
    Options:

    - validator: A dotted path to a subclass of `lira.validators.Validator`.
    - language: Optional language used for highlighting of the content.
    - state: Optional initial state of the test block.

    The content can be used to display a default text.

    Example:

    .. test:: Write a comment
       :validator: lira.validators.CommentValidator
       :language: python

       # Just write a simple comment :)
    """

    option_spec = {
        "validator": importable,
        "language": str,
        "state": validate_state,
    }
    required_arguments = 1
    final_argument_whitespace = True
    has_content = True


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.document = self._get_document(self.content)

    def _get_document(self, content):
        settings = OptionParser(components=(Parser,)).get_default_values()
        directives.register_directive("test-block", TestBlockDirective)
        directives.register_directive("code-block", CodeBlockDirective)

        parser = Parser()
        source = str(self.source) if self.source else "lira-unknown-source"
        document = new_document(source, settings)

        parser.parse(content, document)
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
            elif tag == "directive":
                directive_name = child.attributes.get("name")
                if directive_name == "test-block":
                    nodes.append(self._parse_test_block(child))
                elif directive_name == "code-block":
                    nodes.append(self._parse_code_block(child))
            elif tag in self.terminal_nodes:
                nodes.append(self.terminal_nodes[tag](child.astext()))
            elif tag in self.container_nodes:
                nodes.append(self.container_nodes[tag](*self._parse_content(child)))
            else:
                logger.warning("Node with tag %(tag)s is not supported", {"tag": tag})
        return nodes

    def _parse_code_block(self, node):
        attrs = node.attributes
        language = attrs["arguments"][0]
        code = list(attrs["content"])
        return booknodes.CodeBlock(
            code,
            language=language,
        )

    def _parse_test_block(self, node):
        attrs = node.attributes
        description = attrs["arguments"][0]
        options = attrs["options"]
        validator = options["validator"]
        state = options.get("state", State.UNKNOWN)
        language = options.get("language")
        content = list(attrs["content"])
        return booknodes.TestBlock(
            content,
            validator=validator,
            description=description,
            state=state,
            language=language,
        )

    def _parse_section(self, node):
        title = node.children[0].astext()
        return booknodes.Section(
            *self._parse_content(node, start=1),
            title=title,
        )
