class Validator:
    def __init__(self):
        pass

    def validate(self, value, options):
        raise NotImplementedError

    def hints(self, value, options):
        return []


class CommentValidator(Validator):
    def validate(self, value, options):
        # TODO: actually validate
        return value
