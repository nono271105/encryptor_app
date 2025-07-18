# 🔐 Chiffreur de Fichiers

Application graphique Python pour chiffrer et déchiffrer des fichiers en toute sécurité.

## 📋 Fonctionnalités

- **Interface graphique intuitive** avec drag & drop
- **Chiffrement sécurisé** avec la bibliothèque `cryptography` (Fernet)
- **Génération automatique de clés** pour le chiffrement
- **Déchiffrement** avec clé fournie par l'utilisateur
- **Gestion des erreurs** complète
- **Sauvegarde automatique** des fichiers dans le dossier `outputs/`

## 🛠️ Installation

### Prérequis
- Python 3.7+
- pip

### Installation des dépendances
```bash
pip install PyQt5 cryptography
```

### Structure du projet
```
chiffreur_app/
│
├── main.py              # Lanceur principal
├── ui.py                # Interface utilisateur PyQt5
├── crypto_utils.py      # Utilitaires de chiffrement
├── outputs/             # Dossier des fichiers générés
└── README.md           # Ce fichier
```

## 🚀 Utilisation

### Lancement
```bash
python main.py
```

### Chiffrement d'un fichier
1. **Déposez un fichier** dans la zone centrale ou cliquez pour sélectionner
2. **Cliquez sur "Chiffrer"**
3. **Copiez et sauvegardez la clé générée** (TRÈS IMPORTANT!)
4. Le fichier chiffré (`.enc`) sera créé dans le dossier `outputs/`

### Déchiffrement d'un fichier
1. **Déposez le fichier chiffré** (`.enc`)
2. **Collez la clé** dans le champ prévu
3. **Cliquez sur "Déchiffrer"**
4. Le fichier déchiffré sera créé dans le dossier `outputs/`

## 🔐 Sécurité

### ⚠️ AVERTISSEMENTS IMPORTANTS
- **La perte de la clé rend la récupération des données IMPOSSIBLE**
- **Sauvegardez toujours votre clé dans un endroit sûr**
- **Ne partagez jamais vos clés par email ou messagerie non sécurisée**

### Bonnes pratiques
- Utilisez un gestionnaire de mots de passe pour stocker vos clés
- Faites plusieurs copies de vos clés importantes
- Testez le déchiffrement avant de supprimer l'original
- Ne stockez pas les clés avec les fichiers chiffrés

## 📁 Gestion des fichiers

### Formats supportés
- **Tous types de fichiers** (documents, images, vidéos, etc.)
- **Aucune limite de taille** (dans la limite de la mémoire disponible)

### Fichiers générés
- **Fichiers chiffrés** : `nom_fichier.enc`
- **Fichiers déchiffrés** : `nom_fichier.dec`
- **Localisation** : dossier `outputs/` créé automatiquement

## 🐛 Gestion des erreurs

L'application gère les erreurs suivantes :
- Fichier non sélectionné
- Clé manquante pour le déchiffrement
- Clé invalide ou incorrecte
- Fichier corrompu ou déjà déchiffré
- Fichier inexistant
- Problèmes de permissions

## 🏗️ Compilation (optionnel)

Pour créer un exécutable :

```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

## 🔧 Développement

### Architecture
- **`main.py`** : Point d'entrée, initialisation
- **`ui.py`** : Interface PyQt5, gestion des événements
- **`crypto_utils.py`** : Logique de chiffrement/déchiffrement

### Dépendances
- **PyQt5** : Interface graphique
- **cryptography** : Chiffrement Fernet
- **pathlib** : Gestion des chemins
- **os** : Opérations système

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer des améliorations
- Ajouter des fonctionnalités

---

**⚠️ RAPPEL IMPORTANT : Sauvegardez toujours vos clés de chiffrement !**
