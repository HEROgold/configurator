"""Module defining the ConfigurationParser protocol."""

from abc import ABC, abstractmethod
from collections.abc import Mapping
from io import TextIOWrapper
from pathlib import Path
from typing import NotRequired, TypedDict, Unpack


class GetOptions(TypedDict):
    """Options for the get method."""

    fallback: NotRequired[str]
    raw: NotRequired[bool]
    vars: NotRequired[Mapping[str, str]] | None


class ConfigurationParser(ABC):
    """Configuration Parser that allows for easier manipulation of different config file types."""

    @abstractmethod
    def read(self, file: Path, encoding: str | None = None) -> None:
        """Read the configuration file."""

    @abstractmethod
    def get(self, section: str, option: str, **kwargs: Unpack[GetOptions]) -> str:
        """Get a value from the configuration file."""

    @abstractmethod
    def has_section(self, section: str) -> bool:
        """Check if a section exists in the configuration file."""

    @abstractmethod
    def add_section(self, section: str) -> None:
        """Add a section to the configuration file."""

    @abstractmethod
    def has_option(self, section: str, option: str) -> bool:
        """Check if an option exists in a section of the configuration file."""

    @abstractmethod
    def set(self, section: str, option: str, value: str | None = None) -> None:
        """Set a value in the configuration file."""

    @abstractmethod
    def write(self, fp: TextIOWrapper, *, space_around_delimiters: bool = True) -> None:
        """Write the configuration file."""
