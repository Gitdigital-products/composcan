"""Known vulnerability scanner."""
import json, urllib.request, ssl
class VulnScanner:
    def scan(self, path: Path) -> dict:
        from composcan.scanners.dep_scanner import DependencyScanner
        deps = DependencyScanner().scan(path)
        vulns = []
        # Query OSV.dev for each dependency (batch)
        queries = [{"package": {"name": d["name"]}, "version": d["version"]} for d in deps.get("dependencies",[]) if d["version"] != "latest"]
        if not queries:
            return {"vulnerabilities": [], "total": 0, "critical": 0}
        try:
            ctx = ssl.create_default_context()
            req = urllib.request.Request("https://api.osv.dev/v1/querybatch",
                data=json.dumps({"queries": queries[:50]}).encode(),
                headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
                data = json.loads(resp.read())
            dep_names = [d["name"] for d in deps.get("dependencies",[])]
            for i, result in enumerate(data.get("results",[])):
                for v in result.get("vulns",[]):
                    vulns.append({"package": dep_names[i] if i < len(dep_names) else "unknown", "id": v.get("id",""), "description": v.get("summary","No summary"), "severity": "medium"})
        except Exception:
            pass
        return {"vulnerabilities": vulns, "total": len(vulns), "critical": sum(1 for v in vulns if v["severity"]=="critical")}
