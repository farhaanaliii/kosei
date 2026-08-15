import subprocess
import zipfile

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
	
	try:
		with zipfile.ZipFile(project.apk, "a") as apk:
			apk.write(project.bin / "classes.dex", "classes.dex")
		
		print("[*] appending classes successfully!")
		return True
	except Exception as e:
		print("[*] appending classes failed!")
		print(str(e))
		return False
	

