import logging

from .base_groups import BaseQGroups
from ..models import StoredQGroupsModel


logger = logging.getLogger(__name__)


class StoredQGroups(BaseQGroups[StoredQGroupsModel]):
    """Класс полноценной работы с JSON файлом групп."""

    ModelClass = StoredQGroupsModel