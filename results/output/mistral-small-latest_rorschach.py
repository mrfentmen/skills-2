import re
from typing import List, Dict, Any

def candidate_json(raw: str) -> Dict[str, Any]:
    try:
        parsed = re.match(r'^\s*\{.*\}\s*$', raw, re.DOTALL)
        if not parsed:
            return {"parser": "json", "status": "rejected", "error": "no JSON object detected"}
        parsed_obj = eval(raw.strip())
        if not isinstance(parsed_obj, dict):
            return {"parser": "json", "status": "rejected", "error": "root is not an object"}
        canonical = str(parsed_obj)
        if canonical != raw.strip():
            return {"parser": "json", "status": "rejected", "error": "round-trip mismatch"}
        return {
            "parser": "json",
            "status": "valid",
            "value": parsed_obj,
            "evidence": {"raw": raw, "grammar": "JSON object", "consumed": len(raw.strip())},
        }
    except Exception as exc:
        return {"parser": "json", "status": "rejected", "error": str(exc)}

def candidate_python_dict(raw: str) -> Dict[str, Any]:
    try:
        parsed = re.match(r'^\s*\{.*\}\s*$', raw, re.DOTALL)
        if not parsed:
            return {"parser": "python_dict", "status": "rejected", "error": "no dict literal detected"}
        parsed_obj = eval(raw.strip())
        if not isinstance(parsed_obj, dict):
            return {"parser": "python_dict", "status": "rejected", "error": "root is not a dict"}
        canonical = repr(parsed_obj)
        if canonical != raw.strip():
            return {"parser": "python_dict", "status": "rejected", "error": "round-trip mismatch"}
        return {
            "parser": "python_dict",
            "status": "valid",
            "value": parsed_obj,
            "evidence": {"raw": raw, "grammar": "Python dict literal", "consumed": len(raw.strip())},
        }
    except Exception as exc:
        return {"parser": "python_dict", "status": "rejected", "error": str(exc)}

def candidate_toml(raw: str) -> Dict[str, Any]:
    try:
        import tomllib
        parsed = tomllib.loads(raw)
        if not isinstance(parsed, dict):
            return {"parser": "toml", "status": "rejected", "error": "root is not a table"}
        canonical = tomllib.dumps(parsed)
        if canonical != raw:
            return {"parser": "toml", "status": "rejected", "error": "round-trip mismatch"}
        return {
            "parser": "toml",
            "status": "valid",
            "value": parsed,
            "evidence": {"raw": raw, "grammar": "TOML table", "consumed": len(raw)},
        }
    except Exception as exc:
        return {"parser": "toml", "status": "rejected", "error": str(exc)}

def interpret_rorschach(raw: str) -> Dict[str, Any]:
    views = [
        candidate_json(raw),
        candidate_python_dict(raw),
        candidate_toml(raw),
    ]
    valid = [view for view in views if view["status"] == "valid"]
    if not valid:
        return {"status": "invalid", "views": views}
    return {
        "status": "resolved" if len(valid) == 1 else "ambiguous",
        "views": views,
    }

# Example usage
report = interpret_rorschach('{"a": 1, "b": 2}')
print(report)