"""
Interface utilisateur PyQt5 pour l'application de chiffrement
"""

import os
import sys
from pathlib import Path
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QTextEdit, 
                             QFileDialog, QMessageBox, QFrame, QApplication)
from PyQt5.QtCore import Qt, QMimeData, QUrl
from PyQt5.QtGui import QFont, QClipboard, QDragEnterEvent, QDropEvent

from crypto_utils import generate_key, encrypt_file, decrypt_file, validate_key, key_to_string
from cryptography.fernet import InvalidToken

class DropZone(QLabel):
    """Zone de dépôt de fichiers avec drag & drop"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setMinimumHeight(150)
        self.setStyleSheet("""
            QLabel {
                border: 3px dashed #aaa;
                border-radius: 10px;
                background-color: #f9f9f9;
                color: #666;
                font-size: 16px;
                padding: 20px;
            }
            QLabel:hover {
                border-color: #0078d4;
                background-color: #e6f3ff;
            }
        """)
        self.setAlignment(Qt.AlignCenter)
        self.setText("📁 Déposez votre fichier ici\nou cliquez pour sélectionner")
        self.setAcceptDrops(True)
        
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Événement lors de l'entrée du drag"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setStyleSheet("""
                QLabel {
                    border: 3px dashed #0078d4;
                    border-radius: 10px;
                    background-color: #e6f3ff;
                    color: #0078d4;
                    font-size: 16px;
                    padding: 20px;
                }
            """)
    
    def dragLeaveEvent(self, event):
        """Événement lors de la sortie du drag"""
        self.setStyleSheet("""
            QLabel {
                border: 3px dashed #aaa;
                border-radius: 10px;
                background-color: #f9f9f9;
                color: #666;
                font-size: 16px;
                padding: 20px;
            }
            QLabel:hover {
                border-color: #0078d4;
                background-color: #e6f3ff;
            }
        """)
    
    def dropEvent(self, event: QDropEvent):
        """Événement lors du drop du fichier"""
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        if files:
            self.parent_window.set_file_path(files[0])
        self.dragLeaveEvent(event)
        
    def mousePressEvent(self, event):
        """Clic sur la zone pour ouvrir le sélecteur de fichier"""
        if event.button() == Qt.LeftButton:
            self.parent_window.open_file_dialog()

class CryptoApp(QMainWindow):
    """Application principale de chiffrement/déchiffrement"""
    
    def __init__(self):
        super().__init__()
        self.current_file_path = None
        self.current_key = None
        self.init_ui()
        
    def init_ui(self):
        """Initialise l'interface utilisateur"""
        self.setWindowTitle("🔐 Chiffreur de Fichiers")
        self.setGeometry(100, 100, 600, 700)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Titre
        title = QLabel("🔐 Chiffreur de Fichiers")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setStyleSheet("color: #0078d4; margin-bottom: 20px;")
        layout.addWidget(title)
        
        # Zone de dépôt
        self.drop_zone = DropZone(self)
        layout.addWidget(self.drop_zone)
        
        # Affichage du fichier sélectionné
        self.file_label = QLabel("Aucun fichier sélectionné")
        self.file_label.setWordWrap(True)
        self.file_label.setStyleSheet("color: #666; font-size: 12px; margin: 10px 0;")
        layout.addWidget(self.file_label)
        
        # Champ de clé
        key_layout = QVBoxLayout()
        key_label = QLabel("Clé de déchiffrement (optionnel pour chiffrement):")
        key_label.setStyleSheet("font-weight: bold; margin-bottom: 5px;")
        key_layout.addWidget(key_label)
        
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Collez votre clé ici pour déchiffrer...")
        self.key_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                font-size: 12px;
                border: 2px solid #ddd;
                border-radius: 5px;
                font-family: monospace;
            }
            QLineEdit:focus {
                border-color: #0078d4;
            }
        """)
        key_layout.addWidget(self.key_input)
        
        layout.addLayout(key_layout)
        
        # Boutons d'action
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        self.encrypt_btn = QPushButton("🔒 Chiffrer")
        self.encrypt_btn.setMinimumHeight(50)
        self.encrypt_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
            QPushButton:disabled {
                background-color: #6c757d;
            }
        """)
        self.encrypt_btn.clicked.connect(self.encrypt_file)
        button_layout.addWidget(self.encrypt_btn)
        
        self.decrypt_btn = QPushButton("🔓 Déchiffrer")
        self.decrypt_btn.setMinimumHeight(50)
        self.decrypt_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
            QPushButton:pressed {
                background-color: #bd2130;
            }
            QPushButton:disabled {
                background-color: #6c757d;
            }
        """)
        self.decrypt_btn.clicked.connect(self.decrypt_file)
        button_layout.addWidget(self.decrypt_btn)
        
        layout.addLayout(button_layout)
        
        # Zone de messages
        self.message_area = QTextEdit()
        self.message_area.setMaximumHeight(200)
        self.message_area.setReadOnly(True)
        self.message_area.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 5px;
                padding: 10px;
                font-size: 12px;
                font-family: monospace;
                color: #000000;  
            }
        """)
        layout.addWidget(self.message_area)
        
        # Boutons utilitaires
        util_layout = QHBoxLayout()
        
        self.copy_key_btn = QPushButton("📋 Copier la clé")
        self.copy_key_btn.setEnabled(False)
        self.copy_key_btn.clicked.connect(self.copy_key)
        self.copy_key_btn.setStyleSheet("""
            QPushButton {
                background-color: #17a2b8;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 12px;
                padding: 8px 16px;
            }
            QPushButton:hover:enabled {
                background-color: #138496;
            }
            QPushButton:disabled {
                background-color: #6c757d;
            }
        """)
        util_layout.addWidget(self.copy_key_btn)
        
        self.open_outputs_btn = QPushButton("📂 Ouvrir dossier outputs")
        self.open_outputs_btn.clicked.connect(self.open_outputs_folder)
        self.open_outputs_btn.setStyleSheet("""
            QPushButton {
                background-color: #6f42c1;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 12px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #5a32a3;
            }
        """)
        util_layout.addWidget(self.open_outputs_btn)
        
        self.clear_btn = QPushButton("🗑️ Effacer")
        self.clear_btn.clicked.connect(self.clear_all)
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 12px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        util_layout.addWidget(self.clear_btn)
        
        layout.addLayout(util_layout)
        
        # Message d'avertissement
        warning = QLabel("ATTENTION: La perte de la clé rend la récupération des données impossible!")
        warning.setStyleSheet("""
            QLabel {
                background-color: #ffffff;
                border: 1px solid #ffeaa7;
                border-radius: 5px;
                padding: 10px;
                color: #000000;
                font-weight: bold;
                font-size: 12px;
            }
        """)
        warning.setWordWrap(True)
        layout.addWidget(warning)
        
        # Activer/désactiver les boutons
        self.update_buttons()
        
    def set_file_path(self, file_path):
        """Définit le chemin du fichier sélectionné"""
        self.current_file_path = file_path
        filename = os.path.basename(file_path)
        self.file_label.setText(f"📄 Fichier sélectionné: {filename}")
        self.file_label.setStyleSheet("color: #28a745; font-weight: bold; font-size: 12px; margin: 10px 0;")
        self.add_message(f"Fichier sélectionné: {file_path}")
        self.update_buttons()
        
    def open_file_dialog(self):
        """Ouvre la boîte de dialogue de sélection de fichier"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Sélectionner un fichier", 
            "", 
            "Tous les fichiers (*.*)"
        )
        if file_path:
            self.set_file_path(file_path)
            
    def update_buttons(self):
        """Met à jour l'état des boutons"""
        has_file = self.current_file_path is not None
        self.encrypt_btn.setEnabled(has_file)
        self.decrypt_btn.setEnabled(has_file)
        
    def add_message(self, message, is_error=False):
        """Ajoute un message à la zone de messages"""
        if is_error:
            formatted_message = f"ERREUR: {message}"
        else:
            formatted_message = f"{message}"
        
        self.message_area.append(formatted_message)
        self.message_area.verticalScrollBar().setValue(
            self.message_area.verticalScrollBar().maximum()
        )
        
    def encrypt_file(self):
        """Chiffre le fichier sélectionné"""
        if not self.current_file_path:
            self.add_message("Aucun fichier sélectionné", True)
            return
            
        try:
            # Générer une nouvelle clé
            key = generate_key()
            self.current_key = key
            
            # Chiffrer le fichier
            self.add_message("Chiffrement en cours...")
            encrypted_path = encrypt_file(self.current_file_path, key)
            
            # Afficher le succès
            key_str = key_to_string(key)
            self.add_message(f"Chiffrement réussi!")
            self.add_message(f"Fichier chiffré: {encrypted_path}")
            self.add_message(f"CLÉ GÉNÉRÉE: {key_str}")
            self.add_message("SAUVEGARDEZ CETTE CLÉ IMMÉDIATEMENT!")
            
            # Activer le bouton de copie
            self.copy_key_btn.setEnabled(True)
            
        except Exception as e:
            self.add_message(f"Erreur lors du chiffrement: {str(e)}", True)
            
    def decrypt_file(self):
        """Déchiffre le fichier sélectionné"""
        if not self.current_file_path:
            self.add_message("Aucun fichier sélectionné", True)
            return
            
        key_str = self.key_input.text().strip()
        if not key_str:
            self.add_message("Clé de déchiffrement manquante", True)
            return
            
        try:
            # Valider la clé
            key = validate_key(key_str)
            
            # Déchiffrer le fichier
            self.add_message("Déchiffrement en cours...")
            decrypted_path = decrypt_file(self.current_file_path, key)
            
            # Afficher le succès
            self.add_message(f"Déchiffrement réussi!")
            self.add_message(f"Fichier déchiffré: {decrypted_path}")
            
        except InvalidToken:
            self.add_message("Clé incorrecte ou fichier corrompu", True)
        except ValueError as e:
            self.add_message(f"Clé invalide: {str(e)}", True)
        except Exception as e:
            self.add_message(f"Erreur lors du déchiffrement: {str(e)}", True)
            
    def copy_key(self):
        """Copie la clé dans le presse-papiers"""
        if self.current_key:
            clipboard = QApplication.clipboard()
            clipboard.setText(key_to_string(self.current_key))
            self.add_message("Clé copiée dans le presse-papiers")
            
    def open_outputs_folder(self):
        """Ouvre le dossier outputs"""
        outputs_path = Path("outputs").resolve()
        if outputs_path.exists():
            if sys.platform == "win32":
                os.startfile(outputs_path)
            elif sys.platform == "darwin":
                os.system(f"open '{outputs_path}'")
            else:
                os.system(f"xdg-open '{outputs_path}'")
        else:
            self.add_message("Le dossier outputs n'existe pas encore", True)
            
    def clear_all(self):
        """Efface tous les champs et réinitialise"""
        self.current_file_path = None
        self.current_key = None
        self.file_label.setText("Aucun fichier sélectionné")
        self.file_label.setStyleSheet("color: #666; font-size: 12px; margin: 10px 0;")
        self.key_input.clear()
        self.message_area.clear()
        self.copy_key_btn.setEnabled(False)
        self.update_buttons()
        self.add_message("Interface réinitialisée")