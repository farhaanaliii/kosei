import subprocess
from pathlib import Path

from apk_build.project import Project
from apk_build.constants import DATA



def compile_resources(project: Project) -> bool:
	print("[*] compiling resources")
	
	res = subprocess.run([
		"aapt2",
		"compile",
		"--dir", project.res,
		"-o", project.compiled
	], capture_output=True, text=True)
	
	if res.returncode == 0:
		print("[*] resources compiled successfully!")
		return True
	else:
		print("[*] resources compiling failed!")
		print(res.stderr)
		return False
	

def link_resources(project: Project) -> bool:
	print("[*] linking resources")
	
	flats = sorted(project.compiled.rglob("*.flat"))
	
	res = subprocess.run([
		"aapt2",
		"link",
		"-I", DATA / "android.jar",
		"--manifest", project.manifest,
		"--java", project.generated,
		"-o", project.apk,
		*flats
	], capture_output=True, text=True)
	
	if res.returncode == 0:
		print("[*] resources linked successfully!")
		return True
	else:
		print("[*] resource linking failed!")
		print(res.stderr)
		return False



def append_classes(project: Project) -> bool:
	print("[*] appending classes")
	
	res = subprocess.run([
		"aapt",
		"add",
		"-f",
		project.apk,
		project.bin / "classes.dex"
	], capture_output=True, text=True)
	
	if res.returncode == 0:
		print("[*] appending classes successfully!")
		return True
	else:
		print("[*] appending classes failed!")
		print(res.stderr)
		return False

