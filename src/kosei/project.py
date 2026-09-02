import shutil
from xml.etree import ElementTree
from pathlib import Path


class Project:
	def __init__(self, project_folder: Path):
		self.path = project_folder
		self._init_paths()
		
		self._strings_tree = ElementTree.parse(self.res / "values" / "strings.xml")
		self._strings_root = self._strings_tree.getroot()
		self._manifest_tree = ElementTree.parse(self.manifest)
		self._manifest_root = self._manifest_tree.getroot()
		
		self._init_app()
	
	def _init_app(self):
		self.app_name = self.get_string("app_name")
		self.package_name = self._manifest_root.get("package")
		
		uses_sdk = self._manifest_root.find("uses-sdk")
		self.min_api = uses_sdk.get("{http://schemas.android.com/apk/res/android}minSdkVersion")
		
		self.apk = self.build / f"{self.app_name}.apk"
		self.signed_apk = self.path / f"{self.app_name}.apk"
	
	def get_string(self, name: str) -> str | None:
		element = self._strings_root.find(f"./string[@name='{name}']")
		return element.text if element is not None else None

	def _init_paths(self):
		self.build = self.path / "build"
		self.temp = self.build / "temp"
		self.generated = self.build / "generated"
		self.bin = self.build / "bin"
		self.compiled = self.build / "compiled"
		self.manifest = self.path / "AndroidManifest.xml"
		self.res = self.path / "res"
		self.src = self.path / "src"
		self.assets = self.path / "assets"
		
		for path in (self.build, self.temp, self.generated, self.bin, self.compiled):
			path.mkdir(exist_ok=True)
	
	@property
	def libs(self) -> list[Path]:
		return list((self.path / "libs").glob("*.jar"))
	
	def clean(self) -> bool:
		if not self.build.exists():
			print(f"[*] Nothing to clean in '{self.path}'")
			return True

		shutil.rmtree(self.build)
		print(f"[*] Cleaned build directory '{self.build}'")
		return True
		
