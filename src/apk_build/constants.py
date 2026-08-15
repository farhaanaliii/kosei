from pathlib import Path


BASE = Path(__file__).resolve().parent.parent
DATA = BASE / "data"
TEMPLATES = BASE / "templates"


DALVIK_VM = "/apex/com.android.art/bin/dalvikvm"
