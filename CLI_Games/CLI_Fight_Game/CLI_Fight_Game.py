import random
import time
import json
import os
import datetime


#to code: custom, more items, item finder rng, cleanup aesthetics

#Constants
SAVEFILE = "CLI_Fight_Game_Suggestions.json"
DEBUGPASS = "md@0405"
SESSIONSTARTTIME = time.time()


#Global Variables
numenemy = 1
defplayerhp = 100
defplayermaxhp = 100
defplayeratk = 10
defplayername = "Hero"
deforchp = 100
deforcmaxhp = 100
deforcatk = 10
defhlthpotionname = '[H]ealth Potion'
defcritrunename = "[R]une of Damaging"
defhlthpotionhp = 25
defcritruneatk = 35
defcritweightage = [10,3,1]
defcritpop = range(1,4) 
gamename = "The Mad Orc Slayer"
orcrunechancepop = range(0,2)
orcrunechanceweightage = [3,1]
homechoices = {"back","b","home","menu"}
item_hotkeys = {
    defhlthpotionname: "h",
    defcritrunename: "r"
}
#defplyrattackupdatemsg = f"{player["name"]} HP: {player["hp"]} || Enemy HP: {orc["hp"]}"
#defplyrhealupdatemsg = f"{player["name"]} heals {hlthpotionhp}"
#deforcattackupdatemsg = f"{player["name"]} HP: {player["hp"]} || Enemy HP: {orc["hp"]}"
#deforchealupdatemsg = f"{orc["name"]} heals {hlthpotionhp}"
sessionstats = {
        "sessions": 0,
        "wins": 0,
        "losses": 0,
        "currentstreak": 0,
        "beststreak": 0,
        "winrate": 0,
}

# Utility Functions

def getinput(
    prompt,

    # Mode toggles
    allowstr=True,      #whether or not to allow letters, automatically disables all checks for 'string rules' toggles.
    intgrs=False,       #whether or not numbers are allowed. when combined with false allowstr, switches to integer checking mode

    # String rules
    spclchar=False,         #whether special characters are allowed -- does not include spaces
    allowspaces=True,      #whether spaces are allowed anywhere in the string (by default whitespaces are removed with .strip() before this toggle is checked)
    min_length=1,           #minimum character length for input, only checked in string mode(inclusive)
    max_length=999,         #maximum character length for input, only checked in string mode (inclusive)

    # Integer rules
    min_value=1,            #minimum value for number. only applies in 'integer mode', i.e when only integer inputs are validated. 
    max_value=999,          #maximum value for number. only applies in 'integer mode', i.e when only integer inputs are validated.

    # Choices
    choices=None,           #if set to list/tuple/set, etc, function checks if input is a part of defined choices. special case in integer mode (refer above).

    # Error messages
    errormsg="Invalid input.",
    errormsg_stronly= "Input must have letters.",
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
            # CHOICES (case-insensitive) CHECK
            if choices is not None:
                if value.lower() not in {str(c).lower() for c in choices}:
                    print(f"Error: {errormsg_choices}\nTry Again.")
                    continue
                else:
                    return value
                    break

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

            return value

        # ---------- INVALID CONFIG ----------
        print("Error: Invalid input configuration.\n")

def gettimeprint():
    elapsedseconds = int(time.time() - SESSIONSTARTTIME)
    hours = elapsedseconds // 3600
    minutes = (elapsedseconds % 3600) // 60
    seconds = elapsedseconds % 60
    timeprint = f"{hours}hrs {minutes}mins {seconds}s"
    return timeprint

def getmenuchoice(
        menuprompt
        ):
    menuchoice = getinput(
        prompt= menuprompt,
        allowstr= False,
        intgrs = True,
    )
    menuchoiceint = int(menuchoice)
    return menuchoiceint

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

# Game Functions

def charactercreation():
    player = {
        "name": defplayername,
        "hp": defplayerhp,
        "maxhp": defplayermaxhp,
        "atk": defplayeratk,
        "inventory": [defhlthpotionname, defcritrunename],
        "dmg": 0,
     }
    orc = {
        "name": "Orc",
        "hp": deforchp,
        "maxhp": deforcmaxhp,
        "atk": deforcatk,
        "inventory": [defhlthpotionname, defcritrunename],
        "dmg": 0,
    }
    return player, orc

def playeraction(
        player,
        orc,
):
          hlthpotionhp = defhlthpotionhp
          while True:
              #------ Player Turn ------
            action = getinput(
              prompt = "\n[A]ttack, [H]eal, view [I]nventory? or view Hea[L]th: ",
              choices = {"Attack","Heal","H","A", "Inventory", "I", "health", "L",}
          )
            if action.startswith("a"):
              crit_list = random.choices(population=defcritpop,weights=defcritweightage,k=1)
              crit = crit_list[0]
              print(f"Critical Hit! Critical Multiplier: {crit}") if crit != 1 else ""
              player["dmg"] = player["atk"]*crit
              orc["hp"] = max(0, orc["hp"] - player["dmg"])
              print(f"{player["name"]} attacks, dealing {player["dmg"]} damage!!")
              time.sleep(1)
              print(f"{player["name"]} HP: {player["hp"]} || Enemy HP: {orc["hp"]}")
              return player, orc
              
            elif action.startswith("h") and defhlthpotionname in player["inventory"] and action != "health":
              if player["hp"] >= player["maxhp"]:
                    print("Already at Max Health!")
                    print(f"{player["name"]} HP: {player["hp"]} || Enemy HP: {orc["hp"]}")
                    continue
              else:
                healamount = min(hlthpotionhp, player["maxhp"] - player["hp"])
                player["hp"] += healamount
                player["inventory"].remove(defhlthpotionname)
                print(f"{player["name"]} heals {healamount} HP!!")
                print(f"{player["name"]} HP: {player["hp"]} || Enemy HP: {orc["hp"]}")
                return player, orc
              
            elif action.startswith("h") and defhlthpotionname not in player["inventory"] and action != "health":
                print(f"No More {defhlthpotionname} available!")
                print(f"{player["name"]} HP: {player["hp"]} || Enemy HP: {orc["hp"]}")
                continue

            elif action.startswith("i"):
                print(player["inventory"])
                print("Press [B] at any time to go back")
                print("To View Descriptions Of Items, Select Yes And Then The Item You Want To View The Description For, Then 'View'")
                validinventorychoices = set({})
                validinventorychoices.update(homechoices)
                for i in player["inventory"]:
                    validinventorychoices.add(i)
                    if "[" in i and "]" in i:
                        startindex = i.find("[") + 1
                        endindex = i.find("]")
                        hotkey = i[startindex:endindex]
                        validinventorychoices.add(hotkey.lower())

                inventoryuse = getinput(
                    prompt= "Do you want to choose an item to use? ([Y]es or [N]o):  ",
                    choices = {"Yes","Y","No","N", *homechoices}, 
                    )
                if inventoryuse in homechoices:
                    continue
                if inventoryuse.startswith("y"):
                    print(player["inventory"])
                    inventoryaction = getinput(
                        prompt= "Choose item to use or view info about:  ",
                        choices= validinventorychoices,
                    )
                    if inventoryaction in homechoices:
                        continue
                    useorview = getinput(
                        prompt= "[U]se or [V]iew Item?:  ",
                        choices= {"Use","U","View","V", *homechoices},
                    )
                    if useorview in homechoices:
                        continue
                    if useorview.startswith("u"):
                        if inventoryaction.startswith("h") or inventoryaction == defhlthpotionname.lower():
                            if player["hp"] >= player["maxhp"]:
                                print("Already at Max Health!")
                                print(f"{player["name"]} HP: {player["hp"]} || Enemy HP: {orc["hp"]}")
                                continue
                            else:
                                healamount = min(hlthpotionhp, player["maxhp"] - player["hp"])
                                player["hp"] += healamount
                                player["inventory"].remove(defhlthpotionname)
                                print(f"{player["name"]} heals {healamount} HP!!")
                                print(f"{player["name"]} HP: {player["hp"]} || Enemy HP: {orc["hp"]}")
                                return player, orc                              

                        elif inventoryaction.startswith("r") or inventoryaction == defcritrunename.lower():
                            player["inventory"].remove(defcritrunename)
                            print(f"You Use {defcritrunename}!")
                            crit = 4
                            print(f"Critical Hit! Critical Multiplier: {crit}") if crit != 1 else ""
                            player["dmg"] = player["atk"]*crit
                            orc["hp"] = max(0, orc["hp"] - player["dmg"])
                            print(f"{player["name"]} attacks, dealing {player["dmg"]} damage!!")
                            time.sleep(1)
                            print(f"{player["name"]} HP: {player["hp"]} || Enemy HP: {orc["hp"]}")
                            return player, orc
                    elif useorview.startswith("v"):
                        if inventoryaction.startswith("b"):
                            continue
                        if inventoryaction.startswith("h"):
                            print(f"{defhlthpotionname} increases health by {defhlthpotionhp}. Consumed on use and skips turn.")
                            continue
                        elif inventoryaction.startswith("r"):
                            print(f"{defcritrunename} ensures critical hit 1 level stronger than normal possible crit level. Consumed on use and skips turn.")
                            continue
                    else:
                        continue
                elif inventoryuse.startswith("n"):
                    continue
                else:
                    continue
            elif action == "l" or action == "health" or action == "view health":
                print(f"\n{player["name"]} HP: {player["hp"]} || Enemy HP: {orc["hp"]}")

def enemyaction(
        player,
        orc,
):
    hlthpotionhp = defhlthpotionhp
    hlthpotionname = defhlthpotionname
    critrunename = defcritrunename
    while True:
              #------ Enemy Turn -------
            for i in range(numenemy):
                if orc["hp"] > (0.75 * orc["maxhp"]) and critrunename in orc["inventory"]:
                    #orcruneusechance = random.choices(population= orcrunechancepop, weights= orcrunechanceweightage,k=1)
                    #orcruneuse = orcruneusechance[0]
                    #if orcruneuse != 0:
                        print(f"{orc["name"]} uses {critrunename}!!")
                        orc["inventory"].remove(defcritrunename)
                        crit = 4
                        print(f"Critical Damage! Critical Multiplier: {crit}")
                        orc["dmg"] = orc["atk"]*crit
                        player["hp"] = max(0, player["hp"] - orc["dmg"])
                        print(f"{orc["name"]} attack, dealing {orc["dmg"]} damage!!")
                        time.sleep(1)
                        print(f"{player["name"]} HP: {player["hp"]} || Enemy HP: {orc["hp"]}")
                        return player, orc

                elif orc["hp"] > (0.40 * orc["maxhp"]):
                    crit_list = random.choices(population=defcritpop,weights=defcritweightage,k=1)
                    crit = crit_list[0]
                    print(f"Orc Does Critical Damage! Critical Multiplier: {crit}") if crit != 1 else ""
                    orc["dmg"] = orc["atk"]*crit
                    player["hp"] = max(0, player["hp"] - orc["dmg"])
                    print(f"{orc["name"]} attacks, dealing {orc["dmg"]} damage!!")
                    time.sleep(1)
                    print(f"{player["name"]} HP: {player["hp"]} || Enemy HP: {orc["hp"]}")
                    return player, orc

                elif orc["hp"] <= (0.4 * orc["maxhp"]) and hlthpotionname in orc["inventory"]:
                    if orc["hp"] >= orc["maxhp"]:
                        print(f"Already at Max Health!")
                        continue
                    else:
                        healamount = min(hlthpotionhp, orc["maxhp"] - orc["hp"])
                        orc["hp"] += healamount
                        orc["inventory"].remove(hlthpotionname)
                        print(f"{orc["name"]} heals {healamount} HP!!")
                        print(f"{player["name"]} HP: {player["hp"]} || Enemy HP: {orc["hp"]}")
                        return player, orc

                elif orc["hp"] <= (0.4 * orc["maxhp"]) and hlthpotionname not in orc["inventory"]:
                    crit_list = random.choices(population=defcritpop,weights=defcritweightage,k=1)
                    crit = crit_list[0]
                    print(f" Orc Does Critical Damage! Critical Multiplier: {crit}") if crit != 1 else ""
                    orc["dmg"] = orc["atk"]*crit
                    player["hp"] = max(0, player["hp"] - orc["dmg"])
                    print(f"{orc["name"]} attacks, dealing {orc["dmg"]} damage!!")
                    time.sleep(1)
                    print(f"{player["name"]} HP: {player["hp"]} || Enemy HP: {orc["hp"]}")
                    return player, orc

def battle(
        Victory_Message = "VICTORYY!!! The Enemy Has Been Slain!!!",
        Defeat_Message = "Defeat... You Died...."
):
     player, orc = charactercreation()

     print(f"A Wild {orc["name"]} appears!\nIt wields a glowing blade, sharp enough to slice bone like butter, and twists its ugly face into a twisted smile.\nIt charges at you.")
     print(f"{player["name"]} HP: {player["hp"]} || Enemy HP: {orc["hp"]}")
     while player["hp"] > 0 and orc["hp"] > 0:
            player, orc = playeraction(player= player, orc= orc)
            print(f"\n{player["name"]} HP: {player["hp"]} || Enemy HP: {orc["hp"]}")
            if orc["hp"] <= 0:
                print(Victory_Message)
                return True
            
            player, orc = enemyaction(player= player, orc= orc)
            print(f"\n{player["name"]} HP: {player["hp"]} || Enemy HP: {orc["hp"]}")
            if player["hp"] <= 0:
                print(Defeat_Message)
                return False

def debugmode():
    while True:
        passkey = getinput(
            prompt= f"Enter Debug Password (B for Menu)",
            spclchar= True,
            intgrs = True,
    )
        if passkey in homechoices:
            break
        elif passkey != DEBUGPASS:
            print("Password Incorrect.\n Try Again")
            continue
        elif passkey == DEBUGPASS:
            print("Debug Mode Accessed. Welcome, Developer:\n")
            print("Debug Mode Under Development.")
            while True:
                suggestionenter = getinput(
                    prompt= f"Do you wish to make a suggestion for a feature to be included in debug mode? (Y/N):\n",
                    choices= {"yes","y","no","n", *homechoices},
                ) 
                if suggestionenter.startswith("y"):
                    while True:
                            suggestion = getinput(
                                prompt= "Enter Feature Suggestion Below. The More Details The Better!\n('B' to go back):\n\n",
                                spclchar= True,
                                intgrs= True,
                            )
                            if suggestion in homechoices:
                                break
                            else:
                                savesuggestion(suggestion= suggestion, mode= "debug")
                                print(f"Suggestion Saved Successfully! Thank You!")
                if suggestionenter.startswith("n"):
                    break

def suggestionmode():
    print("Hello!\nPlease Enter Your Suggestions in The Input Prompt Below. The More Details The Merrier!\n('B' to go back)")
    suggestion = getinput(
        prompt= "Enter Feature Suggestion Below:\n",
        spclchar = True,
        intgrs= True
    )
    if suggestion not in homechoices:
        success = savesuggestion(
            suggestion= suggestion, mode= "normal"
    )
        if success:
            time.sleep(2)
            print("Input Saved Successfully!\nThank You!")
        else:
            print("Error Saving Input.")
            time.sleep(2)
            print("We Are Terribly Sorry. Please Contact The Developer Immediately.")
    else:
        pass

# Combine All The Other Functions Into A Single Looped Function:
def main():
    while True:
        menuchoiceint = getmenuchoice(
            menuprompt= f"""
================{gamename.upper()}=================
1. Battle
2. View Stats
3. Quit Game
4. Debug Mode
5. Suggestions
===================================================
Select Option (Numbers Only!):
""",
)
        if menuchoiceint == 1:
            didwin = battle()
            sessionstats["sessions"] += 1
            if didwin:
                sessionstats["wins"] += 1
                sessionstats["currentstreak"] += 1
                print (f"Current Streak: {sessionstats["currentstreak"]}")
                if sessionstats["currentstreak"] > sessionstats["beststreak"]:
                    sessionstats["beststreak"] = sessionstats["currentstreak"]
                    print(f"New Record!!!! Best Streak: {sessionstats['beststreak']}")
            else:
                sessionstats["losses"] += 1
                print(f"Streak Broken!!!")
                sessionstats["currentstreak"] = 0
                input("\nBattle Ended. Press Enter to Return to Menu.")

        elif menuchoiceint == 2:
            timeprint = gettimeprint()
            if sessionstats["sessions"] > 0:
                sessionstats["winrate"] = (sessionstats["wins"] / sessionstats["sessions"]) * 100
            print(f"""
=============== Session Stats ===============
Games Played: {sessionstats['sessions']}
Time Played: {timeprint}
Wins: {sessionstats['wins']}
Losses: {sessionstats['losses']}
Streak: {sessionstats['currentstreak']}
Best Streak: {sessionstats['beststreak']}
Win Rate: {sessionstats['winrate']}
""")
            input("\nPress Enter to Return to Menu.")

        elif menuchoiceint == 3:
            print(f"Thank You for Playing {gamename}!!")
            print(f"Goodbye.")
            endgame = True
            return endgame
        elif menuchoiceint == 4:
            debugmode()
        elif menuchoiceint == 5:
            suggestionmode()
        else:
            print(f"\n\nInvalid Input.\n\n")
            time.sleep(1)
            continue


# Game Loop:

while True:
    endgame = main()
    if endgame:
        break








