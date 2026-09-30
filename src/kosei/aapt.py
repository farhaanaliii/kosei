import subprocess
import zipfile

from kosei.project import Project
from kosei.constants import TOOLCHAIN


def compile_resources(project: Project) -> bool:
	res_files = [f for f in project.res.rglob("*") if f.is_file()]
	modified = project.filter_modified(res_files)

	if not modified and sorted(project.compiled.rglob("*.flat")):
		return True

	print("[*] compiling resources")
	
	res = subprocess.run([
		"aapt2",
		"compile",
		"--dir", project.res,
		"-o", project.compiled
	], capture_output=True, text=True)
	
	if res.returncode == 0:
		project.update_cache(res_files)
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
		"-I", TOOLCHAIN / "android.jar",
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
	libs = list(project.native_libs.rglob("*.so")) if project.native_libs.exists() else []
	dex_files = sorted(project.bin.glob("classes*.dex"))
	
	try:
		with zipfile.ZipFile(project.apk, "a") as apk:
			print("[*] appending classes")
			for dex in dex_files:
				apk.write(dex, dex.name)
			
			if libs:
				print("[*] appending native libs")
				for lib in libs:
					apk.write(lib, f"lib/{lib.relative_to(project.native_libs).as_posix()}")
		
		return True
	except Exception as e:
		print("[*] appending classes failed!")
		print(str(e))
		return False


def align_apk(project: Project) -> bool:
	print("[*] aligning apk")
	
	res = subprocess.run([
		"zipalign",
		"-p",
		"-f",
		"4",
		project.apk,
		project.aligned_apk
	], capture_output=True, text=True)
	
	if res.returncode == 0:
		return True
	else:
		print("[*] apk alignment failed!")
		print(res.stderr)
		return False



	

