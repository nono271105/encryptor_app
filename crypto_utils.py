"""
Utilitaires de chiffrement/déchiffrement
Utilise la bibliothèque cryptography avec Fernet
"""

import os
import json
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken

def generate_key():
    """
    Génère une clé de chiffrement Fernet
    
    Returns:
        bytes: Clé de chiffrement encodée en base64
    """
    return Fernet.generate_key()

def encrypt_file(file_path, key):
    """
    Chiffre un fichier avec la clé fournie
    
    Args:
        file_path (str): Chemin vers le fichier à chiffrer
        key (bytes): Clé de chiffrement
        
    Returns:
        str: Chemin vers le fichier chiffré
        
    Raises:
        FileNotFoundError: Si le fichier n'existe pas
        Exception: Pour toute autre erreur de chiffrement
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Le fichier {file_path} n'existe pas")
    
    # Créer l'objet Fernet
    fernet = Fernet(key)
    
    # Lire le fichier original
    with open(file_path, 'rb') as file:
        original_data = file.read()
    
    # Créer les métadonnées avec l'extension originale
    original_path = Path(file_path)
    metadata = {
        'original_extension': original_path.suffix,
        'original_name': original_path.stem
    }
    
    # Convertir les métadonnées en JSON puis en bytes
    metadata_json = json.dumps(metadata).encode('utf-8')
    metadata_length = len(metadata_json)
    
    # Créer le contenu à chiffrer : [longueur_metadata][metadata][données_originales]
    content_to_encrypt = metadata_length.to_bytes(4, byteorder='big') + metadata_json + original_data
    
    # Chiffrer le contenu complet
    encrypted_data = fernet.encrypt(content_to_encrypt)
    
    # Créer le nom du fichier chiffré
    encrypted_filename = f"{original_path.stem}.enc"
    
    # Créer le dossier outputs s'il n'existe pas
    outputs_dir = Path("outputs")
    outputs_dir.mkdir(exist_ok=True)
    
    encrypted_path = outputs_dir / encrypted_filename
    
    # Écrire le fichier chiffré
    with open(encrypted_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted_data)
    
    return str(encrypted_path)

def decrypt_file(file_path, key):
    """
    Déchiffre un fichier avec la clé fournie
    
    Args:
        file_path (str): Chemin vers le fichier à déchiffrer
        key (bytes): Clé de déchiffrement
        
    Returns:
        str: Chemin vers le fichier déchiffré
        
    Raises:
        FileNotFoundError: Si le fichier n'existe pas
        InvalidToken: Si la clé est incorrecte
        Exception: Pour toute autre erreur de déchiffrement
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Le fichier {file_path} n'existe pas")
    
    # Créer l'objet Fernet
    fernet = Fernet(key)
    
    # Lire le fichier chiffré
    with open(file_path, 'rb') as encrypted_file:
        encrypted_data = encrypted_file.read()
    
    # Déchiffrer les données
    try:
        decrypted_content = fernet.decrypt(encrypted_data)
    except InvalidToken:
        raise InvalidToken("Clé de déchiffrement incorrecte ou fichier corrompu")
    
    # Extraire la longueur des métadonnées (4 premiers bytes)
    metadata_length = int.from_bytes(decrypted_content[:4], byteorder='big')
    
    # Extraire les métadonnées
    metadata_bytes = decrypted_content[4:4+metadata_length]
    metadata = json.loads(metadata_bytes.decode('utf-8'))
    
    # Extraire les données originales
    original_data = decrypted_content[4+metadata_length:]
    
    # Reconstruire le nom du fichier avec l'extension originale
    original_extension = metadata.get('original_extension', '')
    original_name = metadata.get('original_name', Path(file_path).stem)
    
    # Créer le nom du fichier déchiffré avec l'extension originale
    if original_extension:
        decrypted_filename = f"{original_name}_decrypted{original_extension}"
    else:
        decrypted_filename = f"{original_name}_decrypted"
    
    # Créer le dossier outputs s'il n'existe pas
    outputs_dir = Path("outputs")
    outputs_dir.mkdir(exist_ok=True)
    
    decrypted_path = outputs_dir / decrypted_filename
    
    # Écrire le fichier déchiffré
    with open(decrypted_path, 'wb') as decrypted_file:
        decrypted_file.write(original_data)
    
    return str(decrypted_path)

def validate_key(key_string):
    """
    Valide une clé de chiffrement au format string
    
    Args:
        key_string (str): Clé sous forme de string
        
    Returns:
        bytes: Clé validée en bytes
        
    Raises:
        ValueError: Si la clé n'est pas valide
    """
    try:
        # Convertir en bytes si nécessaire
        if isinstance(key_string, str):
            key_bytes = key_string.encode('utf-8')
        else:
            key_bytes = key_string
        
        # Tenter de créer un objet Fernet pour valider
        Fernet(key_bytes)
        return key_bytes
        
    except Exception as e:
        raise ValueError(f"Clé invalide: {str(e)}")

def key_to_string(key_bytes):
    """
    Convertit une clé bytes en string lisible
    
    Args:
        key_bytes (bytes): Clé en bytes
        
    Returns:
        str: Clé en string
    """
    return key_bytes.decode('utf-8')