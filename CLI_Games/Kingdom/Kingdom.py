from abc import ABC, abstractmethod
import Python_Utilities as p
import time

# --- CONFIGURATION (CONSTANTS) ---
startfood = 25
startgld = 25
startwood = 25

# Farm Stats
farmfoodprodn = 25
farmgoldprodn = 0
farmwoodprodn = -5
farmfoodcost = 10
farmgoldcost = 10
farmwoodcost = 20
farmtime = 1

# Mine Stats
minefoodprodn = -5
minegoldprodn = 25
minewoodprodn = -5
minefoodcost = 15
minegoldcost = 20
minewoodcost = 25
minetime = 2

# Woodcutter Stats
woodcutterfoodprodn = -5
woodcuttergoldprodn = 0
woodcutterwoodprodn = 35
woodcutterfoodcost = -5
woodcuttergoldcost = 10
woodcutterwoodcost = 5
woodcuttertime = 1

# Population Consumption
popfoodreq = 1

# --- CLASS DEFINITIONS ---

class resources:
    def __init__(self, Food: int, Gold: int, Wood: int):
        self.food = Food
        self.gold = Gold
        self.wood = Wood

    def __str__(self):
        fcol = p.red if self.food <= 0 else p.green
        gcol = p.red if self.gold <= 0 else p.green
        wcol = p.red if self.wood <= 0 else p.green
        return f"[Food: {fcol}{self.food}{p.magenta} | Gold: {gcol}{self.gold}{p.magenta} | Wood: {wcol}{self.wood}{p.magenta}]"

    def __add__(self, other):
        return resources(self.food + other.food, self.gold + other.gold, self.wood + other.wood)
    
    def __sub__(self, other):
        return resources(self.food - other.food, self.gold - other.gold, self.wood - other.wood)

    def __ge__(self, other):
        return (self.food >= other.food) and (self.gold >= other.gold) and (self.wood >= other.wood)

class building(ABC):
    def __init__(self, name: str, amount: int):
        self.name = name
        self.amount = amount

    @abstractmethod
    def getprodn(self): pass
    @abstractmethod
    def getcost(self): pass
    @abstractmethod
    def time(self): pass
    
    def __str__(self):
        return f"{self.name} (x{self.amount})"

# --- CONCRETE BUILDINGS ---
class farm(building):
    def getprodn(self):
        return resources(farmfoodprodn*self.amount, farmgoldprodn*self.amount, farmwoodprodn*self.amount)
    def getcost(self):
        return resources(farmfoodcost*self.amount, farmgoldcost*self.amount, farmwoodcost*self.amount)
    def time(self):
        return farmtime * self.amount

class mine(building):
    def getprodn(self):
        return resources(minefoodprodn*self.amount, minegoldprodn*self.amount, minewoodprodn*self.amount)
    def getcost(self):
        return resources(minefoodcost*self.amount, minegoldcost*self.amount, minewoodcost*self.amount)
    def time(self):
        return minetime * self.amount

class woodcutter(building):
    def getprodn(self):
        return resources(woodcutterfoodprodn*self.amount, woodcuttergoldprodn*self.amount, woodcutterwoodprodn*self.amount)
    def getcost(self):
        return resources(woodcutterfoodcost*self.amount, woodcuttergoldcost*self.amount, woodcutterwoodcost*self.amount)
    def time(self):
        return woodcuttertime * self.amount

# --- KINGDOM MANAGER ---
class kingdom:
    def __init__(self, name: str, population: int, buildings: list):
        self.name = name
        self.population = population
        self.buildings = buildings
        self.resources = resources(startfood, startgld, startwood)
        self.turncount = 0
    
    def __str__(self):
        b_list = ", ".join([str(b) for b in self.buildings]) if self.buildings else "None"
        string = f"""
{p.yellow}=== {self.name} (Day {self.turncount}) ===
{p.blue}Population: {p.magenta}{self.population}
{p.blue}Resources: {p.magenta}{self.resources}
{p.blue}Buildings: {p.magenta}{b_list}
"""
        return string

    def resourcecheck(self):
        # 1. Starvation Check
        if self.resources.food < 0:
            deficit = abs(self.resources.food)
            self.population -= deficit
            self.resources.food = 0
            print(f"{p.red}💀 STARVATION! {deficit} people died.")
            if self.population <= 0:
                print(f"{p.red}The Kingdom has fallen. GAME OVER.")
                exit()
        
        # 2. Population Growth Check (NEW LOGIC)
        # If we have 2x more food than required, pop grows by 10%
        food_needed = self.population * popfoodreq
        if self.resources.food > (food_needed * 2):
            growth = max(1, int(self.population * 0.10)) # Grow by 10% (min 1 person)
            self.population += growth
            print(f"{p.green}👶 Baby Boom! Population increased by {growth}.")

        # 3. Bankruptcy Check
        if self.resources.gold < 0:
            print(f"{p.red}📉 BANKRUPTCY! Economy crashing...")

    def advanceday(self):
        self.turncount += 1
        print(f"{p.cyan}--- Advancing to Day {self.turncount} ---")
        
        # Production
        for b in self.buildings:
            prod = b.getprodn()
            self.resources += prod

        # Consumption
        total_food_cost = self.population * popfoodreq
        self.resources.food -= total_food_cost
        
        # Checks (Growth/Death)
        self.resourcecheck()

    def addbuilding(self, new_building: building):
        cost = new_building.getcost()
        if self.resources >= cost:
            print(f"{p.green}Constructing {new_building.name}...")
            self.resources = self.resources - cost
            # Instant build for now to keep game fast
            self.buildings.append(new_building) 
            print(f"{p.green}Construction Complete! {new_building.name} added.")
        else:
            print(f"{p.red}Not enough resources! Need: {cost.food}F {cost.gold}G {cost.wood}W")

# --- CHEATS ENGINE ---
class Cheats:
    @staticmethod
    def run(k: kingdom, code: str, *args, **kwargs):
        print(f"\n{p.yellow}--- CHEAT ACTIVATED: {code} ---")
        
        if code == "INSTANT_BUILD":
            for b in args:
                k.buildings.append(b)
                print(f"God Mode: Built {b.name}")
                
        elif code == "SET_RESOURCES":
            if 'food' in kwargs: k.resources.food = kwargs['food']
            if 'gold' in kwargs: k.resources.gold = kwargs['gold']
            if 'wood' in kwargs: k.resources.wood = kwargs['wood']
            print("God Mode: Resources Updated.")
            
        elif code == "ADD_POP": # NEW CHEAT
            if 'amount' in kwargs:
                k.population += kwargs['amount']
                print(f"God Mode: Population increased by {kwargs['amount']}")

        elif code == "SKIP_TIME": # NEW CHEAT
            days = kwargs.get('days', 5) # Default to 5 days
            print(f"God Mode: Warping {days} days into the future...")
            for _ in range(days):
                k.advanceday()
                time.sleep(0.1) # Fast forward animation

# --- MAIN LOOP ---
def main():
    print(f"{p.cyan}Welcome to Kingdom Builder v2.0!")
    name = input("Enter Kingdom Name: ")
    my_kingdom = kingdom(name, 10, []) 

    running = True
    while running:
        print(my_kingdom)
        
        print(f"{p.cyan}--- ACTIONS ---")
        print("[1] Advance Day")
        print(f"[2] Build Farm (Cost: {farmfoodcost}F {farmgoldcost}G {farmwoodcost}W)")
        print(f"[3] Build Mine (Cost: {minefoodcost}F {minegoldcost}G {minewoodcost}W)")
        print(f"[4] Build Woodcutter (Cost: {woodcutterfoodcost}F {woodcuttergoldcost}G {woodcutterwoodcost}W)")
        print(f"{p.yellow}[5] CHEAT: Resources (Motherlode)")
        print(f"{p.yellow}[6] CHEAT: Add 100 People")
        print(f"{p.yellow}[7] CHEAT: Warp 10 Days")
        print("[Q] Quit")
        
        choice = input(f"{p.yellow}Select Action: ").upper()
        
        if choice == '1':
            my_kingdom.advanceday()
        elif choice == '2':
            my_kingdom.addbuilding(farm("Farm", 1))
        elif choice == '3':
            my_kingdom.addbuilding(mine("Mine", 1))
        elif choice == '4':
            my_kingdom.addbuilding(woodcutter("Woodcutter", 1))
            
        # CHEAT MENUS
        elif choice == '5':
            Cheats.run(my_kingdom, "SET_RESOURCES", food=500, gold=500, wood=500)
        elif choice == '6':
            Cheats.run(my_kingdom, "ADD_POP", amount=100)
        elif choice == '7':
            Cheats.run(my_kingdom, "SKIP_TIME", days=10)
            
        elif choice == 'Q':
            running = False
        else:
            print(f"{p.red}Invalid Option!")

if __name__ == "__main__":
    main()