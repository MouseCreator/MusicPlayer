from model.models import Models
from model.music import RepeatOption


class RepeatService:

    def __init__(self, models: Models):
        self._models = models

    def on_song_finished(self):
        repeat = self._models.state.get_record().repeat_option
        if repeat == RepeatOption.NO_REPEAT:
            self._play_next_song(looped_list=False)
        elif repeat == RepeatOption.REPEAT_ONE:
            current = self._models.current.get_current()
            self._models.current.set_current(current)
        elif repeat == RepeatOption.REPEAT_ALL:
            self._play_next_song(looped_list=True)

    def _play_next_song(self, looped_list: bool):
        current = self._models.current.get_current()
        if current is None:
            return
        index = self._models.playlist.index_of(current)
        index = index + 1
        if index >= self._models.playlist.size():
            if looped_list:
                first = self._models.playlist.at_index(0)
                self._models.current.set_current(first)
        else:
            self._models.current.set_current(self._models.playlist.view()[index])
