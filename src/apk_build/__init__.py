import argparse
from pathlib import Path

from .project import Project
from . import aapt
from . import dalvikvm



def main() -> None:
	parser = argparse.ArgumentParser()
	
	parser.add_argument("project", type=Path, help="Project directory")
	
	args = parser.parse_args()
	
	project = Project(args.project.resolve())
	print(f"[*] building '{project.app_name}'")
	
	aapt.compile_resources(project)
	dalvikvm.compile_java(project)
	dalvikvm.compile_classes(project)
	aapt.build_apk(project)
	aapt.append_classes(project)
	dalvikvm.sign_apk(project)


	