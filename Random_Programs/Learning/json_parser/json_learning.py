from typing import Iterator

"""Attempt To Make A JSON Parser"""

SPECIAL_CHARACTERS: dict[str, dict[str, dict[str, str]] | dict[str, str] | str] = {
    "Stack_Characters": {
        "JsonObject": {
            "Open": "{",
            "Close": "}",
        },
        "JsonArray": {
            "Open": "[",
            "Close": "]",
        },
    },
    "Identifier": {
        "KeyValueAssigner": ":",
        "StringOpener": '"',
    },
    "Comma": ",",
}


class JsonExceptions:
    """Special Exceptions For JSON Parsing."""

    class JsonStructureError(ValueError):
        """Exception Raised When JSON Content/Format Is Invalid."""

        def __init__(self, message: str, source_string=None):
            super().__init__(message)
            self.source_string = source_string

        def __str__(self):
            return f"{self.__class__.__name__}" + super().__str__(self)  # fmt: skip

        @staticmethod
        def verify(
            condition: bool, message: str = "JSON Structure Invalid", source_string=None
        ):
            """Verifies Whether Condition, Else Raises JsonStructureError."""
            if not condition:
                raise JsonDecodeError(message, source_string)

    class JsonRegistryError(ValueError):
        """Exception Raised When JSON Code Malfunctions, Specifically A Mismatch In JSON Object/Array Registries."""

        def __init__(self, message: str, source_string=None):
            super().__init__(message)
            self.source_string = source_string

        def __str__(self):
            return f"{self.__class__.__name__}" + super().__str__()  # fmt: skip

        @staticmethod
        def verify(
            condition: bool, message: str = "JSON Registry Invalid", source_string=None
        ):
            """Verifies Whether Condition, Else Raises JsonRegistryError."""
            if not condition:
                raise JsonRegistryError(message, source_string)

    class JsonStackError(ValueError):
        """Exception Raised When Decoding Stack Is Invalid."""

        def __init__(self, message: str, source_string=None):
            super().__init__(message)
            self.source_string = source_string

        def __str__(self):
            return f"{self.__class__.__name__}" + super().__str__()  # fmt: skip


JsonDecodeError = JsonExceptions.JsonStructureError
JsonRegistryError = JsonExceptions.JsonRegistryError
JsonStackError = JsonExceptions.JsonStackError


class PreParsingOperations:
    """Operations Performed On File Before Parsing"""

    @staticmethod
    def stringify(filename_: str) -> str:
        """Turns JSON File Into Single String, Whitespace Preserved."""
        with open(filename_, "r") as f:
            superstring = "".join(line for line in f)
        return superstring

    @staticmethod
    def whitespace_remover(superstring_: str) -> str:
        """Removes Whitespace From Stringified JSON File, Preserving Whitespace Inside Strings."""
        return_string_parts: list[str] = list(superstring_)
        is_string_part: bool = False
        for char_index, char in enumerate(return_string_parts):
            if (
                char == '"'
                and return_string_parts[char_index - 1 : char_index + 1] != "\\"
            ):
                # Open String Part
                is_string_part = True
            elif (
                char == '"'
                and return_string_parts[char_index - 1 : char_index + 1] != "\\"
                and is_string_part
            ):
                # Close String Part
                is_string_part = False
            if char == " " and not is_string_part:
                # Actual Whitespace Remover
                return_string_parts[char_index] = ""
        return "".join(return_string_parts)


class JsonObject:
    """JSON Object That Translates To Python Dictionary."""

    REGISTRY: list["JsonObject"] = []
    REGISTRY_COUNT: int = 0

    def __init__(self):
        JsonRegistryError.verify(
            len(JsonObject.REGISTRY) == JsonObject.REGISTRY_COUNT,
            f"{self.__class__.__name__} Registry Mismatch",
        )
        JsonObject.REGISTRY.append(self)
        JsonObject.REGISTRY_COUNT += 1

    def __str__(self):
        return "JsonObject"


class JsonArray:
    """JSON Array That Translates Into Python List."""

    REGISTRY: list["JsonArray"] = []
    REGISTRY_COUNT: int = 0

    def __init__(self):
        JsonRegistryError.verify(
            len(JsonArray.REGISTRY) == JsonArray.REGISTRY_COUNT,
            f"{self.__class__.__name__} Registry Mismatch",
        )
        JsonArray.REGISTRY.append(self)
        JsonArray.REGISTRY_COUNT += 1

    def __str__(self):
        return "JsonArray"


stack: list[JsonObject | JsonArray] = []


def stack_updater(char: str):
    """Adds/Removes Object/Array From Stack."""
    global stack, SPECIAL_CHARACTERS

    def open_jsonobject():
        """Open JSON Object To Stack"""
        stack.append(JsonObject())

    def close_jsonobject():
        """Remove JSON Object From Stack"""
        JsonDecodeError.verify(
            isinstance(stack[-1], JsonObject), "JSON Structure Invalid", char
        )
        stack.pop()

    def open_jsonarray():
        """Open JSON Object To Stack"""
        stack.append(JsonArray())

    def close_jsonarray():
        """Close JSON Object From Stack"""
        JsonDecodeError.verify(
            isinstance(stack[-1], JsonArray), "JSON Structure Invalid", char
        )
        stack.pop()

    stack_dispatch_values = {
        SPECIAL_CHARACTERS["Stack_Characters"]["JsonObject"]["Open"]: open_jsonobject,
        SPECIAL_CHARACTERS["Stack_Characters"]["JsonObject"]["Close"]: close_jsonobject,
        SPECIAL_CHARACTERS["Stack_Characters"]["JsonArray"]["Open"]: open_jsonarray,
        SPECIAL_CHARACTERS["Stack_Characters"]["JsonArray"]["Close"]: close_jsonarray,
    }
    handler = stack_dispatch_values.get(char)
    if handler:
        handler()
    # for char_index, char in enumerate(string_):
    #     handler = stack_dispatch_values.get(char)
    #     if handler:
    #         handler()


def get_current_type(_stack) -> int:
    """Returns 0 If Last Value In Stack Is Object, 1 If Array."""
    last_value: JsonObject | JsonArray = stack[-1]
    if isinstance(last_value, JsonObject):
        return 0
    elif isinstance(last_value, JsonArray):
        return 1
    else:
        raise JsonStackError(f"Last Stack Value Not Recognised, {last_value}")


def string_parser(string_iterator: Iterator[str]):
    """Parse Strings."""
    content: str = ""
    is_escaped: bool = False
    for char_index, char in enumerate(string_iterator):
        if is_escaped:
            content += char
            is_escaped = False
            continue
        if char == "\\":
            is_escaped = True
            continue
        elif char == '"':
            return content
        content += char
    raise JsonDecodeError("Unterminated String")


def number_parser(string_iterator: Iterator[str]):
    """Parse Numbers."""
    # check for : negative, decimal, e (scientific notation),
    # check if number - non-allowed char - number -> JSONStructureError
