🎮 Gestionnaire de Collection de Jeux Vidéo

✨ Fonctionnalités

Aucune dépendance externe : Conçu entièrement avec la bibliothèque standard de Python.

Sauvegarde automatique & Support UTF-8 : Votre collection est automatiquement sauvegardée dans collection.json après chaque modification. Gère parfaitement les caractères spéciaux et les accents.

Opérations CRUD complètes :

➕ Ajouter des jeux avec Titre, Plateforme, Genre et Année de sortie.

📋 Lister l'intégralité de votre collection.

🔍 Rechercher des jeux de manière dynamique par Titre, Plateforme ou Genre.

📝 Modifier vos jeux existants de manière sélective (conserve les valeurs actuelles si le champ est laissé vide).

🗑️ Supprimer des jeux à l'aide de leur numéro de ligne affiché.

Robustesse : Détecte et gère automatiquement l'absence ou la corruption du fichier JSON.

Statistiques clés : Affiche le nombre total de jeux, le nombre de plateformes uniques et l'année du jeu le plus récent de votre collection.

🌐 Export HTML : Génère un fichier collection.html moderne, responsive et autonome comprenant :

Une alternance de couleurs pour les lignes du tableau (effet zébré).

Des en-têtes de tableau interactifs — cliquez sur n'importe quelle colonne (Titre, Plateforme, Genre, Année) pour trier la liste dynamiquement (propulsé par du JavaScript natif et exécutable hors-ligne).

🚀 Comment l'exécuter

Prérequis

Vous avez uniquement besoin de Python 3.6+ installé sur votre système.

Installation

Clonez ce dépôt GitHub :

git clone [https://github.com/T209995/game-collection-manager.git](https://github.com/T209995/game-collection-manager.git)
cd game-collection-manager


Lancez le script :

python collection.py


📂 Structure des Fichiers

collection.py — Le script Python principal.

collection.json — La base de données JSON auto-générée stockant vos jeux.

collection.html — La page web interactive et responsive auto-générée.

🎨 Aperçu de l'export HTML interactif

La page HTML exportée est entièrement autonome et fonctionne à 100 % hors-ligne. Vous pouvez cliquer sur les en-têtes de colonnes pour trier instantanément vos jeux :

Le tri textuel gère proprement les accents français et la casse.

Le tri par année s'effectue naturellement de manière chronologique.

📝 Licence

Ce projet est sous licence libre et disponible sous les termes de la Licence MIT.
