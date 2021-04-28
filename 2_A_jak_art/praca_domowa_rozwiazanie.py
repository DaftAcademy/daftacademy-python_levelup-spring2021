import re
from itertools import chain
from typing import List


def greetings(func):
    def wrapper(*args):
        value = func(*args)
        values = value.split(" ")
        values = " ".join(map(lambda x: f"{x[0].upper()}{x[1:].lower()}", values))
        return f"Hello {values}"
        # Alternative solution
        # value = value.title()
        # return f"Hello {value}"

    return wrapper


def is_palindrome(func):
    def check_palindrome(fsentence: str):
        if len(fsentence) < 1:
            return True
        else:
            if fsentence[0] == fsentence[-1]:
                return check_palindrome(fsentence[1:-1])
            else:
                return False

    def wrapper(*args):
        regex = re.compile(r"[A-Za-z0-9]+")
        sentence = func(*args)
        filtered_sentence = "".join(filter(regex.match, sentence)).lower()
        palindrome = check_palindrome(filtered_sentence)

        if palindrome:
            return f"{sentence} - is palindrome"
        else:
            return f"{sentence} - is not palindrome"

    return wrapper


def format_output(*required_keys):
    def decorator(func):
        def build_value(keys: List[List[str]], source_dict: dict):
            values = [source_dict[key] for key in keys]
            return " ".join(values)

        def wrapper(*args):
            dec_arguments = [required_key.split("__") for required_key in required_keys]
            func_output = func(*args)

            if not all(k in func_output.keys() for k in set(chain(*dec_arguments))):
                raise ValueError

            new_output = {}
            for (idx, dec_argument) in enumerate(dec_arguments):
                value = build_value(dec_argument, func_output)
                new_output[required_keys[idx]] = value

            return new_output

        return wrapper

    return decorator


def add_instance_method(klass):
    def decorator(func):
        def wrapper(self):
            return func()

        setattr(klass, func.__name__, wrapper)
        return func

    return decorator


def add_class_method(klass):
    def decorator(func):
        # @classmethod
        def wrapper(cls):
            return func()

        # setattr(klass, func.__name__, wrapper)
        setattr(klass, func.__name__, classmethod(wrapper))
        return func

    return decorator


# Alternative solution - static method
# def add_class_method(klass):
#     def decorator(func):
#         # @statcimethod
#         def wrapper():
#             return func()

#         # setattr(klass, func.__name__, wrapper)
#         setattr(klass, func.__name__, staticmethod(wrapper))
#         return func

#     return decorator
