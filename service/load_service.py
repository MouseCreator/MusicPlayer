from typing import List

from model.models import Models
from model.music import Music


class LoadService:
    def __init__(self, models: Models):
        self._models = models

    def _convert_list(self, files: List[str]) -> List[Music]:
        pass

    def load_files(self, files: List[str]) -> None:
        if not files:
            return
        music_list = self._convert_list(files)
        self._models.playlist.append(music_list)
        if not self._models.current.get_current():
            self._models.current.set_current(music_list[0])