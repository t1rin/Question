from pydantic import BaseModel, ValidationError


Answer = str | list[str]
QuestionGroup = dict[str, Answer]

class QuestionGroups(BaseModel):
    data: dict[str, QuestionGroup]

class Question(BaseModel):
    group: str | None = None
    title: str | None = None
    right_answers: list[str] = []
    all_answers: list[str] = []

    def is_right(self, answer: str) -> bool:
        return answer in self.right_answers
