class Node:

    is_terminal = False
    valid_options = set()

    def __init__(self, *children, **options):
        self.content = None
        self.children = []
        if self.is_terminal:
            self.content = children[0]
        else:
            self.children = children

        self.options = {}
        for option, value in options.items():
            if option in self.valid_options:
                self.options[option] = value

    def append(self, node):
        if self.is_terminal:
            raise ValueError
        self.children.append(node)

    def extend(self, nodes):
        if self.is_terminal:
            raise ValueError
        self.children.extend(nodes)

    def text(self):
        return self.content or ""

    @property
    def tagname(self):
        return self.__class__.__name__


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
    pass


class Prompt(Node):
    pass


class Test(Node):

    valid_options = {"validator", "help", "description"}


class Section(Node):

    valid_options = {"title"}


class Note(Node):
    pass
