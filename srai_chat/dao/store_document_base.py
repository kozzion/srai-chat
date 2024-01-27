from abc import ABC, abstractmethod
from typing import List, Optional


class StoreDocumentBase(ABC):
    @abstractmethod
    def delete_all(self) -> int:
        raise NotImplementedError()

    @abstractmethod
    def count(self) -> int:
        raise NotImplementedError()

    @abstractmethod
    def insert_one(self, message: dict) -> None:
        raise NotImplementedError()

    @abstractmethod
    def find_one(self, query: dict) -> Optional[dict]:
        raise NotImplementedError()

    @abstractmethod
    def find(self, query: dict) -> List[dict]:
        raise NotImplementedError()

    @abstractmethod
    def update_one(self, query: dict, update: dict, upsert=False) -> None:
        raise NotImplementedError()
