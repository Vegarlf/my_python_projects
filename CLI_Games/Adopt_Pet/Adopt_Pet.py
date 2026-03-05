import random
import time
import colorama as cl
import Python_Utilities as pu
import re

cl.init(autoreset=True)

red = cl.Fore.RED
blue = cl.Fore.BLUE
green = cl.Fore.GREEN
magenta = cl.Fore.MAGENTA
yellow = cl.Fore.YELLOW
cyan = cl.Fore.CYAN
gamename = "Adopt A Pet"


def reduceitemcount(
    target,
    item,
    index,
    searchstring=r"x(\d+)$",
):
    match = re.search(searchstring, item)
    if match:
        count = int(match.group(1))
        if count < 1:
            count = 1
        basename = item[: match.start()].strip()
    else:
        count = 1
        basename = item
    count -= 1
    if count == 0:
        target.inventory.pop(index)
        print(f"{magenta}You Are Out Of{cyan} {basename + "s"}{magenta}.")
        found = True
    elif count == 1:
        target.inventory[index] = basename
        found = True
    else:
        target.inventory[index] = f"{basename} x{count}"
        found = True
    return count, basename, found


class pet:
    def __init__(self, name, species, inventory=None):
        self.name = pu.title(name)
        self.species = pu.title(species)

        self.hunger = 50
        self.boredom = 50
        self.energy = 50
        self.state = True
        self.alive = True
        if not inventory:
            self.inventory = ["Basic Food x2", "Energy Bar x2", "Tennis Ball"]
        else:
            self.inventory = inventory

    def tick(self):
        if not self.state:
            self.hunger += 20
            self.boredom += 20
            self.energy -= 20
        self.hunger += 10
        self.boredom += 10
        self.energy -= 10

        if self.hunger >= 100:
            print(f"{yellow}{self.name}{red} {"has starved to death".title()}...")
            self.alive = False
        elif self.boredom >= 100:
            print(
                f"{yellow}{self.name}{red} {"ran away because".title()} {"It"} {"was too bored".title()}..."
            )
            self.alive = False
        elif self.energy <= 10:
            print(
                f"{yellow}{self.name}{red} {"is too tired!".title()} {"hunger and boredom increase faster.".title()}"
            )
            self.state = False

    def feed(self):
        found = False
        for index, item in enumerate(self.inventory):
            if "food" in item.strip().lower():

                self.hunger -= 15
                self.energy += 5
                self.hunger = max(0, self.hunger)
                self.energy = min(100, self.energy)

                count, basename, found = reduceitemcount(self, item, index)
                print(
                    f"\n{green}{"you feed".title()} {yellow}{self.name}{blue} {basename}{green}!! Nom Nom Nom."
                )

                break
        if not found:
            print(f"{red}{pu.title("you dont have any food in your inventory!!")}")

    def play(self):
        if not self.state:
            print(f"{yellow}{self.name}{red} {pu.title("is too tired to play...")}")
        else:
            found = False
            for index, item in enumerate(self.inventory):
                if "ball" in item.strip().lower():
                    print(
                        f"\n{green}{pu.title("you play fetch with")} {yellow}{self.name}."
                    )

                    self.hunger += 10
                    self.boredom -= 15
                    self.energy -= 10
                    self.hunger = max(0, self.hunger)
                    self.boredom = max(0, self.boredom)
                    self.energy = min(100, self.energy)

                    lostchancepop = range(0, 2)
                    lostchanceweights = [2, 1]
                    lostchance = random.choices(
                        population=lostchancepop, weights=lostchanceweights, k=1
                    )
                    lost = lostchance[0]
                    if lost == 1:
                        print(
                            f"{blue}{pu.title("oh no! you lost the ball while playing fetch!!")}"
                        )
                        count, basename, found = reduceitemcount(self, item, index)

                    break
            if not found:
                print(
                    f"{red}{pu.title("you dont have any balls to play fetch with in your inventory!!")}"
                )

    def sleep(self):
        print(f"{yellow}{self.name}{green} {pu.title("takes a long nice nap...")}")
        print(
            f"\n{cyan}{pu.title("wait 10 seconds while")}{yellow} {self.name} {cyan} {pu.title("wakes up from their nap...")}"
        )
        for i in range(10, 0, -1):
            print(f"{i}...")
            time.sleep(1)
        self.energy += 30
        self.hunger += 5
        self.energy = min(100, self.energy)

    def __str__(self):
        hungercol = cl.Fore.RED if self.hunger > 75 else cl.Fore.GREEN
        boredomcol = cl.Fore.RED if self.boredom > 75 else cl.Fore.GREEN
        energycol = cl.Fore.RED if self.energy < 25 else cl.Fore.GREEN
        string = f"""
\n{cyan}----------------------------------------------{magenta}
---->> {yellow}{self.name}{magenta} Of The {green}{self.species}{magenta} <<----
-----------------------------------------------
Hunger: {hungercol}{blue}{self.hunger}%{magenta}
Boredom: {boredomcol}{blue}{self.boredom}%{magenta}
Energy: {energycol}{blue}{self.energy}%{magenta}
-----------------------------------------------"""
        return string


while True:
    print(f"{red}{gamename}!!!")
    pname = pu.getinput(
        prompt=f"{cyan}Name Your Pet\n>>{yellow}  ",
        max_length=99,
        intgrs=True,
        spclchar=True,
        allowspaces=True,
    )
    pspecies = pu.getinput(
        prompt=f"{cyan}Pet Species\n>>{yellow}  ",
        allowspaces=True,
    )

    pet1 = pet(pname, pspecies)

    while pet1.alive:
        print(pet1.__str__())

        print(
            f"{blue}\n[1] Feed\n[2] Play\n[3] Sleep\n[4] Do Nothing\n[5] View Inventory"
        )
        choice = pu.get_integer_input(
            prompt="\n>>  ",
            min=1,
            max=5,
        )

        if choice == 1:
            pet1.feed()
        elif choice == 2:
            pet1.play()
        elif choice == 3:
            pet1.sleep()
        elif choice == 4:
            print(
                f"{magenta}You're Too {red}BUSY{magenta} To Spend Time With Your {green}Adorable Perfect Cute Loving Pet The CUTEST {yellow}{pet1.name}{magenta}......\n{magenta}In Fact, You're {red}SO{magenta} Busy That You Can't Play For Another {red}10{magenta} seconds!"
            )
            for i in range(1, 11):
                print(f"{i}...")
                time.sleep(1)
        elif choice == 5:
            print(pet1.inventory)
            time.sleep(1)
            continue
        else:
            print("Invalid Choice")
            continue

        pet1.tick()
        time.sleep(0.75)

    print(f"{red}{pu.title("game over")}")
    if pu.getretryv2():
        continue
    else:
        print(f"{red}THANK YOU FOR PLAYING {yellow}{gamename}{red}!!!")
