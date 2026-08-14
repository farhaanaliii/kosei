import subprocess
from pathlib import Path

from apk_build.constants import *



#aapt package -m -J gen -M AndroidManifest.xml -S res -I android.jar

def compile_resources(project_folder: Path) -> bool:
	print("[*] compiling resources")
	
	res = subprocess.run([
		"aapt",
		"package",
		"-m",
		"-J", GENERATED,
		"-M", project_folder / "AndroidManifest.xml",
		"-S", project_folder / "res",
		"-I", DATA / "android.jar"
	], capture_output=True, text=True)
	
	if res.returncode == 0:
		print("[*] resources compiled successfully!")
		return True
	else:
		print("[*] resources compiling failed!")
		print(res.stderr)
		return False
	
"""
./aapt package -f -I android.jar -S res -M AndroidManifest.xml -F hello.apk --no-version-vectors
"""

def build_apk(project_folder: Path) -> bool:
	print("[*] building resources")
	
	res = subprocess.run([
		"aapt",
		"package",
		"-f",
		"-I", DATA / "android.jar",
		"-S", project_folder / "res",
		"-M", project_folder / "AndroidManifest.xml",
		"-F", project_folder / "hello.apk",
		"--no-version-vectors"
	], capture_output=True, text=True)
	
	if res.returncode == 0:
		print("[*] apk built successfully!")
		return True
	else:
		print("[*] apk building failed!")
		print(res.stderr)
		return False


"""
aapt add -f ../hello.apk classes.dex
"""

def append_classes(project_folder: Path) -> bool:
	print("[*] appending classes")
	
	res = subprocess.run([
		"aapt",
		"add",
		"-f",
		project_folder / "hello.apk",
		BIN / "classes.dex"
	], capture_output=True, text=True)
	
	if res.returncode == 0:
		print("[*] appending classes successfully!")
		return True
	else:
		print("[*] appending classes failed!")
		print(res.stderr)
		return False

