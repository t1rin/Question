from typing import TypeAlias


JSONAnswer: TypeAlias = str | list[str]
JSONQuestionGroup: TypeAlias = dict[str, JSONAnswer]
JSONWrongAnswers: TypeAlias = dict[str, JSONQuestionGroup]

StoredAnswer: TypeAlias = tuple[str, bool]
StoredQuestion: TypeAlias = str
StoredGroup: TypeAlias = str
