import os
import pathlib

import tomllib


class Basic:
    def __init__(self) -> None:
        config = self.load_config_file()
        print("toml data:", config)

        self.RUNTIME_PATH = "/run/user/1000/ncspot"  # we find ncspot.sock here, where we make UNIX socket conncetion
        self.DEBUG: bool = False
        pass

    def load_config_file(self):
        ## Config file will be either in
        # ~/.config/ncspot-discord/config.toml (has priority)
        # config.toml (project source)

        config_path = pathlib.Path("~/.config/ncspot-discord/")
        load_file = None

        if config_path.exists():
            load_file = os.path.join(config_path, "config.toml")

            if not load_file:
                load_file = os.path.join("config.toml")

            with open(load_file, "rb") as config_file:
                data = tomllib.load(config_file)
                return data


basic = Basic()
