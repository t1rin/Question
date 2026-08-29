import os
import logging
from abc import ABC, abstractmethod
from typing import (Generic, TypeVar,
                    Protocol, runtime_checkable)

import orjson

from ..models import ValidationError


logger = logging.getLogger(__name__)


@runtime_checkable
class ModelProtocol(Protocol):
    data: dict
    def __init__(self, data: dict) -> None: ...

ModelT = TypeVar('ModelT', bound=ModelProtocol)


class BaseQGroups(ABC, Generic[ModelT]):
    """Базовый класс для работы с JSON файлом групп."""

    ModelClass: type[ModelT]
    
    def __init__(self, path_to_json: str | None = None) -> None:
        self._json_cache: bytes | None = None

        self._init_groups()
        if path_to_json:
            self.load_json(path_to_json)

    def _is_normal_data(self, data: dict) -> bool:
        try: self.ModelClass(data=data)
        except ValidationError:
            return False
        return True

    def _is_normal_json(self) -> bool:
        assert self._path is not None
        if not os.path.exists(self._path):
            return False
        try:
            with open(self._path, "rb") as json_file:
                data = orjson.loads(json_file.read())
        except Exception as e:
            logger.error(f"Некорректная структура json файла: {e}")
            return False
        return self._is_normal_data(data)

    def _create_json(self) -> None:
        index = 0
        assert self._path is not None
        name = self._path.split(".")
        while os.path.exists(self._path):
            if os.path.exists((str(index)+".").join(name)):
                index += 1
                continue
            os.rename(self._path, (str(index)+".").join(name))

        with open(self._path, "wb") as json_file:
            json_file.write(orjson.dumps({}))

        logger.info("Создан новый " + self._path)

    def _read_json(self) -> None:
        assert self._path is not None
        with open(self._path, "rb") as json_file:
            data = orjson.loads(json_file.read())
            self._init_groups(data=data)

    def _update_json(self) -> None:
        assert self._path is not None
        with open(self._path, "wb") as json_file:
            data = orjson.dumps(
                self._data, 
                option=orjson.OPT_INDENT_2 | orjson.OPT_SORT_KEYS)
            json_file.write(data)
        self._invalidate_cache()

    def _invalidate_cache(self) -> None:
        self._json_cache = None

    def _init_groups(self, data: dict | None = None) -> None:
        """Функция объединения данных."""
        self._groups = self.ModelClass(data=(data or {}))
        self._data = self._groups.data
        self._invalidate_cache()

    @abstractmethod
    def _merge(self, *datas: dict) -> dict:
        """Функция объединения данных"""
        pass

    def load_json(self, path_to_json: str | None) -> None:
        """Функция подключения JSON файла"""
        self._path = path_to_json
        if path_to_json is not None:
            if not self._is_normal_json():
                self._create_json()
            self._read_json()

    def load_data(self, data: dict) -> None:
        """Функция загрузки данных"""
        if self._is_normal_data(data):
            new_data = self._merge(self._data, data)
            self._init_groups(data=new_data)
            if self._path:
                self._update_json()
        else:
            logger.error("json данные не имеют смысла")

    def get_all_data_bytes(self) -> bytes:
        """Получить все данные в виде сериализованного JSON (с кэшированием)"""
        if self._json_cache is not None:
            return self._json_cache
        
        self._json_cache = orjson.dumps(
            self._data,
            option=orjson.OPT_INDENT_2 | orjson.OPT_SORT_KEYS)
        return self._json_cache

    def get_all_data_str(self) -> str:
        """Получить все данные в виде JSON строки (с кэшированием)"""
        return self.get_all_data_bytes().decode('utf-8')

    @property
    def data(self) -> dict:
        return self._data
