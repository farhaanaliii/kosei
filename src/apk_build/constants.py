from pathlib import Path


BASE = Path(__file__).resolve().parent.parent
DATA = BASE / "data"
CACHE = DATA / "cache"
TEMPLATES = BASE / "templates"


_vm1 = "/system/bin/dalvikvm"
_vm2 = "/apex/com.android.art/bin/dalvikvm"
DALVIK_VM = _vm1 if Path(_vm1).exists() else _vm2
