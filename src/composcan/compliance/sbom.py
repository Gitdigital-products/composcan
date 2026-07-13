"""SCA SBOM generation."""
from pathlib import Path; import json; from datetime import datetime, timezone
from composcan.scanners.dep_scanner import DependencyScanner
class CompOSBOM:
    def generate(self, path: Path) -> dict:
        deps = DependencyScanner().scan(path)
        return {"bomFormat": "CycloneDX", "specVersion": "1.5", "version": 1, "metadata": {"timestamp": datetime.now(timezone.utc).isoformat(), "tools": [{"name": "composcan", "version": "0.1.0"}]}, "components": [{"name": d["name"], "version": d["version"], "purl": f"pkg:{d['ecosystem']}/{d['name']}@{d['version']}"} for d in deps.get("dependencies",[])]}
