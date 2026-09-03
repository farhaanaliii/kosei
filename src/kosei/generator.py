import shutil
from pathlib import Path

from kosei.constants import TEMPLATES


def replace_placeholder(file_path: Path, placeholder: str, content: str):
    text = file_path.read_text(encoding="utf-8")
    text = text.replace(placeholder, content)
    file_path.write_text(text, encoding="utf-8")


def create_project(app_name: str, package_name: str=None, path: Path=None) -> bool:
    path = path or Path(".")
    
    if package_name is None:
        clean_name = "".join(c.lower() for c in app_name if c.isalnum()) or "myapp"
        package_name = f"com.example.{clean_name}"
    
    path.mkdir(exist_ok=True)
    project_folder = path / app_name if path.name != app_name else path
    
    if project_folder.exists() and any(project_folder.iterdir()):
        print(f"[x] '{str(project_folder)}' already exists and is not empty!")
        return False

    shutil.copytree(TEMPLATES / "default", project_folder)

    packge_dir = project_folder / "src" / "package"
    target_dir = project_folder / "src" / Path(*package_name.split("."))
    target_dir.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(packge_dir, target_dir)    
    
    replace_placeholder(project_folder / "AndroidManifest.xml", "{package_name}", package_name)
    replace_placeholder(project_folder / "res" / "values" / "strings.xml", "{app_name}", app_name)
    replace_placeholder(target_dir / "Applications.java", "{package_name}", package_name)
    replace_placeholder(target_dir / "CrashActivity.java", "{package_name}", package_name)
    replace_placeholder(target_dir / "MainActivity.java", "{package_name}", package_name)
    
    print(f"[*] App project '{app_name}' created!")
    return True
