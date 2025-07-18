
"""
Application de chiffrement/déchiffrement de fichiers
Lanceur principal
"""

import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import QApplication
from ui import CryptoApp

def main():
    """Point d'entrée principal de l'application"""
    app = QApplication(sys.argv)
    app.setApplicationName("Chiffreur de Fichiers")
    app.setApplicationVersion("1.0")
    
    # Créer le dossier outputs s'il n'existe pas
    outputs_dir = Path("outputs")
    outputs_dir.mkdir(exist_ok=True)
    
    # Lancer l'interface
    window = CryptoApp()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()