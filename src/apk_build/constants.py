from importlib.resources import files
from pathlib import Path


DATA = files("apk_build") / data
DALVIK_VM = "/apex/com.android.art/bin/dalvikvm"
TEMPLATES = files("apk_build") / "templates"

