import tomli
import os
from pathlib import Path

toml_path = os.getenv("CONFIG_PATH")
print("Config path: ", toml_path)

with Path(toml_path).open(mode='rb') as fp:
    config = tomli.load(fp)

