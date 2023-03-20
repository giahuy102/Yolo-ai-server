import tomli

from pathlib import Path

toml_path = Path(__file__).parent.parent.parent / 'config' / 'server.toml'

with toml_path.open(mode='rb') as fp:
    config = tomli.load(fp)

