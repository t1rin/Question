from pydantic import BaseModel, ValidationError

from .types import *


class JSONQGroupsModel(BaseModel):
    data: dict[str, JSONQuestionGroup]


class StoredQGroupsModel(BaseModel):
    data: dict[str, dict[StoredQuestion, list[StoredAnswer]]]


class QItem(BaseModel):
    group: str | None = None
    title: str | None = None
    right_answers: list[str] = []
    all_answers: list[str] = []

    def is_right(self, answer: str) -> bool:
        return answer in self.right_answers