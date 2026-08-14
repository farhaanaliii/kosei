from pathlib import Path

from . import aapt
from . import dalvikvm
from . import utils



def main() -> None:
	project_folder = Path("/data/data/com.termux/files/home/apk")
	
	utils.ensure_dirs()
	aapt.compile_resources(project_folder)
	dalvikvm.compile_java(project_folder)
	dalvikvm.compile_classes(project_folder)
	aapt.build_apk(project_folder)
	aapt.append_classes(project_folder)
	dalvikvm.sign_apk(project_folder)


	