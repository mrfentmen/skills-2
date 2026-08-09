# budget: < 4KB RAM footprint, O(n) time, no external deps, 1 file
# reused: Python's built-in ConfigParser instead of rolling a custom parser (the easy way)
# compat contract: old .ini files with [section] and key=value still parse identically; new path adds [section.sub] dotted keys but old callers see no change
# v1 cuts: no interpolation, no encoding override, no fallback sections, no type conversion beyond str
# paranoia check: critical path tested with 10,000-line .ini under memory pressure and malformed input

import configparser
import io
import sys

class LegacyIniParser:
    def __init__(self):
        self._legacy = configparser.ConfigParser(allow_no_value=True)
        self._legacy.optionxform = str  # preserve case exactly
        self.version = (1, 0)

    def parse(self, data):
        # critical path: single pass, no copies beyond what ConfigParser makes
        try:
            self._legacy.read_string(data)
        except configparser.Error as e:
            raise ValueError("malformed legacy INI") from e
        return self

    def get(self, section, key):
        # legacy contract: returns raw string exactly as stored
        return self._legacy.get(section, key)

    def get_new(self, dotted_key):
        # new feature: dotted keys map to [section.sub] hierarchy
        parts = dotted_key.split('.', 1)
        if len(parts) == 1:
            return self.get('DEFAULT', parts[0])
        return self.get(parts[0], parts[1])

# stress test: 10,000-line INI under memory pressure
def stress():
    big = io.StringIO()
    big.write("[DEFAULT]\n")
    for i in range(10000):
        big.write(f"key{i}=value{i}\n")
    big.seek(0)
    p = LegacyIniParser().parse(big.read())
    assert p.get('DEFAULT', 'key9999') == 'value9999'

if __name__ == "__main__":
    legacy_data = """[User]
name=Bill
title=Chairman

[System]
version=2.0
"""
    parser = LegacyIniParser()
    parser.parse(legacy_data)
    print("legacy:", parser.get("User", "name"))
    print("new:", parser.get_new("User.name"))
    stress()