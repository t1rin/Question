from pydantic import BaseModel, ValidationError


class QuestionValidationError(ValidationError):
    pass


class JSONQGroups(BaseModel):
    JSONAnswer = str | list[str]
    JSONQuestionGroup = dict[str, JSONAnswer]
    data: dict[str, JSONQuestionGroup]


class StoredQuestionGroups(BaseModel):
    Answer = tuple[str, bool]
    Question = str
    Group = str
    data: dict[str, dict[Question, list[Answer]]]


class QuestionItem(BaseModel):
    group: str | None = None
    title: str | None = None
    right_answers: list[str] = []
    all_answers: list[str] = []

    def is_right(self, answer: str) -> bool:
        return answer in self.right_answers
