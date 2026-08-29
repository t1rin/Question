# type: ignore
import logging

from .base_groups import BaseQGroups
from ..models import *


logger = logging.getLogger(__name__)


class SimpleQGroups(BaseQGroups[SimpleQGroupsModel]):
    """Класс упрощенной работы с JSON файлом групп."""

    ModelClass = SimpleQGroupsModel

    def _merge(self, *datas: dict) -> dict:
        ... 

    def to_stored(self, wrong_answers: SimpleWrongAnswers | None = None,
                  fill_missing: int = 3) -> StoredQGroupsModel:
        ...