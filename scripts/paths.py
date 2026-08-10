"""Shared paths for WOGROK tooling."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config"
LAYERS = ROOT / "layers"
OUTPUT = ROOT / "output"
TEMPLATE = ROOT / "template"
MANIFESTS = ROOT / "manifests"
REPORTS = ROOT / "reports"

TRAITS_JSON = CONFIG / "traits.json"
RULES_JSON = CONFIG / "rules.json"
CANVAS_JSON = CONFIG / "canvas.json"
BASE_PNG = LAYERS / "base" / "wogrok_base.png"
