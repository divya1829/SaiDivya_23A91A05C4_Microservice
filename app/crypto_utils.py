import base64
import re
from pathlib import Path
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

DATA_SEED_PATH = Path("data/seed.txt")



def load_private_key():
    """Load RSA private key from PEM file"""
    with open("student_private.pem", "rb") as f:
        private_key_data = f.read()

    private_key = serialization.load_pem_private_key(
        private_key_data,
        password=None,
    )
    return private_key


def decrypt_seed(encrypted_seed_b64: str, private_key) -> str:
    """
    Decrypt base64-encoded encrypted seed using RSA/OAEP with SHA-256.
    Returns 64-character lowercase hex seed.
    """

    # 1. Base64 decode
    try:
        ciphertext = base64.b64decode(encrypted_seed_b64)
    except Exception:
        raise ValueError("Invalid base64 encrypted seed")

    # 2. RSA decrypt
    try:
        plaintext_bytes = private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    except Exception:
        raise ValueError("RSA decryption failed")

    # 3. Decode UTF-8
    try:
        hex_seed = plaintext_bytes.decode("utf-8")
    except UnicodeDecodeError:
        raise ValueError("Decrypted plaintext is not valid UTF-8")

    # 4. Validate 64-char lowercase hex
    if len(hex_seed) != 64:
        raise ValueError("Seed must be 64 characters long")

    if not re.fullmatch(r"[0-9a-f]{64}", hex_seed):
        raise ValueError("Seed must be lowercase hexadecimal")

    return hex_seed


def decrypt_and_store_seed(encrypted_seed_b64: str) -> str:
    """
    Decrypt encrypted seed and store it at /data/seed.txt
    """
    private_key = load_private_key()
    seed = decrypt_seed(encrypted_seed_b64, private_key)

    DATA_SEED_PATH.parent.mkdir(parents=True, exist_ok=True)
    DATA_SEED_PATH.write_text(seed)

    return seed
