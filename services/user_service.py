from database.db import get_client
from auth.auth_utils import hash_password, verify_password


def get_user_by_email(email: str) -> dict | None:
    res = get_client().table("users").select("*").eq("email", email).execute()
    return res.data[0] if res.data else None


def register_user(name: str, email: str, password: str, role: str = "user") -> dict:
    """
    Register a new user.
    Raises ValueError if email already exists.
    Returns the created user row.
    """
    if get_user_by_email(email):
        raise ValueError("An account with this email already exists.")

    hashed = hash_password(password)
    res = (
        get_client()
        .table("users")
        .insert({"name": name, "email": email, "password": hashed, "role": role})
        .execute()
    )
    return res.data[0]


def authenticate_user(email: str, password: str) -> dict | None:
    """
    Return user dict if credentials match, else None.
    """
    user = get_user_by_email(email)
    if user and verify_password(password, user["password"]):
        return user
    return None
