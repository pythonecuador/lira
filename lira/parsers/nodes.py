from copy import copy

from lira.validators import get_validator


def _get_attributes_proxy(attributes, **values):
    class AttributesProxy:
        __slots__ = attributes

        def __init__(self, **kwargs):
            for item, value in kwargs.items():
                setattr(self, item, value)

    return AttributesProxy(**values)


class Node:

    """
    Base class for a node.

    :param content: Content for this node (usually only for terminal nodes).
    :param children: List of children.
    :param attributes: Dictionary of valid attributes.

    If it's a terminal node, it doesn't have children.
    Only attributes from `valid_attributes` are recognized.
    """

    is_terminal = False
    """If it's a terminal node (without children)"""

    valid_attributes = set()
    """A set of valid attributes for this node."""

    def __init__(self, content=None, *, children=None, attributes=None):
        if self.is_terminal and children:
            raise ValueError("A terminal node can't have children")
        if not self.is_terminal and content:
            raise ValueError("A no terminal node can't have content")

        self.content = content
        """Raw content of the node"""

        self.children = children or []
        """List of children of this node."""

        attributes = attributes or {}
        self.attributes = _get_attributes_proxy(self.valid_attributes, **attributes)
        """Named tuple with the attributes for this node"""

        self.parent = None
        """Parent node"""

        for child in self.children:
            child.parent = self

        self._initial_attributes = copy(self.attributes)
        self._initial_content = copy(self.content)

    def _trim_text(self, text, max_len=30):
        split = text.split("\n")
        text = split[0]
        if len(text) > max_len or len(split) > 1:
            text = text[:max_len] + "..."
        return text

    def reset(self):
        """Reset attributes and content of the node to their initial values."""
        self.content = copy(self._initial_content)
        self.attributes = copy(self._initial_attributes)

    def text(self):
        """Text representation of the node."""
        return self.content or ""

    @property
    def tagname(self):
        """Name of the node."""
        return self.__class__.__name__

    def __repr__(self):
        if self.is_terminal:
            text = self._trim_text(self.text())
            return f'<{self.tagname}: "{text}">'
        return f"<{self.tagname}: {self.children}>"


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

    Attributes:

    - title

    Children can be any of:

    - :py:class:`Paragraph`
    - :py:class:`TestBlock`
    - :py:class:`CodeBlock`
    - :py:class:`Admonition`
    """

    valid_attributes = {"title"}

    def __repr__(self):
        title = self.attributes.title
        return f"<{self.tagname} {title}: {self.children}>"


class Admonition(NestedNode):

    """
    Text inside a box, usually to give a warning or a note to the user.

    Attributes:

    - title: The title of the admonition, defaults to ``type``.
    - type: one of ``note``, ``warning``, or ``tip``.

    Children can be any of:

    - :py:class:`Paragraph`
    """

    valid_attributes = {"title", "type"}

    def __repr__(self):
        title = self.attributes.title
        return f"<{self.tagname} {title}: {self.children}>"


class CodeBlock(Node):

    """
    Syntax highlighted block.

    The content of this node should be a list of lines.

    Attributes:

    - language
    """

    is_terminal = True
    valid_attributes = {"language"}

    def text(self):
        return "\n".join(self.content)

    def __repr__(self):
        lang = self.attributes.language
        code = self._trim_text(self.text())
        return f"<{self.tagname} {lang}: {code}>"


class TestBlock(Node):

    """
    Challenge/response block to interact with the user.

    Attributes:

    - validator: dotted path to a :py:class:`lira.validator.Validator` class.
    - description
    - state
    - language
    - extension: used to open a new file when editing.
    """

    is_terminal = True
    valid_attributes = {"validator", "description", "state", "language", "extension"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._validator_class = get_validator(self.attributes.validator)
        self._validator = self._validator_class(node=self)

    def text(self):
        return "\n".join(self.content)

    def reset(self):
        super().reset()
        self._validator = self._validator_class(node=self)

    def validate(self):
        self._validator.run()
        return self._validator

    def __repr__(self):
        description = self.attributes.description
        validator = self.attributes.validator
        return f"<{self.tagname} {validator}: {description}>"


class Prompt(Node):

    # TODO

    is_terminal = True
