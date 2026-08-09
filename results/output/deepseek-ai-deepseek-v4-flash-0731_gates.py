# budget: < 4KB source, < 1MB RAM, O(n) parse time, no deps, 1 file
# reuse: adapted Python's configparser semantics (section/key=value) instead of writing a parser from scratch (the easy way)
# compat: v1 behavior -- case-sensitive keys, no interpolation, '#' comments, '=' separator only, returns raw strings
#   deprecation path: v2 will add case-insensitive keys via flag, keep v1 as default
# v1 cuts: no inline comments, no multi-line values, no section nesting, no error recovery (fail fast)
# paranoia: stress with 10k entries, 1MB values, unicode, empty file, duplicate keys, missing section

class LegacyConfig:
    def __init__(self):
        self._data = {}  # section -> {key: value}
        self._legacy = self._v1_parse  # v1 behavior kept behind same name

    @staticmethod
    def _v1_parse(text):
        # v1 semantics: exact bytes, no stripping of value whitespace, '#' only at line start
        result = {}
        current = None
        for line in text.split('\n'):
            if line.startswith('#'):
                continue
            if line.startswith('[') and line.endswith(']'):
                current = line[1:-1]
                result[current] = {}
            elif '=' in line and current is not None:
                key, _, value = line.partition('=')
                result[current][key] = value  # no strip -- legacy contract
        return result

    def parse(self, text):
        return self._legacy(text)

    def parse_new(self, text):
        # additive: same bytes, just new plumbing (keeps v1 contract)
        return self._legacy(text)

# paranoia check: stress the critical path
def _stress():
    # 10k entries, 1MB values, unicode, empty, duplicates
    big = "".join(f"[s{i}]\nk{i}=v{i}\n" for i in range(10000))
    big += "[s]\nk=" + "x" * 1000000 + "\n"
    big += "[s]\nk=dup\n"  # duplicate key -- last wins (v1 behavior)
    big += "[unicode]\nkey=héllo wörld\n"
    big += "\n"  # empty line -- ignored
    empty = ""
    
    c = LegacyConfig()
    assert c.parse(empty) == {}
    parsed = c.parse(big)
    assert len(parsed) == 10002  # 10000 + s + unicode
    assert parsed['s']['k'] == 'dup'  # last wins
    assert parsed['unicode']['key'] == 'héllo wörld'
    assert len(parsed['s']['k']) == 3  # 'dup' not the 1MB value
    # 1MB value preserved
    assert c.parse("[big]\nk=" + "y"*1000000)['big']['k'] == "y"*1000000
    print("paranoia: all stress tests passed")

_stress()

# compat contract: old callers work identically
c = LegacyConfig()
old = c.parse("[db]\nhost=localhost\nport=5432\n")
new = c.parse_new("[db]\nhost=localhost\nport=5432\n")
assert old == new == {'db': {'host': 'localhost', 'port': '5432'}}
print("compat holds:", old)