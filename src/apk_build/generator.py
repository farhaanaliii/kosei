import shutil
from pathlib import Path

from apk_build.constants import TEMPLATES


def replace_placeholder(file_path: Path, placeholder: str, content: str):
    text = file_path.read_text(encoding="utf-8")
    text = text.replace(placeholder, content)
    file_path.write_text(text, encoding="utf-8")


def create_project(path: Path, app_name: str, package_name: str) -> bool:
    path.mkdir(exist_ok=True)
    project_folder = path / app_name
    
    if project_folder.exists():
        print(f"[x] '{str(project_folder)}' already exists!")
        return False

    shutil.copytree(TEMPLATES / "default", project_folder)

    packge_dir = project_folder / "src" / "package"
    target_dir = project_folder / "src" / Path(*package_name.split("."))
    shutil.move(packge_dir, target_dir)    
    
    replace_placeholder(project_folder / "AndroidManifest.xml", "{package_name}", package_name)
    replace_placeholder(project_folder / "res" / "values" / "strings.xml", "{app_name}", app_name)
    replace_placeholder(target_dir / "Applications.java", "{package_name}", package_name)
    replace_placeholder(target_dir / "CrashActivity.Java", "{package_name}", package_name)
    replace_placeholder(target_dir / "MainActivity.java", "{package_name}", package_name)
    
    print(f"[*] App project '{app_name}' created!")
    return True
