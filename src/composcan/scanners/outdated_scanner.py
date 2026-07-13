"""Outdated dependency checker."""
from pathlib import Path
class OutdatedScanner:
    def scan(self, path: Path) -> dict:
        outdated = []
        for f in path.rglob("package.json"):
            if "node_modules" in str(f): continue
            try:
                import json
                d = json.loads(f.read_text())
                for name, ver in d.get("dependencies",{}).items():
                    if ver.startswith("^") or ver.startswith("~"):
                        outdated.append({"package": name, "current": ver, "file": str(f), "note": "Use exact version pinning"})
            except: pass
        return {"outdated": outdated, "total": len(outdated)}
