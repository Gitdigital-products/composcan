"""License compliance analyzer."""
from pathlib import Path
RESTRICTIVE = {"GPL-3.0","GPL-2.0","AGPL-3.0","SSPL-1.0","OSL-3.0"}
PERMISSIVE = {"MIT","Apache-2.0","BSD-2-Clause","BSD-3-Clause","ISC","0BSD","Unlicense","CC0-1.0"}
class LicenseAnalyzer:
    def analyze(self, path: Path) -> dict:
        licenses = []
        for f in list(path.rglob("LICENSE*")) + list(path.rglob("COPYING*")):
            if "node_modules" in str(f) or ".venv" in str(f): continue
            try:
                c = f.read_text(errors="ignore")[:2000].lower()
                if "mit license" in c: lic = "MIT"
                elif "apache license" in c and "2.0" in c: lic = "Apache-2.0"
                elif "gnu general public license" in c: lic = "GPL-3.0"
                elif "gnu affero" in c: lic = "AGPL-3.0"
                elif "berkeley software distribution" in c: lic = "BSD-3-Clause"
                else: lic = "Unknown"
                licenses.append({"package": f.parent.name or "project", "license": lic, "file": str(f)})
            except: pass
        risk = "high" if any(l["license"] in RESTRICTIVE for l in licenses) else "low" if all(l["license"] in PERMISSIVE for l in licenses) else "medium"
        return {"licenses": licenses, "risk_level": risk, "total": len(licenses)}
