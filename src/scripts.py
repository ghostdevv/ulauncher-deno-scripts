import json
import shutil
import hashlib
import subprocess
from typing import TypedDict
from pathlib import Path
from src.render import render_message
from urllib.parse import urlparse
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
import os

DEFAULT_CONFIG_DIR = Path(__file__).parent / "../default-config"
SCRIPTS_DIR = Path.home() / ".config/ulauncher/deno-scripts"


class ScriptConfig(TypedDict):
    id: str
    name: str
    description: str
    file: str | Path | None


def parse_file_option(input_str: str):
    try:
        parsed = urlparse(input_str)
        if parsed.scheme and parsed.netloc:
            return input_str
    except:
        pass

    try:
        path = Path(input_str)

        if path.is_absolute():
            return path if path.exists() else None

        return SCRIPTS_DIR / path
    except:
        pass

    return None


class Scripts:
    scripts: list[ScriptConfig] | None = None

    def __init__(self):
        if not SCRIPTS_DIR.exists():
            shutil.copytree(DEFAULT_CONFIG_DIR, SCRIPTS_DIR)

        shutil.copyfile(
            DEFAULT_CONFIG_DIR / "config.schema.json",
            SCRIPTS_DIR / "config.schema.json",
        )

        self.load()

    def load(self):
        CONFIG_FILE = SCRIPTS_DIR / "config.json"

        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            self.scripts = [
                {
                    "id": hashlib.md5(
                        json.dumps(script, sort_keys=True).encode()
                    ).hexdigest(),
                    "name": script["name"],
                    "description": script["description"],
                    "file": parse_file_option(script["file"]),
                }
                for script in config["scripts"]
            ]

    def run(self, script_id: str):

        if self.scripts is None:
            return render_message("Error", "No configuration found")

        script = next((s for s in self.scripts if s["id"] == script_id), None)
        if not script:
            return render_message("Error", f"Script not found ({script_id})")

        file = script["file"]

        if file is None:
            return render_message(
                "Error", f"Unable to parse script file option ({script["name"]})"
            )

        if file is Path and not file.exists():
            return render_message("Error", f"Script file not found ({script["name"]})")

        env = os.environ.copy()
        env["DENO_NO_PACKAGE_JSON"] = "1"
        env["DENO_NO_UPDATE_CHECK"] = "1"
        env["NO_COLOR"] = "1"

        if shutil.which("deno") is None:
            env["DENO_INSTALL"] = str(Path.home() / ".deno")
            env["PATH"] = f"{env.get("PATH")}{os.pathsep}{Path.home() / '.deno/bin'}"

        process = subprocess.run(
            ["deno", "run", "--no-prompt", file],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            env=env,
        )

        log = process.stdout.strip()

        return RenderResultListAction(
            [
                ExtensionResultItem(
                    icon="images/deno-scripts.png",
                    name=f"Script {'succeeded' if process.returncode == 0 else f'failed with code {process.returncode}'}",
                    description=log if log else "No output logged",
                    on_enter=(CopyToClipboardAction(log) if log else HideWindowAction()),
                )
            ]
        )
