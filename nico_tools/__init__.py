from pathlib import Path
import os

# データの保存領域を作成

storage_path = "{0}{1}.pyniconico".format(Path.home(), os.sep)
if not os.path.exists(storage_path):
    os.makedirs(storage_path)
