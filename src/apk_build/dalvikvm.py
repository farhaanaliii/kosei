import os
import subprocess
from pathlib import Path 

from apk_build.project import Project
from apk_build.constants import DATA, DALVIK_VM



def compile_java(project: Project) -> bool:
	print("[*] compiling java")
	
	sources = list((project.src).rglob("*.java"))
	classpath = [
		DATA / "android.classes.jar",
		project.generated,
		*project.libs
	]
	
	res = subprocess.run([
		DALVIK_VM,
		f"-Djava.io.tmpdir={project.temp}",
		"-Xmx256m",
		"-cp", DATA / "ecj.jar",
		"org.eclipse.jdt.internal.compiler.batch.Main",
		"-proc:none",
		"-16",
		"-cp", os.pathsep.join(map(str, classpath)),
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
	
	classes = list((project.bin / "classes").rglob("*.class"))
	
	res = subprocess.run([
		DALVIK_VM,
		"-Xmx256m",
		"-cp", DATA / "d8.dex",
		"com.android.tools.r8.D8",
		"--lib", DATA / "android.jar",
		"--output", project.bin,
		*classes,
		*project.libs
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
		"com.android.apksigner.ApkSignerTool",
		"sign",
		"--ks", DATA / "debug.jks",
		"--ks-type", "JKS",
		"--ks-pass", "pass:android",
		"--key-pass", "pass:android",
		"--ks-key-alias", "androiddebugkey",
    	"--v1-signing-enabled", "true",
    	"--v2-signing-enabled", "true",
    	"--v3-signing-enabled", "true",
    	"--v4-signing-enabled", "false",
		"--out", project.signed_apk,
		project.apk,
	], capture_output=True, text=True)
	
	if res.returncode == 0:
		print("[*] apk signed successfully!")
		return True
	else:
		print("[*] apk signing failed!")
		print(res.stderr)
		return False

