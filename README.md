# apk-build

A simple Python tool to compile, build, and sign Android APKs natively on Android environments (Termux / DalvikVM).

## Features

- **Resource Compilation**: Compiles Android XML resources with `aapt`.
- **Java Compilation**: Compiles Java code using Eclipse Compiler for Java (`ecj.jar`) via `dalvikvm`.
- **Dexing**: Converts `.class` files to `classes.dex` using `dx.dex`.
- **Packaging & Signing**: Packages the APK and signs it using `apksigner.dex` with `test.jks`.

## Project Structure

Target Android project directory format:

```text
my-project/
├── AndroidManifest.xml
├── res/
│   └── values/
│       └── strings.xml  # Must define <string name="app_name">AppName</string>
└── src/
    └── ...              # Java source code (*.java)
```

## Requirements

- **Python**: `>= 3.14` (or managed via [`uv`](https://github.com/astral-sh/uv))
- **Environment**: Android/Termux with `aapt` in system `PATH` and Dalvik VM at `/apex/com.android.art/bin/dalvikvm`.
- **Data Dependencies**: Bundled in `./data/` (`android.jar`, `android.classes.jar`, `ecj.jar`, `dx.dex`, `apksigner.dex`, `test.jks`).

## Usage

Using `uv`:

```bash
uv run apk-build <path-to-project>
```

Or using standard Python:

```bash
python -m apk_build <path-to-project>
```

## Output

After a successful build, the following files will be created in your target project directory:
- `[AppName].apk` — Unsigned APK file
- `[AppName]_sign.apk` — Signed APK ready for installation
