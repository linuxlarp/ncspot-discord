import json
import os

import core.config as config
import core.logs as logger
import core.models as models


class RPC:
    def __init__(self) -> None:
        self.config = config.basic
