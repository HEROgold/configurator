"""Adapter for .toml files, doesn't fully support TOML."""
import tomllib
from io import TextIOWrapper
from pathlib import Path
from typing import Any, Unpack

from confkit.adapters.configuration_parser import GetOptions
from confkit.sentinels import UNSET

from .configuration_parser import ConfigurationParser

# Doesnt support writing

type TomlTypes = str | int | float | bool | None
type TomlData = dict[str, dict[str, TomlTypes]]

def dump(data: TomlData, fp: TextIOWrapper, *, space_around_delimiters: bool = False) -> None:
    """Dump TOML data to a file."""
    for section, options in data.items():
        fp.write(f"[{section}]\n")
        for option, value in options.items():
            if space_around_delimiters:
                fp.write(f"{option} = {value}\n")
            else:
                fp.write(f"{option}={value}\n")
        fp.write("\n")

class TomlParser(ConfigurationParser):
    """Configuration parser adapter for TOML files."""

    def __init__(self, data: dict[str, Any]) -> None:
        """Initialize the parser with data."""
        super().__init__()
        self.data: TomlData = data

    def read(self, file: Path, encoding: str | None = None) -> None:
        """Read a TOML file and load its contents."""
        with file.open("rb", encoding=encoding) as f:
            self.data = tomllib.load(f)

    def get(self, section: str, option: str, **kwargs: Unpack[GetOptions]) -> str:
        """Get a configuration option."""
        _section = self.data.get(section, self.data)
        value = (
            _section.get(option, UNSET)
            if isinstance(_section, dict)
            else str(_section)
        )

        # Set value to fallback if still UNSET. (shorter than ternary or if statement)
        # !value = kwargs.get("fallback") if value is UNSET and kwargs.get("fallback") is not None else value
        value is UNSET and (value := kwargs.get("fallback", UNSET)) # pyright: ignore[reportUnusedExpression]

        if value is UNSET:
            msg = f"Missing option '{option}' in section '{section}'"
            raise KeyError(msg)
        return str(value)

    def has_section(self, section: str) -> bool:
        """Check if a section exists."""
        return section in self.data

    def add_section(self, section: str) -> None:
        """Add a section to the data."""
        self.data[section] = {}

    def has_option(self, section: str, option: str) -> bool:
        """Check if an option exists in a section."""
        return option in self.data.get(section, {})

    def set(self, section: str, option: str, value: str | None = None) -> None:
        """Set an option in a section."""
        if not self.has_section(section):
            self.add_section(section)
        self.data[section][option] = value

    def write(self, fp: TextIOWrapper, *, space_around_delimiters: bool = False) -> None:
        """Write the configuration data to a file."""
        dump(self.data, fp, space_around_delimiters=space_around_delimiters)
