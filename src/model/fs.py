import os
import season

config = wiz.config("config")
STORAGE_PATH = config.STORAGE_PATH
Model = season.util.os.FileSystem(os.path.join(STORAGE_PATH))