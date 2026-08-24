import re


# JWT pattern: header.payload.signature
JWT_PATTERN = re.compile(
    r"\beyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\b"
)

# Common credential/secret patterns
SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key\s*[:=]\s*)[^\s,]+"),
    re.compile(r"(?i)(access[_-]?token\s*[:=]\s*)[^\s,]+"),
    re.compile(r"(?i)(secret[_-]?token\s*[:=]\s*)[^\s,]+"),
]


def redact_sensitive_output(text: str) -> str:
    """
    Redact JWTs and credential-like values from model output.
    """

    if not isinstance(text, str):
        text = str(text)

    # Redact JWT-shaped tokens
    text = JWT_PATTERN.sub("[REDACTED]", text)

    # Redact credential-like values
    for pattern in SECRET_PATTERNS:
        text = pattern.sub(r"\1[REDACTED]", text)

    return text


test_outputs = [
    "Normal response: authentication completed successfully.",

    "The access token is: abc123SECRET456",

    "JWT received: "
    "eyJhbGciOiJIUzI1NiJ9."
    "eyJ1c2VyIjoiYWRtaW4ifQ."
    "SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",

    "The secret-token: SUPER_SECRET_VALUE",
]


for number, output in enumerate(test_outputs, start=1):

    print("\n" + "=" * 70)
    print(f"PROJECT 3 S2 TEST {number}")
    print("=" * 70)

    print("Original output:")
    print(output)

    safe_output = redact_sensitive_output(output)

    print("\nProtected output:")
    print(safe_output)

    if safe_output != output:
        print("[S2] SENSITIVE DATA REDACTED")
    else:
        print("[S2] PASS | No sensitive data detected")
