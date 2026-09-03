<div align="center">

# kosei

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
- Termux with `aapt2` in `$PATH`
- ART at `/apex/com.android.art/bin/dalvikvm` or `/system/bin/dalvikvm`
- Bundled runtime binaries in `src/data/`

## Installation

Create a virtual environment and install in editable mode using `uv`:

```bash
uv venv
uv pip install -e .
```

## Usage

Create a project with default package (com.example.hello):

```bash
kosei new Hello
```

Create a project with custom package and directory:

```bash
kosei new Hello -p com.mycompany.hello -d ./projects
```

Build project in current directory:

```bash
kosei build
```

Build project in specified directory:

```bash
kosei build ./projects/Hello
```

Clean build artifacts:

```bash
kosei clean ./projects/Hello
```

Alternative Python module execution:

```bash
python -m kosei new Hello
python -m kosei build
```

Build Outputs:
- `build/[AppName].apk` — Unsigned intermediate package inside the project build directory
- `[AppName].apk` — v1/v2/v3 signed APK ready for installation

## data Directory

All runtime binaries live under `src/data/` and execute natively on Android's `dalvikvm` engine.

| File | Description | Purpose |
|---|---|---|
| `android.jar` | Android framework resource stubs | Passed to `aapt2 link -I` to resolve `@android:` attribute references and generate `R.java` |
| `android.classes.jar` | Android framework class definitions | Passed to `ecj.jar` via `-cp` so the Java compiler resolves `android.*` imports |
| `ecj.jar` | Eclipse Java Compiler 3.27.0 (patched for Dalvik) | Invoked via `dalvikvm -cp ecj.jar org.eclipse.jdt.internal.compiler.batch.Main` to compile Java source into `.class` files (up to Java 16) |
| `d8.dex` | Google D8 Dexer packaged as `.dex` | Invoked via `dalvikvm -cp d8.dex com.android.tools.r8.D8` to desugar and convert `.class` bytecode into `classes.dex` |
| `apksigner.dex` | Android APK Signer tool packaged as `.dex` | Invoked via `dalvikvm -cp apksigner.dex com.android.apksigner.ApkSignerTool` to apply v1, v2, and v3 signatures |
| `debug.pk8` | PKCS8 private key for debug signing | Provided to `apksigner` via `--key` to sign debug builds |
| `debug.x509.pem` | X.509 certificate for debug signing | Provided to `apksigner` via `--cert` alongside `debug.pk8` |

## Technical Roadmap

- [x] **Native ART Engine Execution**: Execute compilation toolchain (`ecj`, `d8`, `apksigner`) natively on Dalvik VM without host JDK dependencies.
- [x] **Java 16 & Google D8 Support**: Modernized compilation pipeline with ECJ 3.27.0 and Google D8 dexer replacing legacy dx.
- [x] **Jar & Native Binary Bundling**: Automated linking for 3rd-party `.jar` files in `libs/` and `.so` binaries in `lib/`.
- [x] **Automatic Multidex Support**: DEX splitting and secondary dex injection for large codebases exceeding 64k method limits.
- [ ] **Custom Release Keystore Profiles**: CLI options (`--keystore`, `--alias`, `--ks-pass`, `--key-pass`) for production signing.
- [ ] **Incremental Compilation Engine**: Hashing system to cache resource compilation and Java bytecode, rebuilding only modified sources.
- [ ] **Zipalign Optimization Engine**: Native 4-byte boundary alignment for uncompressed zip entries prior to signature verification.
- [ ] **Kotlin Compiler Support**: Integration of `kotlinc` targeting Dalvik/ART bytecode for `.kt` source files.
- [ ] **AAR & Remote Dependency Resolution**: Parsing `.aar` archives and automated transitive Maven package resolution.
- [ ] **Automated ADB Deployment**: Device deployment via `--install` and `--launch` options using local ADB service.

## Maintainer

Created and maintained by [Farhan Ali](https://github.com/farhaanaliii) (i.farhanali.dev@gmail.com).


