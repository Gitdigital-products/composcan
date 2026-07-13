import sys, json, argparse; from pathlib import Path; from composcan import __version__
def build_parser():
    p = argparse.ArgumentParser(prog="composcan", description="CompOScan - Software Composition Analysis")
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = p.add_subparsers(dest="command")
    sub.add_parser("scan", help="Scan project dependencies").add_argument("path", nargs="?", default=".")
    sub.add_parser("vulns", help="Check for known vulnerabilities").add_argument("path", nargs="?", default=".")
    sub.add_parser("licenses", help="Analyze license compliance").add_argument("path", nargs="?", default=".")
    sub.add_parser("outdated", help="Find outdated dependencies").add_argument("path", nargs="?", default=".")
    sub.add_parser("sbom", help="Generate SBOM").add_argument("path", nargs="?", default=".")
    sub.add_parser("compliance", help="Check OSS compliance").add_argument("path", nargs="?", default=".")
    return p
def main(argv=None):
    args = build_parser().parse_args(argv)
    if not args.command:
        build_parser().print_help(); return 0
    if args.command == "scan":
        from composcan.scanners.dep_scanner import DependencyScanner
        result = DependencyScanner().scan(Path(args.path))
        print(json.dumps(result, indent=2))
        return 0
    elif args.command == "vulns":
        from composcan.scanners.vuln_scanner import VulnScanner
        result = VulnScanner().scan(Path(args.path))
        for v in result.get("vulnerabilities", []):
            print(f"  [{v['severity'].upper():8s}] {v['package']}: {v['description']}")
        print(f"\n  Total: {result.get('total', 0)}  Critical: {result.get('critical', 0)}")
        return 1 if result.get("critical",0) > 0 else 0
    elif args.command == "licenses":
        from composcan.scanners.license_scanner import LicenseAnalyzer
        result = LicenseAnalyzer().analyze(Path(args.path))
        for l in result.get("licenses", []):
            print(f"  {l['license']:20s} {l['package']}")
        print(f"\n  Risk: {result.get('risk_level', 'unknown')}")
        return 1 if result.get("risk_level") == "high" else 0
    elif args.command == "outdated":
        from composcan.scanners.outdated_scanner import OutdatedScanner
        result = OutdatedScanner().scan(Path(args.path))
        print(json.dumps(result, indent=2))
        return 0
    elif args.command == "sbom":
        from composcan.compliance.sbom import CompOSBOM
        sbom = CompOSBOM().generate(Path(args.path))
        print(json.dumps(sbom, indent=2))
        return 0
    elif args.command == "compliance":
        from composcan.compliance.oss_check import OSSCompliance
        result = OSSCompliance().check(Path(args.path))
        for c in result["checks"]:
            s = "PASS" if c["passed"] else "FAIL"
            print(f"  [{s}] {c['name']}: {c['detail']}")
        return 0 if result["passed"] else 1
if __name__ == "__main__":
    sys.exit(main())
