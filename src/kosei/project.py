import shutil
from xml.etree import ElementTree
from pathlib import Path


class Project:
	def __init__(self, project_folder: Path):
		self.path = project_folder
		self._init_paths()
		
		self._strings_root = ElementTree.parse(self.res / "values" / "strings.xml").getroot()
		self._manifest_root = ElementTree.parse(self.manifest).getroot()
		self._android_ns = "{http://schemas.android.com/apk/res/android}"
  
		self._init_app()
	
	def _init_app(self):
		self.app_name = self.get_string("app_name")
		self.package_name = self._manifest_root.get("package")
		
		uses_sdk = self._manifest_root.find("uses-sdk")
		self.min_api = uses_sdk.get(f"{self._android_ns}minSdkVersion")
		
		version_name = self._manifest_root.get(f"{self._android_ns}versionName")
		self.apk = self.build / f"{self.app_name}_unsigned.apk"
		self.signed_apk = self.path / f"{self.app_name}_v{version_name}.apk"
	
	def get_string(self, name: str) -> str:
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
		self.native_libs = self.path / "lib"
		
		
		for path in (self.build, self.temp, self.generated, self.bin, self.compiled):
			path.mkdir(exist_ok=True)
	
	@property
	def libs(self) -> list:
		return list((self.path / "libs").glob("*.jar"))
	
	def clean(self) -> bool:
		if not self.build.exists():
			print(f"[*] Nothing to clean in '{self.path}'")
			return True

		shutil.rmtree(self.build)
		print(f"[*] Cleaned build directory '{self.build}'")
		return True
		
