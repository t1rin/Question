from typing import TypeAlias

from pydantic import BaseModel, ValidationError



JSONAnswer: TypeAlias = str | list[str]
JSONQuestionGroup: TypeAlias = dict[str, JSONAnswer]
JSONWrongAnswers: TypeAlias = dict[str, JSONQuestionGroup]

StoredAnswer: TypeAlias = tuple[str, bool]
StoredQuestion: TypeAlias = str
StoredGroup: TypeAlias = str


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