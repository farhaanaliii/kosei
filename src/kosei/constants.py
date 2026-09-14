from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
TOOLCHAIN = Path.home() / ".kosei" / "toolchain"
TOOLCHAIN_VERSION = "v0.1.0"
TEMPLATES = BASE / "templates"

DEPENDENCIES = [
    "android.jar",
    "android.classes.jar",
    "ecj.jar",
    "d8.dex",
    "apksigner.dex",
    "debug.pk8",
    "debug.x509.pem",
]

_vm1 = "/system/bin/dalvikvm"
_vm2 = "/apex/com.android.art/bin/dalvikvm"
DALVIK_VM = _vm1 if Path(_vm1).exists() else _vm2

BUFFER_SIZE = 64 * 1024


