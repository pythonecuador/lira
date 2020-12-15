import importlib
import logging
from copy import deepcopy

from lira.parsers import State

log = logging.getLogger(__name__)


class ValidationError(Exception):

    pass


class Validator:

    """Base class for validators."""

    def __init__(self):
        self.error: Exception = None
        self.is_valid = False
        self.message = None
        self.data = self.get_data()
        self.original_data = deepcopy(self.data)
        self.tries = 0
        self.previous_errors = []

    def run(self) -> bool:
        self.is_valid = False
        self.tries += 1
        try:
            self.data = self.get_data()
            self.data = self.validate(data=self.data)
            self.on_success()
        except ValidationError as e:
            self.on_failure(e)
        except Exception as e:
            log.exception("Error while running validator.")
            self.on_exception(e)
        else:
            self.is_valid = True
        return self

    def get_data(self) -> str:
        raise NotImplementedError

    def on_success(self):
        pass

    def on_failure(self, e: ValidationError):
        self.error = e
        self.previous_errors.append(e)
        self.message = str(e) or "Wrong answer :("

    def on_exception(self, e: Exception):
        self.error = e
        self.message = (
            "Something unexpected happened! Check your logs for more information"
        )

    def validate(self, data: str) -> bool:
        """
        Validate the value.

        :raises ValidationError: If the value is incorrect.
        :returns: The final value of `content`.
        """
        return data


class TestBlockValidator(Validator):
    def __init__(self, node):
        self.node = node
        super().__init__()

    def get_data(self) -> str:
        return self.node.text()

    def on_success(self):
        super().on_success()
        self.message = "Awesome, you did it!"
        self.node.attributes.state = State.VALID
        self.node.content = self.data.split("\n")

    def on_failure(self, e: Exception):
        super().on_failure(e)
        self.node.attributes.state = State.INVALID

    def on_exception(self, e: Exception):
        super().on_exception(e)
        self.node.attributes.state = State.UNKNOWN


def get_validator(validator_path) -> Validator:
    module_name, class_name = validator_path.rsplit(".", 1)
    module = importlib.import_module(module_name)
    validator = getattr(module, class_name, None)
    return validator
