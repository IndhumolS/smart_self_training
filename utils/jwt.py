from jose import JWTError, jwt

SECRET_KEY = "your-secret-key"  # Use the same one used to encode the JWT
ALGORITHM = "HS256"

def get_email_from_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise ValueError("Email not found in token.")
        return email
    except JWTError as e:
        raise ValueError("Invalid token") from e
