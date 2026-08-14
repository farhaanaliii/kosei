from apk_build.constants import *



def ensure_dirs():
	BUILD.mkdir(exist_ok=True)
	TEMP.mkdir(exist_ok=True)
	GENERATED.mkdir(exist_ok=True)
	BIN.mkdir(exist_ok=True)
	
	DATA.mkdir(exist_ok=True)
	

