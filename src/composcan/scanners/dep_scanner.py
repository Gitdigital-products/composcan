"""Dependency discovery scanner."""
from pathlib import Path
import json

MANIFEST_MAP = {
    "package.json": "npm", "requirements.txt": "pypi", "pyproject.toml": "pypi",
    "Cargo.toml": "cargo", "go.mod": "go", "Gemfile": "ruby", "pom.xml": "maven",
    "composer.json": "php", "Pipfile": "pypi", "setup.py": "pypi",
}

class DependencyScanner:
    def scan(self, path: Path) -> dict:
        deps = []
        for manifest, eco in MANIFEST_MAP.items():
            for f in path.rglob(manifest):
                if "node_modules" in str(f) or ".venv" in str(f):
                    continue
                parsed = self._parse(f, manifest)
                for n, v in parsed.items():
                    deps.append({"name": n, "version": v, "ecosystem": eco, "file": str(f)})
        return {"dependencies": deps, "total": len(deps), "ecosystems": list(set(d["ecosystem"] for d in deps))}

    def _parse(self, path: Path, manifest: str) -> dict:
        try:
            if manifest == "package.json":
                d = json.loads(path.read_text())
                result = {}
                for s in ("dependencies", "devDependencies"):
                    for n, v in d.get(s, {}).items():
                        result[n] = v
                return result
            elif manifest == "requirements.txt":
                result = {}
                for line in path.read_text().splitlines():
                    line = line.strip()
                    if not line or line.startswith("#") or line.startswith("-"):
                        continue
                    name = line.split(">=")[0].split("<=")[0].split("==")[0].strip()
                    result[name] = "latest"
                return result
            elif manifest == "Cargo.toml":
                try:
                    import tomllib
                except ImportError:
                    import tomli as tomllib
                d = tomllib.loads(path.read_text())
                result = {}
                for n, v in d.get("dependencies", {}).items():
                    if isinstance(v, dict):
                        result[n] = v.get("version", "")
                    else:
                        result[n] = v
                return result
        except Exception:
            pass
        return {}
