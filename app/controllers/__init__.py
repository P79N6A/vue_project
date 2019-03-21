"""Controller global functions.

Contains functions and classes for data cleaning and validation.
Contains a pagination function that is used in most query results.

"""

import bleach
import decimal
import datetime

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
#all_validators["not_empty"] = not_empty

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
    to_return["query_result"] = [i for i in query_results[:limit]]

    return to_return


def serialize(to_serialize):
    """Serializes a list of objects based on attribute types."""

    # ! NEEDS TO SUPPORT RECURSION !
    # ! NEEDS TO POPULATE FIELDS ATTRIBUTE FOR RESPONSE DICTIONARY !

    '''
    return_list = []

    for to_serialize in object_list[:1]:
        current_serialize_dict = dict()
        for field in to_serialize._fields:
            value = getattr(to_serialize, field)
            if value is None:
                current_serialize_dict[field] = value
            elif type(value) in [int, str, bool]:
                current_serialize_dict[field] = value
            elif type(value) in [list, dict]:
                # RECURSION HERE
                pass
            elif type(value) == decimal.Decimal:
                current_serialize_dict[field] = str(value)
            elif type(value) == datetime.datetime:
                current_serialize_dict[field] = str(value)

        return_list.append(current_serialize_dict)

    return return_list
    '''
    #print(to_serialize)

    if to_serialize is None:
        return (None, None)
    elif type(to_serialize) == int:
        return (to_serialize, "integer")
    elif type(to_serialize) == str:
        return (to_serialize, "string")
    elif type(to_serialize) == bool:
        return (to_serialize, "boolean")
    elif type(to_serialize) == decimal.Decimal:
        return (str(to_serialize), "decimal")
    elif type(to_serialize) == list:
        return_list = []
        # Handle results of [None]
        if not (len(to_serialize) == 1 and to_serialize[0] == None):
            for to_reserialize in to_serialize:
                return_list.append(serialize(to_reserialize))
        return (return_list, "list")
    elif type(to_serialize) == datetime.datetime:
        return (to_serialize.strftime("{%Y-%m-%d %H:%M:%S}"), "datetime")
    else:
        raise TyperError("Serializer for type {} not implemented.".format(type(to_serialize)))


def process_result(object_list, required_list=[], exclude_list=[]):
    """Serializes values in passed list and applies metadata for return"""
    if type(object_list) != list:
        object_list = [object_list]

    return_list = []

    for to_process in object_list:
        field_dict = dict()

        iter_list = to_process._fields if hasattr(to_process, "_fields") else [x.name for x in to_process.__table__.columns]

        for index, field in enumerate(iter_list):
            if field not in exclude_list:
                current_field_dict = dict()

                value = getattr(to_process, field)
                serialized_value = serialize(value)

                current_field_dict["type"] = serialized_value[1]
                current_field_dict["label"] = field
                current_field_dict["required"] = True if field in required_list else False
                current_field_dict["order"] = index
                current_field_dict["value_attrib"] = field
                current_field_dict["value"] = serialized_value[0]

                field_dict[field] = current_field_dict

        return_list.append(field_dict)

    return return_list
