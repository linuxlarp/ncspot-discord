import logging
import json
import datetime
import traceback
import core.config as config

from pathlib import Path
from colorama import init as colorama_init, Fore, Back, Style

colorama_init(autoreset=True)


class Logger:
    def __init__(self):
        self.levels = {
            "error": (Fore.RED + Style.BRIGHT, "ERROR"),
            "warn": (Fore.YELLOW + Style.BRIGHT, "WARN"),
            "info": (Fore.BLUE + Style.BRIGHT, "INFO"),
            "success": (Fore.GREEN + Style.BRIGHT, "SUCCESS"),
            "debug": (Fore.WHITE + Style.DIM, "DEBUG"),
        }

    def _log(self, level: str, message: str, data=None):
        if level not in self.levels:
            level = "info"

        color_code, prefix = self.levels[level]
        color_prefix = f"{color_code}{prefix}{Style.RESET_ALL}"

        console_line = f"{Style.RESET_ALL} {color_prefix} {message}"
        print(console_line)

        if data is not None:
            if isinstance(data, BaseException):
                detail = "".join(traceback.format_exception(type(data), data, data.__traceback__)).rstrip()
            elif isinstance(data, (dict, list, tuple)):
                detail = json.dumps(data, indent=2, default=str)
            else:
                detail = str(data)

            formatted = f" └─ {detail}"
            print(f"{Fore.LIGHTBLACK_EX}{formatted}{Style.RESET_ALL}")

    def error(self, m, d=None): self._log("error", m, d)
    def warn(self, m, d=None): self._log("warn", m, d)
    def info(self, m, d=None): self._log("info", m, d)
    def success(self, m, d=None): self._log("success", m, d)
    def debug(self, m, d=None):
        if config.basic.DEBUG is True:
            self._log("debug", m, d)
