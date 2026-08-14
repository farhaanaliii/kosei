import argparse
from pathlib import Path

from .project import Project
from .generator import create_project
from . import aapt
from . import dalvikvm



def main() -> None:
	parser = argparse.ArgumentParser()
	
	subparsers = parser.add_subparsers(dest="command", required=True)
	new = subparsers.add_parser("new")
	new.add_argument("name")
	new.add_argument("directory", type=Path)
	new.add_argument("package")
	
	build = subparsers.add_parser("build")
	build.add_argument("project", type=Path)
 
	args = parser.parse_args()
	
	if args.command == "new":
		create_project(path=args.directory.resolve(), app_name=args.name, package_name=args.package)
	elif args.command == "build":
		project = Project(args.project.resolve())
		print(f"[*] building '{project.app_name}'")
		
		aapt.compile_resources(project)
		aapt.link_resources(project)
		dalvikvm.compile_java(project)
		dalvikvm.compile_classes(project)
		aapt.append_classes(project)
		dalvikvm.sign_apk(project)


	