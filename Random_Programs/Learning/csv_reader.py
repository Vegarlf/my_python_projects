"""."""

from typing import Any, Optional, Generic, TypeVar, Self
from collections.abc import Iterable, Mapping, Callable


class MoveableDict[K, V](dict[K, V]):
    """Dict With Functions For Moving Keys To Top Or Bottom."""

    def __init__(
        self, provided_dict: dict[K, V], key_type: type[K], value_type: type[V]
    ):
        self.key_type = key_type
        self.value_type = value_type
        for k, v in provided_dict.items():
            self._check(k, v)
        super().__init__(provided_dict)

    def _check(self, k: object, v: object) -> None:
        if not isinstance(k, self.key_type):
            raise TypeError(
                f"Key {k!r} is {type(k).__name__}, expected {self.key_type.__name__}"
            )
        if not isinstance(v, self.value_type):
            raise TypeError(
                f"Value {v!r} is {type(v).__name__}, expected {self.value_type.__name__}"
            )

    # inefficient as holy fuck. think of something better you lazy ass.
    def move_to_top(self, key: Any):
        """Move Specified Key Value Pair To The Top Of The Dictionary.
        Returns unchanged if key not in dict."""
        if key not in self:
            return self
        for k in list(self):
            if k != key:
                self[k] = self.pop(k)
        return self

    def move_to_bottom(self, key: Any):
        """Move Specified Key Value Pair To The Bottom Of The Dictionary.
        Returns unchanged if key not in dict."""
        if key not in self.keys():
            return self
        self[key] = self.pop(key)
        return self

    def see_last(self) -> tuple[Any, Any] | None:
        """returns tuple of k-v pair at end of dict.
        Returns None if dict not provided"""
        if not self:
            return None
        last_key = next(reversed(self))
        return last_key, self[last_key]


type valuedict = dict[str, str]


def csv_reader(file_name: str) -> tuple[tuple[valuedict, ...], int]:
    """Read CSV files.

    Read csv files, split each row into columns based on commas,
    and create dictionaries for each row with column numbers as keys to values contained in those
    columns.
    everything is treated as a string.
    also counts the number of columns in each row and creates a sorted ascending list int.
    this can be used to find maximum and minumum number of columns.
    returns tuple of dictionaries for csv data and list of integers for column numbers.

    Parameters
    file_name: str = name of file to be read"""
    values: list[valuedict] = []

    with open(file_name, "r") as fx:
        for line_count, line in enumerate(fx):
            if not line.strip(", \n"):
                values.append({"None": "None"})
                continue
            split_columns: list[str] = line.rstrip(", \n").split(",")
            value: MoveableDict[str, str] = MoveableDict(
                {
                    "Line No.": str(line_count),
                    **{f"Column {ix}": a.strip() for ix, a in enumerate(split_columns)},
                },
                str,
                str,
            )
            values.append(value)
    max_columns: int = max((len(v) - 1 for v in values), default=0)
    return tuple(values), max_columns


def dict_search(
    data: tuple[valuedict, ...], criteria: dict[str, str | Callable[[str | None], bool]]
) -> tuple[valuedict, ...]:
    """Search If  Specified Criteria Matches A Value In Data.

    criteria must be inputted with keys as column values to check from and values
    either callables (lambda) or exact values to check against.
    checks if any row in any dictionary in data has a column-data pair that
    results true for either callable(data) or data == value and appends that
    dictionary to a list.

    Parameters
    data: tuple[valuedict]: tuple of dictionaries to check against
    criteria: dict : dictionary of column - value | callable to check against"""
    results: list[valuedict] = []
    for item in data:
        match = True
        for key, condition in criteria.items():
            val = item.get(key)
            if callable(condition):
                try:
                    if not condition(val):
                        match = False
                        break
                except (ValueError, TypeError, AttributeError):
                    match = False
                    break
            elif val != condition:
                match = False
                break
        if match:
            results.append(item)
    return tuple(results)


if __name__ == "__main__":
    result, columns = csv_reader("testdata.csv")
    with open("results.txt", "w") as f:
        f.write(
            f"Min Number Of Columns: {columns[0]}\nMax Number Of Columns: {columns[-1]}\n"
        )
        f.write("-" * 50 + "\n")

    print(f"Min Number Of Columns: {columns[0]}")
    print(f"Max Number Of Columns: {columns[-1]}\n\n")
    matches_gryff = dict_search(result, {"Column 6": "True"})

    with open("results.txt", "a") as f:
        f.write(f"Total Matches: {len(matches_gryff)}\n")
        f.write("-" * 50 + "\n")

    for i, x in enumerate(matches_gryff, start=1):
        with open("results.txt", "a") as f:
            f.write(f"Match No. {i}\n")
            for k, v in x.items():
                f.write(f"{k}: {repr(v)}\n")
            f.write("\n")
        print(f"Total Matches: {len(matches_gryff)}\n")
        print(f"Match No {i}")
        for k, v in x.items():
            print(f"{k}: {repr(v)}")
        print("\n")

    print("\n\n")

    with open("results.txt", "a") as f:
        f.write("-" * 50 + "\n")
        f.write("CSV DATA\n")
        f.write("-" * 50 + "\n")

    for i, x in enumerate(result):
        with open("results.txt", "a") as f:
            for k, v in x.items():
                f.write(f"{k}: {repr(v)}\n")
            f.write("\n")
        print(f"---Row {i}---")
        for k, v in x.items():
            print(f"{k}: {repr(v)}")
        print("\n")
