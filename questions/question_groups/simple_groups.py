import logging
from random import sample

from .base_groups import BaseQGroups
from ..types import StoredMode
from ..models import *


logger = logging.getLogger(__name__)


class SimpleQGroups(BaseQGroups[SimpleQGroupsModel]):
    """Класс упрощенной работы с JSON файлом групп."""

    ModelClass = SimpleQGroupsModel

    def _merge(self, *datas: dict) -> dict:
        """Объединение нескольких словарей данных,
        используемых SimpleQGroupsModel"""
        if len(datas) == 1:
            return datas[0]
        groups_names = set().union(*[set(d.keys()) for d in datas])
        if len(groups_names) == sum([len(i) for i in datas]):
            return dict((i[0], i[1]) for j in datas for i in j.items())
        new_dicts = {}
        for group_name in groups_names:
            values = []
            for dictionary in datas:
                if group_name in dictionary.keys():
                    values.append(dictionary[group_name])
            if all(isinstance(i, str) for i in values):
                if len(values:=list(set(values))) == 1:
                    new_dicts[group_name] = values[0]
                else:
                    new_dicts[group_name] = values
            elif any(isinstance(i, list) for i in values):
                new_values = []
                for value in values:
                    if isinstance(value, list):
                        new_values += value
                    else:
                        new_values.append(value)
                if len(new_values := list(set(new_values))) == 1:
                    new_dicts[group_name] = new_values[0]
                else:
                    new_dicts[group_name] = new_values
            else:
                new_dicts[group_name] = self._merge(*values)
        return new_dicts

    def _flatten_answers(self, values: list) -> list[str]:
        """Уникальный список всех правильных ответов группы (пул для дистракторов).
        Строится один раз на группу — O(len(group))."""
        seen: set[str] = set()
        flat: list[str] = []
        for value in values:
            for answer in (value if isinstance(value, list) else (value,)):
                if answer not in seen:
                    seen.add(answer)
                    flat.append(answer)
        return flat

    def _generate_wrong_answers(self, pool: list[str], pool_set: set[str],
                                exclude: set[str], count: int) -> list[str]:
        """Сэмплирует до `count` уникальных ответов из pool, не входящих в exclude"""
        if count <= 0 or not pool:
            return []

        available = len(pool) - len(exclude & pool_set)
        take = min(count, available)
        if take <= 0:
            return []

        buffer_size = min(len(pool), take + len(exclude))
        drawn = sample(pool, buffer_size)
        wrong = [a for a in drawn if a not in exclude][:take]

        if len(wrong) < take:
            wrong = [a for a in pool if a not in exclude][:take]

        return wrong

    def to_stored(self, wrong_answers: SimpleWrongAnswers | None = None,
                  fill_missing: int = 3) -> StoredQGroupsModel:
        if not isinstance(fill_missing, int) or fill_missing < 0:
            logger.error("Ожидается fill_missing -> [int >= 0]")
            fill_missing = 0

        if wrong_answers is not None and not self._is_normal_data(wrong_answers):
            logger.error("wrong_answers имеет некорректную структуру, игнорируется")
            wrong_answers = None

        stored: dict = {}

        for group, items in self.data.items():
            values = list(items.values())
            pool = self._flatten_answers(values)
            pool_set = set(pool)

            group_wrong = wrong_answers.get(group, {}) if wrong_answers else {}
            group_stored: dict[str, list[tuple[str, bool]]] = {}

            for question, value in items.items():
                right = set(value) if isinstance(value, list) else {value}

                explicit = group_wrong.get(question)
                if explicit is not None:
                    wrong = list(dict.fromkeys(
                        explicit if isinstance(explicit, list) else [explicit]))
                    wrong = [a for a in wrong if a not in right]
                else:
                    wrong = []

                if len(wrong) < fill_missing:
                    exclude = right | set(wrong)
                    wrong += self._generate_wrong_answers(
                        pool, pool_set, exclude, fill_missing - len(wrong))

                entries: list[tuple[str, bool]] = [(a, True) for a in right]
                entries += [(a, False) for a in wrong]
                group_stored[question] = entries

            stored[group] = {StoredMode.QUESTION: group_stored,
                             StoredMode.ANSWER: {}}

        return StoredQGroupsModel(data=stored)