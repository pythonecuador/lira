import importlib
import logging

from lira.parsers import State

log = logging.getLogger(__name__)


class ValidationError(Exception):

    """Exception to raise when the data isn't valid."""

    pass


class Validator:

    """
    Base class for validators.

    The :py:meth:`run` method should be called to validate the given data.
    Usage:

    .. code:: python

       validator = Validator(data="Validate me!")
       validator.run()
       print(validator.is_valid)
       print(validator.data)
       print(validator.message)
    """

    def __init__(self, data=None):
        self.is_valid = False
        """Was the data valid?"""

        self.error: Exception = None
        """Current raised exception."""

        self.message = None
        """Optional message to show after the validation."""

        self.data = data
        """Data to validate."""

        self.tries = 0
        """Current number of tries."""

        self.previous_errors = []
        """List of previous validation errors."""

    def run(self):
        """
        Run the validator.

        This will increment :py:attr:`tries`, and in case of failure it wil add
        the exception to :py:attr:`previous_errors`.
        """
        try:
            self.is_valid = False
            self.tries += 1
            self.data = self.validate(data=self._get_data())
            self.is_valid = True
            self.on_success()
        except ValidationError as e:
            self.error = e
            self.on_failure(e)
            self.previous_errors.append(e)
        except Exception as e:
            log.exception("Error while running validator.")
            self.error = e
            self.on_exception(e)
        return self

    def _get_data(self) -> str:
        """Get the data to validate."""
        return self.data

    def on_success(self):
        """To be called if the validation was successful."""
        self.message = "Awesome, you did it!"

    def on_failure(self, e: ValidationError):
        """To be called if the validation wasn't successful."""
        self.message = str(e) or "Wrong answer :("

    def on_exception(self, e: Exception):
        """To be called if an unhandled exception was raised."""
        self.message = (
            "Something unexpected happened! Check your logs for more information"
        )

    def validate(self, data: str) -> bool:
        """
        Validate the value.

        :raises ValidationError: If the value is incorrect.
        :returns: The final value of :py:attr:`data`.
        """
        return data


class TestBlockValidator(Validator):

    """
    Base validator for :py:class:`lira.parsers.nodes.TestBlock` nodes.

    :param node: TestBlock node to validate.
    :type node: lira.parsers.nodes.TestBlock
    """

    def __init__(self, node):
        self.node = node
        super().__init__()

    def _get_data(self) -> str:
        return self.node.text()

    def on_success(self):
        super().on_success()
        self.node.attributes.state = State.VALID
        self.node.content = self.data.split("\n")

    def on_failure(self, e: Exception):
        super().on_failure(e)
        self.node.attributes.state = State.INVALID

    def on_exception(self, e: Exception):
        super().on_exception(e)
        self.node.attributes.state = State.UNKNOWN


def get_validator_class(validator_path, subclass=None):
    """
    Get a validator class from a dotted path.

    :raises ValueError: If the class isn't a subclass of :py:class:`Validator`.
    """
    module_name, class_name = validator_path.rsplit(".", 1)
    module = importlib.import_module(module_name)
    validator = getattr(module, class_name, None)
    subclass = subclass or Validator
    if not issubclass(subclass, Validator):
        log.warning(
            "Subclass isn't a subclass of validator. subclass=%",
            subclass.__name__,
        )
        raise ValueError
    if not issubclass(validator, subclass):
        log.warning(
            "Validator isn't a subclass of validator. subclass=% validator=%s",
            subclass.__name__,
            validator_path,
        )
        raise ValueError
    return validator
