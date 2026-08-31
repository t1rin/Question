from typing import TypeAlias
from enum import StrEnum

    
class StoredMode(StrEnum):
    QUESTION = "question"
    ANSWER = "answer"


SimpleAnswer: TypeAlias = str | list[str]
SimpleQuestionGroup: TypeAlias = dict[str, SimpleAnswer]
SimpleWrongAnswers: TypeAlias = dict[str, SimpleQuestionGroup]

StoredAnswer: TypeAlias = tuple[str, bool]
StoredQuestions: TypeAlias = dict[str, list[StoredAnswer]]
StoredGroups: TypeAlias = dict[str, dict[StoredMode, StoredQuestions]]

