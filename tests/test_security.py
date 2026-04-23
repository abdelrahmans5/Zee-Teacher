from app.crypto import hash_password, verify_password


def test_hash_and_verify():
    raw = "Admin@123"
    hashed = hash_password(raw)
    assert hashed != raw
    assert verify_password(raw, hashed)
    assert not verify_password("wrong", hashed)
