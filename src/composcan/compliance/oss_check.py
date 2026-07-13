"""Open source compliance checker."""
from pathlib import Path
class OSSCompliance:
    def check(self, path: Path) -> dict:
        checks = []
        has_license = any(f.name.startswith("LICENSE") for f in path.iterdir() if f.is_file()) if path.is_dir() else False
        checks.append({"name": "License file", "passed": has_license, "detail": "LICENSE file found" if has_license else "No LICENSE file"})
        has_readme = any(f.name.startswith("README") for f in path.iterdir() if f.is_file()) if path.is_dir() else False
        checks.append({"name": "README", "passed": has_readme, "detail": "README found" if has_readme else "No README"})
        has_contributing = any("contributing" in f.name.lower() for f in path.iterdir() if f.is_file()) if path.is_dir() else False
        checks.append({"name": "Contributing guide", "passed": has_contributing, "detail": "CONTRIBUTING found" if has_contributing else "No CONTRIBUTING file"})
        has_security = any("security" in f.name.lower() for f in path.iterdir() if f.is_file()) if path.is_dir() else False
        checks.append({"name": "Security policy", "passed": has_security, "detail": "SECURITY.md found" if has_security else "No SECURITY policy"})
        return {"checks": checks, "passed": all(c["passed"] for c in checks), "total": len(checks)}
