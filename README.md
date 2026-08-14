# apk-build

A simple Python tool to compile, build, and sign Android APKs natively on Android environments (Termux / DalvikVM).

## Features

- **Resource Compilation**: Compiles Android XML resources with `aapt`.
- **Java Compilation**: Compiles Java code using Eclipse Compiler for Java (`ecj.jar`) via `dalvikvm`.
- **Dexing**: Converts `.class` files to `classes.dex` using the modern `d8.jar` (with Java 8 desugaring).
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
- **Data Dependencies**: Bundled in `./data/` (`android.jar`, `android.classes.jar`, `ecj.jar`, `d8.jar`, `apksigner.dex`, `test.jks`).

## Compatibility & API Support

Based on the build pipeline (`ecj` with `-7` flag and legacy `dx.dex`), the compiled APKs have specific API constraints:

- **Minimum Recommended API:** **21 (Android 5.0 Lollipop)**. With the D8 compiler upgrade, this pipeline fully supports modern Java 8 features (like lambdas) through desugaring, targeting API 21 by default.
- **Java Language Support:** Java 8 (using the `-8` flag in `ecj` and desugared by `d8`).
- **Templates:** The provided `templates/default` defaults to `minSdkVersion="21"` and `targetSdkVersion="33"`. It is set up with modern Android 12+ requirements (like explicit `android:exported` flags on activities) to ensure seamless installation on modern devices.

## Usage

The tool provides a Command-Line Interface (CLI) for generating and building projects.

### 1. Create a New Project

Use the `new` command to generate a template project. You must provide the app name, the target directory, and the Java package name.

Using `uv`:
```bash
uv run apk-build new "My App" ./projects com.example.myapp
```
Or using standard Python:
```bash
python -m apk_build new "My App" ./projects com.example.myapp
```

### 2. Build an Existing Project

Use the `build` command to compile and sign the project.

Using `uv`:
```bash
uv run apk-build build ./projects/MyApp
```
Or using standard Python:
```bash
python -m apk_build build ./projects/MyApp
```

## Output

After a successful build, the following files will be created in your target project directory:
- `[AppName].apk` — Unsigned APK file
- `[AppName]_sign.apk` — Signed APK ready for installation
