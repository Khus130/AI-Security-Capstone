from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature


print("=" * 70)
print("PROJECT 4 - ED25519 TAMPERED MESSAGE VERIFICATION")
print("=" * 70)

# Load the generated keys
with open("private_key.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(
        f.read(),
        password=None
    )

with open("public_key.pem", "rb") as f:
    public_key = serialization.load_pem_public_key(f.read())


# Original message
original_message = "Agent authentication request approved"

# Sign the ORIGINAL message
signature = private_key.sign(original_message.encode())

print("\n[1] ORIGINAL MESSAGE")
print(original_message)

print("\n[2] SIGNING")
print("Ed25519 signature generated successfully.")

# First verify the genuine message
try:
    public_key.verify(signature, original_message.encode())
    print("[VERIFY] Original message -> ACCEPTED")
except InvalidSignature:
    print("[VERIFY] Original message -> REJECTED")


# Change ONLY ONE CHARACTER
tampered_message = "Agent authentication request approveD"

print("\n[3] TAMPERING TEST")
print("Original : " + original_message)
print("Tampered : " + tampered_message)
print("Change   : one character")


# Verify tampered message using ORIGINAL signature
try:
    public_key.verify(signature, tampered_message.encode())
    print("[CRITICAL ERROR] Tampered message was accepted!")

except InvalidSignature:
    print("\n[SECURITY ALERT] TAMPERED MESSAGE REJECTED")
    print("[ERROR TYPE] InvalidSignature")
    print("[ERROR] Ed25519 signature verification failed.")
    print("[REASON] Message was modified after signing.")
    print("[RESULT] Integrity verification PASSED")


print("\n" + "=" * 70)
print("PROJECT 4 SCREENSHOT 4 - VERIFICATION COMPLETE")
print("=" * 70)
