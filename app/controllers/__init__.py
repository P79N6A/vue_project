"""Controller global functions.

Contains functions and classes for data cleaning and validation.
Contains a pagination function that is used in most query results.

"""

import bleach

from flask_bcrypt import Bcrypt
from jsonschema import validators, Draft4Validator
from jsonschema.exceptions import ValidationError

bcrypt = Bcrypt()


def not_empty(validator, value, instance, schema):
    """Raises error if the casted string is empty."""
    if value and len(str(instance)) == 0:
        yield ValidationError("Required")


def is_id(validator, value, instance, schema):
    """Raises error if instance cannot be cast into int or is not None"""
    if value:
        try:
            test = int(instance)
        except:
            if instance is not None:
                yield ValidationError("Invalid ID")

# Get all existing validators and add in custom ones.
all_validators = dict(Draft4Validator.VALIDATORS)
all_validators["not_empty"] = not_empty

CustomValidator = validators.create(
    meta_schema=Draft4Validator.META_SCHEMA,
    validators=all_validators
)


def clean_data(request_data, schema=None):
    """ Data cleaner.

    Casts against a schema, if present.
    Bleaches all strings.
    Returns a dictionary of cleaned data.

    """
    return_dict = dict()

    for k, v in request_data.items():
        if (schema is not None and
                k in schema["properties"] and
                "type" in schema["properties"][k]):
            # Cast
            cast_type = schema["properties"][k]["type"]
            if cast_type == "string":
                v = str(v)
            elif cast_type == "integer":
                v = int(v)
                if k in ["limit", "offest"] and v < 0:
                    v = 0
            elif cast_type == "id" and v is not None:
                v = int(v)

        if isinstance(v, str):
            v = bleach.clean(v)

        return_dict[k] = v

    return return_dict


def populate_return(query_results, limit, offset):
    """ Populates return dictionary for paginated responses.

    Everything that is paginated is overqueried by one to determine if more
    pages exist. This is used to determine the 'has next' parameter, but the
    extra result needs to be removed from the returned results.

    The offset can be used to determine if there are any previous pages.

    """
    to_return = dict()
    to_return["has_next"] = False if len(query_results) < limit else True
    to_return["has_prev"] = False if offset == 0 else True
    to_return["query_result"] = [i.serialize for i in query_results[:limit]]

    return to_return
