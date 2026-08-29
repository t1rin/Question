import logging

from .base_groups import BaseQGroups
from ..models import SimpleQGroupsModel


logger = logging.getLogger(__name__)


class SimpleQGroups(BaseQGroups[SimpleQGroupsModel]):
    """Класс упрощенной работы с JSON файлом групп."""

    ModelClass = SimpleQGroupsModel