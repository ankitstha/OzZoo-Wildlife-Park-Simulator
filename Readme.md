# OzZoo - Wildlife Park Simulator

OzZoo is a Python command-line simulation game where the player manages a wildlife park by caring for animals, organising enclosures, managing food, adjusting ticket prices, and progressing through each day.

## Features

- Manage multiple Australian animal species, including Koala, Kangaroo, Wombat, Platypus, Emu, and Wedge-Tailed Eagle.
- Track animal condition through health, hunger, happiness, and alive status.
- Place animals into habitat-specific enclosures such as forest, grassland, burrow, wetland, savanna, and aviary.
- Feed animals and monitor their wellbeing over time.
- Interact with the zoo through a menu-driven command-line interface.
- Handle invalid actions with custom exception classes.

## Project Structure

- `main.py` - Entry point for the command-line interface and menu system.
- `zoo.py` - Core zoo management logic.
- `animals.py` - Animal hierarchy, species definitions, and animal factory.
- `enclosure.py` - Enclosure model and enclosure management rules.
- `visitor.py` - Visitor-related behaviour.
- `exception.py` - Custom exception classes used throughout the project.

## Animal Types

The project currently includes the following animal species:

- Koala
- Kangaroo
- Wombat
- Platypus
- Emu
- Wedge-Tailed Eagle

## Technologies Used

- Python
- Object-oriented programming
- Abstract base classes
- Inheritance
- Exception handling
- Factory pattern

## Getting Started

### Prerequisites

Make sure Python 3 is installed on your system.

### Run the Program

1. Clone this repository:
   ```bash
   git clone https://github.com/ankitstha/OzZoo-Wildlife-Park-Simulator.git
   ```

2. Open the project folder:
   ```bash
   cd OzZoo-Wildlife-Park-Simulator
   ```

3. Run the program:
   ```bash
   python main.py
   ```

## How It Works

The player manages the zoo through a text-based menu. During gameplay, the user can manage animals and enclosures, feed animals, adjust ticket pricing, use care-related features, and advance the simulation day by day.

## Design Overview

This project applies object-oriented programming principles:

- **Abstraction** through the base `Animal` class.
- **Inheritance** through `Mammal`, `Bird`, and the individual animal subclasses.
- **Encapsulation** by storing animal and zoo state inside class attributes and methods.
- **Factory pattern** through `AnimalFactory`, which creates animal objects from species names.

## Example Species Data

| Animal | Habitat | Preferred Food |
|---|---|---|
| Koala | Forest | Eucalyptus |
| Kangaroo | Grassland | Grass |
| Wombat | Burrow | Roots |
| Platypus | Wetland | Shrimp |
| Emu | Savanna | Seeds |
| Wedge-Tailed Eagle | Aviary | Meat |

## Purpose

This project was developed as a Python simulation assignment to demonstrate class design, inheritance, modular programming, and exception handling in a practical game-based system.

## Future Improvements

- Add save/load game support.
- Add more animal species.
- Improve balancing for zoo economy and animal care.
- Add richer visitor and event systems.

## License

This project is for educational purposes unless otherwise stated.