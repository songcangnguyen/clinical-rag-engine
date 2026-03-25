import re

# --- Role definitions ---
# Each role maps to which document categories they can access
ROLE_PERMISSIONS = {
    "clinician": ["clinical", "guidelines", "pharmacy"],
    "informatics": ["data_dictionary", "clinical", "guidelines"],
    "hr": ["payroll", "hr_policy"],
    "admin": ["clinical", "guidelines", "pharmacy", "data_dictionary", "payroll", "hr_policy"]
}

# --- Simulated users ---
# In a real app these would come from a database
USERS = {
    "dr_smith": {"password": "clinic123", "role": "clinician"},
    "analyst_jane": {"password": "data456", "role": "informatics"},
    "hr_bob": {"password": "hr789", "role": "hr"},
    "admin_root": {"password": "admin000", "role": "admin"}
}

# --- PII patterns to redact ---
PII_PATTERNS = {
    "SSN": r"\b\d{3}-\d{2}-\d{4}\b",
    "Phone": r"\b\d{3}[-.\s]\d{3}[-.\s]\d{4}\b",
    "Email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
    "DOB": r"\b(0[1-9]|1[0-2])/(0[1-9]|[12]\d|3[01])/\d{4}\b",
    "MRN": r"\bMRN[:\s]?\d{6,10}\b",
}

def authenticate_user(username: str, password: str):
    """Check if username and password are correct. Returns user info or None."""
    user = USERS.get(username)
    if user and user["password"] == password:
        return {"username": username, "role": user["role"]}
    return None

def get_allowed_categories(role: str):
    """Return list of document categories this role can access."""
    return ROLE_PERMISSIONS.get(role, [])

def redact_pii(text: str) -> str:
    """Scan text and replace any PII with a redacted placeholder."""
    for pii_type, pattern in PII_PATTERNS.items():
        text = re.sub(pattern, f"[REDACTED {pii_type}]", text)
    return text

def is_authorized(role: str, doc_category: str) -> bool:
    """Check if a role is allowed to access a specific document category."""
    allowed = get_allowed_categories(role)
    return doc_category in allowed