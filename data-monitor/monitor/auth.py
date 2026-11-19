"""MEMBER 1 - User accounts: salted PBKDF2 password hashes stored in SQLite."""
import hashlib
import hmac
import re
import secrets
import sqlite3
from datetime import datetime

from . import storage

ITERATIONS = 200_000
USER_RE = re.compile(r"^[a-z0-9_.-]{3,20}$")


def _hash(pwd, salt_hex):
    return hashlib.pbkdf2_hmac("sha256", pwd.encode(), bytes.fromhex(salt_hex), ITERATIONS).hex()


def password_problems(pwd):
    problems = []
    if len(pwd) < 8:
        problems.append("at least 8 characters")
    if not re.search(r"[A-Za-z]", pwd):
        problems.append("a letter")
    if not re.search(r"\d", pwd):
        problems.append("a number")
    return problems


def create_user(username, pwd):
    """Returns (True, normalized_username) or (False, error_message)."""
    u = username.strip().lower()
    if not USER_RE.match(u):
        return False, "Username must be 3-20 characters: letters, numbers, . _ -"
    if u == "guest":
        return False, "That username is reserved."
    problems = password_problems(pwd)
    if problems:
        return False, "Password needs " + ", ".join(problems) + "."
    salt = secrets.token_hex(16)
    c = storage._conn()
    try:
        with c:
            c.execute("INSERT INTO users(username,salt,pwd_hash,created,theme) VALUES(?,?,?,?,?)",
                      (u, salt, _hash(pwd, salt),
                       datetime.now().isoformat(timespec="seconds"), None))
    except sqlite3.IntegrityError:
        return False, "That username is already taken."
    finally:
        c.close()
    return True, u


def verify_user(username, pwd):
    """Returns the normalized username if the credentials are right, else None."""
    u = username.strip().lower()
    c = storage._conn()
    row = c.execute("SELECT salt, pwd_hash FROM users WHERE username=?", (u,)).fetchone()
    c.close()
    if row is None:
        _hash(pwd, "00" * 16)  # keep timing similar for unknown users
        return None
    return u if hmac.compare_digest(row[1], _hash(pwd, row[0])) else None


def change_password(username, old, new):
    if verify_user(username, old) is None:
        return False, "Current password is incorrect."
    problems = password_problems(new)
    if problems:
        return False, "New password needs " + ", ".join(problems) + "."
    salt = secrets.token_hex(16)
    c = storage._conn()
    with c:
        c.execute("UPDATE users SET salt=?, pwd_hash=? WHERE username=?",
                  (salt, _hash(new, salt), username.strip().lower()))
    c.close()
    return True, "Password updated."


def get_theme(username):
    c = storage._conn()
    row = c.execute("SELECT theme FROM users WHERE username=?", (username,)).fetchone()
    c.close()
    return row[0] if row else None


def set_theme(username, theme):
    c = storage._conn()
    with c:
        c.execute("UPDATE users SET theme=? WHERE username=?", (theme, username))
    c.close()
