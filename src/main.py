"""CLI entry point for OzZoo."""

import os
import platform
from zoo import Zoo
from enclosure import Enclosure
from exception import (
    InsufficientFundsError, EnclosureFullError,
    IncompatibleSpeciesError, InsufficientFoodError, AnimalNotFoundError
)

BORDER = "=" * 60
THIN   = "-" * 60


def clear():
    """Clear the terminal screen (Windows + Unix)."""
    os.system("cls" if platform.system() == "Windows" else "clear")


def print_header(zoo: Zoo):
    animals = zoo.all_animals()
    avg_health = (sum(a.health for a in animals) / len(animals)) if animals else 0.0
    avg_hunger = (sum(a.hunger for a in animals) / len(animals)) if animals else 0.0

    print(f"\n{BORDER}")
    print(f"  🦘  OzZoo — Wildlife Park Simulator  🐨")
    print(THIN)
    print(f"  📅 Day        : {zoo.day}")
    print(f"  💰 Funds      : ${zoo.funds:,.2f}")
    print(f"  🐾 Animals    : {len(animals)}")
    print(f"  🏗 Enclosures : {len(zoo.enclosures)}")
    print(f"  ❤️  Avg Health : {avg_health:.1f}%")
    print(f"  🍽 Avg Hunger : {avg_hunger:.1f}%")
    print(BORDER)


def print_menu():
    print(f"\n{THIN}")
    print("  [1] View Animals")
    print("  [2] View Enclosures")
    print("  [3] View Food Stock")
    print("  [4] Buy Food")
    print("  [5] Buy Animal")
    print("  [6] Feed an Animal")
    print("  [7] Vet an Animal")
    print("  [8] Clean an Enclosure")
    print("  [T] Set Ticket Price")
    print("  [N] Next Day  ▶")
    print("  [Q] Quit")
    print(THIN)


def setup_zoo(zoo: Zoo):
    from animals import AnimalFactory

    animal_list = [
        ("kangaroo",           "Kanga"),
        ("kangaroo",           "Boomer"),
        ("wombat",             "Digger"),
        ("koala",              "Sleepy"),
        ("emu",                "Dash"),
        ("platypus",           "Perry"),
        ("wedge-tailed eagle", "Aquila"),
    ]

    enclosures = {}
    for species, name in animal_list:
        habitat = AnimalFactory.get_habitat(species)
        if habitat not in enclosures:
            enc = Enclosure(f"{habitat.title()} Habitat", habitat, 5)
            zoo.add_enclosure(enc)
            enclosures[habitat] = enc
        zoo.buy_animal(species, name, enclosures[habitat], cost=0)


def main():
    zoo = Zoo()
    setup_zoo(zoo)

    while not zoo.game_over:
        clear()
        print_header(zoo)
        print_menu()
        choice = input("  Choose an action: ").strip().lower()

        if choice == "1":
            clear()
            print(f"\n{BORDER}")
            print("  🐾 ANIMALS")
            print(THIN)
            for enc in zoo.enclosures:
                print(f"\n  🏠 {enc.name}")
                for a in enc.animals:
                    print(f"    └─ {a}")
            input(f"\n  Press Enter to return...")

        elif choice == "2":
            clear()
            print(f"\n{BORDER}")
            print("  🏗 ENCLOSURES")
            print(THIN)
            for enc in zoo.enclosures:
                print(f"  {enc}")
            input(f"\n  Press Enter to return...")

        elif choice == "3":
            clear()
            print(f"\n{BORDER}")
            print("  🥦 FOOD STOCK")
            print(THIN)
            for k, v in zoo._food.status().items():
                print(f"  {k:<15}: {v:.1f} units")
            input(f"\n  Press Enter to return...")

        elif choice == "4":
            clear()
            print(f"\n{BORDER}")
            print("  🛒 BUY FOOD")
            print(THIN)
            print("  Types: eucalyptus / grass / roots / shrimp / seeds / meat")
            food_type = input("  Food type : ").strip().lower()
            try:
                amount = float(input("  Amount    : "))
                zoo.buy_food(food_type, amount)
                print(f"  ✅ Purchased {amount}x {food_type}.")
            except (InsufficientFundsError, KeyError, ValueError) as e:
                print(f"  ❌ {e}")
            input("\n  Press Enter to return...")

        elif choice == "5":
            clear()
            print(f"\n{BORDER}")
            print("  🐨 BUY ANIMAL")
            print(THIN)
            print("  Species: koala / kangaroo / wombat / platypus / emu / wedge-tailed eagle")
            species = input("  Species    : ").strip().lower()
            name    = input("  Name       : ").strip()
            for i, enc in enumerate(zoo.enclosures):
                print(f"  [{i}] {enc.name}")
            try:
                idx = int(input("  Enclosure #: "))
                zoo.buy_animal(species, name, zoo.enclosures[idx], cost=500.0)
                print(f"  ✅ {name} the {species} added!")
            except (InsufficientFundsError, EnclosureFullError, IncompatibleSpeciesError, ValueError) as e:
                print(f"  ❌ {e}")
            input("\n  Press Enter to return...")

        elif choice == "6":
            clear()
            print(f"\n{BORDER}")
            print("  🍽 FEED ANIMAL")
            print(THIN)
            for enc in zoo.enclosures:
                for a in enc.animals:
                    print(f"  🐾 {a.name:<14} Hunger: {a.hunger:.0f}")
            animal_name = input("\n  Animal name: ").strip()
            try:
                msg = zoo.feed_animal(animal_name)
                print(f"  ✅ {msg}")
            except (AnimalNotFoundError, InsufficientFoodError) as e:
                print(f"  ❌ {e}")
            input("\n  Press Enter to return...")

        elif choice == "7":
            clear()
            print(f"\n{BORDER}")
            print("  🩺 VET ANIMAL  (costs $150)")
            print(THIN)
            for enc in zoo.enclosures:
                for a in enc.animals:
                    print(f"  🐾 {a.name:<14} HP: {a.health:.0f}")
            animal_name = input("\n  Animal name: ").strip()
            try:
                msg = zoo.vet_animal(animal_name)
                print(f"  ✅ {msg}")
            except (AnimalNotFoundError, InsufficientFundsError) as e:
                print(f"  ❌ {e}")
            input("\n  Press Enter to return...")

        elif choice == "8":
            clear()
            print(f"\n{BORDER}")
            print("  🧹 CLEAN ENCLOSURE")
            print(THIN)
            for i, enc in enumerate(zoo.enclosures):
                print(f"  [{i}] {enc.name}  — Cleanliness: {enc.get_cleanliness():.0f}%")
            try:
                idx = int(input("  Enclosure #: "))
                zoo.enclosures[idx].clean()
                print("  ✅ Enclosure cleaned!")
            except (IndexError, ValueError):
                print("  ❌ Invalid selection.")
            input("\n  Press Enter to return...")

        elif choice == "t":
            clear()
            print(f"\n{BORDER}")
            print("  🎟 SET TICKET PRICE")
            print(THIN)
            print(f"  Current price: ${zoo.ticket_price}")
            try:
                price = float(input("  New price ($): "))
                zoo.ticket_price = price
                print(f"  ✅ Ticket price set to ${price:.2f}")
            except ValueError:
                print("  ❌ Invalid price.")
            input("\n  Press Enter to return...")

        elif choice == "n":
            clear()
            result = zoo.advance_day()
            print(f"\n{BORDER}")
            print(f"  📅 DAY {result['day']} REPORT")
            print(THIN)
            print(f"  💰 Funds: ${result['funds']:,.2f}")
            print(f"\n  📋 Events:")
            for msg in result["log"]:
                print(f"    {msg}")
            input("\n  Press Enter to continue...")

        elif choice == "q":
            clear()
            print(f"\n  Thanks for playing OzZoo! 🦘\n")
            break

    if zoo.game_over:
        clear()
        print(f"\n{'!' * 60}")
        print(f"  GAME OVER: {zoo._game_over_reason}")
        print(f"  You survived {zoo.day} days!")
        print(f"{'!' * 60}\n")


if __name__ == "__main__":
    main()