import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent.parent
backend_root = Path(__file__).resolve().parent.parent

for p in (str(repo_root), str(backend_root)):
    if p not in sys.path:
        sys.path.insert(0, p)
