import logging
from abc import ABC
from typing import Generic, TypeVar


logger = logging.getLogger(__name__)
ModelT = TypeVar('ModelT')


class BaseQGroups(ABC, Generic[ModelT]):
    """Базовый класс для работы с JSON файлом групп."""

    ModelClass: type[ModelT]
