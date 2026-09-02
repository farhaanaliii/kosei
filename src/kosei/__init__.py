import argparse
from pathlib import Path

from .project import Project
from .generator import create_project
from . import aapt
from . import dalvikvm


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="kosei",
        description="Compiles, packages, and signs Android APKs directly on Android via Termux."
    )
    
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    new = subparsers.add_parser("new", help="Create a new Android app project")
    new.add_argument("name", help="App name (e.g. 'Hello')")
    new.add_argument("package", nargs="?", default=None, help="Package name (default: com.example.<name>)")
    new.add_argument("directory", nargs="?", type=Path, default=None, help="Target directory (default: current directory)")
    new.add_argument("-p", "--package-name", dest="flag_package", help="Override package name")
    new.add_argument("-d", "--dir", dest="flag_dir", type=Path, help="Override target directory")
    
    build = subparsers.add_parser("build", help="Build an Android project into a signed APK")
    build.add_argument("project", nargs="?", type=Path, default=Path("."), help="Project directory (default: current directory)")
    
    clean = subparsers.add_parser("clean", help="Clean build artifacts for a project")
    clean.add_argument("project", nargs="?", type=Path, default=Path("."), help="Project directory (default: current directory)")

    args = parser.parse_args()
    
    if args.command == "new":
        package = args.flag_package or args.package
        directory = args.flag_dir or args.directory or Path(".")
        create_project(app_name=args.name, package_name=package, path=directory.resolve())
    elif args.command == "clean":
        project_path = args.project.resolve()
        project = Project(project_path)
        project.clean()
    elif args.command == "build":
        project_path = args.project.resolve()
        project = Project(project_path)
        print(f"[*] building '{project.app_name}'")
        
        if not aapt.compile_resources(project):
            return
        if not aapt.link_resources(project):
            return
        if not dalvikvm.compile_java(project):
            return
        if not dalvikvm.compile_classes(project):
            return
        if not aapt.append_classes(project):
            return
        if not dalvikvm.sign_apk(project):
            return
