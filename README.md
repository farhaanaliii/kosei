<div align="center">

# apk-build

[![Python Version](https://img.shields.io/badge/python-3.14%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Android%20%7C%20Termux-orange.svg)](https://termux.dev)

Compiles, packages, and signs Android APKs directly on Android devices via Termux. No host machine, Android Studio, or desktop SDK installation required.

</div>

## Build Pipeline

```text
aapt2 compile     ->  compile res/ into .flat files
aapt2 link        ->  link .flat + AndroidManifest.xml -> .apk + R.java
ecj.jar (3.27.0)  ->  compile .java + R.java -> .class files (Java 16)
d8.dex            ->  desugar and convert .class -> classes.dex
zipfile           ->  inject classes.dex into the .apk
apksigner.dex     ->  sign the .apk with debug.pk8 and debug.x509.pem
```

## Requirements

- Python >= 3.14
- Termux environment with `aapt2` in `$PATH`
- Android ART runtime (`/apex/com.android.art/bin/dalvikvm` or `/system/bin/dalvikvm`)
- Bundled runtime binaries in `./src/data/`

## Installation

Install editable mode from the project root:

```bash
pip install -e .
```

## Usage

```bash
# create a project with default package (com.example.hello)
apk new Hello

# create a project with custom package and directory
apk new Hello com.mycompany.hello ./projects

# build project in current directory
apk build

# build project in specified directory
apk build ./projects/Hello

# clean build artifacts
apk clean ./projects/Hello
```

Build Outputs:
- `build/[AppName].apk` — Unsigned intermediate package inside the project build directory
- `[AppName].apk` — v1/v2/v3 signed APK ready for installation

## data Directory

All runtime binaries live under `src/data/` and execute natively on Android's `dalvikvm` engine.

| File | What it is | How it's used |
|---|---|---|
| `android.jar` | Android framework resource stubs | Passed to `aapt2 link -I` to resolve `@android:` attribute references and generate `R.java` |
| `android.classes.jar` | Android framework class definitions | Passed to `ecj.jar` via `-cp` so the Java compiler resolves `android.*` imports |
| `ecj.jar` | Eclipse Java Compiler 3.27.0 (patched for Dalvik) | Invoked via `dalvikvm -cp ecj.jar org.eclipse.jdt.internal.compiler.batch.Main` to compile Java source into `.class` files (up to Java 16) |
| `d8.dex` | Google D8 Dexer packaged as `.dex` | Invoked via `dalvikvm -cp d8.dex com.android.tools.r8.D8` to desugar and convert `.class` bytecode into `classes.dex` |
| `apksigner.dex` | Android APK Signer tool packaged as `.dex` | Invoked via `dalvikvm -cp apksigner.dex com.android.apksigner.ApkSignerTool` to apply v1, v2, and v3 signatures |
| `debug.pk8` | PKCS8 private key for debug signing | Provided to `apksigner` via `--key` to sign debug builds |
| `debug.x509.pem` | X.509 certificate for debug signing | Provided to `apksigner` via `--cert` alongside `debug.pk8` |

## Roadmap

- [x] **Pipeline Error Handling**: Abort build execution immediately if any step (`aapt2`, `ecj`, `d8`, `apksigner`) fails.
- [x] **External Libraries (`libs/`)**: Support bundling 3rd-party `.jar` dependencies.
- [x] **Assets Support (`assets/`)**: Automatically pass project `assets/` directory to `aapt2 link`.
- [x] **Java 16 Support**: Upgrade ECJ to 3.27.0 and replace legacy `dx` with Google D8.
- [ ] **Custom Release Keystore**: Add CLI options to sign with release keystores (`--ks`, `--ks-pass`, `--key-pass`, `--alias`).
- [ ] **Zipalign Optimization**: Align uncompressed zip entries to 4-byte boundaries before signing.
- [ ] **Native Libraries (`lib/`)**: Support bundling pre-compiled `.so` files into the APK.
- [ ] **Additional CLI Commands**: `apk clean` and `apk run`.
- [ ] **Incremental Building**: Cache compiled resources and Java classes, recompiling only modified sources.
- [ ] **Kotlin Support**: Integrate standalone `kotlinc` for `.kt` source file compilation.
