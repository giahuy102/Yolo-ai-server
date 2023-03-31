import tomli

from pathlib import Path

toml_path = Path(__file__).parents[2] / 'config' / 'server.toml'

with toml_path.open(mode='rb') as fp:
    config = tomli.load(fp)

