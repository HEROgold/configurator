
import json
from io import TextIOWrapper
from pathlib import Path
from typing import Unpack

from confkit.adapters.configuration_parser import ConfigStructure, ConfigurationParser, GetOptions
from confkit.sentinels import UNSET


class JsonParser(ConfigurationParser):
    """JSON configuration parser."""

    def __init__(self, data: ConfigStructure) -> None:
        super().__init__()
        self.data: ConfigStructure = data

    def read(self, file: Path, encoding: str | None = None) -> None:
        with file.open(encoding=encoding) as f:
            self.data = json.load(f)

    def get(self, section: str, option: str, **kwargs: Unpack[GetOptions]) -> str:
        _section = self.data.get(section, self.data)
        value = (
            _section.get(option, UNSET)
            if isinstance(_section, dict)
            else str(_section)
        )

        # Set value to fallback if still UNSET. (shorter than ternary or if statement)
        value is UNSET and (value := kwargs.get("fallback", UNSET))  # pyright: ignore[reportUnusedExpression]

        if value is UNSET:
            msg = f"Missing option '{option}' in section '{section}'"
            raise KeyError(msg)
        return str(value)

    def has_section(self, section: str) -> bool:
        return section in self.data

    def add_section(self, section: str) -> None:
        self.data[section] = {}

    def has_option(self, section: str, option: str) -> bool:
        return option in self.data.get(section, {})

    def set(self, section: str, option: str, value: str | None = None) -> None:
        if not self.has_section(section):
            self.add_section(section)
        self.data[section][option] = value

    def write(self, fp: TextIOWrapper, *, space_around_delimiters: bool = False) -> None:
        delimiters = (", ", ": ") if space_around_delimiters else (",", ":")
        json.dump(self.data, fp, indent=4, separators=delimiters)
