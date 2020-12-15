from lira.validators import TestBlockValidator, ValidationError


class LiraValidator(TestBlockValidator):
    def validate(self, data):
        if "Lira is awesome!" != data.strip():
            raise ValidationError
        return data

    def on_success(self):
        super().on_success()
        if self.tries <= 1:
            self.message = "Awesome, you did it at the first try!"
        else:
            self.message = f"You did it at the {self.tries} try!"
