from typing import Self

from model.callback import Callback


class LoadState:
    _last_folder: str | None
    def __init__(self, callback: Callback[Self],  last_folder: str | None):
        self._callback = callback
        self._last_folder = last_folder

    def set_last_folder(self, folder: str):
        self._last_folder = folder
        self._callback.call(self)

    def get_last_folder(self) -> str:
        return self._last_folder