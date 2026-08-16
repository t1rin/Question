from typing import Any

from .models import Answer


class Question:
    def __init__(self, group: str | None = None, 
                 title: str | None = None, 
                 answer: list | None = None, 
                 *answers: Answer) -> None:
        self._title = title
        self._group = group
        self._right_answers = answer or []
        self._all_answers = list(answers)
    
    def load(self, data: tuple[str, str, list, list]) -> None:
        right_answers, all_answers = [], []
        for answer, right in data[-1]:
            all_answers.append(answer)
            if right: 
                right_answers.append(answer)
        self._group = data[0]
        self._title = data[1]
        self._right_answers = right_answers
        self._all_answers = all_answers
    
    def get_title(self) -> str:
        if self._title is None:
            return ""
        return self._title
    
    def get_group(self) -> str:
        if self._group is None:
            return ""
        return self._group
    
    def get_answers(self) -> list:
        if not isinstance(self._all_answers, list):
            return []
        return self._all_answers
    
    def is_right(self, answer: str) -> bool:
        if not isinstance(self._right_answers, list):
            return False
        return answer in self._right_answers