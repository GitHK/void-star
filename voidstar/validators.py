import re
from collections import deque


class BaseValidator:
    def __init__(self, required=False, not_empty=False):
        self.required = required
        self.not_empty = not_empty

    def to_validate(self, value):
        raise NotImplementedError()

    def set_value(self, value):
        self.value = value

    def validate(self):
        return self.to_validate(self.value)


class ValidationError(Exception):
    pass


class StringIntValidator(BaseValidator):
    def __init__(self, max=None, min=None, **kwargs):
        super().__init__(**kwargs)
        self.max = max
        self.min = min

    def to_validate(self, value):
        try:
            integer_value = int(value)
            if self.max is not None and integer_value > self.max:
                raise ValidationError("Max value %s is not lower than %s" % (value, self.max))

            if self.min is not None and integer_value < self.min:
                raise ValidationError("Min value %s is not higher than %s" % (value, self.min))

        except ValueError:
            raise ValidationError('Value is not integer: %s' % value)

        return integer_value


def check_single_validator(params, validator_name, validator, matches):
    def make_validation_tuple(param):
        validator.set_value(params[param])
        return param, validator.validate()

    def check_not_empty(validator_name):
        validator_value = params[validator_name]
        if validator.not_empty and validator_value == '':
            raise ValidationError("Parameter '%s' can't be empty" % validator_name)

    if validator_name not in params:
        occurrences = 0
        for parameter in params:
            if re.search(validator_name, parameter) is not None:
                check_not_empty(parameter)
                matches.append(make_validation_tuple(parameter))
                occurrences += 1

        if validator.required and occurrences == 0:
            raise ValidationError("No parameter match found for: '%s'" % validator_name)

    else:
        check_not_empty(validator_name)
        matches.append(make_validation_tuple(validator_name))


def validate(parameters, validation_schema):
    matches = deque()
    for parameter_name, validator in validation_schema.items():
        check_single_validator(parameters, parameter_name, validator, matches)

    return dict(matches)
