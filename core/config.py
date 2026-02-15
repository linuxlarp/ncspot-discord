import os
import pathlib

import tomllib


class Basic:
    def __init__(self) -> None:
        config = self.load_config_file()

        self.RUNTIME_PATH: str = config.get("socket", {}).get("RUNTIME_PATH", "/run/user/1000/ncspot")   # we find ncspot.sock here, where we make UNIX socket conncetion
        self.DEBUG: bool = config.get("general", {}).get("DEBUG", False)
        pass

    def load_config_file(self):
        ## Config file will be either in
        # ~/.config/ncspot-discord/config.toml (has priority)
        # config.toml (project source)

        CORE_DIR = os.path.dirname(os.path.abspath(__file__))
        PROJECT_DIR = os.path.dirname(CORE_DIR) # We do this since we run from /core for this module

        CONFIG_PATH = pathlib.Path("~/.config/ncspot-discord/").expanduser()
        load_file = None

        user_config = CONFIG_PATH / "config.toml"
        if user_config.exists():
            load_file = str(user_config)
            print(f"Attempting to load config from: {load_file}")

        if not load_file:
            project_config = os.path.join(PROJECT_DIR, "config.toml")

            if os.path.exists(project_config):
                load_file = project_config
                print(f"Attempting to load config from: {project_config}")
            else:
                raise FileNotFoundError(
                    "Configuration file was not found in either:\n",
                    f"- {user_config}\n",
                    f"- {project_config}"
                )

        with open(load_file, "rb") as config_file:
            data = tomllib.load(config_file)
            print("Config loaded!")

        return data


basic = Basic()
