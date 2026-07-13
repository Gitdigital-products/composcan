from pathlib import Path
from composcan.scanners.dep_scanner import DependencyScanner
def test_npm_deps(tmp_path):
    (tmp_path / "package.json").write_text('{"dependencies": {"express": "^4.18.0", "lodash": "^4.17.21"}}')
    result = DependencyScanner().scan(tmp_path)
    assert result["total"] == 2
    assert any(d["ecosystem"] == "npm" for d in result["dependencies"])
def test_pypi_deps(tmp_path):
    (tmp_path / "requirements.txt").write_text("requests==2.31.0\nflask>=3.0.0\n")
    result = DependencyScanner().scan(tmp_path)
    assert result["total"] >= 1
