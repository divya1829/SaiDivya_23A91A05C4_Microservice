from app.totp_utils import generate_totp_code, verify_totp_code

code = generate_totp_code()
print("Generated TOTP:", code)

result = verify_totp_code(code)
print("Verification result:", result)
