#!/usr/bin/env python3
import sys
sys.path.append("/app")

from datetime import datetime, timezone
from app.totp_utils import generate_totp_code
from pathlib import Path

SEED_FILE = Path("/data/seed.txt")
OUT_FILE = Path("/cron/last_code.txt")

def main():
    if not SEED_FILE.exists():
        return

    hex_seed = SEED_FILE.read_text().strip()
    code = generate_totp_code(hex_seed)

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    line = f"{ts} - 2FA Code: {code}\n"

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(line)

if __name__ == "__main__":
    main()
