from abc import ABC
from typing import Any, Dict, List


class BaseController(ABC):
    def start_game_handler(self, form: Dict[str, List[str]]) -> Any:
        pass
