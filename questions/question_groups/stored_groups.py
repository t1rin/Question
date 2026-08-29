# type: ignore
import logging

from .base_groups import BaseQGroups
from ..models import StoredQGroupsModel, QItem


logger = logging.getLogger(__name__)


class StoredQGroups(BaseQGroups[StoredQGroupsModel]):
    """Класс полноценной работы с JSON файлом групп."""

    ModelClass = StoredQGroupsModel

    def _merge(self, *datas: dict) -> dict:
        ...

    def add_question(self, group: str, title: str,
                     right_answers: list[str],
                     wrong_answers: list[str],
                     reverse: bool = False) -> None:
        ...

    def get_groups(self) -> list[str]:
        ...

    def get_qitems(self, group: str,
                   reverse: bool = False,
                   ) -> list[QItem]:
        ...

    def get_question(self, group: str, title: str,
                     reverse: bool = False,
                     quentity_ans: int = 3,
                     ) -> QItem | None:
        ...

    def get_rand_question(self, group: str,
                          reverse: bool = False,
                          quentity_ans: int = 3,
                          ) -> QItem | None:
        ...