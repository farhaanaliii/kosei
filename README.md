# apk-build

Compiles, packages, and signs Android APKs directly on Android via Termux. No host machine, no Android Studio, no SDK installation required.

It works by invoking the device's own ART runtime (`dalvikvm`) to run Java-based build tools, combined with `aapt2` for resource compilation and Python's standard `zipfile` for APK assembly.

## Build Pipeline

```
aapt2 compile     ->  compile res/ into .flat files
aapt2 link        ->  link .flat + AndroidManifest.xml -> .apk + R.java
ecj.jar           ->  compile .java + R.java -> .class files
dx.dex            ->  convert .class -> classes.dex
zipfile           ->  inject classes.dex into the .apk
apksigner.dex     ->  sign the .apk with debug.jks
```

## Requirements

- Python >= 3.14
- Termux with `aapt2` in `$PATH`
- ART at `/apex/com.android.art/bin/dalvikvm`
- Populated `./data/` directory (see below)

## Project Layout

```
my-project/
├── AndroidManifest.xml
├── res/
│   └── values/
│       └── strings.xml    # must contain <string name="app_name">
└── src/
    └── ...                # Java source files
```

## Installation

Install once from the project root:

```bash
pip install -e .
```

This is an editable install — changes to any file under `src/apk_build/` take effect immediately with no reinstall needed. Only reinstall if you modify `pyproject.toml` (e.g. add a new entry point).

## Usage

```bash
# scaffold a new project
apk-build new "My App" ./projects com.example.myapp

# build it
apk-build build ./projects/MyApp
```

Or without the installed entrypoint:

```bash
python -m apk_build new "My App" ./projects com.example.myapp
python -m apk_build build ./projects/MyApp
```

Output:
- `build/[AppName].apk` — unsigned, inside the project's `build/` directory
- `[AppName].apk` — v1/v2/v3 signed, written to the project root

## data/ Directory

All runtime binaries live here. None of these are available natively in Termux, so they are bundled manually.

| File | What it is | How it's used |
|---|---|---|
| `android.jar` | Android framework resource stubs (compile-time only) | Passed to `aapt2 link -I` to resolve `@android:` attribute references and produce `R.java` |
| `android.classes.jar` | Android framework class library | Passed to `ecj.jar` via `-cp` so the Java compiler can resolve `android.*` imports against real API definitions |
| `ecj.jar` | Eclipse Compiler for Java — a self-contained `javac` replacement bundled as a runnable `.jar` | Invoked via `dalvikvm -cp ecj.jar org.eclipse.jdt.internal.compiler.batch.Main` to compile `.java` source into `.class` bytecode |
| `dx.dex` | The `dx` Dalvik cross-assembler, itself packaged as a `.dex` | Invoked via `dalvikvm -cp dx.dex dx.dx.command.Main --dex` to translate `.class` bytecode into `classes.dex` (Dalvik bytecode) |
| `apksigner.dex` | Google's `apksigner` tool packaged as a `.dex` | Invoked via `dalvikvm -cp apksigner.dex com.android.apksigner.ApkSignerTool sign` to apply JAR (v1), APK Signature Scheme v2, and v3 signatures |
| `debug.jks` | PKCS12 keystore holding the standard Android debug key (`androiddebugkey`) | Provided to `apksigner.dex` via `--ks`. Password is `android` on both the store and key |

## TODO / Roadmap

- [x] **Pipeline Error Handling**: Abort build execution immediately if any step (`aapt2`, `ecj`, `dx`, `apksigner`) fails.
- [x] **External Libraries (`libs/`)**: Support bundling 3rd-party `.jar` dependencies.
- [x] **Assets Support (`assets/`)**: Automatically pass project `assets/` directory to `aapt2 link`.
- [ ] **Custom Release Keystore**: Add CLI options to sign with release keystores (`--ks`, `--ks-pass`, `--key-pass`, `--alias`).
- [ ] **Zipalign Optimization**: Align uncompressed zip entries to 4-byte boundaries before signing.
- [ ] **Native Libraries (`lib/`)**: Support bundling pre-compiled `.so` files into the APK.
- [ ] **Additional CLI Commands**:
  - `apk clean <project>`: Remove build artifacts.
  - `apk run <project>`: Install and launch APK directly on device via Termux (`pm install` / `am start`).
- [ ] **Incremental Building**: Cache compiled resources and Java classes, recompiling only modified sources.
- [ ] **Kotlin Support**: Integrate standalone `kotlinc` for `.kt` source file compilation.
- [ ] **Project Config File**: Optional `apk.toml` file for build settings and app metadata.

