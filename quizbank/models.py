from pydantic import (BaseModel, ConfigDict,
                      ValidationError)

from .types import *


class SimpleQGroupsModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    data: dict[str, SimpleQuestionGroup]


class StoredQGroupsModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    data: StoredGroups


class QItem(BaseModel):
    group: str | None = None
    title: str | None = None
    right_answers: list[str] = []
    wrong_answers: list[str] = []

    @property
    def all_answers(self) -> list[str]:
        """Все ответы в перемешку"""
        from random import shuffle
        _result = self.right_answers + self.wrong_answers
        shuffle(_result)
        return _result

    def is_right(self, answer: str) -> bool:
        """Проверка на правильность ответа"""
        return answer in self.right_answers