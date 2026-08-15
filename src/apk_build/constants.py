from importlib.resources import files


DATA = files("apk_build") / "data"
DALVIK_VM = "/apex/com.android.art/bin/dalvikvm"
TEMPLATES = files("apk_build") / "templates"

