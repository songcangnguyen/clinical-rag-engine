import sys
import os
sys.path.insert(0, os.path.abspath("."))

from app.core.security import authenticate_user, redact_pii, is_authorized

print("=== Testing Authentication ===")

# Test correct login
user = authenticate_user("dr_smith", "clinic123")
print(f"dr_smith login: {user}")

# Test wrong password
user2 = authenticate_user("dr_smith", "wrongpassword")
print(f"Wrong password: {user2}")

# Test unknown user
user3 = authenticate_user("hacker", "hack123")
print(f"Unknown user: {user3}")

print("\n=== Testing Authorization ===")
print(f"clinician sees payroll? {is_authorized('clinician', 'payroll')}")
print(f"clinician sees clinical? {is_authorized('clinician', 'clinical')}")
print(f"hr sees payroll? {is_authorized('hr', 'payroll')}")
print(f"admin sees payroll? {is_authorized('admin', 'payroll')}")

print("\n=== Testing PII Redaction ===")
sample_text = """
Patient John Doe, DOB: 03/15/1985
SSN: 123-45-6789
Phone: 555-867-5309
Email: john.doe@hospital.com
MRN: 9876543
Diagnosis: Type 2 Diabetes
"""
redacted = redact_pii(sample_text)
print("Original:")
print(sample_text)
print("Redacted:")
print(redacted)