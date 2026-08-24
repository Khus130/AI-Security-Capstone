from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
from pathlib import Path


# Generate Ed25519 key pair
private_key = ed25519.Ed25519PrivateKey.generate()
public_key = private_key.public_key()


# Save private key
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

Path("private_key.pem").write_bytes(private_pem)


# Save public key
public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

Path("public_key.pem").write_bytes(public_pem)


print("=" * 60)
print("PROJECT 4 - ED25519 KEY PAIR GENERATION")
print("=" * 60)

print("[SUCCESS] Ed25519 key pair generated")
print("[CREATED] private_key.pem")
print("[CREATED] public_key.pem")

print("\nKey files:")
print(" - private_key.pem")
print(" - public_key.pem")

print("\n[SUCCESS] Both key files created successfully.")
