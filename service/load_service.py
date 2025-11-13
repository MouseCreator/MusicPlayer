import os
import uuid
from typing import List

from model.models import Models
from model.music import Music


class LoadService:
    def __init__(self, models: Models):
        self._models = models

    def _convert_list(self, files: List[str]) -> List[Music]:
        music_list = []

        for filename in files:
            music = Music()
            music.id = uuid.uuid4().int
            full_name = os.path.abspath(filename)
            base_name = os.path.basename(filename)
            name, ext = os.path.splitext(base_name)

            music.filename = full_name
            music.extension = ext.lstrip(".")
            music.name = name

            music_list.append(music)

        return music_list

    def load_files(self, files: List[str]) -> None:
        if not files:
            return
        music_list = self._convert_list(files)
        self._models.playlist.append(music_list)
        if not self._models.current.get_current():
            self._models.current.set_current(music_list[0])