from pydantic import BaseModel, ValidationError

from .types import *


class JSONQGroups(BaseModel):
    data: dict[str, JSONQuestionGroup]


class StoredQuestionGroups(BaseModel):
    data: dict[str, dict[StoredQuestion, list[StoredAnswer]]]


class QuestionItem(BaseModel):
    group: str | None = None
    title: str | None = None
    right_answers: list[str] = []
    all_answers: list[str] = []

    def is_right(self, answer: str) -> bool:
        return answer in self.right_answers