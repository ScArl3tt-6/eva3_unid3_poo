from cryptography.fernet import Fernet
import os
from typing import Iterable, Optional


def generate_key() -> str:
    """Generate a new Fernet key (base64 urlsafe) and return it as a str."""
    return Fernet.generate_key().decode()


def load_key() -> bytes:
    """Load the encryption key from the `ENCRYPTION_KEY` environment variable.

    Raises RuntimeError if the variable is not set.
    """
    key = os.getenv("ENCRYPTION_KEY")
    if not key:
        raise RuntimeError("ENCRYPTION_KEY environment variable is not set")
    if isinstance(key, str):
        key = key.encode()
    return key


def encrypt_str(plaintext: str, key: Optional[bytes] = None) -> str:
    """Encrypt a UTF-8 string and return the token as a str."""
    if key is None:
        key = load_key()
    f = Fernet(key)
    token = f.encrypt(plaintext.encode())
    return token.decode()


def decrypt_str(token: str, key: Optional[bytes] = None) -> str:
    """Decrypt a token produced by `encrypt_str` and return the original string."""
    if key is None:
        key = load_key()
    f = Fernet(key)
    return f.decrypt(token.encode()).decode()


def encrypt_object_fields(obj, fields: Iterable[str], key: Optional[bytes] = None) -> None:
    """Encrypt specified string fields of an object in-place.

    Example: encrypt_object_fields(user, ['email', 'ssn'])
    """
    if key is None:
        key = load_key()
    for field in fields:
        if hasattr(obj, field):
            val = getattr(obj, field)
            if val is None:
                continue
            # Only encrypt simple values; convert to str first
            try:
                enc = encrypt_str(str(val), key)
                setattr(obj, field, enc)
            except Exception:
                # Skip fields that cannot be encrypted
                continue


def decrypt_object_fields(obj, fields: Iterable[str], key: Optional[bytes] = None) -> None:
    """Decrypt specified fields of an object in-place."""
    if key is None:
        key = load_key()
    for field in fields:
        if hasattr(obj, field):
            val = getattr(obj, field)
            if val is None:
                continue
            try:
                dec = decrypt_str(str(val), key)
                setattr(obj, field, dec)
            except Exception:
                # If decryption fails, leave the value as-is
                continue


__all__ = [
    "generate_key",
    "load_key",
    "encrypt_str",
    "decrypt_str",
    "encrypt_object_fields",
    "decrypt_object_fields",
]
