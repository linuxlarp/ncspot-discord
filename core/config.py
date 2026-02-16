import os
import pathlib

import tomllib

import core.config as config
import core.logs as logger


class Basic:
    def __init__(self) -> None:
        config = self.load_config_file()

        self.DEBUG: bool = config.get("general", {}).get("DEBUG", False)
        self.ENABLE_LOGGING: bool = config.get("general", {}).get(
            "ENABLE_LOGGING", False
        )
        self.RUNTIME_PATH: str = config.get("socket", {}).get(
            "RUNTIME_PATH", "/run/user/1000/ncspot"
        )  # we find ncspot.sock here, where we make UNIX socket conncetion

        pass

    def load_config_file(self):
        ## Config file will be either in
        # ~/.config/ncspot-discord/config.toml (has priority)
        # config.toml (project source)

        TEMP_LOGS = logger.Logger()
        CORE_DIR = os.path.dirname(os.path.abspath(__file__))
        PROJECT_DIR = os.path.dirname(
            CORE_DIR
        )  # We do this since we run from /core for this module

        CONFIG_PATH = pathlib.Path("~/.config/ncspot-discord/").expanduser()
        load_file = None

        user_config = CONFIG_PATH / "config.toml"
        if user_config.exists():
            load_file = str(user_config)
            TEMP_LOGS.info(f"Attempting to load config from: {load_file}")

        if not load_file:
            project_config = os.path.join(PROJECT_DIR, "config.toml")

            if os.path.exists(project_config):
                load_file = project_config
                TEMP_LOGS.info(f"Attempting to load config from: {load_file}")
            else:
                TEMP_LOGS.error(
                    "Failed to load configuration >",
                    "Configuration file was not found in either:\n",
                    f"- {user_config}\n",
                    f"- {project_config}",
                )

                raise FileNotFoundError()

        with open(load_file, "rb") as config_file:
            data = tomllib.load(config_file)
            TEMP_LOGS.success("Config successfully loaded.")

        return data


basic = Basic()
