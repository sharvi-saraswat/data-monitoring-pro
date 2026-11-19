import os, sys, tempfile
from pathlib import Path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from monitor import auth, storage


def _fresh_db():
    storage.DB = Path(tempfile.mkdtemp()) / "t.db"


def test_signup_login_flow():
    _fresh_db()
    assert auth.create_user("Sharvi", "abc12345")[0]
    assert not auth.create_user("sharvi", "abc12345")[0]          # duplicate (case-insensitive)
    assert not auth.create_user("x", "abc12345")[0]               # bad username
    assert not auth.create_user("newuser", "short")[0]            # weak password
    assert auth.verify_user("SHARVI", "abc12345") == "sharvi"
    assert auth.verify_user("sharvi", "wrongpass1") is None
    assert auth.verify_user("nobody", "abc12345") is None


def test_change_password_and_theme():
    _fresh_db()
    auth.create_user("amit", "pass12345")
    assert not auth.change_password("amit", "bad", "newpass123")[0]
    assert auth.change_password("amit", "pass12345", "newpass123")[0]
    assert auth.verify_user("amit", "pass12345") is None
    assert auth.verify_user("amit", "newpass123") == "amit"
    auth.set_theme("amit", "Sunset")
    assert auth.get_theme("amit") == "Sunset"
