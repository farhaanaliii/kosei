import glob
import os
import shutil
import subprocess
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "src" / "data"


def patch_ecj() -> None:
    ecj_url = "https://repo1.maven.org/maven2/org/eclipse/jdt/ecj/3.27.0/ecj-3.27.0.jar"
    util_url = "https://raw.githubusercontent.com/eclipse-jdt/eclipse.jdt.core/R4_21/org.eclipse.jdt.core/compiler/org/eclipse/jdt/internal/compiler/util/Util.java"
    openjdk_url = "https://github.com/adoptium/temurin8-binaries/releases/download/jdk8u422-b05/OpenJDK8U-jre_x64_windows_hotspot_8u422b05.zip"

    urllib.request.urlretrieve(ecj_url, "ecj-3.27.0.jar")
    urllib.request.urlretrieve(util_url, "Util.java")
    urllib.request.urlretrieve(openjdk_url, "openjdk8.zip")

    with open("Util.java", "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_get_bytes = """\tpublic static byte[] getInputStreamAsByteArray(InputStream input) throws IOException {
\t\tjava.io.ByteArrayOutputStream buffer = new java.io.ByteArrayOutputStream();
\t\tbyte[] data = new byte[8192];
\t\tint nRead;
\t\twhile ((nRead = input.read(data, 0, data.length)) != -1) {
\t\t\tbuffer.write(data, 0, nRead);
\t\t}
\t\treturn buffer.toByteArray();
\t}
"""
    new_read_n = """\tpublic static byte[] readNBytes(InputStream input, int byteLength) throws IOException {
\t\tjava.io.ByteArrayOutputStream buffer = new java.io.ByteArrayOutputStream();
\t\tbyte[] data = new byte[Math.min(byteLength, 8192)];
\t\tint totalRead = 0;
\t\twhile (totalRead < byteLength) {
\t\t\tint toRead = Math.min(data.length, byteLength - totalRead);
\t\t\tint nRead = input.read(data, 0, toRead);
\t\t\tif (nRead == -1) break;
\t\t\tbuffer.write(data, 0, nRead);
\t\t\ttotalRead += nRead;
\t\t}
\t\treturn buffer.toByteArray();
\t}
"""
    lines[470:473] = [new_get_bytes]
    lines[478:481] = [new_read_n]

    with open("Util.java", "w", encoding="utf-8") as f:
        f.writelines(lines)

    subprocess.run(["javac", "-cp", "ecj-3.27.0.jar", "-source", "8", "-target", "8", "-d", ".", "Util.java"], check=True)

    z_open = zipfile.ZipFile("openjdk8.zip")
    rt_name = [n for n in z_open.namelist() if n.endswith("rt.jar")][0]
    z_open.extract(rt_name, "rt_extracted")
    z_open.close()

    z_rt = zipfile.ZipFile(Path("rt_extracted") / rt_name)

    with open("org/eclipse/jdt/internal/compiler/util/Util.class", "rb") as f:
        c_util = f.read()
    with open("org/eclipse/jdt/internal/compiler/util/Util$1.class", "rb") as f:
        c_util1 = f.read()
    with open("org/eclipse/jdt/internal/compiler/util/Util$Displayable.class", "rb") as f:
        c_util_disp = f.read()

    zin = zipfile.ZipFile("ecj-3.27.0.jar", "r")
    zout = zipfile.ZipFile(DATA / "ecj-patched.jar", "w")

    for item in zin.infolist():
        buffer = zin.read(item.filename)
        if item.filename == "org/eclipse/jdt/internal/compiler/util/Util.class":
            buffer = c_util
        elif item.filename == "org/eclipse/jdt/internal/compiler/util/Util$1.class":
            buffer = c_util1
        elif item.filename == "org/eclipse/jdt/internal/compiler/util/Util$Displayable.class":
            buffer = c_util_disp
        zout.writestr(item, buffer)

    for item in z_rt.infolist():
        if item.filename.startswith("javax/lang/model/") or item.filename.startswith("javax/annotation/processing/"):
            zout.writestr(item.filename, z_rt.read(item.filename))

    zin.close()
    z_rt.close()
    zout.close()

    subprocess.run(["d8", "--output", ".", str(DATA / "ecj-patched.jar")], check=True)

    z = zipfile.ZipFile(DATA / "ecj-patched.jar", "a")
    z.write("classes.dex", "classes.dex")
    z.close()

    shutil.copy(DATA / "ecj-patched.jar", DATA / "ecj.jar")
    (DATA / "ecj-patched.jar").unlink(missing_ok=True)
    Path("classes.dex").unlink(missing_ok=True)


def patch_d8(d8_jar_path: Path) -> None:
    subprocess.run(["d8", "--lib", str(DATA / "android.jar"), "--output", "d8_out.jar", str(d8_jar_path)], check=True)
    shutil.copy("d8_out.jar", DATA / "d8.dex")
    Path("d8_out.jar").unlink(missing_ok=True)


if __name__ == "__main__":
    patch_ecj()
