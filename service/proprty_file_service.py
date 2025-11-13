import os
from abc import ABC, abstractmethod


class PropertyFileService(ABC):
    @abstractmethod
    def load(self, filepath: str) -> dict:
        pass
    @abstractmethod
    def save(self, filepath: str, data: dict) -> None:
        pass
    @abstractmethod
    def exists(self, filepath: str) -> bool:
        pass


class PropertyFileServiceImpl(PropertyFileService):

    def load(self, filepath: str) -> dict:
        if not os.path.exists(filepath):
            return {}

        properties = {}
        with open(filepath, "r") as f:
            for line in f:
                line = line.strip()
                if not line or "=" not in line:
                    continue

                key, value = line.split("=", 1)
                properties[key.strip()] = value.strip()
        return properties
    def save(self, filepath: str, data: dict):
        with open(filepath, "w") as f:
            for key, value in data.items():
                f.write(f"{key}={value}\n")

    def exists(self, filepath) -> bool:
        return os.path.exists(filepath)