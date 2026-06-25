import json
import os
import html

FICHIER_COLLECTION = 'collection.json'
FICHIER_HTML = 'collection.html'

def effacer_ecran():
    """
    Efface l'invite de commande de manière portable (Windows / Unix).
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def charger_collection():
    """
    Charge la collection depuis le fichier JSON.
    Gère l'absence du fichier ou sa corruption.
    """
    if not os.path.exists(FICHIER_COLLECTION):
        return []
    
    try:
        with open(FICHIER_COLLECTION, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        # Sécurité : on avertit et on repart de zéro si le JSON est invalide
        print("\n⚠️ Fichier corrompu, on part de zéro.")
        return []

def sauvegarder_collection(collection):
    """
    Sauvegarde la liste des jeux dans le fichier JSON.
    Force l'UTF-8 pour conserver les caractères spéciaux (accents, etc.).
    """
    try:
        with open(FICHIER_COLLECTION, 'w', encoding='utf-8') as f:
            json.dump(collection, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde : {e}")

def ajouter_jeu(collection):
    """
    Demande les infos à l'utilisateur et ajoute un nouveau jeu à la liste.
    """
    print("\n--- ➕ Ajouter un jeu ---")
    titre = input("Titre du jeu : ").strip()
    plateforme = input("Plateforme (ex: PS5, PC, Switch) : ").strip()
    annee = input("Année de sortie : ").strip()
    genre = input("Genre (ex: RPG, Action) : ").strip()
    
    if titre and plateforme and annee and genre:
        nouveau_jeu = {
            "titre": titre,
            "plateforme": plateforme,
            "annee": annee,
            "genre": genre
        }
        collection.append(nouveau_jeu)
        sauvegarder_collection(collection)
        print("✅ Jeu ajouté avec succès !")
    else:
        print("❌ Erreur : Tous les champs doivent être remplis.")

def lister_jeux(collection):
    """
    Affiche tous les jeux de la collection avec leur numéro de ligne.
    Utilise .get() pour éviter les crashs si d'anciens jeux n'ont pas de genre.
    """
    print("\n--- 📋 Ma Collection ---")
    if not collection:
        print("La collection est vide pour le moment.")
        return False
    
    for index, jeu in enumerate(collection):
        titre = jeu.get('titre', 'Sans titre')
        plateforme = jeu.get('plateforme', 'Inconnue')
        genre = jeu.get('genre', 'Non spécifié')
        annee = jeu.get('annee', 'Inconnue')
        print(f"[{index + 1}] {titre} - {plateforme} - {genre} ({annee})")
    return True

def rechercher_jeu(collection):
    """
    Propose un sous-menu pour rechercher un jeu par titre, plateforme ou genre.
    """
    print("\n--- 🔍 Rechercher un jeu ---")
    if not collection:
        print("La collection est vide, aucune recherche possible.")
        return

    print("1. Rechercher par titre")
    print("2. Rechercher par plateforme")
    print("3. Rechercher par genre")
    
    choix = input("\n👉 Choisissez un type de recherche (1-3) : ").strip()
    
    if choix == '1':
        cle = 'titre'
        label = "titre"
    elif choix == '2':
        cle = 'plateforme'
        label = "plateforme"
    elif choix == '3':
        cle = 'genre'
        label = "genre"
    else:
        print("❌ Option invalide. Retour au menu principal.")
        return
        
    mot_cle = input(f"Entrez le mot-clé pour le {label} : ").strip().lower()
    
    resultats = [jeu for jeu in collection if mot_cle in jeu.get(cle, '').lower()]
    
    if resultats:
        print(f"\n🎯 Résultats de la recherche ({len(resultats)} trouvé(s)) :")
        for jeu in resultats:
            titre = jeu.get('titre', 'Sans titre')
            plateforme = jeu.get('plateforme', 'Inconnue')
            genre = jeu.get('genre', 'Non spécifié')
            annee = jeu.get('annee', 'Inconnue')
            print(f"- {titre} - {plateforme} - {genre} ({annee})")
    else:
        print(f"🤷 Aucun jeu trouvé avec ce mot-clé dans le {label}.")

def modifier_jeu(collection):
    """
    Affiche la liste complète et permet de modifier sélectivement un jeu.
    L'utilisateur valide chaque champ existant s'il le laisse vide.
    """
    print("\n--- 📝 Modifier un jeu ---")
    if not lister_jeux(collection):
        return
        
    choix = input("\nEntrez le numéro du jeu à modifier (ou 'a' pour annuler) : ").strip()
    
    if choix.lower() == 'a':
        print("Action annulée.")
        return
        
    try:
        index = int(choix) - 1
        if 0 <= index < len(collection):
            jeu = collection[index]
            print(f"\nModification de : {jeu.get('titre', 'Sans titre')}")
            print("(Laissez vide pour conserver la valeur actuelle)")
            
            nouveau_titre = input(f"Nouveau titre [{jeu.get('titre')}]: ").strip()
            nouvelle_plateforme = input(f"Nouvelle plateforme [{jeu.get('plateforme')}]: ").strip()
            nouvelle_annee = input(f"Nouvelle année [{jeu.get('annee')}]: ").strip()
            nouveau_genre = input(f"Nouveau genre [{jeu.get('genre')}]: ").strip()
            
            # Mise à jour sélective si l'utilisateur a saisi une valeur
            if nouveau_titre:
                jeu['titre'] = nouveau_titre
            if nouvelle_plateforme:
                jeu['plateforme'] = nouvelle_plateforme
            if nouvelle_annee:
                jeu['annee'] = nouvelle_annee
            if nouveau_genre:
                jeu['genre'] = nouveau_genre
                
            sauvegarder_collection(collection)
            print("✅ Jeu modifié avec succès !")
        else:
            print("❌ Erreur : Numéro invalide.")
    except ValueError:
        print("❌ Erreur : Veuillez entrer un nombre valide.")

def afficher_statistiques(collection):
    """
    Affiche les statistiques clés de la collection :
    - Nombre total de jeux
    - Nombre de plateformes distinctes
    - L'année de sortie la plus récente
    """
    print("\n--- 📊 Statistiques de la Collection ---")
    if not collection:
        print("La collection est vide. Aucune statistique à afficher.")
        return

    total_jeux = len(collection)
    
    # Compter les plateformes uniques (en ignorant la casse et les espaces superflus)
    plateformes = set(jeu.get('plateforme', '').strip().lower() for jeu in collection if jeu.get('plateforme'))
    nb_plateformes = len(plateformes)
    
    # Trouver l'année la plus récente (en s'assurant qu'elle est bien numérique)
    annees_valides = []
    for jeu in collection:
        annee_str = str(jeu.get('annee', '')).strip()
        if annee_str.isdigit():
            annees_valides.append(int(annee_str))
            
    annee_max = max(annees_valides) if annees_valides else "Inconnue"
    
    print(f"📈 Nombre total de jeux : {total_jeux}")
    print(f"🎮 Nombre de plateformes différentes : {nb_plateformes}")
    print(f"📅 Année la plus récente : {annee_max}")

def supprimer_jeu(collection):
    """
    Affiche la liste et permet de supprimer un jeu via son numéro de ligne.
    """
    print("\n--- 🗑️ Supprimer un jeu ---")
    if not lister_jeux(collection):
        return
    
    choix = input("\nEntrez le numéro du jeu à supprimer (ou 'a' pour annuler) : ").strip()
    
    if choix.lower() == 'a':
        print("Action annulée.")
        return
        
    try:
        index = int(choix) - 1
        if 0 <= index < len(collection):
            jeu_supprime = collection.pop(index)
            sauvegarder_collection(collection)
            print(f"✅ Le jeu '{jeu_supprime.get('titre', 'Sans titre')}' a été supprimé !")
        else:
            print("❌ Erreur : Numéro invalide.")
    except ValueError:
        print("❌ Erreur : Veuillez entrer un nombre valide.")

def exporter_html(collection):
    """
    Génère un fichier HTML autonome lisible hors-ligne avec style CSS embarqué
    et possibilité de trier dynamiquement les colonnes en JavaScript.
    """
    print("\n--- 🌐 Exporter en HTML ---")
    total_jeux = len(collection)
    
    # Construction des lignes du tableau en échappant les balises HTML sensibles
    lignes_tableau = ""
    if not collection:
        lignes_tableau = """
        <tr>
            <td colspan="4" class="no-games">La collection est vide pour le moment.</td>
        </tr>
        """
    else:
        for jeu in collection:
            titre = html.escape(str(jeu.get('titre', 'Sans titre')))
            plateforme = html.escape(str(jeu.get('plateforme', 'Inconnue')))
            genre = html.escape(str(jeu.get('genre', 'Non spécifié')))
            annee = html.escape(str(jeu.get('annee', 'Inconnue')))
            
            lignes_tableau += f"""
            <tr>
                <td><strong>{titre}</strong></td>
                <td>{plateforme}</td>
                <td>{genre}</td>
                <td>{annee}</td>
            </tr>\n"""

    # Template HTML autonome avec CSS et JavaScript de tri interactif
    contenu_html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ma Collection de Jeux Vidéo</title>
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
        /* Indicateurs de tri */
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
            <h1>🎮 Ma Collection de Jeux Vidéo</h1>
            <div class="badge-stats">
                📊 Total : {total_jeux} {"jeu" if total_jeux <= 1 else "jeux"}
            </div>
        </header>
        <div class="info-tri">💡 Cliquez sur les en-têtes de colonnes (Titre, Plateforme, etc.) pour trier la liste.</div>
        <table>
            <thead>
                <tr>
                    <th id="col-titre">Titre</th>
                    <th id="col-plateforme">Plateforme</th>
                    <th id="col-genre">Genre</th>
                    <th id="col-annee">Année</th>
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

            // Ne pas trier s'il n'y a pas de jeux
            if (rows.length === 1 && rows[0].querySelector('.no-games')) return;

            headers.forEach((header, index) => {{
                header.addEventListener('click', () => {{
                    const isAscending = header.classList.contains('th-sort-asc');
                    
                    // Réinitialiser les flèches sur toutes les colonnes
                    headers.forEach(h => h.classList.remove('th-sort-asc', 'th-sort-desc'));
                    
                    const direction = isAscending ? -1 : 1;
                    
                    rows.sort((rowA, rowB) => {{
                        const cellA = rowA.children[index].textContent.trim();
                        const cellB = rowB.children[index].textContent.trim();
                        
                        // Si on trie par Année (index de colonne 3), on applique un tri numérique
                        if (index === 3) {{
                            const numA = parseInt(cellA, 10);
                            const numB = parseInt(cellB, 10);
                            if (!isNaN(numA) && !isNaN(numB)) {{
                                return (numA - numB) * direction;
                            }}
                        }}
                        
                        // Tri alphabétique (gère correctement les accents français)
                        return cellA.localeCompare(cellB, 'fr', {{ sensitivity: 'base' }}) * direction;
                    }});
                    
                    // Appliquer la bonne classe pour l'icône de tri
                    if (isAscending) {{
                        header.classList.add('th-sort-desc');
                    }} else {{
                        header.classList.add('th-sort-asc');
                    }}
                    
                    // Réinjecter les lignes triées dans le tableau
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
        print(f"✅ Fichier HTML exporté avec succès ! ({FICHIER_HTML})")
    except Exception as e:
        print(f"❌ Erreur lors de l'exportation HTML : {e}")

def main():
    """
    Boucle principale gérant le menu interactif.
    """
    effacer_ecran()
    collection = charger_collection()
    
    while True:
        print("\n" + "="*30)
        print("🎮 GESTIONNAIRE DE JEUX VIDÉO")
        print("="*30)
        print("1. Ajouter un jeu")
        print("2. Lister la collection")
        print("3. Rechercher un jeu")
        print("4. Modifier un jeu")
        print("5. Supprimer un jeu")
        print("6. Afficher les statistiques")
        print("7. Exporter la collection en HTML")
        print("8. Quitter")
        print("="*30)
        
        choix = input("👉 Choisissez une option (1-8) : ").strip()
        
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
            print("👋 Au revoir !")
            break
        else:
            print("❌ Option non reconnue. Veuillez réessayer.")

if __name__ == "__main__":
    main()
