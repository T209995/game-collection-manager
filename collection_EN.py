import json
import os
import html

FICHIER_COLLECTION = 'collection.json'
FICHIER_HTML = 'collection.html'

def effacer_ecran():
    """
    Clears the terminal screen in a portable way (Windows / Unix).
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def charger_collection():
    """
    Loads the collection from the JSON file.
    Handles missing files or JSON corruption gracefully.
    """
    if not os.path.exists(FICHIER_COLLECTION):
        return []
    
    try:
        with open(FICHIER_COLLECTION, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        # Security: warns the user and starts from scratch if JSON is invalid
        print("\n⚠️ Corrupted file, starting from scratch.")
        return []

def sauvegarder_collection(collection):
    """
    Saves the game list into the JSON file.
    Forces UTF-8 encoding to preserve special characters.
    """
    try:
        with open(FICHIER_COLLECTION, 'w', encoding='utf-8') as f:
            json.dump(collection, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"❌ Error during save: {e}")

def ajouter_jeu(collection):
    """
    Asks the user for details and adds a new game to the collection.
    """
    print("\n--- ➕ Add a Game ---")
    titre = input("Game Title: ").strip()
    plateforme = input("Platform (e.g., PS5, PC, Switch): ").strip()
    annee = input("Release Year: ").strip()
    genre = input("Genre (e.g., RPG, Action): ").strip()
    
    if titre and plateforme and annee and genre:
        nouveau_jeu = {
            "titre": titre,
            "plateforme": plateforme,
            "annee": annee,
            "genre": genre
        }
        collection.append(nouveau_jeu)
        sauvegarder_collection(collection)
        print("✅ Game added successfully!")
    else:
        print("❌ Error: All fields are required.")

def lister_jeux(collection):
    """
    Displays all games in the collection with their line numbers.
    Uses .get() to prevent crashes if older games lack some keys.
    """
    print("\n--- 📋 My Collection ---")
    if not collection:
        print("Your collection is currently empty.")
        return False
    
    for index, jeu in enumerate(collection):
        titre = jeu.get('titre', 'Untitled')
        plateforme = jeu.get('plateforme', 'Unknown')
        genre = jeu.get('genre', 'Unspecified')
        annee = jeu.get('annee', 'Unknown')
        print(f"[{index + 1}] {titre} - {plateforme} - {genre} ({annee})")
    return True

def rechercher_jeu(collection):
    """
    Provides a sub-menu to search games by Title, Platform, or Genre.
    """
    print("\n--- 🔍 Search Games ---")
    if not collection:
        print("Your collection is empty, search unavailable.")
        return

    print("1. Search by Title")
    print("2. Search by Platform")
    print("3. Search by Genre")
    
    choix = input("\n👉 Choose a search option (1-3): ").strip()
    
    if choix == '1':
        cle = 'titre'
        label = "title"
    elif choix == '2':
        cle = 'plateforme'
        label = "platform"
    elif choix == '3':
        cle = 'genre'
        label = "genre"
    else:
        print("❌ Invalid option. Returning to main menu.")
        return
        
    mot_cle = input(f"Enter keyword for {label}: ").strip().lower()
    
    resultats = [jeu for jeu in collection if mot_cle in jeu.get(cle, '').lower()]
    
    if resultats:
        print(f"\n🎯 Search Results ({len(resultats)} found):")
        for jeu in resultats:
            titre = jeu.get('titre', 'Untitled')
            plateforme = jeu.get('plateforme', 'Unknown')
            genre = jeu.get('genre', 'Unspecified')
            annee = jeu.get('annee', 'Unknown')
            print(f"- {titre} - {plateforme} - {genre} ({annee})")
    else:
        print(f"🤷 No games found with that keyword in {label}.")

def modifier_jeu(collection):
    """
    Displays the list and allows selective editing of a game's details.
    Leaving a field blank preserves its current value.
    """
    print("\n--- 📝 Edit a Game ---")
    if not lister_jeux(collection):
        return
        
    choix = input("\nEnter the number of the game to edit (or 'c' to cancel): ").strip()
    
    if choix.lower() == 'c':
        print("Action canceled.")
        return
        
    try:
        index = int(choix) - 1
        if 0 <= index < len(collection):
            jeu = collection[index]
            print(f"\nEditing: {jeu.get('titre', 'Untitled')}")
            print("(Leave blank to keep current value)")
            
            nouveau_titre = input(f"New title [{jeu.get('titre')}]: ").strip()
            nouvelle_plateforme = input(f"New platform [{jeu.get('plateforme')}]: ").strip()
            nouvelle_annee = input(f"New year [{jeu.get('annee')}]: ").strip()
            nouveau_genre = input(f"New genre [{jeu.get('genre')}]: ").strip()
            
            # Selective update
            if nouveau_titre:
                jeu['titre'] = nouveau_titre
            if nouvelle_plateforme:
                jeu['plateforme'] = nouvelle_plateforme
            if nouvelle_annee:
                jeu['annee'] = nouvelle_annee
            if nouveau_genre:
                jeu['genre'] = nouveau_genre
                
            sauvegarder_collection(collection)
            print("✅ Game updated successfully!")
        else:
            print("❌ Error: Invalid number.")
    except ValueError:
        print("❌ Error: Please enter a valid number.")

def afficher_statistiques(collection):
    """
    Displays key statistics of the collection:
    - Total number of games
    - Unique platforms count
    - Most recent release year
    """
    print("\n--- 📊 Collection Statistics ---")
    if not collection:
        print("Your collection is empty. No statistics to display.")
        return

    total_jeux = len(collection)
    
    # Count unique platforms (case-insensitive and trimmed)
    plateformes = set(jeu.get('plateforme', '').strip().lower() for jeu in collection if jeu.get('plateforme'))
    nb_plateformes = len(plateformes)
    
    # Find the most recent release year (only digital strings)
    annees_valides = []
    for jeu in collection:
        annee_str = str(jeu.get('annee', '')).strip()
        if annee_str.isdigit():
            annees_valides.append(int(annee_str))
            
    annee_max = max(annees_valides) if annees_valides else "Unknown"
    
    print(f"📈 Total games: {total_jeux}")
    print(f"🎮 Unique platforms: {nb_plateformes}")
    print(f"📅 Newest game release: {annee_max}")

def supprimer_jeu(collection):
    """
    Displays the list and deletes a game by its line number.
    """
    print("\n--- 🗑️ Delete a Game ---")
    if not lister_jeux(collection):
        return
    
    choix = input("\nEnter the number of the game to delete (or 'c' to cancel): ").strip()
    
    if choix.lower() == 'c':
        print("Action canceled.")
        return
        
    try:
        index = int(choix) - 1
        if 0 <= index < len(collection):
            jeu_supprime = collection.pop(index)
            sauvegarder_collection(collection)
            print(f"✅ '{jeu_supprime.get('titre', 'Untitled')}' has been removed!")
        else:
            print("❌ Error: Invalid number.")
    except ValueError:
        print("❌ Error: Please enter a valid number.")

def exporter_html(collection):
    """
    Generates an offline-ready, standalone HTML file with CSS and JS column sorting.
    """
    print("\n--- 🌐 Export to HTML ---")
    total_jeux = len(collection)
    
    # Building table rows with escaped HTML characters
    lignes_tableau = ""
    if not collection:
        lignes_tableau = """
        <tr>
            <td colspan="4" class="no-games">Your collection is empty.</td>
        </tr>
        """
    else:
        for jeu in collection:
            titre = html.escape(str(jeu.get('titre', 'Untitled')))
            plateforme = html.escape(str(jeu.get('plateforme', 'Unknown')))
            genre = html.escape(str(jeu.get('genre', 'Unspecified')))
            annee = html.escape(str(jeu.get('annee', 'Unknown')))
            
            lignes_tableau += f"""
            <tr>
                <td><strong>{titre}</strong></td>
                <td>{plateforme}</td>
                <td>{genre}</td>
                <td>{annee}</td>
            </tr>\n"""

    # Self-contained HTML template with UI Styles and Sorting JS
    contenu_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Video Game Collection</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f4f6f9;
            color: #333333;
            margin: 0;
            padding: 30px 15px;
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background-color: #ffffff;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        }}
        header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 3px solid #3498db;
            padding-bottom: 15px;
            margin-bottom: 25px;
            flex-wrap: wrap;
            gap: 15px;
        }}
        h1 {{
            margin: 0;
            color: #2c3e50;
            font-size: 28px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .badge-stats {{
            background-color: #e8f4fd;
            color: #2980b9;
            border: 1px solid #3498db;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 15px;
        }}
        .info-tri {{
            font-size: 13px;
            color: #7f8c8d;
            margin-bottom: 10px;
            font-style: italic;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 5px;
        }}
        th, td {{
            padding: 14px 18px;
            text-align: left;
            border-bottom: 1px solid #e0e0e0;
        }}
        th {{
            background-color: #34495e;
            color: #ffffff;
            text-transform: uppercase;
            font-size: 13px;
            letter-spacing: 0.8px;
            font-weight: 600;
            position: relative;
            cursor: pointer;
            user-select: none;
            transition: background-color 0.2s ease;
        }}
        th:hover {{
            background-color: #2c3e50;
        }}
        /* Sort indicators */
        th::after {{
            content: ' ↕';
            font-size: 11px;
            color: rgba(255, 255, 255, 0.5);
            position: absolute;
            right: 12px;
        }}
        th.th-sort-asc::after {{
            content: ' ▲';
            color: #3498db;
        }}
        th.th-sort-desc::after {{
            content: ' ▼';
            color: #3498db;
        }}
        tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        tr:hover {{
            background-color: #f1f4f6;
            transition: background-color 0.2s ease;
        }}
        .no-games {{
            text-align: center;
            padding: 40px;
            color: #7f8c8d;
            font-style: italic;
        }}
        @media (max-width: 600px) {{
            header {{
                flex-direction: column;
                align-items: flex-start;
            }}
            th, td {{
                padding: 10px;
                font-size: 14px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🎮 My Video Game Collection</h1>
            <div class="badge-stats">
                📊 Total: {total_jeux} {"game" if total_jeux <= 1 else "games"}
            </div>
        </header>
        <div class="info-tri">💡 Click on column headers (Title, Platform, etc.) to sort the list.</div>
        <table>
            <thead>
                <tr>
                    <th id="col-titre">Title</th>
                    <th id="col-plateforme">Platform</th>
                    <th id="col-genre">Genre</th>
                    <th id="col-annee">Year</th>
                </tr>
            </thead>
            <tbody>
                {lignes_tableau}
            </tbody>
        </table>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', () => {{
            const table = document.querySelector('table');
            const headers = table.querySelectorAll('th');
            const tbody = table.querySelector('tbody');
            const rows = Array.from(tbody.querySelectorAll('tr'));

            if (rows.length === 1 && rows[0].querySelector('.no-games')) return;

            headers.forEach((header, index) => {{
                header.addEventListener('click', () => {{
                    const isAscending = header.classList.contains('th-sort-asc');
                    
                    headers.forEach(h => h.classList.remove('th-sort-asc', 'th-sort-desc'));
                    
                    const direction = isAscending ? -1 : 1;
                    
                    rows.sort((rowA, rowB) => {{
                        const cellA = rowA.children[index].textContent.trim();
                        const cellB = rowB.children[index].textContent.trim();
                        
                        // Numerical sort for Year column (index 3)
                        if (index === 3) {{
                            const numA = parseInt(cellA, 10);
                            const numB = parseInt(cellB, 10);
                            if (!isNaN(numA) && !isNaN(numB)) {{
                                return (numA - numB) * direction;
                            }}
                        }}
                        
                        // Alphabetical sort (handling accents cleanly)
                        return cellA.localeCompare(cellB, undefined, {{ sensitivity: 'base' }}) * direction;
                    }});
                    
                    if (isAscending) {{
                        header.classList.add('th-sort-desc');
                    }} else {{
                        header.classList.add('th-sort-asc');
                    }}
                    
                    rows.forEach(row => tbody.appendChild(row));
                }});
            }});
        }});
    </script>
</body>
</html>
"""

    try:
        with open(FICHIER_HTML, 'w', encoding='utf-8') as f:
            f.write(contenu_html)
        print(f"✅ HTML file exported successfully! ({FICHIER_HTML})")
    except Exception as e:
        print(f"❌ Error during HTML export: {e}")

def main():
    """
    Main interactive loop.
    """
    effacer_ecran()
    collection = charger_collection()
    
    while True:
        print("\n" + "="*30)
        print("🎮 VIDEO GAME COLLECTION MANAGER")
        print("="*30)
        print("1. Add a game")
        print("2. List my collection")
        print("3. Search for a game")
        print("4. Modify a game")
        print("5. Delete a game")
        print("6. Show statistics")
        print("7. Export collection to HTML")
        print("8. Exit")
        print("="*30)
        
        choix = input("👉 Choose an option (1-8): ").strip()
        
        if choix == '1':
            ajouter_jeu(collection)
        elif choix == '2':
            lister_jeux(collection)
        elif choix == '3':
            rechercher_jeu(collection)
        elif choix == '4':
            modifier_jeu(collection)
        elif choix == '5':
            supprimer_jeu(collection)
        elif choix == '6':
            afficher_statistiques(collection)
        elif choix == '7':
            exporter_html(collection)
        elif choix == '8':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Unrecognized option. Please try again.")

if __name__ == "__main__":
    main()
