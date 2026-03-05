
import random

# NOTE:
# The Common getinput() function used has a special if condition at the top
# To allow for special input needs such as in getmoneystats() where you need
# an otherwise integer input with select choices for string inputs.
# This can result in getinput() providing different types of variables.

# Global Variables

casinoname = "The Python Guessers Casino"
moneystartdefault = 100
moneywrongdefault = 5
moneywindefault = 50
moneylosedefault = 75  

# Common Utility Functions

def getinput(
    prompt,

    # Mode toggles
    allowstr=True,
    intgrs=False,

    # String rules
    stronly = False,
    spclchar=False,
    allowspaces=True,
    min_length=1,
    max_length=999,

    # Integer rules
    min_value=1,
    max_value=999,

    # Choices
    choices=None,

    # Error messages
    errormsg="Invalid input.",
    errormsg_stronly= "Input must be letters.",
    errormsg_intonly="Input must be a valid integer.",
    errormsg_intgrs="Numbers are not allowed.",
    errormsg_spclchar="Special characters are not allowed.",
    errormsg_spaces="Spaces are not allowed.",
    errormsg_choices="Invalid choice.",
    errormsg_range= "Input out of allowed range.",
):
    while True:
        raw = input(prompt)
        value = raw.strip().lower()

        if not value:
            print(f"Error: {errormsg}\nTry Again.\n")
            continue

        # ---------- INTEGER MODE ----------
        if intgrs and not allowstr:  
            
            # SPECIAL CHOICE CONDITION:
            if choices is not None:
                if value.lower() in {str(c).lower() for c in choices}:
                    return value
            else:
                try:
                    num = int(value)
                except ValueError:
                    print(f"Error: {errormsg_intonly}\nTry Again.\n")
                    continue

                if min_value is not None and num < min_value:
                    print(f"Error: {errormsg_range}\nAllowed Range:\n{min_value} - {max_value}.\nTry Again.\n")
                    continue

                if max_value is not None and num > max_value:
                    print(f"Error: {errormsg_range}\nAllowed Range:\n{min_value} - {max_value}.\nTry Again.\n")
                    continue

                if choices is not None and num not in choices:
                    print(f"Error: {errormsg_choices}\nAllowed Choices:\n{choices}.\nTry Again.\n")
                    continue 

                return num

        # ---------- STRING MODE ----------
        if allowstr:
            # Length check
            length = len(value)
            if length not in range(min_length, max_length + 1):
                print(
                    f"Error: Input length must be between "
                    f"{min_length} and {max_length} characters.\n"
                    "Try Again.\n"
                )
                continue

            if stronly and any(not ch.isalpha() for ch in value):
                print(f"Error: {errormsg_stronly}\nTry Again. \n")
                continue

            # Must contain at least one letter
            if not any(ch.isalpha() for ch in value):
                print(f"Error: {errormsg}\nTry Again.\n")
                continue

            # Digits
            if not intgrs and any(ch.isdigit() for ch in value):
                print(f"Error: {errormsg_intgrs}\nTry Again.\n")
                continue

            # Spaces
            if not allowspaces and " " in value:
                print(f"Error: {errormsg_spaces}\nTry Again.\n")
                continue

            # Special characters
            if not spclchar and any(not ch.isalnum() and ch != " " for ch in value):
                print(f"Error: {errormsg_spclchar}\nTry Again.\n")
                continue

            # Choices (case-insensitive)
            if choices is not None:
                if value.lower() not in {str(c).lower() for c in choices}:
                    print(f"Error: {errormsg_choices}\nTry Again.\n")
                    continue

            return value

        # ---------- INVALID CONFIG ----------
        print("Error: Invalid input configuration.\n")

def getintegerinput(
    prompt,
    errormsg="Value must be a valid integer.",
    errormsgmin="Value is too low.",
    errormsgmax="Value is too high.",
    min=None,
    max=None,
    intonly=True
):
    while True:
        raw = input(prompt).strip()

        try:
            value = int(raw) if intonly else raw
        except ValueError:
            print(f"Error: {errormsg}\nTry Again.\n")
            continue

        if intonly:
            if min is not None and value < min:
                print(f"Error: {errormsgmin}\nTry Again.\n")
                continue
            if max is not None and value > max:
                print(f"Error: {errormsgmax}\nTry Again.\n")
                continue

        return raw, value

def getretry():
      retry = getinput(prompt= "Run Program Again? (Yes/No): ",
                       choices= {"y","yes","n","no"},
                       ).lower()
      
      return retry.startswith("y")

# Game Functions

def getdifficulty():
    difficulty = getinput(prompt = "Select Difficulty.\nDifficulty levels change range of numbers and amount of guesses.\nOptions:\nEasy: 1-25, 5 attempts\nMedium: 1-50, 10 attempts\nHard: 1-100, 15 attempts\nReply with 'custom' to customize range and guesses:  ", 
                                    allowspaces = False,
                                    choices = {"easy", "medium", "hard", "custom"}
                                    ).lower()
    return difficulty

def getrangeguess():
    difficulty = getdifficulty()
    if difficulty == "easy":
        rangemin = 1
        rangemax = 25
        attempts = 5
    elif difficulty == "medium":
        rangemin = 1
        rangemax = 50
        attempts = 10
    elif difficulty == "hard":
        rangemin = 1
        rangemax = 100
        attempts = 15
        print("COOKED")
    elif difficulty == "custom":
        rangemin = getinput(prompt = "Minimum Value for Range(Included): ",
                                               allowstr= False,
                                               intgrs= True,
                                               min_value= 1,
                                               max_value = 999)
        rangemax = getinput(prompt = "Maximum Value for Range(Included): ", 
                            allowstr= False,
                            intgrs= True,
                            min_value= 2, 
                            max_value= 1000)
        attempts = getinput(prompt = "Number of Attempts: ", 
                            allowstr= False,
                            intgrs= True,
                            min_value= 1, max_value= 100)         

    return attempts, rangemin, rangemax, difficulty
         
def getmoneystats():
    print("Select Money Parameters. Type 'Default' To Start With Default Parameters")
    moneystartinput = getinput(prompt= "Money Amount to Start With:  $",
                               allowstr= False,
                               intgrs= True)

    if moneystartinput == "default":
        moneystart = moneystartdefault
        moneywrong = moneywrongdefault
        moneywin = moneywindefault
        moneylose = moneylosedefault
    elif moneystartinput != "default":
        moneystart = int(moneystartinput)

        moneywronginput = getinput(prompt= "Amount Deducted For Each Wrong Guess (Keep This Small):  $",
                               allowstr= False,
                               intgrs= True)
        moneywrong = int(moneywronginput)
        #----------------------------------------------
        moneywininput = getinput(prompt= "Amount Added For Each Win:  $",
                             allowstr= False,
                             intgrs= True)
        moneywin = int(moneywininput)
        #---------------------------------------
        moneyloseinput = getinput(prompt= "Amount Deducted For Each Game Loss:  $",
                              allowstr= False,
                              intgrs= True)
        moneylose = int(moneyloseinput)

    return moneystart, moneywrong, moneywin, moneylose

def main():
  print(f"""
Welcome tooooo {casinoname}. Rules are:
1) Don't be an IDIOT
2) Get Luckyy
A random number is selected from a range according to the difficulty selected
Number of attempts are generated according to difficulty selected
You start with $100(customizable). Every wrong guess costs $5, and every correct guess gets you $50. Everytime you lose the game, you lose $75.
Enjoy!
-----------------------------------------------------------------------------------------------------------------------------------------------
""")
  attempts, rangemin, rangemax, difficulty = getrangeguess()
  moneystart, moneywrong, moneywin, moneylose = getmoneystats()
  magicnumber = random.randint(rangemin, rangemax)
  i = 0
  money = moneystart
  print(f"Selected Difficulty Level: {difficulty.title()}")
  print(f"Guess Range (Inclusive): {rangemin} - {rangemax}")
  print(f"Starting With: ${moneystart}")
  print(f"Number of Guesses: {attempts}")
  print("-------------------------------------------------------------")
  guess = None
  while i < attempts:
      guess = getinput(prompt= "Guessed Number:  ",
                     errormsg= "ITS SUPPOSED TO BE A NUMBER YOU ABSOLUTE DUMBASS ARE YOU FUCKING ILLITERATE I HAVE SPENT TWICE THE TIME I SHOULD HAVE ON THIS PROJECT ADDING CONDITIONS FOR BASIC FUCKING NUMBER INPUTS SO THAT ABSOLUTE BLASPHEMOUS IDIOTS LIKE YOU DONT BREAK MY GAME",
                     allowstr= False,
                     intgrs= True,
                     min_value= rangemin,
                     max_value= rangemax)
      if guess > magicnumber:
          print("In the clouds, come back down!")
          i += 1
          money -= moneywrong
          print(f"Guesses Left: {attempts - i}")
          print(f"Money Left: {money}")
          print("----------------------------------------")
      elif guess < magicnumber:
          print("Too deep, come back up!")
          i += 1
          money -= moneywrong
          print(f"Guesses left: {attempts - i   }")
          print(f"Money Left: {money}")
          print("----------------------------------------")
      elif guess == magicnumber:
          break
  if guess == magicnumber:
        money += moneywin
        print("BOOYAH, YOUUU WON")
        print(f"The Magic Number Was....   {magicnumber}!")
        print(f"CONGRATULATIONS, BABYY")
        print(f"You won with {attempts - i} guesses remaining and ${money}!\nCome Back Again!!")
        win = True
  if i >= attempts and guess != magicnumber:
      money -= moneylose
      print("Out of Guesses! You Lose!")
      print(f"The Magic Number Was....   {magicnumber}!")
      print("HAHAAAAAAA BOZO")
      print(f"You ended up losing with ${money} in the bank.\nGive Us More Money!!")
      win = False

  return money
  
# Game Loop

while True:
    main()
    if getretry() != True:
        print(f"Thank You For Visiting {casinoname}! Hope We See You Again!")
        break


  