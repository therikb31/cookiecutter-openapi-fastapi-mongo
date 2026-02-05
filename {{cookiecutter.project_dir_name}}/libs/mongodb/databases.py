"""
Enum class for all the MongoDB databases used by the project
"""

from enum import Enum


class MongoDatabases(Enum):
    PROJECT = "{{ cookiecutter.mongodb_name }}"
