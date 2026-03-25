"""CLI entry point with ASCII art borders."""

from zoo import Zoo
from enclosure import Enclosure
from exception import InsufficientFundsError, EnclosureFullError

BORDER = "=" * 60

def print_header(day: int, funds: float):
    print(f"\n{BORDER}")
    print(f"  🦘 OzZoo  |  Day {day}  |  Funds: ${funds:,.2f}")
    print(BORDER)

def print_status(zoo: Zoo):
    print("\n📋 ENCLOSURES:")
    for enc in zoo.enclosures:
        print(f"  {enc}")
        for animal in enc.animals:
            print(f"    └─ {animal}")

def print_menu():
    print(f"\n{'-'*40}")
    print("  [1] Advance to next day")
    print("  [2] Buy food")
    print("  [3] Clean an enclosure")
    print("  [4] View food inventory")
    print("  [5] Buy a new animal")
    print("  [Q] Quit")
    print(f"{'-'*40}")

def setup_zoo(zoo):
    from animals import AnimalFactory
    from enclosure import Enclosure

    # List of animals to add (species, name)
    animal_list = [
        ("kangaroo", "Kanga"),
        ("kangaroo", "Boomer"),
        ("wombat", "Digger"),
        ("koala", "Sleepy"),
        ("emu", "Dash"),
        ("platypus", "Perry"),
    ]

    # Store enclosures by habitat
    enclosures = {}

    for species, name in animal_list:
        # 🔥 Get correct habitat automatically
        habitat = AnimalFactory.get_habitat(species)

        # If enclosure for this habitat doesn't exist → create it
        if habitat not in enclosures:
            enclosure = Enclosure(f"{habitat.title()} Habitat", habitat, 5)
            zoo.add_enclosure(enclosure)
            enclosures[habitat] = enclosure

        # Add animal to correct enclosure
        zoo.buy_animal(species, name, enclosures[habitat], cost=0)

def main():
    zoo = Zoo()
    setup_zoo(zoo)

    print(f"\n{'*'*60}")
    print("  Welcome to OzZoo! G'day, Manager!")
    print(f"{'*'*60}")

    while not zoo.game_over:
        print_header(zoo.day, zoo.funds)
        print_status(zoo)
        print_menu()

        choice = input("  Enter choice: ").strip().lower()

        if choice == "1":
            result = zoo.advance_day()
            print(f"\n📅 Day {result['day']} complete!")
            for msg in result["log"]:
                print(f"  {msg}")

        elif choice == "2":
            food_type = input("  Food type (eucalyptus/grass/roots/shrimp/seeds/meat): ").strip()
            try:
                amount = float(input("  Amount to buy: "))
                zoo.buy_food(food_type, amount)
                print(f"  ✅ Purchased {amount}x {food_type}.")
            except (InsufficientFundsError, KeyError) as e:
                print(f"  ❌ {e}")

        elif choice == "3":
            for i, enc in enumerate(zoo.enclosures):
                print(f"  [{i}] {enc.name}")
            try:
                idx = int(input("  Enclosure number: "))
                zoo.enclosures[idx].clean()
                print("  ✅ Enclosure cleaned!")
            except (IndexError, ValueError):
                print("  ❌ Invalid selection.")

        elif choice == "4":
            print("\n🥦 Food Inventory:")
            for k, v in zoo._food.status().items():
                print(f"  {k}: {v:.1f} units")

        elif choice == "5":
            species = input("  Species: ").strip()
            name    = input("  Name: ").strip()
            for i, enc in enumerate(zoo.enclosures):
                print(f"  [{i}] {enc.name}")
            try:
                idx = int(input("  Place in enclosure #: "))
                zoo.buy_animal(species, name, zoo.enclosures[idx], cost=500.0)
                print(f"  ✅ {name} the {species} added!")
            except (InsufficientFundsError, EnclosureFullError, ValueError) as e:
                print(f"  ❌ {e}")

        elif choice == "q":
            print("\n  Thanks for playing OzZoo! 🦘")
            break

    if zoo.game_over:
        print(f"\n{'!'*60}")
        print(f"  GAME OVER: {zoo._game_over_reason}")
        print(f"  You survived {zoo.day} days!")
        print(f"{'!'*60}")

if __name__ == "__main__":
    main()