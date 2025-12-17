import base64
import pyotp
from pathlib import Path

SEED_PATH = Path("data/seed.txt")


def _get_base32_seed():
    if not SEED_PATH.exists():
        raise FileNotFoundError("Seed not decrypted yet")

    hex_seed = SEED_PATH.read_text().strip()
    seed_bytes = bytes.fromhex(hex_seed)
    return base64.b32encode(seed_bytes).decode()


def generate_totp_code() -> str:
    base32_seed = _get_base32_seed()
    totp = pyotp.TOTP(base32_seed, digits=6, interval=30)
    return totp.now()


def verify_totp_code(code: str, valid_window: int = 1) -> bool:
    base32_seed = _get_base32_seed()
    totp = pyotp.TOTP(base32_seed, digits=6, interval=30)
    return totp.verify(code, valid_window=valid_window)
