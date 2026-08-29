import logging

from .question_groups import *
from .models import QItem, StoredQGroupsModel


logger = logging.getLogger(__name__)


class QuestionBank:
    def __init__(self, path_to_simple: str | None = None,
                 path_to_stored: str | None = None) -> None:
        self._stored_groups = StoredQGroups(path_to_stored)
        self._simple_groups = SimpleQGroups(path_to_simple)

    def add_question(self, *args, **kwargs) -> None:
        self._stored_groups.add_question(*args, **kwargs)

    def get_groups(self) -> list[str]:
        return self._stored_groups.get_groups()

    def get_qitems(self, *args, **kwargs) -> list[QItem] | None:
        return self._stored_groups.get_qitems(*args, **kwargs)

    def get_question(self, *args, **kwargs) -> QItem | None:
        return self._stored_groups.get_question(*args, **kwargs)

    def get_rand_question(self, *args, **kwargs) -> QItem | None:
        return self._stored_groups.get_rand_question(*args, **kwargs)

    def to_stored(self, *args, **kwargs) -> StoredQGroupsModel:
        return self._simple_groups.to_stored(*args, **kwargs)

