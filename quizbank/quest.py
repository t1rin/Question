import logging

from .question_groups import *


logger = logging.getLogger(__name__)


class QuestionBank:
    """Класс управления группами вопросов."""

    default_fill_missing = 10

    def __init__(self, path_to_simple: str | None = None,
                 path_to_stored: str | None = None) -> None:
        self._stored_groups = StoredQGroups(path_to_stored)
        self._simple_groups = SimpleQGroups(path_to_simple)

        if path_to_simple:
            self._synchronize()

        self._need_synchronization = False

    def _synchronize(self) -> None:
        """Функция синхронизации SimpleQGroups с StoredQGroups"""
        _stored = self._simple_groups.to_stored(
            fill_missing=self.default_fill_missing)
        self._stored_groups.load_data(_stored.data)

    def __getattr__(self, name):
        if self._need_synchronization:
            self._synchronize()
            self._need_synchronization = False
        stored_attr = getattr(self._stored_groups, name)
        return stored_attr if not callable(stored_attr) else stored_attr

    def load_simple_json(self, path_to_json: str) -> None:
        self._simple_groups.load_json(path_to_json)
        self._need_synchronization = True

    def load_simple_data(self, data: dict) -> None:
        self._simple_groups.load_data(data)
        self._need_synchronization = True

    def get_simple_data(self) -> dict:
        return self._simple_groups.data

