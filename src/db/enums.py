import enum

class FormType(enum.Enum):
    INVESTOR = "investor"
    STARTUP = "startup"

class Role(enum.Enum):
    USER = "User"
    ADMIN = "Admin"

class Currency(enum.Enum):
    RUB = "RUB"
    USD = "USD"
    EUR = "EUR"

class DocVerificationStatus(enum.Enum):
    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"