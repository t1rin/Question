from pydantic import BaseModel, ValidationError

from .types import *


class SimpleQGroupsModel(BaseModel):
    data: dict[str, SimpleQuestionGroup]


class StoredQGroupsModel(BaseModel):
    data: StoredGroups


class QItem(BaseModel):
    group: str | None = None
    title: str | None = None
    right_answers: list[str] = []
    wrong_answers: list[str] = []

    @property
    def all_answers(self) -> list[str]:
        """Все ответы (правильные + неправильные)"""
        return self.right_answers + self.wrong_answers

    def is_right(self, answer: str) -> bool:
        return answer in self.right_answers