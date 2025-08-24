"""Adapted parser for INI files."""

from configparser import ConfigParser
from io import TextIOWrapper
from pathlib import Path
from typing import Unpack

from confkit.adapters.configuration_parser import ConfigurationParser, GetOptions


class IniParser(ConfigurationParser):
    def __init__(self, parser: ConfigParser) -> None:
        super().__init__()
        self._parser = parser

    def read(self, file: Path, encoding: str | None = None) -> None:
        self._parser.read(file, encoding=encoding)

    def get(self, section: str, option: str, **kwargs: Unpack[GetOptions]) -> str:
        return self._parser.get(section, option, **kwargs)

    def has_section(self, section: str) -> bool:
        return self._parser.has_section(section)

    def add_section(self, section: str) -> None:
        return self._parser.add_section(section)

    def has_option(self, section: str, option: str) -> bool:
        return self._parser.has_option(section, option)

    def set(self, section: str, option: str, value: str | None = None) -> None:
        return self._parser.set(section, option, value)

    def write(self, fp: TextIOWrapper, *, space_around_delimiters: bool = True) -> None:
        return self._parser.write(fp, space_around_delimiters=space_around_delimiters)
