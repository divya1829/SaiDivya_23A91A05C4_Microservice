from app.crypto_utils import decrypt_and_store_seed

# Read encrypted seed
with open("encrypted_seed.txt", "r") as f:
    encrypted_seed = f.read().strip()

print("Decrypting seed...")

seed = decrypt_and_store_seed(encrypted_seed)

print("SUCCESS ✅")
print("Decrypted seed:", seed)
print("Saved to /data/seed.txt")
