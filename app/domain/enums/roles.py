from enum import Enum

class Role(str, Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"
    AGENT = "AGENT"
    USER= "USER"