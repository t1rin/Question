from typing import TypeAlias
from enum import IntEnum

    
class StoredMode(IntEnum):
    QUESTION = 0
    ANSWER = 1


SimpleAnswer: TypeAlias = str | list[str]
SimpleQuestionGroup: TypeAlias = dict[str, SimpleAnswer]
SimpleWrongAnswers: TypeAlias = dict[str, SimpleQuestionGroup]

StoredAnswer: TypeAlias = tuple[str, bool]
StoredQuestions: TypeAlias = dict[str, list[StoredAnswer]]
StoredGroups: TypeAlias = dict[str, dict[StoredMode, StoredQuestions]]

