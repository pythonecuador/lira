class Validator:
    """Base class for validators."""

    def __init__(self):
        pass

    def validate(self, value, options):
        """
        Validate the value.

        Return `True` or `False` if the value is correct or not.
        """
        raise NotImplementedError

    def hints(self, value, options):
        """List of strings as hints for the user."""
        return []


class CommentValidator(Validator):
    def validate(self, value, options):
        # TODO: actually validate
        return value
