import subprocess
from pathlib import Path 

from apk_build.project import Project
from apk_build.constants import DATA, DALVIK_VM





"""
/apex/com.android.art/bin/dalvikvm \
    -Djava.io.tmpdir=tmp \
    -Xmx256m \
    -cp ecj.jar \
    org.eclipse.jdt.internal.compiler.batch.Main \
    -proc:none \
    -7 \
    -cp android.classes.jar \
    -cp gen \
    -d bin/classes \
    -sourcepath src \
    $(find src -type f -name "*.java")
"""

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
		"-7",
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
	

"""
/system/bin/dalvikvm -Xmx256m -cp dx.dex dx.dx.command.Main --dex --output=./bin/classes.dex ./bin/classes
"""

def compile_classes(project: Project) -> bool:
	print("[*] compiling classes")
	
	res = subprocess.run([
		DALVIK_VM,
		"-Xmx256m",
		"-cp", DATA / "dx.dex",
		"dx.dx.command.Main",
		"--dex",
		"--output", project.bin / "classes.dex",
		project.bin / "classes"
	], capture_output=True, text=True)
	
	if res.returncode == 0:
		print("[*] classes compiled successfully!")
		return True
	else:
		print("[*] classes compiling failed!")
		print(res.stderr)
		return False



"""
/system/bin/dalvikvm -cp apksigner.dex net.fornwall.apksigner.Main -p android test.jks hello.apk hello.1.0.apk
"""

def sign_apk(project: Project) -> bool:
	print("[*] signing apk")
	
	res = subprocess.run([
		DALVIK_VM,
		"-cp", DATA / "apksigner.dex",
		"net.fornwall.apksigner.Main",
		"-p",
		"android",
		DATA / "test.jks",
		project.path / f"{project.app_name}.apk",
		project.path / f"{project.app_name}_sign.apk"
	], capture_output=True, text=True)
	
	if res.returncode == 0:
		print("[*] apk signed successfully!")
		return True
	else:
		print("[*] apk signing failed!")
		print(res.stderr)
		return False

