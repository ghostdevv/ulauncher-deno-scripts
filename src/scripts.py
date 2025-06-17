import json
import shutil
from typing import TypedDict
from pathlib import Path

DEFAULT_CONFIG_DIR = Path(__file__).parent / "../default-config"
SCRIPTS_DIR = Path.home() / ".config/ulauncher/deno-scripts"


class ScriptConfig(TypedDict):
    name: str
    description: str
    file: str


class Scripts:
    scripts: list[ScriptConfig] | None = None

    def __init__(self):
        if not SCRIPTS_DIR.exists():
            shutil.copytree(DEFAULT_CONFIG_DIR, SCRIPTS_DIR)

        self.load()

    def load(self):
        CONFIG_FILE = SCRIPTS_DIR / "config.json"
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            self.scripts = [
                {
                    "name": script["name"],
                    "description": script["description"],
                    "file": script["file"],
                }
                for script in config["scripts"]
            ]
