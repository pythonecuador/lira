class Node:

    """
    Base class for a node.

    - `is_terminal`: If it's a terminal node (without children).
    - `valid_options`: A set of valid options for this node.

    If it's a terminal node, the first argument is the text of this node,
    otherwise the arguments are the children of this node.

    All kwarg arguments are the options of this node
    (only options from `valid_options` are recognized).
    """

    is_terminal = False
    valid_options = set()

    def __init__(self, *children, **options):
        self.content = None
        self.children = []
        if self.is_terminal:
            self.content = children[0]
        else:
            self.children = list(children)

        self.options = {}
        for option, value in options.items():
            if option not in self.valid_options:
                raise ValueError(
                    f"Invalid option {option}. "
                    f"Valid options are {self.valid_options}"
                )
            self.options[option] = value

    def _trim_text(self, text, max_len=30):
        text = text.split("\n")[0]
        if len(text) > max_len:
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
            return f'{self.tagname}: "{text}"'
        return f"{self.tagname}: {self.children}"

    def __repr__(self):
        return str(self)


class Text(Node):

    is_terminal = True


class Strong(Node):

    is_terminal = True


class Emphasis(Node):

    is_terminal = True


class Literal(Node):

    is_terminal = True


class Paragraph(Node):
    pass


class CodeBlock(Node):

    is_terminal = True
    valid_options = {"language"}

    def __str__(self):
        lang = self.options["validator"]
        code = self._trim_text(self.text())
        return f"{lang}: {code}"


class Prompt(Node):

    is_terminal = True


class Test(Node):

    is_terminal = True
    valid_options = {"validator", "help", "description"}

    def __str__(self):
        description = self.options["description"]
        validator = self.options["validator"]
        return f"{validator}: {description}"


class Section(Node):

    valid_options = {"title"}

    def __str__(self):
        title = self.options["title"]
        return f"{self.tagname} ({title}): {self.children}"


class Note(Node):

    is_terminal = True
    valid_options = {"title"}

    def __str__(self):
        title = self.options["title"]
        content = self._trim_text(self.text())
        return f"{self.tagname} ({title}): {content}"
