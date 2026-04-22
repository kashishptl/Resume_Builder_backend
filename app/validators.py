import re


# ===================== COMMON HELPERS =====================

def clean_string(value):
    return value.strip() if isinstance(value, str) else value


def validate_email(email):
    email = clean_string(email).lower()
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    if not email:
        return "Email is required"

    if not re.match(pattern, email):
        return "Invalid email format"

    return None


def validate_name(name):
    name = clean_string(name)

    if not name:
        return "Name is required"

    if len(name) < 2:
        return "Name must be at least 2 characters"

    if not re.match(r"^[A-Za-z ]+$", name):
        return "Name can only contain letters and spaces"

    return None


def validate_password(password):
    errors = []

    if not password:
        errors.append("Password is required")
        return errors

    if len(password) < 8:
        errors.append("At least 8 characters")

    if not re.search(r"[A-Za-z]", password):
        errors.append("At least one letter")

    if not re.search(r"\d", password):
        errors.append("At least one number")

    if not re.search(r"[@$!%*?&]", password):
        errors.append("At least one special character (@$!%*?&)")

    return errors if errors else None


# ===================== SIGNUP VALIDATION =====================

def validate_signup(data):
    errors = {}

    name_error = validate_name(data.get("name"))
    if name_error:
        errors["name"] = name_error

    email_error = validate_email(data.get("email"))
    if email_error:
        errors["email"] = email_error

    password_errors = validate_password(data.get("password"))
    if password_errors:
        errors["password"] = password_errors

    return errors if errors else None


# ===================== LOGIN VALIDATION =====================

def validate_login(data):
    if not data.get("email") or not data.get("password"):
        return {"message": "Email and password required"}

    return None


# ===================== RESUME VALIDATION =====================

def validate_resume(data):
    errors = {}

    if not data.get("full_name"):
        errors["full_name"] = "Full name is required"

    if not data.get("email"):
        errors["email"] = "Email is required"
    elif not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", data.get("email")):
        errors["email"] = "Invalid email format"

    if "skills" in data and not isinstance(data.get("skills"), list):
        errors["skills"] = "Skills must be a list"

    return errors if errors else None