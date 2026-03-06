"""Utils For Python
Created In Like 2025 December Something When I Knew JackSHIT About Coding And Python,
(still know jackshit)
But I Just Kept Adding Later Utils To It.
"""

#easy colorama coloring...
"""#easy colorama coloring :))
# or u could just import Fore.RED as red, or import Fore,
#but maybe in some situation this'll be useful.
import colorama as clr
clr.init(autoreset=True)
red = clr.Fore.RED
blue= clr.Fore.BLUE
green = clr.Fore.GREEN
yellow = clr.Fore.YELLOW
magenta = clr.Fore.MAGENTA
cyan = clr.Fore.CYAN
black = clr.Fore.BLACK
white = clr.Fore.WHITE

"""


#---------------------------------------------FUNCTIONS-----------------------------------------------------
SAVEFILE = None
SESSIONSTARTTIME = None

# 1) getretry function : asks if user wants to restart program, returns accordingly:
# returns True if answer starts with "y" (includes yes, y, yeah, etc.). Can change this.
# directly depends on getinput() function defined below.
def getretry():
      retry = getinput(prompt= "Run Program Again? (Yes/No): ",
                       choices= {"y","yes","n","no"},
                       ).lower()
      
      return True if retry.startswith("y") else False

# 1.b) Better getretry() independant of getinput():
def getretryv2():
    accepted = {"yes","y","no","n"}
    while True:
            retry = input("Restart? (Y/N):  ")
            if retry not in accepted:
                print("Invalid Input")
                continue
            else:
                 return retry.startswith("y")


# 2) getinput function: huge all-in-one answer validation function with multiple toggles for every cases.
# includes only integers, only strings, strings with toggleable special characters, min/max.
# all string checks are performed on .strip().lower() version of answer.
# !NOTE:
# The function has a special if condition at the top to allow for special answer needs where you need
# an otherwise only integer answer with select choices for string inputs.
# This can result in getinput() providing different data types. Always ensure this part works as intended.
# MORE LIKE THIS "SPECIAL CASE" RESULTS IN EVERYTHING BREAKING AND I JUST
#DECCOMMISSIONED THIS.

def getinput(
    # !BEFORE USING THIS PLEASE PLEASE PLEASE CHECK OUT THE GETINTEGERINPUT BELOW AND YK WHAT
    # !JUST DON'T USE THIS ITS VERY POSSIBLY BROKEN I NEED TO RECODE THIS.
    prompt,

    # Mode toggles
    allowstr=True,      #whether or not to allow letters, automatically disables all checks for 'string rules' toggles.
    intgrs=False,       #whether or not numbers are allowed. when combined with false allowstr, switches to integer checking mode

    # String rules
    spclchar=False,         #whether special characters are allowed -- does not include spaces
    allowspaces=True,      #whether spaces are allowed anywhere in the string (by default whitespaces are removed with .strip() before this toggle is checked)
    min_length=1,           #minimum character length for answer, only checked in string mode(inclusive)
    max_length=999,         #maximum character length for answer, only checked in string mode (inclusive)

    # Integer rules
    min_value=1,            #minimum value for number. only applies in 'integer mode', i.e when only integer inputs are validated. 
    max_value=999,          #maximum value for number. only applies in 'integer mode', i.e when only integer inputs are validated.

    # Choices
    choices=None,           #if set to list/tuple/set, etc, function checks if answer is a part of defined choices. special case in integer mode (refer above).

    # Error messages
    errormsg="Invalid answer.",
    errormsg_stronly= "Input must have letters.",
    errormsg_intonly="Input must be a valid integer.",
    errormsg_intgrs="Numbers are not allowed.",
    errormsg_spclchar="Special characters are not allowed.",
    errormsg_spaces="Spaces are not allowed.",
    errormsg_choices="Invalid choice.",
    errormsg_range= "Input out of allowed range.",
):
    """Do not for the love of god use this its broken I need to recode it,
    if u need to get an integer input check out getintegerinput below."""
    while True:
        raw = input(prompt)
        value = raw.strip().lower()

        if not value:
            print(f"Error: {errormsg}\nTry Again.\n")
            continue

        # ---------- INTEGER MODE ----------
        if intgrs and not allowstr:  
                try:
                    # INTEGER CHECK
                    num = int(value)
                except ValueError:
                    print(f"Error: {errormsg_intonly}\nTry Again.\n")
                    continue

                # RANGE CHECK
                if min_value is not None and max_value is not None and num not in range(min_value, max_value + 1):
                    print(f"Error: {errormsg_range}\nAllowed Range:\n{min_value} - {max_value}.\nTry Again.")
                    continue

                # CHOICES (case-insensitive) CHECK
                if choices is not None and num not in choices:
                    print(f"Error: {errormsg_choices}\nAllowed Choices:\n{choices}.\nTry Again.\n")
                    continue 

                return num

        # ---------- STRING MODE ----------
        if allowstr:
            # LENGTH CHECK
            length = len(value)
            if length not in range(min_length, max_length + 1):
                print(
                    f"Error: Input length must be between "
                    f"{min_length} and {max_length} characters.\n"
                    "Try Again.\n"
                )
                continue

            # LETTER CHECK
            if not any(ch.isalpha() for ch in value):
                print(f"Error: {errormsg}\nTry Again.\n")
                continue

            # INTEGER CHECK
            if not intgrs and any(ch.isdigit() for ch in value):
                print(f"Error: {errormsg_intgrs}\nTry Again.\n")
                continue

            # SPACES CHECK
            if not allowspaces and " " in value:
                print(f"Error: {errormsg_spaces}\nTry Again.\n")
                continue

            # SPECIAL CHARACTERS CHECK
            if not spclchar and any(not ch.isalnum() and ch != " " for ch in value):
                print(f"Error: {errormsg_spclchar}\nTry Again.\n")
                continue

            # CHOICES (case-insensitive) CHECK
            if choices is not None:
                if value.lower() not in {str(c).lower() for c in choices}:
                    print(f"Error: {errormsg_choices}\nTry Again.\n")
                    continue

            return value

        # ---------- INVALID CONFIG ----------
        print("Error: Invalid answer configuration.\n")

# 3) getintegerinput function: function used when only integer inputs are needed, pretty much same as getinput function
# fossilized, not needed, getinput does all the work of this function, yet may serve useful where it is faster to code calls for this function rather than getinput 
# due to the higher number of parameters to define to switch getinput into integer mode.
# does not contain the special integer case condition coded in getinput

# *UPDATE - SOMETIME IN FEB 2026:
#turns out, its really fucking frustrating to use getinput and adjust the parameters everytime,
#(also that function is broken im realllyy overdue to recode that),
#so please do use this it is very much NOT fossilized its very easy to use and adjust
#younger me just wanted to sound cool (i think).
def getintegerinput(
    prompt:str,
    errormsg:str ="Value must be a valid integer.",
    errormsgmin:str ="Value is too low.",
    errormsgmax:str ="Value is too high.",
    min_input:int =0,
    max_input:int =1000,
) -> int:
    """Validates Input, Only Accepts Integers In Range min_input to max_input (exclusive)

    Args:
        prompt (str): Message To Display For Input
        errormsg (str, optional): Standard Error Message To Print. 
        Defaults to "Value must be a valid integer.".
        errormsgmin (str, optional): Error Message Printed When Input Too Low. 
        Defaults to "Value is too low.".
        errormsgmax (str, optional): Error Message Printed When Input Too High. 
        Defaults to "Value is too high.".
        min_input (int, optional): Minimum Allowed Input. 
        Defaults to 0.
        max_input (int, optional): Maximum Allowed Input. 
        Defaults to 1000.

    Returns:
        int: User Input, As Integer
    """
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            print(f"Error: {errormsg}\nTry Again.\n")
            continue

        if value < min_input:
            print(f"Error: {errormsgmin}\nTry Again.\n")
            continue
        if value > max_input:
            print(f"Error: {errormsgmax}\nTry Again.\n")
            continue

        return value


# 4) gettimeprint(): returns time elapsed since SESSIONSTARTTIME, which has to be a previously defined global variable.

def gettimeprint():
    elapsedseconds = int(time.time() - SESSIONSTARTTIME)
    hours = elapsedseconds // 3600
    minutes = (elapsedseconds % 3600) // 60
    seconds = elapsedseconds % 60
    timeprint = f"{hours}hrs {minutes}mins {seconds}s"
    return timeprint

# 6) savesuggestion: saves suggestions. takes a "mode" and "suggestion" parameter. suggestion save format can be altered. by default saves day, date and time as well.

def savesuggestion(
        suggestion,
        mode
):
    folderpath = R"C:\Users\Daivik\Documents\VS"
    filename = SAVEFILE
    fullpath = os.path.join(folderpath, filename)
    timeprint = gettimeprint()
    DATETIMEFORMATTED = datetime.datetime.now().strftime("%A, %B %d, %Y,  %H:%M:%S")
    newentry = {
        "Day and Date": DATETIMEFORMATTED,
        "Time  Played at Input": timeprint,
        "Mode": mode,
        "Suggestion": suggestion.title(),
    }
    currentdata = []
    if os.path.exists(fullpath):
        try:
            with open(fullpath, "r") as f:
                currentdata = json.load(f)
        except json.JSONDecodeError:
            pass
    else:
        print("Error.\nFile Not Found")
    currentdata.append(newentry)
    try:
        os.makedirs(folderpath, exist_ok= True)
        with open(fullpath, "w") as f:
            json.dump(currentdata, f, indent=4)
            return True
    except  Exception as e:
        print(f"Error Saving File: {e}")
        return False

# 7) wrapper function template:

def my_decorator(func):
    @functools.wraps(func) # 1. Preserves the name of the original function
    def wrapper(*args, **kwargs): # 2. Accepts ANY arguments
        # --- DO STUFF BEFORE ---
        print(">>> Starting function...")
        
        # 3. Run original function with its arguments
        result = func(*args, **kwargs)
        
        # --- DO STUFF AFTER ---
        print(">>> Function finished.")
        
        return result # 4. Return the value
    return wrapper


def isprime(n):
    if n <= 1:
        is_prime = False
    else:
        is_prime = True  # Flag variable
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                is_prime = False
                break
        return is_prime

#CSV READER:
#BEcause im pretty fucking proud of having coded this myself,
#added to utils on 6th March 2026
#in fact im pretty fucking proud of this and the dict search and moveable dict classes
#I completely made by myself :)
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
            split_columns:list[str] = line.rstrip(", \n").split(",")
            _columns_length.append(len(split_columns))
            value:MoveableDict = MoveableDict({f"Column {ix}": a.strip() for ix, a in enumerate(split_columns)})
            value["Line No."] = str(line_count)
            value.move_to_top("Line No.")
            values.append(value)
    columns_length:list[int] = sorted(_columns_length)
    return tuple(values), columns_length

#Dict Search For Result Of Above CSV Reader
def dict_search(data:tuple[dict, ...], criteria: dict) -> tuple[dict, ...]:
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
            elif val !=  condition:
                match = False
                break
        if match:
            results.append(item)
    return tuple(results)

#Moveable Dict Class
#also proud of this
class MoveableDict(dict):
    """Dict With Functions For Moving Keys To Top Or Bottom."""
    @staticmethod
    def copy_dict(source: MoveableDict, target:MoveableDict) -> dict[Any, Any]:
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
        _new_dict = self.__class__({key: self[key], **{_k:_v for _k, _v in self.items() if _k != key}})
        MoveableDict.copy_dict(_new_dict, self)
        return self

    def move_to_bottom(self, key):
        """Move Specified Key Value Pair To The Bottom Of The Dictionary."""
        if key not in self.keys():
            return self
        self[key] = self.pop(key)
        return self

#fuck it heres the rest of the shit from that file with the above 3 funcs/classes just do you know
#how to use it:
result, columns = csv_reader("testdata.csv")
with open("results.txt" , "w") as f:
    f.write(f"Min Number Of Columns: {columns[0]}\nMax Number Of Columns: {columns[-1]}\n")
    f.write("-"*50 + "\n")

print(f"Min Number Of Columns: {columns[0]}")
print(f"Max Number Of Columns: {columns[-1]}\n\n")
matches_gryff = dict_search(result, {
    "Column 6": "True"
})

with open("results.txt", "a") as f:
    f.write(f"Total Matches: {len(matches_gryff)}\n")
    f.write("-"*50 + "\n")

for i, x in enumerate(matches_gryff, start = 1):
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
    f.write("-"*50 + "\n")
    f.write("CSV DATA\n")
    f.write("-"*50 + "\n")

for i, x in enumerate(result):
    with open("results.txt", "a") as f:
        for k, v in x.items():
            f.write(f"{k}: {repr(v)}\n")
        f.write("\n")
    print(f"---Row {i}---")
    for k, v in x.items():
        print(f"{k}: {repr(v)}")
    print("\n")

if __name__ == "__main__":
    import pygame
    import functools, os, json, datetime, time, sys
