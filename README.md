# 🎲 RPG Companion — RPG Assistant for D100 Dungeon & Others

Cross-platform role-playing game assistant developed in **Python**, with:
- a graphical interface in **PySide6 / Qt6**, 
- RPG systems stored in **SQLite** database, 
- testing with **pytest / pytest-qt**,
- executable generation with **PyInstaller** (tested under Windows only).

The project is currently primarily focused on **D100 Dungeon**, with an architecture that allows for expansion to other game systems.

## Project Objectives

* Assistant for solo and traditional role-playing games
* Automatic tabletop rolls:
    * Weapons
    * Armor
    * Treasures
    * Encounters (creatures / NPCs)
* Storage of each game system in a **SQLite 3** database
* Modern graphical interface with **Qt6**

## Planned Developments

* Support for other systems:
    * Four Against Darkness
    * Advanced Dungeons & Dragons
* Player character (PC) generation
* Non-player character (NPC) generation
* Rules, tables, and datas entirely driven by SQL database

## Technical Stack

* **Python 3.13+**
* **PySide6 6.10+ / Qt6**
* **SQLAlchemy 2.x+**
* **SQLite 3**
* **pytest 9.x+**
* **pytest-qt 4.5+**
* **PyInstaller 6.17+**
* **invoke 2.2+**

## Version control system
* **Jujutsu (jj) + Git**

## Project Structure

```bash
rpg-companion/
│
├── build/
├── dist/
├── htmlcov/
├── src/
│   ├── __tests__/
|   │   └── __unit__/
│   ├── resources/
│   ├── rpg_companion/
|   │   ├── app/
|   │   ├── assets/
|   |   │   ├── icons/
|   |   │   └── images/
|   │   ├── config/
|   │   ├── data/
|   │   ├── db/
|   │   ├── i18n/
|   │   ├── models/
|   │   ├── repos/
|   │   ├── services/
|   │   ├── types/
|   │   ├── ui/
|   |   │   ├── dialogs/
|   |   │   ├── views/
|   |   │   └── widgets/
|   │   ├── utils/
|   │   └── version/
│   ├── scripts/
│   └── main.py
├── pyproject.toml
├── CHANGELOG.md
├── LICENSE
├── README.md
└── requirements.txt
```

## Installation & Configuration

### 1. Clone the project

```bash
jj git clone https://github.com/ultra-sonic-28/rpg-companion
cd rpg-companion
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate # Linux/Mac
venv\Scripts\activate # Windows
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

*(or via `pyproject.toml` if you are using Poetry or PDM)*

### 4. Run the application

```bash
invoke rpg
```

## Run the tests

```bash
invoke test
```

## Generate an executable

```bash
invoke build
```

The binary will be available in the folder `dist/`.

## Game system management

Each RPG system has:

* Its own SQL tables
* Its own business rules
* Its own generators

This allows for clean and independent extension.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Project Status

✅ In active development — architecture being finalized.

## Contribution

Contributions are welcome:

* Fork
* Branch
* Commit with clear messages
* Pull Request

## Author

Project developed by **ultra-sonic-28**