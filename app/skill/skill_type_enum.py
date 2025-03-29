from enum import Enum


class SkillTypeEnum(str, Enum):
    LANGUAGE = "language"
    FRAMEWORK = "framework"
    LIBRARY = "library"
    DATABASE = "database"
    OPERATING_SYSTEM = "operating_system"
    UTIL = "util"
    OTHER = "other"
