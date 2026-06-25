🎮 Video Game Collection Manager

A lightweight, dependency-free Command Line Interface (CLI) tool written in Python to manage and track your video game library. It automatically saves your collection in a local JSON file and allows you to export your list into a beautiful, responsive, and sortable HTML webpage.

✨ Features

No External Dependencies: Built entirely with Python's standard library.

Auto-Save & UTF-8 Support: Your collection is automatically saved to collection.json after every change. Handles special characters and accents perfectly.

Full CRUD Operations:

➕ Add games with Title, Platform, Genre, and Release Year.

📋 List your entire collection.

🔍 Search games dynamically by Title, Platform, or Genre.

📝 Modify existing games selectively (keeps current values if left blank).

🗑️ Delete games by their listed line number.

Robustness: Auto-detects and gracefully handles missing or corrupted JSON files.

Stats Dashboard: Displays total games, unique platforms, and your newest game's release year.

🌐 HTML Export: Generates a modern, responsive, and standalone collection.html file featuring:

Alternating row colors (zebra striping).

Interactive table headers—click any column (Title, Platform, Genre, Year) to sort dynamically (powered by native, offline JavaScript).

🚀 How to Run

Prerequisites

You only need Python 3.6+ installed on your system.

Installation

Clone this repository:

git clone [https://github.com/T209995/game-collection-manager.git](https://github.com/T209995/game-collection-manager.git)
cd game-collection-manager


Run the script:

python collection.py


📂 File Structure

collection.py — The main executable Python script.

collection.json — Auto-generated database storing your games.

collection.html — Auto-generated, responsive interactive webpage.

🎨 Interactive HTML Export Preview

The exported HTML page is fully self-contained and works 100% offline. You can click on the column headers to sort your collection instantly:

Text sorting handles French accents and special casing seamlessly.

Year sorting is naturally ordered chronologically.

📝 License

This project is open-source and available under the MIT License.
