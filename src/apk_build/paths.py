from pathlib import Path



class Paths:
	def __init__(self, project_folder: Path):
		self.project = project_folder
		self.build = project_folder / "build"
		self.temp = self.build / "temp"
		self.generated = self.build / "generated"
		self.bin = self.build / "bin"
