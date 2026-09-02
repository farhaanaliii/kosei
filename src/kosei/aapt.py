import subprocess
import zipfile

from kosei.project import Project
from kosei.constants import DATA



def compile_resources(project: Project) -> bool:
	print("[*] compiling resources")
	
	res = subprocess.run([
		"aapt2",
		"compile",
		"--dir", project.res,
		"-o", project.compiled
	], capture_output=True, text=True)
	
	if res.returncode == 0:
		return True
	else:
		print("[*] resources compiling failed!")
		print(res.stderr)
		return False
	

def link_resources(project: Project) -> bool:
	print("[*] linking resources")
	
	flats = sorted(project.compiled.rglob("*.flat"))
	args = [
		"aapt2",
		"link",
		"-I", DATA / "android.jar",
		"--manifest", project.manifest,
		"--java", project.generated,
		"-o", project.apk,
		*flats
	]
	
	if project.assets.exists():
		args.extend(["-A", project.assets])
	
	res = subprocess.run(args, capture_output=True, text=True)
	
	if res.returncode == 0:
		return True
	else:
		print("[*] resource linking failed!")
		print(res.stderr)
		return False



def append_classes_and_libs(project: Project) -> bool:
	libs = list(project.native_libs.rglob("*.so"))
	
	try:
		with zipfile.ZipFile(project.apk, "a") as apk:
			print("[*] appending classes")
			apk.write(project.bin / "classes.dex", "classes.dex")
			
			if libs:
				print("[*] appending native libs")
				for lib in libs:
					apk.write(lib, lib.relative_to(project.path).as_posix())
		
		return True
	except Exception as e:
		print("[*] appending classes failed!")
		print(str(e))
		return False


	

