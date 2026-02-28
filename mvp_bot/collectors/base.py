from abc import ABC, abstractmethod
from typing import List

from mvp_bot.types import NarrativeEvent


class BaseCollector(ABC):
    @abstractmethod
    def fetch_recent(self) -> List[NarrativeEvent]:
        raise NotImplementedError
