"""."""

from typing import Any


class MoveableDict(dict):
    """Dict With Functions For Moving Keys To Top Or Bottom."""

    @staticmethod
    def copy_dict(source: "MoveableDict", target: "MoveableDict") -> dict[Any, Any]:
        """Copies source to target.
        WARNING: WILL OVERWRITE target IF IT ALREADY HAS VALUES!!"""
        target.clear()
        target.update(source)
        assert target == source
        return target

    def move_to_top(self, key):
        """Move Specified Key Value Pair To The Top Of The Dictionary."""
        if key not in self.keys():
            return self
        _new_dict = self.__class__(
            {key: self[key], **{_k: _v for _k, _v in self.items() if _k != key}}
        )
        MoveableDict.copy_dict(_new_dict, self)
        return self

    def move_to_bottom(self, key):
        """Move Specified Key Value Pair To The Bottom Of The Dictionary."""
        if key not in self.keys():
            return self
        self[key] = self.pop(key)
        return self

    def see_last(self) -> tuple:
        if self:
            last_key = self.popitem()
            self[last_key[0]] = last_key[1]
            return last_key[0], last_key[1]
        else:
            return ()


def csv_reader(file_name: str) -> tuple[tuple[dict[str, str], ...], list[int]]:
    """Read CSV files.

    Read csv files, split each row into columns based on commas,
    and create dictionaries for each row with column numbers as keys to values contained in those
    columns.
    everything is treated as a string.
    also counts the number of columns in each row and creates a sorted ascending list (list[int]).
    this can be used to find maximum and minumum number of columns.
    returns tuple of dictionaries for csv data and list of integers for column numbers.

    Parameters
    file_name: str = name of file to be read"""
    values: list[dict[str, str]] = []
    _columns_length: list[int] = []
    with open(file_name, "r") as fx:
        for line_count, line in enumerate(fx):
            if not line.strip(", \n"):
                values.append({"None": "None"})
                continue
            split_columns: list[str] = line.rstrip(", \n").split(",")
            _columns_length.append(len(split_columns))
            value: MoveableDict = MoveableDict(
                {f"Column {ix}": a.strip() for ix, a in enumerate(split_columns)}
            )
            value["Line No."] = str(line_count)
            value.move_to_top("Line No.")
            values.append(value)
    columns_length: list[int] = sorted(_columns_length)
    return tuple(values), columns_length


def dict_search(data: tuple[dict, ...], criteria: dict) -> tuple[dict, ...]:
    """Search If  Specified Criteria Matches A Value In Data.

    criteria must be inputted with keys as column values to check from and values
    either callables (lambda) or exact values to check against.
    checks if any row in any dictionary in data has a column-data pair that
    results true for either callable(data) or data == value and appends that
    dictionary to a list.

    Parameters
    data: tuple[dict]: tuple of dictionaries to check against
    criteria: dict : dictionary of column - value | callable to check against"""
    results: list[dict] = []
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
