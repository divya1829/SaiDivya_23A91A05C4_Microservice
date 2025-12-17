from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time

from app.crypto_utils import decrypt_and_store_seed
from app.totp_utils import generate_totp_code, verify_totp_code

app = FastAPI()


# ---------- Request Models ----------

class DecryptSeedRequest(BaseModel):
    encrypted_seed: str


class Verify2FARequest(BaseModel):
    code: str


# ---------- API Endpoints ----------

@app.post("/decrypt-seed")
def decrypt_seed_api(req: DecryptSeedRequest):
    """
    Decrypt encrypted seed and store it in data/seed.txt
    """
    try:
        decrypt_and_store_seed(req.encrypted_seed)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/generate-2fa")
def generate_2fa_api():
    """
    Generate current TOTP code
    """
    try:
        code = generate_totp_code()
        valid_for = 30 - (int(time.time()) % 30)

        return {
            "code": code,
            "valid_for": valid_for
        }
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/verify-2fa")
def verify_2fa_api(req: Verify2FARequest):
    """
    Verify a submitted TOTP code
    """
    try:
        is_valid = verify_totp_code(req.code)
        return {"valid": is_valid}
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
