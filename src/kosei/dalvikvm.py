import os
import subprocess

from kosei.project import Project
from kosei.constants import TOOLCHAIN, DALVIK_VM


def compile_java(project: Project) -> bool:
	sources = list(project.src.rglob("*.java"))
	r_java = project.generated / "R.java"
	if r_java.exists():
		sources.append(r_java)
		
	modified = project.filter_modified(sources)
	classes_dir = project.bin / "classes"
	if not modified and classes_dir.exists() and any(classes_dir.rglob("*.class")):
		return True

	print("[*] compiling java")
	
	classpath = [
		TOOLCHAIN / "android.classes.jar",
		project.generated,
		*project.libs
	]
	
	res = subprocess.run([
		DALVIK_VM,
		f"-Djava.io.tmpdir={project.temp}",
		"-Xmx256m",
		"-cp", TOOLCHAIN / "ecj.jar",
		"org.eclipse.jdt.internal.compiler.batch.Main",
		"-proc:none",
		"-16",
		"-cp", os.pathsep.join(map(str, classpath)),
		"-d", classes_dir,
		"-sourcepath", project.src,
		*sources
	], capture_output=True, text=True)
	
	if res.returncode == 0:
		project.update_cache(sources)
		return True
	else:
		print("[*] java compiling failed!")
		print(res.stderr)
		return False


def compile_classes(project: Project) -> bool:
	classes = list((project.bin / "classes").rglob("*.class"))
	modified = project.filter_modified(classes)
	
	dex_files = list(project.bin.glob("classes*.dex"))
	if not modified and dex_files:
		return True

	print("[*] compiling classes")
	
	res = subprocess.run([
		DALVIK_VM,
		"-Xmx256m",
		"-cp", TOOLCHAIN / "d8.dex",
		"com.android.tools.r8.D8",
		"--lib", TOOLCHAIN / "android.jar",
		"--min-api", str(project.min_api),
		"--output", project.bin,
		*classes,
		*project.libs
	], capture_output=True, text=True)
	
	if res.returncode == 0:
		project.update_cache(classes)
		return True
	else:
		print("[*] classes compiling failed!")
		print(res.stderr)
		return False


def sign_apk(project: Project) -> bool:
	print("[*] signing apk")
	
	res = subprocess.run([
		DALVIK_VM,
		"-cp", TOOLCHAIN / "apksigner.dex",
		"com.android.apksigner.ApkSignerTool",
		"sign",
		"--key", TOOLCHAIN / "debug.pk8",
		"--cert", TOOLCHAIN / "debug.x509.pem",
		"--v1-signing-enabled", "true",
		"--v2-signing-enabled", "true",
		"--v3-signing-enabled", "true",
		"--v4-signing-enabled", "false",
		"--out", project.signed_apk,
		project.apk,
	], capture_output=True, text=True)
	
	if res.returncode == 0:
		return True
	else:
		print("[*] apk signing failed!")
		print(res.stderr)
		return False
