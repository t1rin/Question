from pydantic import BaseModel, ValidationError


Answer = str | list[str]
QuestionGroup = dict[str, Answer]

class QuestionGroups(BaseModel):
    data: dict[str, QuestionGroup]