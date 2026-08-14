import subprocess
from pathlib import Path 

from apk_build.project import Project
from apk_build.constants import DATA, DALVIK_VM



def compile_java(project: Project) -> bool:
	print("[*] compiling java")
	
	sources = list((project.src).rglob("*.java"))
	
	res = subprocess.run([
		DALVIK_VM,
		f"-Djava.io.tmpdir={project.temp}",
		"-Xmx256m",
		"-cp", DATA / "ecj.jar",
		"org.eclipse.jdt.internal.compiler.batch.Main",
		"-proc:none",
		"-cp", DATA / "android.classes.jar",
		"-cp", project.generated,
		"-d", project.bin / "classes",
		"-sourcepath", project.src,
		*sources
	], capture_output=True, text=True)
	
	if res.returncode == 0:
		print("[*] java compiled successfully!")
		return True
	else:
		print("[*] java compiling failed!")
		print(res.stderr)
		return False


def compile_classes(project: Project) -> bool:
	print("[*] compiling classes")
	
	res = subprocess.run([
		DALVIK_VM,
		"-Xmx256m",
		"-cp", DATA / "d8.jar",
		"com.android.tools.r8.D8",
		"--release",
		"--min-api", str(project.min_api),
		"--lib", DATA / "android.classes.jar",
		"--output", project.bin,
		project.bin / "classes"
	], capture_output=True, text=True)
	
	if res.returncode == 0:
		print("[*] classes compiled successfully!")
		return True
	else:
		print("[*] classes compiling failed!")
		print(res.stderr)
		return False


def sign_apk(project: Project) -> bool:
	print("[*] signing apk")
	
	res = subprocess.run([
		DALVIK_VM,
		"-cp", DATA / "apksigner.dex",
		"net.fornwall.apksigner.Main",
		"-p",
		"android",
		DATA / "test.jks",
		project.apk,
		project.signed_apk
	], capture_output=True, text=True)
	
	if res.returncode == 0:
		print("[*] apk signed successfully!")
		return True
	else:
		print("[*] apk signing failed!")
		print(res.stderr)
		return False

