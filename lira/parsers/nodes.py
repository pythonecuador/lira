from functools import namedtuple


class Node:

    """
    Base class for a node.

    If it's a terminal node, the first argument is the text of this node,
    otherwise the arguments are the children of this node.

    All kwarg arguments are the options of this node
    (only options from `valid_options` are recognized).
    """

    is_terminal = False
    """If it's a terminal node (without children)"""

    valid_options = set()
    """A set of valid options for this node"""

    def __init__(self, *children, **options):
        self.content = None
        """Raw content of the node"""

        self.children = []
        """List of children of this node"""

        OptionsProxy = namedtuple("OptionsProxy", self.valid_options)
        self.options = OptionsProxy(**options)
        """Named tuple with the options for this node"""

        if self.is_terminal:
            if children:
                self.content = children[0]
        else:
            self.children = list(children)

    def _trim_text(self, text, max_len=30):
        split = text.split("\n")
        text = split[0]
        if len(text) > max_len or len(split) > 1:
            text = text[:max_len] + "..."
        return text

    def append(self, node):
        """Append a node as a child of this node."""
        if self.is_terminal:
            raise ValueError
        self.children.append(node)

    def extend(self, nodes):
        """Append a list of nodes as a children of this node."""
        if self.is_terminal:
            raise ValueError
        self.children.extend(nodes)

    def text(self):
        """Text representation of the node."""
        return self.content or ""

    @property
    def tagname(self):
        """Name of the node."""
        return self.__class__.__name__

    def __str__(self):
        if self.is_terminal:
            text = self._trim_text(self.text())
            return f'<{self.tagname}: "{text}">'
        return f"<{self.tagname}: {self.children}>"

    def __repr__(self):
        return str(self)


class NestedNode(Node):
    def text(self):
        content = [child.text() for child in self.children]
        return "\n\n".join(content)


class Paragraph(Node):

    """
    Container for inline nodes.

    Inline nodes are:

    - :py:class:`Text`
    - :py:class:`Strong`
    - :py:class:`Emphasis`
    - :py:class:`Literal`
    """

    def text(self):
        content = [child.text() for child in self.children]
        return "".join(content)


class Text(Node):

    """Plain text node."""

    is_terminal = True


class Strong(Node):

    """Text represented as **bold**."""

    is_terminal = True


class Emphasis(Node):

    """Text represented as *italics*."""

    is_terminal = True


class Literal(Node):

    """Text represented with a ``mono space font``."""

    is_terminal = True


class Section(NestedNode):

    """
    Section representation.

    Options:

    - title

    Children can be any of:

    - :py:class:`Paragraph`
    - :py:class:`TestBlock`
    - :py:class:`CodeBlock`
    - :py:class:`Admonition`
    """

    valid_options = {"title"}

    def __str__(self):
        title = self.options.title
        return f"<{self.tagname} {title}: {self.children}>"


class Admonition(NestedNode):

    """
    Text inside a box, usually to give a warning or a note to the user.

    Options:

    - title: The title of the admonition, defaults to ``type``.
    - type: one of ``note``, ``warning``, or ``tip``.

    Children can be any of:

    - :py:class:`Paragraph`
    """

    valid_options = {"title", "type"}

    def __str__(self):
        title = self.options.title
        return f"<{self.tagname} {title}: {self.children}>"


class CodeBlock(Node):

    """
    Syntax highlighted block.

    The content of this node should be a list of lines.

    Options:

    - language
    """

    is_terminal = True
    valid_options = {"language"}

    def text(self):
        return "\n".join(self.content)

    def __str__(self):
        lang = self.options.language
        code = self._trim_text(self.text())
        return f"<{self.tagname} {lang}: {code}>"


class TestBlock(Node):

    """
    Challenge/response block to interact with the user.

    Options:

    - validator: dotted path to a :py:class:`lira.validator.Validator` class.
    - description
    - help
    """

    is_terminal = True
    valid_options = {"validator", "help", "description"}

    def text(self):
        return self.options.description

    def __str__(self):
        description = self.options.description
        validator = self.options.validator
        return f"<{self.tagname} {validator}: {description}>"


class Prompt(Node):

    # TODO

    is_terminal = True
