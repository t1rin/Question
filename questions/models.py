from pydantic import BaseModel, ValidationError


class QuestionValidationError(ValidationError):
    pass


JSONAnswer = str | list[str]
JSONQuestionGroup = dict[str, JSONAnswer]

class JSONQGroups(BaseModel):
    data: dict[str, JSONQuestionGroup]


Answer = tuple[str, bool]
Question = str
Group = str

class StoredQuestionGroups(BaseModel):
    data: dict[str, dict[Question, list[Answer]]]


class QuestionItem(BaseModel):
    group: str | None = None
    title: str | None = None
    right_answers: list[str] = []
    all_answers: list[str] = []

    def is_right(self, answer: str) -> bool:
        return answer in self.right_answers
