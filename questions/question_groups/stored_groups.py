import logging
from random import shuffle, choice

from .base_groups import BaseQGroups
from ..types import StoredMode, StoredAnswer, StoredGroups
from ..models import (StoredQGroupsModel, QItem,
                      ValidationError)


logger = logging.getLogger(__name__)


class StoredQGroups(BaseQGroups[StoredQGroupsModel]):
    """Класс полноценной работы с JSON файлом групп."""

    ModelClass = StoredQGroupsModel

    def _merge(self, *datas: dict) -> dict:
        """Функция объединения данных."""
        result: StoredGroups = {}

        if not datas:
            return result
    
        for data in datas:
            for group_name, group_data in data.items():
                if group_name not in result:
                    result[group_name] = {StoredMode.QUESTION: {},
                                          StoredMode.ANSWER: {}}
                for mode in [StoredMode.QUESTION, StoredMode.ANSWER]:
                    if mode not in group_data:
                        continue
                    for title, answers in group_data[mode].items():
                        if title not in result[group_name][mode]:
                            result[group_name][mode][title] = []
                        result[group_name][mode][title] = list(
                            set([*result[group_name][mode][title], *answers]))
        return result

    def add_question(self, group: str, title: str,
                     right_answers: list[str],
                     wrong_answers: list[str],
                     reverse: bool = False) -> None:
        if self._path and not self._is_normal_json():
            self._create_json()

        try:
            QItem(group=group, title=title,
                  right_answers=right_answers,
                  wrong_answers=wrong_answers)
        except ValidationError as err:
            logger.error("%s (Ожидается" + 
                         " group -> [str], key -> [str]," + 
                         " right_answers -> list[str]," +
                         " wrong_answers -> list[str])", err)
            return

        qmode = (StoredMode.ANSWER if reverse
                 else StoredMode.QUESTION)
        if group not in self.data.keys():
            self.data[group] = {StoredMode.QUESTION: {},
                                StoredMode.ANSWER: {}}

        answers = [*[(ans, True ) for ans in right_answers],
                   *[(ans, False) for ans in wrong_answers]]

        if title not in self.data[group][qmode].keys():
            self.data[group][qmode][title] = answers
        else:
            old_answers = self.data[group][qmode][title]
            self.data[group][qmode][title] = list(
                set([*old_answers, *answers]))
        
        if self._path:
            self._update_json()

    def get_groups(self) -> list[str]:
        return list(self.data.keys())

    def get_qitems(self, group: str,
                   reverse: bool = False,
                   ) -> list[QItem] | None:
        if group not in self.data.keys():
            return None
        qitems_source = self.data[group][int(reverse)]

        qitems = []
        for title, answers in qitems_source.items():
            right_answers, wrong_answers = [], []
            for ans in answers:
                if ans[1]: right_answers.append(ans[0])
                else:      wrong_answers.append(ans[0])
                    
            qitems.append(QItem(group=group,title=title,
                                right_answers=right_answers,
                                wrong_answers=wrong_answers))
        return qitems

    def _building_question(self, group: str, title: str,
                           answers: list[StoredAnswer],
                           quantity: int) -> QItem | None:
        if quantity < 2:
            logger.error("Некорректное количество вариантов ответа")
            return None
        
        if len(answers) < quantity:
            logger.warning(
                "Для вопроса '%s' недостаточно ответов (%s), нужно %s",
                title, len(answers), quantity)

        right_answers: list[str] = []
        wrong_answers: list[str] = []
        for answer_text, is_right in answers:
            if is_right and not right_answers:
                right_answers.append(answer_text)
            elif not is_right and len(wrong_answers) < quantity - 1:
                wrong_answers.append(answer_text)
        
            if len(right_answers) + len(wrong_answers) == quantity:
                break
    
        if not right_answers:
            logger.error("Не найден правильный ответ для вопроса '%s'", title)
            return None
    
        return QItem(group=group, title=title,
                     right_answers=right_answers,
                     wrong_answers=wrong_answers)

    def get_question(self, group: str, title: str,
                     reverse: bool = False,
                     quantity_ans: int = 3,
                     ) -> QItem | None:
        if any(not isinstance(name, str) for name in [title, group]):
            logger.error("Ожидается group -> [str], title -> [str]")
            return None
        if group not in self.get_groups():
            logger.error("Не найдена группа " + group)
            return None

        qmode = (StoredMode.ANSWER if reverse
                 else StoredMode.QUESTION)
        if title not in self.data[group][qmode].keys():
            logger.error("title \"" + title + "\" не найден")
            return None

        answers = self.data[group][qmode][title]
        shuffle(answers)

        return self._building_question(group, title, answers, quantity_ans)


    def get_rand_question(self,
                          group: str | None = None,
                          reverse: bool = False,
                          quantity_ans: int = 3,
                          ) -> QItem | None:
        if not self.data:
            logger.warning("Вопросов нет")
            return None
    
        if group is None:
            group = choice(self.get_groups())
    
        if group not in self.get_groups():
            logger.error("Группа '%s' не найдена", group)
            return None

        qmode = (StoredMode.ANSWER if reverse
                 else StoredMode.QUESTION)
        qitems_source = self.data[group][qmode]
    
        if not qitems_source:
            logger.warning("В группе '%s' нет вопросов", group)
            return None
    
        title = choice(list(qitems_source.keys()))
        answers = qitems_source[title]
    
        shuffle(answers)
    
        return self._building_question(group, title, answers, quantity_ans)